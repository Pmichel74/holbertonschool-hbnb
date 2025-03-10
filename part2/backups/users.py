cat > /home/patri/hbnb/part2/temp_fix/users_api.py << 'EOF'
#!/usr/bin/python3
"""Routes API pour la gestion des utilisateurs"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.middlewares.validation_middleware import ValidationMiddleware
from app.error_handlers import ValidationError, NotFoundError
from app.persistence.storage_engine import storage

api = Namespace('users', description='Opérations sur les utilisateurs')

# Modèles Swagger pour la documentation de l'API
user_input_model = api.model('UserInput', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe'),
    'first_name': fields.String(description='Prénom'),
    'last_name': fields.String(description='Nom')
})

user_update_model = api.model('UserUpdate', {
    'email': fields.String(description='Email de l\'utilisateur'),
    'password': fields.String(description='Mot de passe'),
    'first_name': fields.String(description='Prénom'),
    'last_name': fields.String(description='Nom')
})

user_model = api.model('User', {
    'id': fields.String(description='ID unique'),
    'email': fields.String(description='Email de l\'utilisateur'),
    'first_name': fields.String(description='Prénom'),
    'last_name': fields.String(description='Nom'),
    'created_at': fields.DateTime(description='Date de création'),
    'updated_at': fields.DateTime(description='Date de mise à jour')
})

# Initialiser le service avec notre stockage - en l'important ici pour éviter les imports circulaires
# from app.services.user_service import UserService
# La ligne ci-dessus cause l'import circulaire - créons une solution temporaire
class UserServiceTemp:
    def __init__(self, storage):
        self.storage = storage
        
    def get_all(self):
        from app.models.user import User
        return self.storage.all(User)
        
    def create(self, data):
        from app.models.user import User
        user = User(**data)
        if 'password' in data:
            user.set_password(data['password'])
        self.storage.new(user)
        self.storage.save()
        return user
        
    def get(self, user_id):
        from app.models.user import User
        return self.storage.get(User, user_id)
        
    def update(self, user_id, data):
        user = self.get(user_id)
        if not user:
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"User {user_id} not found")
            
        if 'password' in data:
            user.set_password(data['password'])
            data.pop('password')
            
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
                
        self.storage.save()
        return user
        
    def delete(self, user_id):
        user = self.get(user_id)
        if not user:
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"User {user_id} not found")
            
        self.storage.delete(user)
        self.storage.save()
        return True

# Utiliser notre service temporaire
user_service = UserServiceTemp(storage)

@api.route('/')
class UserList(Resource):
    """Gestion de la collection d'utilisateurs"""
    
    @api.doc('list_users', 
             responses={
                 200: 'Success',
                 500: 'Internal Server Error'
             })
    @api.marshal_list_with(user_model)
    def get(self):
        """Liste tous les utilisateurs"""
        try:
            users = user_service.get_all()
            return [user.to_dict() for user in users]
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('create_user',
             responses={
                 201: 'User Created',
                 400: 'Validation Error',
                 500: 'Internal Server Error'
             })
    @api.expect(user_input_model)
    @api.marshal_with(user_model, code=201)
    @ValidationMiddleware.validate_user_data()
    def post(self):
        """Crée un nouvel utilisateur"""
        try:
            data = request.get_json()
            user = user_service.create(data)
            return user.to_dict(), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))

@api.route('/<user_id>')
@api.param('user_id', 'L\'identifiant de l\'utilisateur')
@api.response(404, 'Utilisateur non trouvé')
class UserResource(Resource):
    """Gestion d'un utilisateur spécifique"""

    @api.doc('get_user',
             responses={
                 200: 'Success',
                 404: 'User Not Found',
                 500: 'Internal Server Error'
             })
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Récupère un utilisateur par son ID"""
        try:
            user = user_service.get(user_id)
            if not user:
                api.abort(404, f"Utilisateur {user_id} non trouvé")
            return user.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('update_user',
             responses={
                 200: 'Success',
                 400: 'Validation Error',
                 404: 'User Not Found',
                 500: 'Internal Server Error'
             })
    @api.expect(user_update_model)
    @api.marshal_with(user_model)
    @ValidationMiddleware.validate_user_data()
    def put(self, user_id):
        """Met à jour un utilisateur"""
        try:
            data = request.get_json()
            updated_user = user_service.update(user_id, data)
            return updated_user.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('delete_user',
             responses={
                 204: 'User Deleted',
                 404: 'User Not Found',
                 500: 'Internal Server Error'
             })
    @api.response(204, 'Utilisateur supprimé')
    def delete(self, user_id):
        """Supprime un utilisateur"""
        try:
            user_service.delete(user_id)
            return '', 204
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))
EOF