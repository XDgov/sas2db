import run
import sqlite3
import unittest


class TestRun(unittest.TestCase):
    # https://docs.python.org/3.7/library/sqlite3.html#sqlite3.Connection.row_factory
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def create_db(self):
        con = sqlite3.connect(':memory:')
        con.row_factory = self.dict_factory
        return con

    def setUp(self):
        self.con = self.create_db()

    def query_one(self, query):
        cur = self.con.cursor()
        cur.execute(query)
        return cur.fetchone()

    def query_many(self, query):
        cur = self.con.cursor()
        cur.execute(query)
        return cur.fetchall()

    def test_import(self):
        run.run_import('example.sas7bdat', self.con)

        count = self.query_one(
            'SELECT COUNT(*) AS count FROM example')['count']
        self.assertEqual(count, 20)

        columns = self.query_many('PRAGMA TABLE_INFO(example)')
        for column in columns:
            self.assertEqual(column['type'], 'string')

    def test_missing_src(self):
        with self.assertRaises(FileNotFoundError):
            run.run_import('nonexistent.sas7bdat', self.con)


if __name__ == '__main__':
    unittest.main()
