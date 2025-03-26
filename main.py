# app.py
from flask import Flask, request, redirect, url_for, render_template
import psycopg2
from config import db_config  # Importer la configuration de la base de données

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    # Récupérer l'ID du dernier tournoi
    cur.execute("SELECT id FROM Tournois ORDER BY date DESC LIMIT 1")
    dernier_tournoi = cur.fetchone()

    if dernier_tournoi:
        tournoi_id = dernier_tournoi[0]
        # Récupérer les résultats du dernier tournoi
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

    return render_template('index.html', resultats=resultats)

@app.route('/classement')
def classement():
    conn = get_db_connection()
    cur = conn.cursor()

    # Récupérer les joueurs triés par score TrueSkill et tier
    cur.execute("""
        SELECT nom, score_trueskill, tier
        FROM Joueurs
        ORDER BY score_trueskill DESC, tier ASC
    """)
    joueurs = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('classement.html', joueurs=joueurs)

@app.route('/add_tournament', methods=['GET', 'POST'])
def add_tournament():
    if request.method == 'POST':
        date = request.form['date']
        joueurs = []

        for i in range(1, 13):
            nom = request.form.get(f'nom{i}')
            score = request.form.get(f'score{i}')
            if nom and score:
                joueurs.append((nom, score))

        conn = get_db_connection()
        cur = conn.cursor()

        # Vérifier si le tournoi existe déjà
        cur.execute("SELECT id FROM Tournois WHERE date = %s", (date,))
        tournoi = cur.fetchone()

        if tournoi is None:
            # Créer un nouveau tournoi
            cur.execute("INSERT INTO Tournois (date) VALUES (%s) RETURNING id", (date,))
            tournoi_id = cur.fetchone()[0]
        else:
            tournoi_id = tournoi[0]

        for nom, score in joueurs:
            # Vérifier si le joueur existe déjà
            cur.execute("SELECT id FROM Joueurs WHERE nom = %s", (nom,))
            joueur = cur.fetchone()

            if joueur is None:
                # Créer un nouveau joueur
                cur.execute("INSERT INTO Joueurs (nom) VALUES (%s) RETURNING id", (nom,))
                joueur_id = cur.fetchone()[0]
            else:
                joueur_id = joueur[0]

            # Ajouter la participation
            cur.execute("INSERT INTO Participations (joueur_id, tournoi_id, score) VALUES (%s, %s, %s)",
                        (joueur_id, tournoi_id, score))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('confirmation'))

    return render_template('add_tournament.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
