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
        sql = """INSERT INTO questions(user_id, question_title, question_body)
                VALUES(%s,%s, %s);"""
        return db_connect.connect(sql, user_id, question_title, question_body)
    
    def upadte_question(self, question_title, question_body, question_id):
        sql = """ UPDATE questions
            SET 
            question_title = %s,
            question_body = %s
            WHERE question_id = %s"""
        return db_connect.connect(sql, question_title, question_body, question_id)
    
    def delete_question(self, question_id):
        sql = """DELETE  FROM questions WHERE question_id=%s;"""
        fetch = db_connect.connect(sql, question_id)
        query = fetch.rowcount
        return query
    
    def show_questions(self):
        sql = """SELECT * FROM questions;"""
        fetch = db_connect.connect(sql, None)
        query = fetch.fetchall()
        return query
    
    def show_single_question(self, question_id):
        sql = """SELECT * FROM questions WHERE question_id=%s;"""
        query = db_connect.connect(
            sql, question_id)
        fetch = query.fetchone()
        return fetch
    
    def insert_answers(self, answer_body, question_id, user_id):
        """ insert a new user into the users table """
        sql = """INSERT INTO answers(user_id, question_id, answer_body)
                VALUES(%s,%s, %s);"""
        return db_connect.connect(sql, user_id, question_id, answer_body)
    
    def update_answer(self, answer_body, answer_id):
        sql = """ UPDATE answers
            SET 
            answer_body = %s
            WHERE answer_id = %s"""
        return db_connect.connect(sql, answer_body, answer_id)
    
    def update_answer_user(self, answer_id):
        sql = """ UPDATE answers
            SET 
            accepted = TRUE
            WHERE answer_id = %s"""
        return db_connect.connect(sql, answer_id)
    
    def get_question_answers(self, question_id):
        sql = """SELECT * FROM answers WHERE question_id=%s;"""
        query = db_connect.connect(
            sql, question_id)
        fetch = query.fetchall()
        return fetch
    
    def get_single_answer(self, answer_id):
        sql = """SELECT * FROM answers WHERE answer_id=%s;"""
        query = db_connect.connect(
            sql, answer_id)
        fetch = query.fetchone()
        return fetch
    
    def delete_answer(self, answer_id):
        pass

