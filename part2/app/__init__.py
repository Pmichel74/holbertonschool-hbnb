#!/usr/bin/python3
"""Initialisation de l'application Flask HBNB"""
from flask import Flask, jsonify
from flask_cors import CORS
from app.config import config

def create_app(config_name='default'):
    """Crée et configure l'application Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialiser CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Route de base pour vérifier que l'API est en ligne
    @app.route('/')
    def index():
        return jsonify({
            "status": "success",
            "message": "HBNB API is running. Access /api for the API documentation."
        })
    
    # Route de test simple
    @app.route('/test')
    def test():
        return jsonify({
            "status": "success",
            "message": "Test route is working!"
        })
    
    # Importation et enregistrement des routes de test
    from app.routes import test_bp
    app.register_blueprint(test_bp)
    
    # Initialisation du stockage (avant l'API pour éviter les problèmes d'accès au stockage)
    with app.app_context():
        from app.persistence import storage_engine
        storage_engine.storage = storage_engine.get_storage()
    
    # Enregistrement du blueprint API
    from app.api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint)
    
    # Initialisation des gestionnaires d'erreurs
    from app.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    @app.teardown_appcontext
    def close_storage(exception):
        """Ferme le stockage à la fin de chaque requête"""
        from app.persistence import storage_engine
        if hasattr(storage_engine, 'storage') and storage_engine.storage:
            storage_engine.storage.close()
    
    return app
