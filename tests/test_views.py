import pytest
import json


def test_get_all(make_response_get_questions):
    assert make_response_get_questions.status_code == 200
    assert  not isinstance(make_response_get_questions.json, list)

def test_get_single_question(make_response_get_questions):
    assert make_response_get_questions.status_code == 200


def test_register_user(make_response_register):
    assert make_response_register.status_code == 201
    
