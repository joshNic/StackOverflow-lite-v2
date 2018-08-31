import os
import pytest
from app.database.db_operations import DbOperations
from app.database.db_connection import DbConnection


@pytest.fixture
def db_operations(scope="module"):
    db_operations_object = DbOperations()
    yield db_operations_object


def test_register_user(db_operations):
    user_email = "joshua@gmail.com"
    user_password = "josha"
    user_hash = "joshua"
    assert db_operations.register_user(user_email, user_password, user_hash)
    # assert db_operations.register_user(user_email, user_password, user_hash) == None


def test_login_user(db_operations):
    user_email = "joshua@gmail.com"
    user_password = "josha"
    assert db_operations.login_user(user_email, user_password)
    assert isinstance(db_operations.login_user(
        user_email, user_password), tuple)


def test_fetch_user_name(db_operations):
    user_email = "joshua@gmail.com"
    assert db_operations.fetch_user_name(user_email)
    assert len(db_operations.fetch_user_name(user_email)) == 4
    assert isinstance(db_operations.fetch_user_name(
        user_email), tuple)
    assert not isinstance(db_operations.fetch_user_name(
        user_email), list)


def test_fetch_user_by_id(db_operations):
    user_id = 5
    assert db_operations.fetch_user_by_id(user_id) == None
    assert not isinstance(db_operations.fetch_user_by_id(
        user_id), tuple)
    assert not isinstance(db_operations.fetch_user_by_id(
        user_id), list)


def test_insert_question(db_operations):
    user_id = 1
    question_title = "Is this all that andela has got"
    question_body = "Am wondering if this as hard as it gets or gets"
    assert db_operations.insert_question(
        user_id, question_title, question_body)


def test_upadte_question(db_operations):
    question_id = 1
    question_title = "all that andela has got"
    question_body = "Am wondering if this as hard as it gets"
    assert db_operations.upadte_question(
        question_title, question_body, question_id)


def test_delete_question(db_operations):
    question_id = 2
    assert db_operations.delete_question(question_id) == 0


def test_show_questions(db_operations):
    assert isinstance(db_operations.show_questions(), list)
    assert len(db_operations.show_questions()) > 0


def test_show_single_question(db_operations):
    question_id = 5
    assert db_operations.show_single_question(question_id) == None
    assert isinstance(db_operations.show_single_question(
        question_id), tuple) == False
    assert len(db_operations.show_single_question(
        question_id)) == 5
    assert not isinstance(db_operations.show_single_question(
        question_id), list)


def test_insert_answer(db_operations):
    user_id = 2
    question_id = 4
    answer_body = "Is this all that andela has got"
    assert db_operations.insert_answers(
        answer_body, question_id, user_id
    )


def test_update_answer(db_operations):
    answer_id = 1
    answer_body = "Is all got"
    assert db_operations.update_answer(
        answer_body, answer_id
    )


def test_update_answer_user(db_operations):
    answer_id = 1
    assert db_operations.update_answer_user(answer_id)


def test_get_question_answers(db_operations):
    question_id = 5
    assert isinstance(db_operations.get_question_answers(question_id), list)
    assert len(db_operations.get_question_answers(question_id)) == 0


def test_get_single_answer(db_operations):
    answer_id = 5
    assert not  isinstance(db_operations.get_single_answer(answer_id), tuple)
    


def test_delete_answer(db_operations):
    answer_id = 7
    assert db_operations.delete_answer(answer_id) == 0
