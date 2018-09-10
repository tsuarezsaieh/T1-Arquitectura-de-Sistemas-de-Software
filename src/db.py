import psycopg2 as psql
import datetime
from os import getenv
from dotenv import load_dotenv
load_dotenv()

DB_NAME = getenv('DB_NAME')
DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
class DB():

    def __init__(self):
        while True:
            try:
                self.conn = psql.connect("dbname={} user={} password={} host={} port={}".format(
                DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT
                ))
                self.cur = self.conn.cursor()
                break
            except:
                pass

    def init_db(self):
        self.cur.execute("DROP TABLE IF EXISTS messages;")
        self.conn.commit()
        self.cur.execute("CREATE TABLE messages(id serial, message text, time text, ip text)")
        self.conn.commit()

        return        

    def new_message(self, req):
        time = str(datetime.datetime.now()).split('.')[0]
        if req.headers['content-type'] and req.headers['content-type'] == 'application/json':
            msg = req.get_json(force=True)['message']
        else:
            msg = req.form['message']
        ip = req.remote_addr

        self.cur.execute('INSERT INTO messages(message, time, ip) values(%s, %s, %s)', (msg, time, ip))
        self.conn.commit()

        data = {}

        return data

    def get_queries(self, page):
        offset = 10 * (page - 1)
        self.cur.execute('SELECT id, message, time, ip FROM messages ORDER BY id DESC LIMIT 10 OFFSET %s;', (offset, ))

        # Devolver los ultimos 100 mensajes
        msgs =  list(map(lambda x: {'id': x[0], 'message': x[1], 'time': x[2], 'ip': x[3]}  ,self.cur))

        return msgs


if __name__ == "__main__":
    db = DB()
    db.init_db()