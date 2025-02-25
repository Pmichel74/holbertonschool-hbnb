from uuid import uuid4

class User:
    def __init__(self, first_name, last_name, email, id=None):
        self.id = id or str(uuid4())
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
