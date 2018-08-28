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
    

