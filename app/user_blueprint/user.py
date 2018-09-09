from flask import Blueprint, jsonify, request, make_response, current_app
from ..models.user_actions import UserActions
from werkzeug.security import check_password_hash
import jwt
import datetime

user_actions_object = UserActions()

mod = Blueprint('user', __name__)


@mod.route('/signup', methods=['POST'])
def register_user():
    if not request.json:
        return jsonify({'error': 'unsupported format'}), 400
    elif 'user_email' not in request.json:
        return jsonify({'error': 'user name is requred'}), 400
    elif 'user_password' not in request.json:
        return jsonify({'error': 'password required'}), 400
    user_email = request.json['user_email']
    user_password = request.json['user_password']
    if not validate_email(user_email):
        user_actions_object.user_register(user_email, user_password)
        return jsonify({'success': 'registered successfully'}), 201
    else:
        return validate_email(user_email)


def validate_email(user_email):
    check_duplicate_email = user_actions_object.get_user(user_email)

    if check_duplicate_email > 0:
        return jsonify({'message': 'Sorry user already exixts'}), 409
    elif len(user_email) < 6:
        return jsonify({'error': 'Email can not be less than six\
            characters'}), 400
    elif user_email.isdigit():
        return jsonify({'error': 'Email format not allowed\
        an email can not only have numbers'}), 400
    elif "@" not in user_email:
        return jsonify({'error': 'Email format not allowed\
        an email must conatain @'}), 400
    elif "." not in user_email:
        return jsonify({'error': 'Email format not allowed\
        an email must conatain . character'}), 400
    elif user_email.startswith("@") or user_email.startswith("."):
        return jsonify({'error': 'Email format not allowed\
        an email must not start with @ or . character'}), 400
    elif "@." in user_email:
        return jsonify({'error': 'Email format not allowed an email must not start with @ or . character next to each other'}), 400
    elif ".@" in user_email:
        return jsonify({'error': 'Email format not allowed an email must not start with @ or . character next to each other'}), 400


@mod.route('/login', methods=['GET'])
def login_user():
    current_app.config['SECRET_KEY'] = 'secret123'
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
                'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    hours=48
                )
            }, current_app.config['SECRET_KEY']
        )
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('unauthorized access', 401, {'WWW-Authenticate':
                                                      'Basic realm="Login required!"'})
