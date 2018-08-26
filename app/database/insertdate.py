import psycopg2
from .config import config


def insert_user(user_email, user_password, hash_password):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO users(user_email, user_password, hash_password)
             VALUES(%s,%s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (user_email, user_password, hash_password))
        # get the generated id back
        # user_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    # return vendor_id
if __name__ == '__main__':
    # insert one user
    insert_user("256jomu@gmail.com", "joshua123", "joshua123")
