#!/usr/bin/python3
"""Routes simples pour tester l'application"""
from flask import Blueprint, jsonify

test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/')
def index():
    """Route de test simple"""
    return jsonify({
        "status": "success",
        "message": "Test route is working!"
    })

@test_bp.route('/hello/<name>')
def hello(name):
    """Route de test avec paramètre"""
    return jsonify({
        "status": "success",
        "message": f"Hello, {name}!"
    })
