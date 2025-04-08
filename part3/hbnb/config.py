import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_JSON_SERIALIZATION_ENABLED = True  # Allow dictionaries as identity values
    JWT_TOKEN_LOCATION = ['headers']  # Look for the JWT in the headers
    JWT_HEADER_TYPE = 'Bearer'  # The JWT should be preceded by this word in the header
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
