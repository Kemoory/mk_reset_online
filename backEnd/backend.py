# backend.py
from flask import Flask, jsonify, request
import psycopg2
from config import db_config

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
    data = request.get_json()
    date = data.get('date')
    joueurs = data.get('joueurs', [])

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM Tournois WHERE date = %s", (date,))
    tournoi = cur.fetchone()

    if tournoi is None:
        cur.execute("INSERT INTO Tournois (date) VALUES (%s) RETURNING id", (date,))
        tournoi_id = cur.fetchone()[0]
    else:
        tournoi_id = tournoi[0]

    for joueur in joueurs:
        nom = joueur['nom']
        score = joueur['score']

        cur.execute("SELECT id FROM Joueurs WHERE nom = %s", (nom,))
        joueur_data = cur.fetchone()

        if joueur_data is None:
            cur.execute("INSERT INTO Joueurs (nom) VALUES (%s) RETURNING id", (nom,))
            joueur_id = cur.fetchone()[0]
        else:
            joueur_id = joueur_data[0]

        cur.execute(
            "INSERT INTO Participations (joueur_id, tournoi_id, score) VALUES (%s, %s, %s)",
            (joueur_id, tournoi_id, score)
        )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
