# frontend.py
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
BACKEND_URL = "http://127.0.0.1:8080"  # URL de l'API backend

@app.route('/')
def index():
    response = requests.get(f"{BACKEND_URL}/dernier-tournoi")
    resultats = response.json()
    return render_template("index.html", resultats=resultats)

@app.route('/classement')
def classement():
    response = requests.get(f"{BACKEND_URL}/classement")
    joueurs = response.json()
    return render_template("classement.html", joueurs=joueurs)

@app.route('/add_tournament', methods=['GET', 'POST'])
def add_tournament():
    if request.method == 'POST':
        date = request.form['date']
        joueurs = []

        for i in range(1, 13):
            nom = request.form.get(f'nom{i}')
            score = request.form.get(f'score{i}')
            if nom and score:
                joueurs.append({'nom': nom, 'score': score})

        payload = {'date': date, 'joueurs': joueurs}
        requests.post(f"{BACKEND_URL}/add-tournament", json=payload)

        return redirect(url_for('confirmation'))

    return render_template("add_tournament.html")

@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
