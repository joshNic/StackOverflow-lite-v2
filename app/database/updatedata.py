import psycopg2
from .config import config


def update_user(user_email, user_password, hash_password, user_id):
    """ update user based on the user id """
    sql = """ UPDATE users
                SET 
                user_email = %s,
                user_password = %s,
                hash_password = %s
                WHERE user_id = %s"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (user_email, user_password, hash_password, user_id))
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
    update_user("256jo@gmail.com", "josh1234", "josh1234", 2)
