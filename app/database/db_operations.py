from db_connection import DbConnection

db_connect = DbConnection()


class DbOperations:
    def register_user(self, user_email, user_password, hash_password):
        """ insert a new vendor into the vendors table """
        sql = """INSERT INTO users(user_email, user_password, hash_password)
                VALUES(%s,%s, %s);"""
        return db_connect.connect(sql, (user_email, user_password, hash_password))

    def login_user(self, user_email, user_password):
        pass
    
    def insert_question(self, user_id, question_title, question_body):
        pass
    
    def upadte_question(self, question_title, question_body, question_id):
        pass
    
    def delete_question(self, question_id):
        pass
    
    def show_questions(self):
        pass
    
    def show_single_question(self, question_id):
        pass
    
    def insert_answers(self, question_id, user_id):
        pass
    
    def update_answer(self, answer_id):
        pass
    
    def delete_answer(self, answer_id):
        pass