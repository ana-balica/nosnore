import os
import sqlite3


PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")

class SqliteDatabase(object):
    """Wrapper class for working with sqlite databases
    """
    def __init__(self, dbname):
        """Initializes a connection to the database and creates a cursor to it

        :param dbname: string name of database
        """
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=()):
        """Execute a query

        :param query: string sqlite valid query
        :param params: tuple of parameters
        """
        self.cursor.execute(query, params)
        self.conn.commit()

    def executemany(self, query, values):
        """Execute many query simultaneously

        :param query: string sqlite valid query
        :param values: list of values to fill in the query
        """
        self.cursor.executemany(query, values)
        self.conn.commit()

    def fetch(self, type='all'):
        """Commit transactions

        :param type: string type of fetch - one, all, many
        :return: fetched data
        """
        if type == 'all':
            return self.cursor.fetchall()
        elif type ==  'one':
            return self.cursor.fetchone()
        elif type == 'many':
            return self.cursor.fetchmany()
        else:
            raise ValueError("Unknown type of fetch - {}".format(type))

    def close(self):
        """Close the connection
        """
        self.conn.close()


class SnoreDatabase(object):
    """Snore features database
    """
    def __init__(self, name):
        """Initialize a connection to a snore db
        """
        self.dbname = os.path.join(PROJECT_PATH, name)
        self.db = SqliteDatabase(self.dbname)

    def create_features_table(self, peaks_count, binareas_count):
        """
        """
        query = """CREATE TABLE features (id integer primary key autoincrement, sid integer{0})"""
        for i in xrange(peaks_count):
            query = query.format(", peak%i_mag real, peak%i_freq real{0}" % (i+1, i+1))

        for i in xrange(binareas_count):
            query = query.format(", binarea%i{0}" % (i+1))

        query = query.replace("{0}", "")
        print query
        self.db.execute(query)
        return self

    def insert_signal_features(self, sid, peaks, binareas):
        """
        """
        columns = len(peaks)*2 + len(binareas)
        query = """INSERT INTO features VALUES (Null, {0}{1})""".format(sid, ", ?"*columns)
        params = []
        for peak in peaks:
            params.append(peak[0])
            params.append(peak[1])
        for bin in binareas:
            params.append(bin)
        params = tuple(params)
        self.db.execute(query, params)
        return self
