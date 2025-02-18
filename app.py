# app.py
from flask import Flask, request, redirect, url_for, render_template
import psycopg2

app = Flask(__name__)

# Configuration de la base de données PostgreSQL
db_config = {
    'dbname': 'votre_base_de_donnees',
    'user': 'votre_utilisateur',
    'password': 'votre_mot_de_passe',
    'host': 'localhost',
    'port': '5432'
}

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
