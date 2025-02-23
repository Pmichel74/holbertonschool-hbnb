import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ma_cle_secrete')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
