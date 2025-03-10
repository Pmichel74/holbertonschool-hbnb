#!/usr/bin/python3
"""Point d'entrée de l'application HBNB"""
import os
from app import create_app

# Déterminer l'environnement (development, production, testing)
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == "__main__":
    # Configurez le mode debug, le port, etc.
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host=host, port=port)
