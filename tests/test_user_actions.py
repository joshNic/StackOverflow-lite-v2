import os
import pytest
from app.models.user_actions import UserActions


@pytest.fixture
def user_actions(scope="module"):
    path = os.path.dirname(__file__)+'/databasetest.ini'
    section = 'postgresqltest'
    user_action_object = UserActions()
    yield user_action_object


def test_user_register(user_actions):
    user_email = "256jomu@gmail.com"
    user_password = "joshua"
    assert user_actions.user_register(user_email, user_password)


def test_user_login(user_actions):
    user_email = "256jomu@gmail.com"
    assert user_actions.user_login(user_email)
    assert isinstance(user_actions.user_login(user_email), tuple)


def test_get_user_by_id(user_actions):
    user_id = 5
    assert user_actions.get_user_by_id(user_id) != None
    assert isinstance(user_actions.get_user_by_id(user_id), tuple)


def test_create_question(user_actions):
    user_id = 1
    question_body = "what is waht was"
    question_title = "this is it"
    assert user_actions.create_question(user_id, question_title, question_body)


def test_view_all_questions(user_actions):
    assert user_actions.view_all_questions()
    assert isinstance(user_actions.view_all_questions(), list)
    assert len(user_actions.view_all_questions()) > 0


def test_view_all_question_answers(user_actions):
    question_id = 8
    assert isinstance(
        user_actions.view_all_question_answers(question_id), list)
    assert len(user_actions.view_all_question_answers(question_id)) == 0


def test_view_single_question(user_actions):
    question_id = 5
    assert  isinstance(
        user_actions.view_single_question(question_id), tuple)
    assert user_actions.view_single_question(question_id) != None


def test_update_question(user_actions):
    question_id = 5
    question_body = "this was not"
    question_title = "Ofcos not for them"
    assert user_actions.update_question(
        question_title, question_body, question_id
    )


def test_delete_question(user_actions):
    question_id = 10
    assert user_actions.delete_question(question_id) == 0


def test_create_answer(user_actions):
    user_id = 2
    question_id = 5
    answer_body = "that was not is"
    assert user_actions.create_answer(user_id, question_id, answer_body)


def test_update_answer(user_actions):
    answer_id = 2
    answer_body = "that was not is"
    assert user_actions.update_answer(answer_id, answer_body)


def test_update_answer_user(user_actions):
    answer_id = 2
    assert user_actions.update_answer_user(answer_id)


def test_fetch_single_answer(user_actions):
    answer_id = 5
    assert isinstance(user_actions.fetch_single_answer(answer_id), tuple) == True
    
