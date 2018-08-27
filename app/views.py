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
