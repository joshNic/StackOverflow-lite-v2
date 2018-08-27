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
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('unauthorized accessss', 401, {'WWW-Authenticate': 
        'Basic realm="Login required!"'})
    user = user_actions_object.user_login(auth.username)
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate':
                                                       'Basic realm="Login required!"'})
    if check_password_hash(user[3], auth.password):
        token = jwt.encode(
            {
                'user_id': user[0], 'exp' :datetime.datetime.utcnow() + datetime.timedelta(
                    minutes=20
                )
            }, app.config['SECRET_KEY']
        )
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('unauthorized access', 401, {'WWW-Authenticate':
                                                      'Basic realm="Login required!"'})
    
