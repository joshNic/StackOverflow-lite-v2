from flask import Blueprint, jsonify, request, make_response, current_app
from ..models.user_actions import UserActions
from werkzeug.security import check_password_hash
import jwt
import datetime
from functools import wraps

user_actions_object = UserActions()

ans_bp = Blueprint('answer', __name__)


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


def check_answer_request():
    if not request.json:
        return jsonify({'error': 'unsupported format'}), 400
    elif 'answer_body' not in request.json:
        return jsonify({'error': 'question body is requred'}), 400

def validate_answer_object(request_object):
    if not request_object:
        return jsonify({'error': 'unsuported format'}), 400
    if 'answer_body' not in request_object:
        return {'error': 'please answer can not be empty'}, 400


@ans_bp.route('/<int:question_id>/answer', methods=['POST'])
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


@ans_bp.route('/<int:question_id>/answer/<int:answer_id>', methods=['PUT'])
@token_required
def upadte_answer(current_user, question_id, answer_id):
    get_one_answer = user_actions_object.fetch_single_answer(answer_id)
    get_one_question = user_actions_object.view_single_question(question_id)

    if get_one_question[1] == current_user:
        update_answer_user = user_actions_object.update_answer_user(
            answer_id)
        if update_answer_user:
            return jsonify({'message': 'Answer Accepted'}), 201
        else:
            return jsonify({'message': 'Answer not Updated'}), 400

    elif get_one_answer[1] == current_user:
        if not check_answer_request():
            answer_body = request.json['answer_body']
            update_answer = user_actions_object.update_answer(
                answer_id, answer_body)
            if update_answer:
                return jsonify({'message': 'Answer successfully update'}), 201
            else:
                return jsonify({'message': 'Answer not Updated'}), 400
        return check_answer_request()
    return jsonify({'message': 'You are not the author of the question or the answer'}), 401
