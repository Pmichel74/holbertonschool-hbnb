from uuid import uuid4

class User:
    def __init__(self, first_name, last_name, email, password=None):
        self.id = str(uuid4())
        self.first_name  = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


    def to_dict(self):
        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
            }
