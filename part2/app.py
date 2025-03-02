from flask import Flask

app = Flask(__name__)

# Import les routes après avoir créé l'application pour éviter les imports circulaires
from app.api.v1 import amenities, places, reviews, users

# Configuration des routes API
app.register_blueprint(amenities.blueprint)
app.register_blueprint(places.blueprint)
app.register_blueprint(reviews.blueprint)
app.register_blueprint(users.blueprint)

if __name__ == '__main__':
    app.run(debug=True)