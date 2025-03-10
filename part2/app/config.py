#!/usr/bin/python3
"""Configuration de l'application"""
import os

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key-for-dev')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-for-dev')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 heure
    DEBUG = False
    TESTING = False
    FILE_STORAGE_PATH = os.environ.get('FILE_STORAGE_PATH', '/home/patri/hbnb/part2/storage')
    STORAGE_TYPE = os.environ.get('STORAGE_TYPE', 'file')  # 'memory', 'file', 'db'

class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    
class TestingConfig(Config):
    """Configuration de test"""
    TESTING = True
    DEBUG = True
    STORAGE_TYPE = 'memory'
    
class ProductionConfig(Config):
    """Configuration de production"""
    # Assurez-vous de définir des variables d'environnement sécurisées en production
    pass
    
# Configurations disponibles
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
