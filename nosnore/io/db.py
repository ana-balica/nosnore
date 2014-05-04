import sqlite3


class SqliteDatabase(object):
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def execute(self, query, commit=False):
        self.cursor.execute(query)
        if commit:
            self.conn.commit()

    def executemany(self, query, values, commit=True):
        self.cursor.executemany(query, values)
        if commit:
            self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
