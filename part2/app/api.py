#!/usr/bin/python3
"""API module"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/reviews', methods=['GET'])
def get_reviews():
    """Get all reviews"""
    return jsonify([])

@app.route('/api/v1/places', methods=['GET'])
def get_places():
    """Get all places"""
    return jsonify([])

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify([])

@app.route('/api/v1/amenities', methods=['GET'])
def get_amenities():
    """Get all amenities"""
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
