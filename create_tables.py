import os
import psycopg2
from app.database.config import config

path = os.path.dirname(__file__)+'/database.ini'
section = 'postgresqltest'
def create_tables():
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
                question_title TEXT NOT NULL,
                question_body TEXT NOT NULL,
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
                answer_body TEXT NOT NULL,
                accepted BOOLEAN NOT NULL DEFAULT FALSE,
                created_at timestamp DEFAULT current_timestamp,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )
    conn = None
    try:
        # read the connection parameters
        params = config(path, section)
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
