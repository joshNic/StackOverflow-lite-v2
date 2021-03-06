from flask import (
    Flask, jsonify, make_response, redirect, json, Response, request, abort
)
import jwt
import time
from datetime import date
from decimal import Decimal
from functools import wraps
from werkzeug.security import check_password_hash
import datetime
from app import create_app
from flask_cors import CORS
import os
from .models.user_actions import UserActions

user_actions_object = UserActions()

app = create_app()
app.config['SECRET_KEY'] = 'secret123'
CORS(app)


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
            current_use = user_actions_object.get_user_by_id(data['user_id'])
            current_user = current_use[0]
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


def validate_answer_object(request_object):
    if not request_object:
        return jsonify({'error': 'unsuported format'}), 400
    if 'answer_body' not in request_object:
        return {'error': 'please answer can not be empty'}, 400

# user signup endpoint


@app.route('/api/v2/auth/signup', methods=['POST'])
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


@app.route('/api/v2/auth/login', methods=['GET'])
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
                'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    hours=48
                )
            }, app.config['SECRET_KEY']
        )
        return jsonify({'token': token.decode('UTF-8')}), 200
    return make_response('unauthorized access', 401, {'WWW-Authenticate':
                                                      'Basic realm="Login required!"'})

# create question endpoint


@app.route('/api/v2/question', methods=['POST'])
@token_required
def post_question(current_user):
    if not check_request():
        title = request.json['question_title']
        body = request.json['question_body']
        if len(title) < 6:
            return jsonify({'message': 'question title too short'}), 400
        elif title.isdigit():
            return jsonify({'message': 'question can not contain only numbers'}), 400

        check_duplicate_title = user_actions_object.get_title(title)
        if check_duplicate_title > 0:
            get_duplicate = user_actions_object.get_question_title(title)
            return jsonify({'message': 'question already asked',
                            'duplicate_question_id': get_duplicate[0]}), 409
        user_actions_object.create_question(current_user, title, body)
        return jsonify({'message': 'question successfully created'}), 201
    return check_request()


def check_request():
    if not request.json:
        return jsonify({'message': 'unsupported format'}), 400
    elif 'question_title' not in request.json:
        return jsonify({'message': 'question title is requred'}), 400
    elif 'question_body' not in request.json:
        return jsonify({'message': 'question body is required'}), 400


def check_answer_request():
    if not request.json:
        return jsonify({'error': 'unsupported format'}), 400
    elif 'answer_body' not in request.json:
        return jsonify({'error': 'question body is requred'}), 400


# get all questions endpoint
@app.route('/api/v2/questions', methods=['GET'])
def get_all():
    results = user_actions_object.view_all_questions()
    container = []
    if len(results) > 0:
        for result in results:
            
            q_obj = {
                'question_id': result[0],
                'question_author_id': result[1],
                'question_title': result[2],
                'question_body': result[3],
                'question_date': result[4].strftime("%A %d. %B %Y"),
                'question_author': result[5]
            }
            container.append(q_obj)
        return jsonify(container), 200
    return jsonify({'message': 'No questions on the platform yet'}), 200

# get all user questions and answers endpoint


@app.route('/api/v2/profile', methods=['GET'])
@token_required
def get_all_user_questions(current_user):
    results = user_actions_object.get_user_questions(current_user)
    result_count = user_actions_object.get_user_question_count(current_user)
    user = user_actions_object.get_user_by_id(current_user)
    answers = user_actions_object.get_user_answers_number(current_user)
    container = []
    containers = [{'count': result_count, 'user': user[1],
                  'answers':json.dumps(Decimal(answers))}]
    if len(results) > 0:
        for result in results:
            q_obj = {
                'question_id': result[0],
                'question_body': result[1],
                'question_title': result[2],
                'answer_count': result[3]
            }
            container.append(q_obj)
        return jsonify({'message':container, 'details':containers}), 200
    return jsonify({'message': 'No questions on the platform yet'}), 200

# get single questions endpoint


@app.route('/api/v2/question/<int:question_id>', methods=['GET'])
def get_single_question(question_id):
    results = user_actions_object.view_single_question(question_id)
    if results:
        answers = user_actions_object.view_all_question_answers(question_id)
        container = []
        answer_container = []
        for result in answers:
            a_obj = {
                'answer_id': result[0],
                'question_author_id': result[1],
                'question_id': result[2],
                'answer_body': result[3],
                'answer_status': result[4],
                'answer_date': result[5].strftime("%A %d. %B %Y"),
                'answer_author':result[6]
            }
            answer_container.append(a_obj)
        q_obj = {
            'question_id': results[0],
            'question_author_id': results[1],
            'question_title': results[2],
            'question_body': results[3],
            'answers': answer_container
        }
        container.append(q_obj)
        return jsonify(container), 200
    return jsonify({'message': 'Questions does not exist'}), 404


