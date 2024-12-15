from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.json
    if auth and auth.get('username') == 'admin' and auth.get('password') == 'password':
        access_token = create_access_token(identity={'username': 'admin'})
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid credentials"}), 401
