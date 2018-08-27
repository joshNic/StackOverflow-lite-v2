from flask import (
    Flask, jsonify, make_response, redirect, json, Response, request
)
import jwt
from functools import wraps
from werkzeug.security import check_password_hash
import datetime
from app import create_app
from .models.user_actions import UserActions

user_actions_object = UserActions()

app = create_app()
app.config['SECRET_KEY'] = 'secret123'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user_actions_object.get_user_by_id(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)

# user signup endpoint
@app.route('/auth/signup', methods=['POST'])
def register_user():
    request_data = request.get_json()
    user_email = request_data['user_email']
    user_password = request_data['user_password']
    reg = user_actions_object.user_register(user_email, user_password)
    return jsonify(reg), 201

# user signin endpoint
@app.route('/auth/login', methods=['GET'])
def login_user():
    pass
