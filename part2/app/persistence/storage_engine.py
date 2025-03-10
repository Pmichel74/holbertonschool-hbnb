#!/usr/bin/python3
"""Module de gestion du stockage"""
import json
import os
import uuid
from datetime import datetime
from flask import current_app


class BaseStorage:
    """Interface de base pour le stockage"""
    
    def all(self, cls=None):
        """Récupère toutes les instances, optionnellement filtrées par classe"""
        pass
        
    def new(self, obj):
        """Ajoute un objet au stockage"""
        pass
        
    def save(self):
        """Persiste les changements"""
        pass
        
    def delete(self, obj):
        """Supprime un objet du stockage"""
        pass
        
    def get(self, cls, id):
        """Récupère un objet spécifique par son id"""
        pass
        
    def close(self):
        """Ferme la session de stockage"""
        pass


class FileStorage(BaseStorage):
    """Implémentation du stockage via fichiers JSON"""
    
    def __init__(self):
        """Initialise le stockage fichier"""
        self.__objects = {}
        self.__file_path = os.path.join(current_app.config['FILE_STORAGE_PATH'], "storage.json")
        os.makedirs(os.path.dirname(self.__file_path), exist_ok=True)
        self.reload()
        
    def all(self, cls=None):
        """Récupère toutes les instances, optionnellement filtrées par classe"""
        if cls is None:
            return list(self.__objects.values())
        return [obj for obj in self.__objects.values() 
                if obj.__class__.__name__ == cls.__name__]
        
    def new(self, obj):
        """Ajoute un objet au stockage"""
        if obj.id is None:
            obj.id = str(uuid.uuid4())
        if not hasattr(obj, 'created_at') or obj.created_at is None:
            obj.created_at = datetime.now()
        obj.updated_at = datetime.now()
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj
        
    def save(self):
        """Persiste les changements dans le fichier JSON"""
        serialized = {}
        for key, obj in self.__objects.items():
            serialized[key] = obj.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(serialized, f)
        
    def delete(self, obj):
        """Supprime un objet du stockage"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
                
    def get(self, cls, id):
        """Récupère un objet spécifique par son id"""
        key = f"{cls.__name__}.{id}"
        return self.__objects.get(key)
        
    def reload(self):
        """Charge les données depuis le fichier JSON"""
        from app.models.user import User
        from app.models.place import Place
        from app.models.amenity import Amenity
        from app.models.review import Review
        
        classes = {
            'User': User,
            'Place': Place,
            'Amenity': Amenity,
            'Review': Review
        }
        
        try:
            if os.path.isfile(self.__file_path):
                with open(self.__file_path, 'r') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        class_name = key.split('.')[0]
                        if class_name in classes:
                            self.__objects[key] = classes[class_name](**value)
        except Exception as e:
            print(f"Error loading data: {e}")
        
    def close(self):
        """Ferme la session (sauvegarde dans ce cas)"""
        self.save()


class MemoryStorage(BaseStorage):
    """Implémentation du stockage en mémoire"""
    
    def __init__(self):
        """Initialise le stockage mémoire"""
        self.__objects = {}
        
    def all(self, cls=None):
        """Récupère toutes les instances, optionnellement filtrées par classe"""
        if cls is None:
            return list(self.__objects.values())
        return [obj for obj in self.__objects.values() 
                if obj.__class__.__name__ == cls.__name__]
        
    def new(self, obj):
        """Ajoute un objet au stockage"""
        if obj.id is None:
            obj.id = str(uuid.uuid4())
        if not hasattr(obj, 'created_at') or obj.created_at is None:
            obj.created_at = datetime.now()
        obj.updated_at = datetime.now()
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj
        
    def save(self):
        """En mémoire, pas besoin de sauvegarder explicitement"""
        pass
        
    def delete(self, obj):
        """Supprime un objet du stockage"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
                
    def get(self, cls, id):
        """Récupère un objet spécifique par son id"""
        key = f"{cls.__name__}.{id}"
        return self.__objects.get(key)
        
    def close(self):
        """Pas besoin de fermeture pour le stockage mémoire"""
        pass


# Instance globale du moteur de stockage
storage = None

def get_storage():
    """Retourne une instance du moteur de stockage configuré"""
    storage_type = current_app.config.get('STORAGE_TYPE', 'memory')
    
    if storage_type == 'memory':
        return MemoryStorage()
    elif storage_type == 'file':
        return FileStorage()
    elif storage_type == 'db':
        # À implémenter plus tard
        # from app.persistence.db_storage import DBStorage
        # return DBStorage()
        raise NotImplementedError("Database storage not yet implemented")
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")
