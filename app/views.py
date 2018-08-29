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
        return jsonify({'error': 'improper data format',
                        'help - proper format': {
                            'answer_body': 'answer body'
                        }}), 400
    if 'answer_body' not in request_object:
        return {'error': 'please answer can not be empty'}

# user signup endpoint
@app.route('/api/v2/auth/signup', methods=['POST'])
def register_user():
    request_data = request.get_json()
    user_email = request_data['user_email']
    user_password = request_data['user_password']
    reg = user_actions_object.user_register(user_email, user_password)
    return jsonify(reg), 201

# user signin endpoint
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
                'user_id': user[0], 'exp' :datetime.datetime.utcnow() + datetime.timedelta(
                    minutes=20
                )
            }, app.config['SECRET_KEY']
        )
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('unauthorized access', 401, {'WWW-Authenticate':
                                                      'Basic realm="Login required!"'})
    
# create question endpoint
@app.route('/api/v2/question', methods=['POST'])
@token_required
def post_question(current_user):
    request_data = request.get_json()
    if not validate_question_object(request_data):
        title = request_data['question_title']
        body = request_data['question_body']
        user_actions_object.create_question(current_user, title, body)
    return jsonify({'message': 'question successfully created'}), 201

def validate_question_object(request_object):
    if not request_object:
        return jsonify({'error': 'improper data format',
                        'help - proper format': {
                            'question_title': 'question title',
                            'question_body': 'question body'

                        }}), 400
    if 'question_title' not in request_object:
        return jsonify({'error': 'please title is required'}), 400
    if 'question_body' not in request_object:
        return jsonify({'error': 'please body is required'}), 400

# get all questions endpoint
@app.route('/api/v2/questions', methods=['GET'])
def get_all():
    results = user_actions_object.view_all_questions()
    container = []
    for result in results:
        q_obj = {
            'question_id':result[0],
            'question_author_id': result[1],
            'question_title': result[2],
            'question_body': result[3]
        }
        container.append(q_obj)
    return jsonify({'All Questions': container}), 200

# get single questions endpoint
@app.route('/api/v2/question/<int:question_id>', methods=['GET'])
def get_single_question(question_id):
    results = user_actions_object.view_single_question(question_id)
    answers = user_actions_object.view_all_question_answers(question_id)
    container = []
    answer_container = []
    for result in answers:
        a_obj = {
            'answer_id':result[0],
            'question_author_id': result[1],
            'question_id': result[2],
            'answer_body': result[3],
            'answer_status': result[4]
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

# update question endpoint
@app.route('/api/v2/question/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    request_data = request.get_json()
    if not validate_question_object(request_data):
        title = request_data['question_title']
        body = request_data['question_body']
        user_actions_object.update_question(title, body, question_id)
    return jsonify({'message': 'Question successfully updated'}), 200

# delete question endpoint
@app.route('/api/v2/question/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    user_actions_object.delete_question(question_id)
    return jsonify({'message': 'Question successfully deleted'}), 200
    
# add answer endpoint
@app.route('/api/v2/question/<int:question_id>/answer', methods=['POST'])
@token_required
def post_answer(current_user, question_id):
    request_data = request.get_json()
    answer_body = request_data['answer_body']
    create_answer = user_actions_object.create_answer(
        current_user, question_id, answer_body
    )
    if create_answer:
        return jsonify({'message': 'Answer successfully added'}), 201
    else:
        return jsonify({'message': 'Answer not added'}), 400

# add update answer endpoint
@app.route('/api/v2/question/<int:question_id>/answer/<int:answer_id>', methods=['PUT'])
@token_required
def upadte_answer(current_user, question_id, answer_id):
    get_one_answer = user_actions_object.fetch_single_answer(answer_id)
    get_one_question = user_actions_object.view_single_question(question_id)
    if get_one_answer[1] == current_user:
        request_data = request.get_json()
        answer_body = request_data['answer_body']
        update_answer = user_actions_object.update_answer(answer_id, answer_body)
        if update_answer:
            return jsonify({'message': 'Answer successfully update'}), 201
        else:
            return jsonify({'message': 'Answer not Updated'}), 400
    
    elif get_one_question[1] == current_user:
        update_answer_user = user_actions_object.update_answer_user(answer_id)
        if update_answer_user:
            return jsonify({'message': 'Answer Accepted'}), 201
        else:
            return jsonify({'message': 'Answer not Updated'}), 400
    else:
        return jsonify({'message': 'You are not the author of the question or the answer'}), 401
