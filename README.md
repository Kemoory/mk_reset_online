# 🏁 Mario Kart Reset Online

## 🎮 Description

**Mario Kart Reset Online** est une application web dynamique permettant de suivre les résultats de tournois de Mario Kart. Elle propose une interface utilisateur pour consulter les résultats des tournois ayant été joués, afficher un classement général des joueurs basé sur l’algorithme **TrueSkill**, et explorer des **statistiques détaillées** sur les performances des joueurs.

Lien vers le [dépôt](https://github.com/Kemoory/mk_reset_online).

## 🚀 Fonctionnalités principales

- 📊 **Consultation des résultats de tournois**  
  Affichage clair des résultats du dernier tournoi ou des précédents.

- 🏆 **Classement général des joueurs**  
  Mise à jour dynamique du classement des joueurs selon leurs performances dans les différents tournois, calculé via **TrueSkill** : [trueskill.org](https://trueskill.org/)

- 📈 **Statistiques détaillées**  
  Accès à diverses statistiques : nombre de victoires, ratio victoires/défaites, score moyen, etc.

## 🛠️ Technologies utilisées

### Frontend
- `HTML` — Structure des pages
- `CSS` + `Bulma` — Design
- `JavaScript` — Interactivité

### Backend
- `Flask` — API et logique serveur

### Base de données
- `PostgreSQL` — Stockage des données des joueurs, tournois et statistiques

## Architecture
```
mk_reset_online/
├── frontend/            # Code HTML/CSS/JS
├── backend/             # Code Flask/Django/Express
├── docker-compose.yml   # Configuration Docker multi-conteneur
└── README.md
```


## 🧪 Installation et lancement

### Prérequis

- Python 3.9+
- PostgreSQL
- Docker & Docker Compose (n'oubliez pas de démarrer docker)

### Via Docker 

Cloner le projet :
```bash
git clone git@github.com:Kemoory/mk_reset_online.git
cd path/to/mk_reset_online
```
Configurer `docker-compose.yml` pour donner l'accès à la base de donner que vous avez créée en amont :
```bash
version: '3.8'

services:
  backend:
    build:
      context: ./backEnd
      dockerfile: Dockerfile.backend
    ports:
      - "8080:8080"
    volumes:
      - pg_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=username
      - POSTGRES_PASSWORD=mypassword
      - POSTGRES_DB=database_name
    restart: unless-stopped

  frontend:
    build:
      context: ./frontEnd
      dockerfile: Dockerfile.frontend
    ports:
      - "5000:5000"
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:8080
    restart: unless-stopped

volumes:
  pg_data:
```
Pour exécuter :
```bash
docker-compose build
docker-compose up
```
Pour arrêter le processus :
```bash
docker-compose down -v 
```