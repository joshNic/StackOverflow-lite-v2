import os
from .db_connection import DbConnection
from app import create_app



class DbOperations:
    def __init__(self):
        
        self.db_connect = DbConnection()
        # self.drop_tables()
        # self.create_tables()
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
    
    def query_answers(self, answer_id):
        sql = """SELECT * FROM answers WHERE answer_id=%s;"""
        query = self.db_connect.connect(sql, answer_id)
        return query.fetchone()
    
    def fetch_question_title(self, question_title):
        fetc = self.query_title(question_title)
        return fetc.fetchone()
    
    def query_title(self, question_title):
        sql = """SELECT * FROM questions WHERE question_title=%s;"""
        query = self.db_connect.connect(sql, question_title)
        return query
    
    def question_title(self, question_title):
        fetch = self.query_title(question_title)
        return fetch.rowcount
    
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
        sql = """
        SELECT
         questions.*, users.user_email
        FROM
         questions 
        LEFT JOIN
         users
        ON
         questions.user_id=users.user_id
        ORDER BY
         questions.created_at DESC;
        """
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
        sql = """
        SELECT
         answers.*, users.user_email
        FROM
         answers 
        LEFT JOIN
         users
        ON
         answers.user_id=users.user_id
        WHERE question_id=%s
        ORDER BY
         answers.created_at DESC;
        """
        query = self.db_connect.connect(
            sql, question_id)
        fetch = query.fetchall()
        return fetch

    def get_user_questions(self, user_id):
        fetch = self.query_user_questions(user_id)
        return fetch.fetchall()
    
    def get_user_question_number(self, user_id):
        fetch = self.query_user_questions(user_id)
        return fetch.rowcount
    
    def query_user_questions(self, user_id):
        sql = """
        SELECT
         questions.question_id,questions.question_body,questions.question_title,count(answers.*) as answer_count
        FROM
         questions 
        LEFT JOIN
         answers
        ON
         questions.question_id=answers.question_id
        WHERE
         questions.user_id=%s
        GROUP BY
         questions.question_id
        ORDER BY
         answer_count DESC;
        """
        query = self.db_connect.connect(
            sql, user_id)
        return query
    
    def get_single_answer(self, answer_id):
        sql = """SELECT * FROM answers WHERE answer_id=%s;"""
        query = self.db_connect.connect(
            sql, answer_id)
        fetch = query.fetchone()
        return fetch
    
    def get_total_answers(self, user_id):
        sql = """
        SELECT COALESCE(SUM(answer_count),0)
            FROM
            (
            SELECT
                questions.question_id,questions.question_body,questions.question_title,count(answers.*) as answer_count, users.user_id, users.user_email
                FROM
                    questions 
                LEFT JOIN
                    answers
                ON
                    questions.question_id=answers.question_id
                LEFT JOIN
                    users
                ON
                    questions.user_id=users.user_id
                WHERE
                    questions.user_id=%s
                GROUP BY
                    questions.question_id,
                    users.user_id
                ORDER BY
                    answer_count DESC
                ) t;
        """
        query = self.db_connect.connect(
            sql, user_id)
        fetch = query.fetchone()[0]
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
