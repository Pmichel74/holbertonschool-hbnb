from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('users', description='Opérations sur les utilisateurs')

# Modèle de validation pour l'entrée
user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='Prénom de l\'utilisateur'),
    'last_name': fields.String(required=True, description='Nom de l\'utilisateur'),
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe')
})

# Modèle de réponse (sans mot de passe)
user_output_model = api.model('UserOutput', {
    'id': fields.String(description='ID unique de l\'utilisateur'),
    'first_name': fields.String(description='Prénom de l\'utilisateur'),
    'last_name': fields.String(description='Nom de l\'utilisateur'),
    'email': fields.String(description='Email de l\'utilisateur')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_input_model, validate=True)
    @api.marshal_with(user_output_model, code=201)
    @api.doc(responses={
        201: 'Utilisateur créé avec succès',
        400: 'Email déjà enregistré ou données invalides'
    })
    def post(self):
        """Créer un nouvel utilisateur"""
        try:
            user_data = api.payload

            # Vérification de l'unicité de l'email
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                api.abort(400, 'Email déjà enregistré')

            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
            
        except Exception as e:
            api.abort(400, str(e))
