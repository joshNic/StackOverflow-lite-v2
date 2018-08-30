import os
from .db_connection import DbConnection
from app import create_app



class DbOperations:
    def __init__(self, path, section):
        self.path = path
        self.section = section
        self.db_connect = DbConnection(self.path, self.section)
    def register_user(self, user_email, user_password, hash_password):
        """ insert a new user into the users table """

        sql = """INSERT INTO users(user_email, user_password, hash_password)
                VALUES(%s,%s, %s);"""
        return self.db_connect.connect(sql, user_email, user_password, hash_password)

    def login_user(self, user_email, user_password):
        sql = """SELECT user_email, user_password FROM users WHERE user_email=%s AND user_password=%s"""
        query = self.db_connect.connect(
            sql, user_email, user_password)
        fetch = query.fetchone()
        return fetch

    def fetch_user_name(self, user_email):
        query = self.query_user_name(user_email)
        return query.fetchone()
    
    def fetch_user(self, user_email):
        query = self.query_user_name(user_email)
        return query.rowcount
    
    def query_user_name(self, user_email):
        sql = """SELECT * FROM users WHERE user_email=%s;"""
        query = self.db_connect.connect(sql, user_email)
        return query
    
    def fetch_question_title(self, question_title):
        sql = """SELECT * FROM questions WHERE question_title=%s;"""
        query = self.db_connect.connect(sql, question_title)
        fetch = query.fetchone()
        return fetch
    
    def question_title(self, question_title):
        sql = """SELECT * FROM questions WHERE question_title=%s;"""
        query = self.db_connect.connect(sql, question_title)
        fetch = query.rowcount
        return fetch
    
    def fetch_user_by_id(self, user_id):
        sql = """SELECT * FROM users WHERE user_id=%s;"""
        query = self.db_connect.connect(
            sql, user_id)
        fetch = query.fetchone()
        return fetch
        
    
    def insert_question(self, user_id, question_title, question_body):
        sql = """INSERT INTO questions(user_id, question_title, question_body)
                VALUES(%s,%s, %s);"""
        return self.db_connect.connect(sql, user_id, question_title, question_body)
    
    def upadte_question(self, question_title, question_body, question_id):
        sql = """ UPDATE questions
            SET 
            question_title = %s,
            question_body = %s
            WHERE question_id = %s"""
        return self.db_connect.connect(sql, question_title, question_body, question_id)
    
    def delete_question(self, question_id):
        sql = """DELETE  FROM questions WHERE question_id=%s;"""
        fetch = self.db_connect.connect(sql, question_id)
        query = fetch.rowcount
        return query
    
    def show_questions(self):
        sql = """SELECT * FROM questions;"""
        fetch = self.db_connect.connect(sql, None)
        query = fetch.fetchall()
        return query
    
    def show_single_question(self, question_id):
        sql = """SELECT * FROM questions WHERE question_id=%s;"""
        query = self.db_connect.connect(
            sql, question_id)
        fetch = query.fetchone()
        return fetch
    
    def insert_answers(self, answer_body, question_id, user_id):
        """ insert a new user into the users table """
        sql = """INSERT INTO answers(user_id, question_id, answer_body)
                VALUES(%s,%s, %s);"""
        return self.db_connect.connect(sql, user_id, question_id, answer_body)
    
    def update_answer(self, answer_body, answer_id):
        sql = """ UPDATE answers
            SET 
            answer_body = %s
            WHERE answer_id = %s"""
        return self.db_connect.connect(sql, answer_body, answer_id)
    
    def update_answer_user(self, answer_id):
        sql = """ UPDATE answers
            SET 
            accepted = TRUE
            WHERE answer_id = %s"""
        return self.db_connect.connect(sql, answer_id)
    
    def get_question_answers(self, question_id):
        sql = """SELECT * FROM answers WHERE question_id=%s;"""
        query = self.db_connect.connect(
            sql, question_id)
        fetch = query.fetchall()
        return fetch
    
    def get_single_answer(self, answer_id):
        sql = """SELECT * FROM answers WHERE answer_id=%s;"""
        query = self.db_connect.connect(
            sql, answer_id)
        fetch = query.fetchone()
        return fetch
    
    def delete_answer(self, answer_id):
        sql = """DELETE  FROM answers WHERE answer_id=%s;"""
        fetch = self.db_connect.connect(sql, answer_id)
        query = fetch.rowcount
        return query
    
    def create_tables(self):
        """ create tables in the PostgreSQL database"""
        commands = (
            """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            user_email VARCHAR(255) NOT NULL,
            user_password VARCHAR(255) NOT NULL,
            hash_password VARCHAR(255) NULL
        )
        """,
            """ 
        CREATE TABLE IF NOT EXISTS questions (
                question_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                question_title VARCHAR(255) NOT NULL,
                question_body VARCHAR(255) NOT NULL,
                created_at timestamp DEFAULT current_timestamp,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE
                )
        """,
            """
        CREATE TABLE IF NOT EXISTS answers (
                answer_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                question_id INTEGER,
                answer_body VARCHAR(255) NOT NULL,
                accepted BOOLEAN NOT NULL,
                created_at timestamp DEFAULT current_timestamp,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
        )
        for command in commands:
            self.db_connect.connect(None, command)
        return True
    
    def drop_tables(self):
        sql = ("""DROP TABLE IF EXISTS users, questions, answers""")
        self.db_connect.connect(sql, None)
        return True 