@app.route('/api/v2/answer/<int:answer_id>', methods=['GET'])
def get_single_answer(answer_id):
    results = user_actions_object.view_single_answer(answer_id)
    if results:
        container = []
        a_obj = {
            'answer_id': results[0],
            'question_author_id': results[1],
            'question_id': results[2],
            'answer_body': results[3],
            'answer_status': results[4]
        }
        container.append(a_obj)
        return jsonify(container), 200
    return jsonify({'message': 'Answer does not exist'}), 404
# update question endpoint


@app.route('/api/v2/question/<int:question_id>', methods=['PUT'])
@token_required
def update_question(current_user, question_id):
    get_one_question = user_actions_object.view_single_question(question_id)
    if get_one_question:
        if get_one_question[1] == current_user:
            if not check_request():
                title = request.json['question_title']
                body = request.json['question_body']
                if len(title) < 6:
                    return jsonify({'message': 'question title too short'}), 400
                elif title.isdigit():
                    return jsonify({'message': 'question can not contain only numbers'}), 400
                check_duplicate_title = user_actions_object.get_title(title)
                if check_duplicate_title > 0:
                    return jsonify({'message': 'Sorry question of same title exists'}), 409
                else:
                    user_actions_object.update_question(
                        title, body, question_id)
                    return jsonify({'message': 'Question successfully updated'}), 200
            return check_request()
        return jsonify({'message': 'You are not the owner of the question'}), 401
    return jsonify({'message': 'Question does not exist'}), 404

# delete question endpoint


@app.route('/api/v2/question/<int:question_id>', methods=['DELETE'])
@token_required
def delete_question(current_user, question_id):
    get_one_question = user_actions_object.view_single_question(question_id)
    if get_one_question:
        if get_one_question[1] == current_user:
            user_actions_object.delete_question(question_id)
            return jsonify({'message': 'Question successfully deleted'}), 200
        return jsonify({'message': 'You are not the owner of the question'}), 401
    return jsonify({'message': 'question does not exist'}), 400

# add answer endpoint


@app.route('/api/v2/question/<int:question_id>/answer', methods=['POST'])
@token_required
def post_answer(current_user, question_id):
    get_one_question = user_actions_object.view_single_question(question_id)
    if get_one_question:
        if not check_answer_request():
            answer_body = request.json['answer_body']
            create_answer = user_actions_object.create_answer(
                current_user, question_id, answer_body
            )
            if create_answer:
                return jsonify({'message': 'Answer successfully added'}), 201
            else:
                return jsonify({'message': 'Answer not added'}), 400
        return check_answer_request()
    return jsonify({'message': 'Question does not exist'}), 404

# add update answer endpoint


@app.route('/api/v2/question/<int:question_id>/answer/<int:answer_id>', methods=['PUT'])
@token_required
def upadte_answer(current_user, question_id, answer_id):
    get_one_answer = user_actions_object.fetch_single_answer(answer_id)
    get_one_question = user_actions_object.view_single_question(question_id)

    
    try:
        if get_one_answer[1] == current_user:
            if not check_answer_request():
                answer_body = request.json['answer_body']
                update_answer = user_actions_object.update_answer(
                    answer_id, answer_body)
                if update_answer:
                    return jsonify({'message': 'Answer successfully update'}), 201
                else:
                    return jsonify({'message': 'Answer not Updated'}), 400
            return check_answer_request()
        elif get_one_question[1] == current_user:
            update_answer_user = user_actions_object.update_answer_user(
                answer_id)
            if update_answer_user:
                return jsonify({'message': 'Answer Accepted'}), 201
            else:
                return jsonify({'message': 'Answer not Updated'}), 400
    except:
        return jsonify({'message': 'Resource not found'}), 404
    return jsonify({'message': 'You are not the author of the question or the answer'}), 401


def validate_email(user_email):
    check_duplicate_email = user_actions_object.get_user(user_email)

    if check_duplicate_email > 0:
        return jsonify({'error': 'Sorry user already exists'}), 409
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
