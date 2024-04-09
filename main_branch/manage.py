#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# Importation des modules nécessaires
import os
import sys

# Définition de la fonction principale
def main():
    """Run administrative tasks."""

    # Définition du fichier de configuration des paramètres de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

    try:
        # Tentative d'importation de la fonction execute_from_command_line de Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Gestion de l'erreur si Django n'est pas installé ou indisponible
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Exécution de la commande passée en ligne de commande
    execute_from_command_line(sys.argv)

# Vérification si le script est exécuté directement
if __name__ == '__main__':
    # Appel de la fonction principale
    main()
