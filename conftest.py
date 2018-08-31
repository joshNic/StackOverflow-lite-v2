import os
import pytest
from app.views import app as create_app
import json
from app.database.db_operations import DbOperations
from app.database.db_connection import DbConnection
from instance.config import TestingConfig

@pytest.fixture
def app():
    app = create_app
    app.config.from_object(TestingConfig)
    # path = os.path.dirname(__file__)+'/databasetest.ini'
    # section = 'postgresqltest'
    # DbConnection(path, section)
    return app


token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MzU3OTY0MzAsInVzZXJfaWQiOjN9.MoKGAIu4NcUttqAvjwWND5i3SDjOcC9UQA-fujdKR8Y'
token2 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1NiwiZXhwIjoxNTM1ODM1MTQ1fQ.yMllFesA7EYg7PnGKENWf0nGVq4-H22lwV6W1AnqsAY'

@pytest.fixture
def make_response_register(client):
    mimetype = 'application/json'
    headers = {
        'mimetype': mimetype
    }
    data = {
        'user_email':'mu@gmail.com',
        'user_password':'joshua'
    }
    url = 'api/v2/auth/signup'
    response = client.post(url, json=data, headers=headers)
    yield response


@pytest.fixture
def make_response_post_question(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
    }
    data = {
        'question_title': 'what do you mean',
        'question_body': 'what does it mean'
    }
    url = '/api/v2/question'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_invalid_token(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': 'hkjhkhkhkjhkjSFjhVJVJcvjVGDdfgjHDFGJHFdhg'
    }
    data = {
        'question_title': 'what do you mean',
        'question_body': 'what does it mean'
    }
    url = '/api/v2/question'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_require_email(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
    }
    data = {
        
        'user_password': 'user_passsword'
    }
    url = '/api/v2/auth/signup'
    response = client.post(url, json=data, headers=headers)
    yield response


@pytest.fixture
def make_response_require_password(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
    }
    data = {
        'user_email': 'user_email'
    }
    url = '/api/v2/auth/signup'
    response = client.post(url, json=data, headers=headers)
    yield response

@pytest.fixture
def make_response_post_question_token(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token
    }
    data = {
        'question_title': 'what do you mean',
        'question_body': 'what does it mean'
    }
    url = '/api/v2/question'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_post_question_invalid(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token
    }
    data = {
        
        'question_body': 'what does it mean'
        }
    url = 'api/v2/question'
    response = client.post(url, data=data, headers=headers)
    yield response

@pytest.fixture
def make_response_get_questions(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
    }
    url = '/api/v2/questions'
    response = client.get(url, headers=headers)
    yield response


@pytest.fixture
def make_response_not_found(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
    }
    url = '/api/v2/questions/joshua?=tia'
    response = client.get(url, headers=headers)
    yield response


@pytest.fixture
def make_response_validate_answer(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token
    }
    data = {
        
    }
    url = '/api/v2/question/5/answer'
    response = client.get(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_validate_answer_object(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token
    }
    data = {

    }
    url = '/api/v2/question/5/answer'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_get_question(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
    }
    url = '/api/v2/question/4'
    response = client.get(url, headers=headers)
    yield response


@pytest.fixture
def make_response_invalid_submit(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
    }
    data = {
        'user_email': '.@joshu@gmail.com',
        'user_password': 'joshua'
    }
    url = '/api/v2/auth/signup'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_email(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
    }
    data = {
        'user_email': 'joshua',
        'user_password': 'joshua'
    }
    url = '/api/v2/auth/signup'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_invalid(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
    }
    data = {
        'user_email': '898',
        'user_password': 'joshua'
    }
    url = '/api/v2/auth/signup'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_inv_submit(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
    }
    data = {
        'user_email': '@',
        'user_password': 'joshua'
    }
    url = '/api/v2/auth/signup'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_check_request(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
    }
    data = {
        
        'question_body': 'mugisha joshua'
    }
    url = '/api/v2/question'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_check_request_token(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token
    }
    data = {
        'question_body': 'mugisha joshua'
    }
    url = '/api/v2/question'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_check_delete(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token
    }
    
    url = '/api/v2/question/3'
    response = client.delete(url, headers=headers)
    yield response


@pytest.fixture
def make_response_check_update(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token
    }

    url = '/api/v2/question/5'
    response = client.put(url, headers=headers)
    yield response


@pytest.fixture
def make_response_check_update_valid(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token2
    }
    data = {
        'question_title': 'what is not wat is not',
        'question_body': 'was not of not ofcos'
    }

    url = '/api/v2/question/4'
    response = client.put(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_check_update_valid_exists(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token2
    }
    data = {
        'question_title': 'what is not wat is not',
        'question_body': 'was not of not ofcos'
    }

    url = '/api/v2/question/7898'
    response = client.put(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_check_update_validate(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token2
    }
    data = {
        'question_title': 'what',
        'question_body': 'was not of not ofcos'
    }

    url = '/api/v2/question/4'
    response = client.put(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_check_update_valid_delete(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token2
    }

    url = '/api/v2/question/39'
    response = client.delete(url, headers=headers)
    yield response


@pytest.fixture
def make_response_check_post_answer(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token2
    }
    data = {
        'answer_body': 'what is not happening'
    }
    url = '/api/v2/question/7778/answer'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_check_post_answer_valid(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token2
    }
    data = {
        'answer_body': 'what is not happening'
    }
    url = '/api/v2/question/1/answer'
    response = client.post(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_check_update_answer_valid(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token2
    }
    data = {
        'answer_body': 'what is not happening happening'
    }
    url = '/api/v2/question/1/answer/87'
    response = client.put(url, data=json.dumps(data), headers=headers)
    yield response


@pytest.fixture
def make_response_check_update_answer_valid_response(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'x-access-token': token
    }
    data = {
        'answer_body': 'what is not happening happening'
    }
    url = '/api/v2/question/1/answer/56'
    response = client.put(url, data=json.dumps(data), headers=headers)
    yield response
