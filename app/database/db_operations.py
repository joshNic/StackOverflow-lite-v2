from .db_connection import DbConnection

db_connect = DbConnection()


class DbOperations:
    def register_user(self, user_email, user_password, hash_password):
        """ insert a new user into the users table """
        sql = """INSERT INTO users(user_email, user_password, hash_password)
                VALUES(%s,%s, %s);"""
        return db_connect.connect(sql, user_email, user_password, hash_password)

    def login_user(self, user_email, user_password):
        sql = """SELECT user_email, user_password FROM users WHERE user_email=%s AND user_password=%s"""
        query = db_connect.connect(
            sql, user_email, user_password)
        fetch = query.fetchone()
        return fetch

    def fetch_user_name(self, user_email):
        sql = """SELECT * FROM users WHERE user_email=%s;"""
        query = db_connect.connect(
            sql, user_email)
        fetch = query.fetchone()
        return fetch
    
    def fetch_user_by_id(self, user_id):
        sql = """SELECT * FROM users WHERE user_id=%s;"""
        query = db_connect.connect(
            sql, user_id)
        fetch = query.fetchone()
        return fetch
        
    
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

