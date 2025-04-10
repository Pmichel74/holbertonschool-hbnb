from flask import Flask, make_response, jsonify, request, redirect
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

# Définir les extensions en premier
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Set JWT configuration
    app.config['JWT_JSON_SERIALIZATION_ENABLED'] = True
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  # Tokens valides pendant 24h
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']  # S'assurer que JWT utilise la clé secrète
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Chercher le token uniquement dans le header
    app.config['JWT_HEADER_NAME'] = 'Authorization'  # Nom du header contenant le token
    app.config['JWT_HEADER_TYPE'] = 'Bearer'  # Type de token (Bearer)
    
    # Configurer CORS
    app.config['CORS_HEADERS'] = 'Content-Type'  # Ajout de la configuration CORS_HEADERS
    
    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # Configurer CORS pour permettre les requêtes cross-origin
    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5500'  # Autoriser l'origine du frontend
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Add POST for reviews
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'  # En-têtes autorisés
        response.headers['Access-Control-Allow-Credentials'] = 'true'  # Autoriser les cookies et les identifiants
        return response
    
    # Simplifier les gestionnaires OPTIONS pour éviter les conflits
    @app.route('/<path:path>', methods=['OPTIONS'])
    @app.route('/', methods=['OPTIONS'])
    def handle_options(path=''):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5500')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 200
    
    # Créer l'API Flask-RestX
    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Add a JWT token to the header with the format: Bearer <JWT_TOKEN>'
        }
    }
    
    api = Api(app, 
              version='1.0', 
              title='HBnB API', 
              description='HBnB Application API', 
              doc='/api/v1/',
              authorizations=authorizations,
              security='Bearer Auth')
    
    # Importer les namespaces APRÈS avoir initialisé db
    # Ces importations sont déplacées ici pour éviter les importations circulaires
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    
    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    @app.route('/api/v1/places', methods=['GET'])
    def places_without_slash():
        return redirect('/api/v1/places/', code=307)  # Temporary redirect to avoid CORS issues
    
    @app.route('/api/v1/places/<place_id>/reviews', methods=['POST', 'OPTIONS'])
    def place_reviews_endpoint(place_id):
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5500')
            response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200
        else:
            # Rediriger vers le bon endpoint du namespace reviews
            # Cette route sert principalement à gérer le CORS pour les requêtes POST
            return redirect('/api/v1/reviews', code=307)  # Temporary redirect
    
    return app
