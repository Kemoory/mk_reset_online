# app.py
from flask import Flask, request, redirect, url_for, render_template, flash
import psycopg2
from config import db_config  # Importer la configuration de la base de données

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Nécessaire pour utiliser flash()

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
    # Gère les cas où score_trueskill ou tier sont NULL
    cur.execute("""
        SELECT 
            nom, 
            COALESCE(score_trueskill, 0) as score_trueskill, 
            COALESCE(tier, 'C') as tier
        FROM Joueurs
        ORDER BY score_trueskill DESC NULLS LAST, tier ASC NULLS LAST
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

        # Parcourir jusqu'à 12 joueurs
        for i in range(1, 13):
            nom = request.form.get(f'nom{i}')
            score = request.form.get(f'score{i}')
            if nom and score:
                try:
                    score_int = int(score)
                except ValueError:
                    flash(f"Le score pour le joueur {i} n'est pas un nombre valide.", "danger")
                    return redirect(url_for('add_tournament'))
                joueurs.append((nom.strip(), score_int))

        if not joueurs:
            flash("Veuillez ajouter au moins un joueur avec son score.", "warning")
            return redirect(url_for('add_tournament'))

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # Vérifier si le tournoi existe déjà
            cur.execute("SELECT id FROM public.tournois WHERE date = %s", (date,))
            tournoi = cur.fetchone()

            if tournoi is None:
                # Créer un nouveau tournoi
                cur.execute("INSERT INTO public.tournois (date) VALUES (%s) RETURNING id", (date,))
                tournoi_id = cur.fetchone()[0]
            else:
                tournoi_id = tournoi[0]

            for nom, score in joueurs:
                # Vérifier si le joueur existe déjà
                cur.execute("SELECT id FROM public.joueurs WHERE nom = %s", (nom,))
                joueur = cur.fetchone()

                if joueur is None:
                    # Créer un nouveau joueur avec des valeurs par défaut pour score_trueskill et tier
                    # En utilisant les valeurs par défaut compatibles avec les contraintes de la table
                    cur.execute("""
                        INSERT INTO public.joueurs (nom, score_trueskill, tier) 
                        VALUES (%s, %s, %s) 
                        RETURNING id
                        """, (nom, 1000.0, 'C'))  # Score initial et tier C par défaut
                    joueur_id = cur.fetchone()[0]
                else:
                    joueur_id = joueur[0]

                # Ajouter la participation
                cur.execute("INSERT INTO public.participations (joueur_id, tournoi_id, score) VALUES (%s, %s, %s)",
                            (joueur_id, tournoi_id, score))

            conn.commit()
            flash("Tournoi et participations ajoutés avec succès.", "success")
        except Exception as e:
            conn.rollback()
            flash("Une erreur est survenue lors de l'ajout du tournoi.", "danger")
            print(e)
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('confirmation'))
    
    # Pour la méthode GET, récupérer tous les joueurs existants pour l'autocomplétion
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Récupérer les noms des joueurs existants
    cur.execute("SELECT id, nom FROM public.joueurs ORDER BY nom")
    result = cur.fetchall()
    
    # Transformer en liste de dictionnaires pour faciliter l'utilisation dans le template
    joueurs = [{"id": row[0], "nom": row[1]} for row in result]
    
    cur.close()
    conn.close()

    return render_template('add_tournament.html', joueurs=joueurs)

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)