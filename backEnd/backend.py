# backend.py
from flask import Flask, jsonify, request
import psycopg2
from config import db_config
from trueskill import Rating, rate
import numpy as np

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(**db_config)

@app.route('/dernier-tournoi')
def dernier_tournoi():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM Tournois ORDER BY date DESC LIMIT 1")
    dernier = cur.fetchone()

    if dernier:
        tournoi_id = dernier[0]
        cur.execute("""
            SELECT Joueurs.nom, Participations.score
            FROM Participations
            JOIN Joueurs ON Participations.joueur_id = Joueurs.id
            WHERE Participations.tournoi_id = %s
            ORDER BY Participations.score DESC
        """, (tournoi_id,))
        resultats = cur.fetchall()
    else:
        resultats = []

    cur.close()
    conn.close()

    return jsonify(resultats)

@app.route('/classement')
def classement():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT nom, score_trueskill, tier
        FROM Joueurs
        ORDER BY score_trueskill DESC, tier ASC
    """)
    joueurs = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(joueurs)

@app.route('/add-tournament', methods=['POST'])
def add_tournament():
    print("Received request to add tournament") #Testing
    data = request.get_json()
    date = data.get('date')
    joueurs = data.get('joueurs', [])
    print(f"Date: {date}, Joueurs: {joueurs}") #Testing
    conn = get_db_connection()
    cur = conn.cursor()
    print("Connected to the database") #Testing

    cur.execute("SELECT id FROM Tournois WHERE date = %s", (date,))
    tournoi = cur.fetchone()

    if tournoi is None:
        cur.execute("INSERT INTO Tournois (date) VALUES (%s) RETURNING id", (date,))
        tournoi_id = cur.fetchone()[0]
    else:
        tournoi_id = tournoi[0]

    positions = {}
    player_ids = {}
    player_ratings = []

    for joueur in joueurs:
        nom = joueur['nom']
        score_brut = joueur['score']
        score=int(score_brut)
        # Récupérer ou créer le joueur
        cur.execute("SELECT id, mu, sigma FROM Joueurs WHERE nom = %s", (nom,))
        joueur_data = cur.fetchone()

        if joueur_data is None:
            cur.execute("INSERT INTO Joueurs (nom) VALUES (%s) RETURNING id", (nom,))
            joueur_id = cur.fetchone()[0]
            mu, sigma = 25.0, 8.333  # valeurs par défaut
        else:
            joueur_id, mu, sigma = joueur_data

        player_ids[nom] = joueur_id
        positions[nom] = -score  # TrueSkill veut rangs croissants, donc scores décroissants
        player_ratings.append((nom, Rating(mu=mu, sigma=sigma)))

        # Enregistrer la participation
        cur.execute(
            "INSERT INTO Participations (joueur_id, tournoi_id, score) VALUES (%s, %s, %s)",
            (joueur_id, tournoi_id, score)
        )

    # Trier les joueurs par score décroissant
    sorted_players = sorted(player_ratings, key=lambda x: positions[x[0]])
    rating_groups = [[r[1]] for r in sorted_players]
    ranks = list(range(len(sorted_players)))

    new_ratings = rate(rating_groups, ranks=ranks)

    # Mettre à jour les joueurs avec leurs nouveaux ratings
    for i, (nom, _) in enumerate(sorted_players):
        new_rating = new_ratings[i][0]
        joueur_id = player_ids[nom]
        cur.execute(
            "UPDATE Joueurs SET mu = %s, sigma = %s WHERE id = %s",
            (new_rating.mu, new_rating.sigma, joueur_id)
        )
    
        # Mise à jour des tiers après mise à jour des scores TrueSkill
    cur.execute("SELECT id, score_trueskill FROM Joueurs WHERE score_trueskill IS NOT NULL")
    joueurs = cur.fetchall()

    if joueurs:
        scores = [score for (_, score) in joueurs]
        q1 = np.percentile(scores, 25)
        q2 = np.percentile(scores, 50)
        q3 = np.percentile(scores, 75)

        for joueur_id, score in joueurs:
            if score >= q3:
                tier = 'S'
            elif score >= q2:
                tier = 'A'
            elif score >= q1:
                tier = 'B'
            else:
                tier = 'C'
            cur.execute("UPDATE Joueurs SET tier = %s WHERE id = %s", (tier, joueur_id))


    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
