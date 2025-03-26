/* static/js/scripts.js */
let joueurCount = 1;

function ajouterJoueur() {
    if (joueurCount >= 12) {
        alert("Vous ne pouvez pas ajouter plus de 12 joueurs.");
        return;
    }
    joueurCount++;
    const joueursContainer = document.getElementById('joueursContainer');
    const newJoueurDiv = document.createElement('div');
    newJoueurDiv.className = 'box joueur';
    newJoueurDiv.innerHTML = `
        <div class="field">
            <label class="label" for="nom${joueurCount}">Nom du joueur ${joueurCount}:</label>
            <div class="control">
                <input type="text" id="nom${joueurCount}" name="nom${joueurCount}" class="input" required>
            </div>
        </div>
        <div class="field">
            <label class="label" for="score${joueurCount}">Score du joueur ${joueurCount}:</label>
            <div class="control">
                <input type="number" id="score${joueurCount}" name="score${joueurCount}" class="input" required>
            </div>
        </div>
        <button type="button" class="button is-danger is-small remove-joueur" onclick="supprimerJoueur(this)">Supprimer</button>
    `;
    joueursContainer.appendChild(newJoueurDiv);
}

function supprimerJoueur(button) {
    const joueurDiv = button.parentElement;
    joueurDiv.remove();
    joueurCount--;
    renumeroterJoueurs();
}

function renumeroterJoueurs() {
    const joueursContainer = document.getElementById('joueursContainer');
    const joueurs = joueursContainer.getElementsByClassName('joueur');
    for (let i = 0; i < joueurs.length; i++) {
        const joueur = joueurs[i];
        joueur.querySelector('label[for^="nom"]').setAttribute('for', `nom${i + 1}`);
        joueur.querySelector('label[for^="nom"]').textContent = `Nom du joueur ${i + 1}:`;
        joueur.querySelector('input[id^="nom"]').setAttribute('id', `nom${i + 1}`);
        joueur.querySelector('input[id^="nom"]').setAttribute('name', `nom${i + 1}`);

        joueur.querySelector('label[for^="score"]').setAttribute('for', `score${i + 1}`);
        joueur.querySelector('label[for^="score"]').textContent = `Score du joueur ${i + 1}:`;
        joueur.querySelector('input[id^="score"]').setAttribute('id', `score${i + 1}`);
        joueur.querySelector('input[id^="score"]').setAttribute('name', `score${i + 1}`);
    }
}



/** Possibilité de faire une requête AJAX pour mettre à jour les scores TrueSkill côté serveur
 * def update_trueskill_scores():
    """Met à jour les scores TrueSkill et tiers des joueurs en fonction de leurs performances"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Récupérer tous les joueurs et leurs participations
        cur.execute("""
            SELECT j.id, j.nom, SUM(p.score), COUNT(p.tournoi_id)
            FROM Joueurs j
            LEFT JOIN Participations p ON j.id = p.joueur_id
            GROUP BY j.id, j.nom
        """)
        joueurs_data = cur.fetchall()
        
        # Calculer un score TrueSkill simplifié pour chaque joueur
        for joueur_id, nom, total_score, nb_tournois in joueurs_data:
            if total_score is None or nb_tournois == 0:
                continue
                
            # Calcul simplifié (à adapter selon votre algorithme de score réel)
            avg_score = total_score / nb_tournois
            trueskill = avg_score * (1 + (nb_tournois * 0.05))  # Bonus pour participation régulière
            
            # Déterminer le tier en fonction du score
            if trueskill > 200:
                tier = 'S'
            elif trueskill > 175:
                tier = 'A'
            elif trueskill > 150:
                tier = 'B'
            else:
                tier = 'C'
                
            # Mettre à jour le joueur
            cur.execute("""
                UPDATE Joueurs
                SET score_trueskill = %s, tier = %s
                WHERE id = %s
            """, (trueskill, tier, joueur_id))
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erreur lors de la mise à jour des scores TrueSkill: {e}")
    finally:
        cur.close()
        conn.close()
 */
