from .user import User
from .question import Question
from .answer import Answer
from ..database.db_operations import DbOperations
from werkzeug.security import generate_password_hash, check_password_hash

userObject = User()
databaseObject = DbOperations()
questionObject = Question()
answerObject = Answer()

class UserActions:
    
    def user_register(self, user_email, user_password):
        userObject.user_email = user_email
        userObject.user_password = user_password
        hash_password = generate_password_hash(userObject.user_password, method='sha256')
        store_user = databaseObject.register_user(
            userObject.user_email, userObject.user_password, hash_password
        )
        return {'message': 'user created'}
    
    def user_login(self, user_email):
        userObject.user_email = user_email
        # userObject.user_password = user_password
        get_user = databaseObject.fetch_user_name(
            userObject.user_email
        )
        return get_user
    
    def get_user_by_id(self, user_id):
        userObject.user_id = user_id
        # userObject.user_password = user_password
        get_user = databaseObject.fetch_user_by_id(
            userObject.user_id
        )
        return get_user
    
    def create_question(self, user_id, title, body):
        userObject.user_id = user_id
        questionObject.title = title
        questionObject.body = body
        insert_question = databaseObject.insert_question(
            userObject.user_id, questionObject.title, questionObject.body
        )
        return insert_question
    
    def view_all_questions(self):
        return databaseObject.show_questions()
    
    def view_single_question(self, question_id):
        fetch_question = databaseObject.show_single_question(question_id)
        return fetch_question
    
    def update_question(self, question_title, question_body, question_id):
        update_question = databaseObject.upadte_question(
            question_title, question_body, question_id
        )
        return update_question
    
    def delete_question(self, question_id):
        delete_question = databaseObject.delete_question(question_id)
        return delete_question
    
    def create_answer(self, user_id, question_id, answer_body):
        answerObject.user_id = user_id
        answerObject.question_id = question_id
        answerObject.answer_body = answer_body

        insert_answer = databaseObject.insert_answers(
            answerObject.answer_body, answerObject.question_id, answerObject.user_id
        )
        return insert_answer

    def delete_answer(self):
        pass
    def update_answer(self, answer_id, answer_body):
        update_answer = databaseObject.update_answer(
            answer_body, answer_id
        )
        return update_answer
    
    def update_answer_user(self, answer_id):
        update_answer_user = databaseObject.update_answer_user(answer_id)
        return update_answer_user
    
    def fetch_single_answer(self, answer_id):
        fetchOne = databaseObject.get_single_answer(answer_id)
        return fetchOne
