#!/usr/bin/python3
"""Module pour le Repository Pattern"""
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from os import getenv


class Repository:
    """Classe Repository pour gérer le stockage des données"""

    def __init__(self):
        """Initialise le repository avec le type de stockage approprié"""
        storage_type = getenv('HBNB_TYPE_STORAGE')
        if storage_type == 'db':
            self._storage = DBStorage()
        else:
            self._storage = FileStorage()
        self._storage.reload()

    def all(self, cls=None):
        """Retourne tous les objets d'une classe donnée"""
        return self._storage.all(cls)

    def new(self, obj):
        """Ajoute un nouvel objet au stockage"""
        self._storage.new(obj)

    def save(self):
        """Sauvegarde les modifications dans le stockage"""
        self._storage.save()

    def delete(self, obj=None):
        """Supprime un objet du stockage"""
        self._storage.delete(obj)

    def reload(self):
        """Recharge les données du stockage"""
        self._storage.reload()

    def close(self):
        """Ferme la session de stockage"""
        self._storage.close()

    def get(self, cls, id):
        """Récupère un objet par sa classe et son ID"""
        return self._storage.get(cls, id)

    def count(self, cls=None):
        """Compte le nombre d'objets dans le stockage"""
        return self._storage.count(cls)
