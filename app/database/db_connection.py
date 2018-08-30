import psycopg2
from .config import config


class DbConnection:
    def __init__(self,path,section):
        self.conn = None
        self.path = path
        self.section = section
        self.params = config(self.path, self.section)
    
    def connect(self,sql, *command):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            # params = config(self.path, self.section)
            # connect to the PostgreSQL server
            self.conn = psycopg2.connect(**self.params)
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
    
