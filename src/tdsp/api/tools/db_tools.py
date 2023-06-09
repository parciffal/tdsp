import psycopg2
import environ


class DatabaseManager(object):

    def __init__(self):
        env = environ.Env()
        environ.Env.read_env()

        self.conn = psycopg2.connect(dbname=env('DATABASE_NAME'),
                                     user=env('USER_NAME'),
                                     host=env('HOST'),
                                     port=env('PORT'),
                                     password=env('PASSWORD'))
        self.cur = self.conn.cursor()


    def query(self, arg, values=None):
        try:
            if values == None:
                self.cur.execute(arg)
            else:
                self.cur.execute(arg, values)
            self.conn.commit()
        except Exception as e:
            print(e)

    def fetchone(self, arg, values=None):
        try:
            if values == None:
                self.cur.execute(arg)
            else:
                self.cur.execute(arg, values)
            return self.cur.fetchone()
        except Exception as e:
            print(e)

    def fetchall(self, arg, values=None):
        try:
            if values == None:
                self.cur.execute(arg)
            else:
                self.cur.execute(arg, values)
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            
    def __del__(self):
        self.conn.close()
