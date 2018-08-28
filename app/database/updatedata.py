import psycopg2
from .config import config


def update_user(status, answer_id):
    """ update user based on the user id """
    sql = """ UPDATE answers
                SET 
                accepted = %s
                WHERE answer_id = %s"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (status, answer_id))
        # get the number of updated rows
        # updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    update_user("True", 2)
