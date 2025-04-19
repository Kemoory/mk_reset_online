# Utiliser une image de base légère Python
FROM python:3.9-slim-bullseye

# Définir le répertoire de travail
WORKDIR /backEnd

# Copier les fichiers nécessaires dans l'image
COPY requirement.txt .
COPY backend.py .
COPY config.py .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirement.txt


# Exposer le port Flask
EXPOSE 8080

# Commande pour démarrer l'application
CMD ["python", "backend.py"]