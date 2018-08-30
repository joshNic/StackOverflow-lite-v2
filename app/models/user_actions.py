from .user import User
from .question import Question
from .answer import Answer
from ..database.db_operations import DbOperations
from werkzeug.security import generate_password_hash, check_password_hash

userObject = User()
questionObject = Question()
answerObject = Answer()


class UserActions:
    def __init__(self):
        self.databaseObject = DbOperations()
        # self.databaseObject.drop_tables()
        # self.databaseObject.create_tables()

    def user_register(self, user_email, user_password):
        userObject.user_email = user_email
        userObject.user_password = user_password
        hash_password = generate_password_hash(
            userObject.user_password, method='sha256')
        self.databaseObject.register_user(
            userObject.user_email, userObject.user_password, hash_password
        )
        return {'message': 'user created'}

    def user_login(self, user_email):
        userObject.user_email = user_email
        # userObject.user_password = user_password
        get_user = self.databaseObject.fetch_user_name(
            userObject.user_email
        )
        return get_user

    def get_user_by_id(self, user_id):
        userObject.user_id = user_id
        # userObject.user_password = user_password
        get_user = self.databaseObject.fetch_user_by_id(
            userObject.user_id
        )
        return get_user

    def create_question(self, user_id, title, body):
        userObject.user_id = user_id
        questionObject.title = title
        questionObject.body = body
        insert_question = self.databaseObject.insert_question(
            userObject.user_id, questionObject.title, questionObject.body
        )
        return insert_question

    def view_all_questions(self):
        return self.databaseObject.show_questions()

    def view_all_question_answers(self, question_id):
        return self.databaseObject.get_question_answers(question_id)

    def view_single_question(self, question_id):
        fetch_question = self.databaseObject.show_single_question(question_id)
        return fetch_question

    def update_question(self, question_title, question_body, question_id):
        update_question = self.databaseObject.upadte_question(
            question_title, question_body, question_id
        )
        return update_question

    def delete_question(self, question_id):
        delete_question = self.databaseObject.delete_question(question_id)
        return delete_question

    def create_answer(self, user_id, question_id, answer_body):
        answerObject.user_id = user_id
        answerObject.question_id = question_id
        answerObject.answer_body = answer_body

        insert_answer = self.databaseObject.insert_answers(
            answerObject.answer_body, answerObject.question_id, answerObject.user_id
        )
        return insert_answer

    def delete_answer(self):
        pass

    def update_answer(self, answer_id, answer_body):
        update_answer = self.databaseObject.update_answer(
            answer_body, answer_id
        )
        return update_answer

    def update_answer_user(self, answer_id):
        update_answer_user = self.databaseObject.update_answer_user(answer_id)
        return update_answer_user

    def fetch_single_answer(self, answer_id):
        fetchOne = self.databaseObject.get_single_answer(answer_id)
        return fetchOne
    
    def get_user_name(self, user_email):
        fetch = self.databaseObject.fetch_user_name(user_email)
        return fetch

    def get_user(self, user_email):
        fetch = self.databaseObject.fetch_user(user_email)
        return fetch

    def get_question_title(self, question_title):
        fetch = self.databaseObject.fetch_question_title(question_title)
        return fetch

    def get_title(self, question_title):
        fetch = self.databaseObject.question_title(question_title)
        return fetch
    
