import psycopg2
from .config import config
import os


class DbConnection:
    def __init__(self):
        self.conn = None
        if os.getenv('APP_Config') == 'testing':
            self.database = 'postgrestest'
        else:
            self.database = 'dl71kl016q7qc'
    def connect(self,sql, *command):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            # params = config(self.path, self.section)
            # connect to the PostgreSQL server
            self.conn = psycopg2.connect(
                database=self.database, user="rqxoljondpygyq", password="859c79cc406ee2799982b5e28f4935ae69cc09842200211a43749c54e7df5087", host="ec2-54-235-86-226.compute-1.amazonaws.com", port="5432"
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
    
