# app/db.py
from app.models.user import User

# Simuler une base de données d'utilisateurs
users_db = {
    1: User(first_name="Alice", last_name="Wonder", email="alice@example.com", is_admin=False),
    2: User(first_name="Bob", last_name="Builder", email="bob@example.com", is_admin=False)
}

def get_all_users():
    return users_db

def get_user_by_id(user_id):
    return users_db.get(user_id)

def add_user(user):
    users_db[user.id] = user

def delete_user(user_id):
    if user_id in users_db:
        del users_db[user_id]
