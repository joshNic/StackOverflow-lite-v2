import os
import psycopg2
from app.database.config import config

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
        
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
            database='dl71kl016q7qc', user="rqxoljondpygyq", password="859c79cc406ee2799982b5e28f4935ae69cc09842200211a43749c54e7df5087", host="ec2-54-235-86-226.compute-1.amazonaws.com", port="5432"
        )
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


