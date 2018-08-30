import psycopg2
from .config import config
import os


class DbConnection:
    def __init__(self):
        self.conn = None
        if os.getenv('APP_Config') == 'testing':
            self.database = 'postgresqltest'
        else:
            self.database = 'postgres'
    def connect(self,sql, *command):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            # params = config(self.path, self.section)
            # connect to the PostgreSQL server
            self.conn = psycopg2.connect(
                database=self.database, user="postgres", password="5y+2X=89", host="127.0.0.1", port="5432"
            )
            # create a cursor
            cur = self.conn.cursor()
            cur.execute(sql, command)
            # close the communication with the PostgreSQL
            # cur.close()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return cur
    
    def close(self):
        self.connect(None, None).close()
        self.conn.close()
        return True
    
