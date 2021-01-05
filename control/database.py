import psycopg2
import logging
logger = logging.getLogger('control-server')
db = psycopg2.connect(database="control_db", user="pi",
                      password="abcd1234", host="127.0.0.1", port="5432")
logger.info('[connected] to database')


class Database:
    def __init__(self):
        self.c = db.cursor()

    def get_all(self):
        self.c.execute('SELECT * FROM props')
        data = self.c.fetchall()
        return data

    def get(self, key):
        self.c.execute("SELECT value FROM props WHERE key = %s", (key,))
        value = self.c.fetchone()

        return value[0]

    def set(self, key, value):
        self.c.execute(
            "UPDATE props SET value = %s WHERE key = %s", (str(value), key))
        db.commit()
        return True
