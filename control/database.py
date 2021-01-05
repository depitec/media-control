class Helper:
    def __init__(self, db):
        self.db = db
        self.c = self.db.cursor()

    def get_all(self):
        self.c.execute('SELECT * FROM props')
        data = self.c.fetchall()
        return data

    def get(self, key):
        self.c.execute('SELECT value FROM props WHERE key = ?', [key])
        value = self.c.fetchone()

        self.db.commit()
        return value[0]

    def set(self, key, value):
        self.c.execute('REPLACE INTO props (key,value) VALUES(?,?)',
                       [key, str(value)])
        self.db.commit()
        return True
