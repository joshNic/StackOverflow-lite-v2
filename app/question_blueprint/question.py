from flask import Blueprint, jsonify, request, make_response, current_app
from ..models.user_actions import UserActions
from werkzeug.security import check_password_hash
import jwt
import datetime
from functools import wraps

user_actions_object = UserActions()

qn_bp = Blueprint('question', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        current_app.config['SECRET_KEY'] = 'secret123'
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_use = user_actions_object.get_user_by_id(data['user_id'])
            current_user = current_use[0]
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def check_request():
    if not request.json:
        return jsonify({'error': 'unsupported format'}), 400
    elif 'question_title' not in request.json:
        return jsonify({'error': 'question title is requred'}), 400
    elif 'question_body' not in request.json:
        return jsonify({'error': 'question body is required'}), 400


@qn_bp.route('/question', methods=['POST'])
@token_required
def post_question(current_user):
    if not check_request():
        title = request.json['question_title']
        body = request.json['question_body']
        if len(title) < 6:
            return jsonify({'error': 'question title too short'}), 400
        elif title.isdigit():
            return jsonify({'error': 'question can not contain only numbers'}), 400

        check_duplicate_title = user_actions_object.get_title(title)
        if check_duplicate_title > 0:
            get_duplicate = user_actions_object.get_question_title(title)
            return jsonify({'message': 'question already asked',
                            'duplicate_question_id': get_duplicate[0]}), 409
        user_actions_object.create_question(current_user, title, body)
        return jsonify({'message': 'question successfully created'}), 201
    return check_request()

# get all questions endpoint


@qn_bp.route('/questions', methods=['GET'])
def get_all():
    results = user_actions_object.view_all_questions()
    container = []
    if len(results) > 0:
        for result in results:
            q_obj = {
                'question_id': result[0],
                'question_author_id': result[1],
                'question_title': result[2],
                'question_body': result[3]
            }
            container.append(q_obj)
        return jsonify({'All Questions': container}), 200
    return jsonify({'messages': 'No questions on the platform yet'}), 200

# get single questions endpoint


@qn_bp.route('/question/<int:question_id>', methods=['GET'])
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
    return jsonify({'message': 'Questions does not exist'}), 404

# update question endpoint


@qn_bp.route('/question/<int:question_id>', methods=['PUT'])
@token_required
def update_question(current_user, question_id):
    get_one_question = user_actions_object.view_single_question(question_id)
    if get_one_question:
        if get_one_question[1] == current_user:
            if not check_request():
                title = request.json['question_title']
                body = request.json['question_body']
                if len(title) < 6:
                    return jsonify({'error': 'question title too short'}), 400
                elif title.isdigit():
                    return jsonify({'error': 'question can not contain only numbers'}), 400
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


@qn_bp.route('/question/<int:question_id>', methods=['DELETE'])
@token_required
def delete_question(current_user, question_id):
    get_one_question = user_actions_object.view_single_question(question_id)
    if get_one_question:
        if get_one_question[1] == current_user:
            user_actions_object.delete_question(question_id)
            return jsonify({'message': 'Question successfully deleted'}), 200
        return jsonify({'error': 'You are not the owner of the question'}), 401
    return jsonify({'message': 'question does not exist'}), 400
