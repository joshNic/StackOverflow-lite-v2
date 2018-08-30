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
    url = 'http://localhost:8080/api/v2/auth/signup'
    response = client.post(url, json=data)
    yield response


# @pytest.fixture
# def make_response_get_question(client):
#     mimetype = 'application/json'
#     headers = {
#         'Content-Type': mimetype
#     }
#     url = '/api/v1/question/2'
#     response = client.get(url, headers=headers)
#     yield response


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
def make_response_get_question(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype
    }
    url = '/api/v2/question/4'
    response = client.get(url, headers=headers)
    yield response
