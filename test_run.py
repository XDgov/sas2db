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

    def test_import(self):
        con = self.create_db()
        run.run_import('example.sas7bdat', con)

        cur = con.cursor()
        cur.execute('SELECT COUNT(*) AS count FROM example')
        count = cur.fetchone()['count']
        self.assertEqual(count, 20)

        cur.execute('PRAGMA TABLE_INFO(example)')
        columns = cur.fetchall()
        for column in columns:
            self.assertEqual(column['type'], 'string')

    def test_missing_src(self):
        con = self.create_db()
        with self.assertRaises(FileNotFoundError):
            run.run_import('nonexistent.sas7bdat', con)


if __name__ == '__main__':
    unittest.main()
