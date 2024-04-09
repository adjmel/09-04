# Utilisez une image de Python comme base
FROM python:3.10.13

# Définition du répertoire de travail dans le conteneur
# WORKDIR /app
WORKDIR .

# Copie du code source et du fichier requirements.txt dans le conteneur
COPY . .

# Installation des dépendances à partir du fichier requirements.txt
RUN pip install -r requirements.txt \
    && python manage.py migrate \
    && pip install Django \
    && pip install -U djangorestframework \
    && pip install djangorestframework_simplejwt \
    && apt install python3 \
    && pip install django-otp \
    && pip install django-user-agents \
    && pip install qrcode \
    && pip install pyotp
    # && pip install django-otp-plugins \

# Commande pour démarrer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
