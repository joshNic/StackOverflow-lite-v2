import pytest
import json


def test_get_all(make_response_get_questions):
    assert make_response_get_questions.status_code == 200
    assert isinstance(make_response_get_questions.json, list)

def test_get_single_question(make_response_get_questions):
    assert make_response_get_questions.status_code == 200

def test_register_user(
    make_response_register, make_response_require_email,
    make_response_require_password
    
):
    assert make_response_register.status_code == 201
    assert make_response_require_email.status_code == 400
    assert 'user name is requred' in make_response_require_email.json['error']
    assert make_response_require_password.status_code == 400
    assert 'password required' in make_response_require_password.json['error']
    
def test_validate_email(
    make_response_email, make_response_invalid_submit,
    make_response_invalid, make_response_inv_submit
):

    assert make_response_invalid_submit.status_code == 400
    assert make_response_email.status_code == 400
    assert make_response_invalid.status_code == 400
    assert make_response_inv_submit.status_code == 400



def test_post_question(
    make_response_post_question, make_response_post_question_token,
    make_response_post_question_invalid
):
    assert make_response_post_question.status_code == 401
    assert make_response_post_question_token.status_code == 401
    assert make_response_post_question_invalid.status_code == 401


def test_check_answer_request(make_response_post_question_invalid):
    assert make_response_post_question_invalid.status_code == 401


def test_not_found(make_response_not_found):
    assert make_response_not_found.status_code == 404


def test_validate_answer_object(
    make_response_validate_answer, make_response_validate_answer_object
):
    assert make_response_validate_answer.status_code == 405
    assert make_response_validate_answer_object.status_code == 401


def test_token_required(make_response_post_question, make_response_invalid_token):
    assert make_response_post_question.status_code == 401
    assert 'Token is missing' in make_response_post_question.json['message']
    assert make_response_invalid_token.status_code == 401
    assert 'Token is invalid' in make_response_invalid_token.json['message']


def test_check_request(make_response_check_request, make_response_check_request_token):
    assert make_response_check_request.status_code == 401
    assert make_response_check_request_token.status_code == 401


def test_delete_question(make_response_check_delete, make_response_check_update_valid_delete):
    assert make_response_check_delete.status_code == 401
    assert make_response_check_update_valid_delete.status_code == 401
    # assert make_response_check_request_token.status_code == 400


def test_update_question(make_response_check_update, make_response_check_update_valid,
                         make_response_check_update_valid_exists, make_response_check_update_validate):
    assert make_response_check_update.status_code == 401
    assert make_response_check_update_valid.status_code == 401
    assert make_response_check_update_valid_exists.status_code == 401
    assert make_response_check_update_validate.status_code == 401


def test_post_answer(make_response_check_post_answer, make_response_check_post_answer_valid):
    assert make_response_check_post_answer.status_code == 401
    assert make_response_check_post_answer_valid.status_code == 401


def test_update_answer(make_response_check_update_answer_valid, make_response_check_update_answer_valid_response):
    assert make_response_check_update_answer_valid.status_code == 401
    assert make_response_check_update_answer_valid_response.status_code == 401
