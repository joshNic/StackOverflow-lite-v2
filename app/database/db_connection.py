import psycopg2
from config import config


class DbConnection:
    def __init__(self):
        self.conn = None
    
    def connect(self, sql, *agrs):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = config()
            # connect to the PostgreSQL server
            self.conn = psycopg2.connect(**params)
            # create a cursor
            cur = self.conn.cursor()
            cur.execute(sql, agrs)
            # close the communication with the PostgreSQL
            cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            exit()
            
    def exit(self):
        if self.conn is not None:
            return self.conn.close()
