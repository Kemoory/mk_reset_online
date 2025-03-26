# app.py
from flask import Flask, request, redirect, url_for, render_template
import psycopg2

app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html', )#resultats=resultats)

@app.route('/classement')
def classement():

    return render_template('classement.html', )#joueurs=joueurs)

@app.route('/add_tournament', methods=['GET', 'POST'])
def add_tournament():

    #return redirect(url_for('confirmation'))

    return render_template('add_tournament.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
