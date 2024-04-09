"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# Importation des modules nécessaires
import os

from django.core.asgi import get_asgi_application

# Définition du fichier de configuration des paramètres de Django pour ASGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Récupération de l'application ASGI de Django
application = get_asgi_application()

