import psycopg2
from .config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_email VARCHAR(255) NOT NULL,
            user_password VARCHAR(255) NOT NULL,
            hash_password VARCHAR(255) NULL
        )
        """,
        """ 
        CREATE TABLE questions (
                question_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                question_title VARCHAR(255) NOT NULL,
                question_body VARCHAR(255) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE
                )
        """,
        """
        CREATE TABLE answers (
                answer_id SERIAL PRIMARY KEY,
                user_id INTEGER,
                question_id INTEGER,
                answer_body VARCHAR(255) NOT NULL,
                accepted BOOLEAN NOT NULL,
                question_body VARCHAR(255) NOT NULL,
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
        params = config()
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
