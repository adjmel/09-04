# Ce code définit une classe MyappConfig qui hérite de la classe AppConfig fournie par Django. 
# Importation de la classe AppConfig fournie par Django
from django.apps import AppConfig

# Définition de la classe de configuration de l'application
class MyappConfig(AppConfig):
    # Définition du champ de clé primaire automatique par défaut
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Définition du nom de l'application
    name = 'myapp'
