import os
import unittest
from . import run


class TestRun(unittest.TestCase):
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

    # https://stackoverflow.com/a/11180583/358804
    def run(self, result=None):
        engine = run.create_db()
        with engine.begin() as con:
            self.con = con
            super(TestRun, self).run(result)

    def query_one(self, query):
        result = self.con.execute(query)
        return result.fetchone()

    def query_many(self, query):
        result = self.con.execute(query)
        return result.fetchall()

    def test_import_sas(self):
        data_path = os.path.join(self.DATA_DIR, 'example.sas7bdat')
        run.run_import(data_path, self.con)

        count = self.query_one('SELECT COUNT(*) FROM example')['COUNT(*)']
        self.assertEqual(count, 20)

        columns = self.query_many('PRAGMA TABLE_INFO(example)')
        column_types = {col['name']: col['type'] for col in columns}
        self.assertEqual(column_types['begin'], 'FLOAT')
        self.assertEqual(column_types['enddate'], 'DATETIME')
        self.assertEqual(column_types['Info'], 'TEXT')
        self.assertEqual(column_types['year'], 'FLOAT')
        self.assertEqual(column_types['Capital'], 'FLOAT')
        self.assertEqual(column_types['YearFormatted'], 'FLOAT')

    def test_import_xport(self):
        data_path = os.path.join(self.DATA_DIR, 'test.xpt')
        run.run_import(data_path, self.con)

        count = self.query_one('SELECT COUNT(*) FROM sas')['COUNT(*)']
        self.assertEqual(count, 6)

        columns = self.query_many('PRAGMA TABLE_INFO(sas)')
        column_types = {col['name']: col['type'] for col in columns}
        self.assertEqual(column_types['VIT_STAT'], 'TEXT')
        self.assertEqual(column_types['ECON'], 'TEXT')
        self.assertEqual(column_types['COUNT'], 'FLOAT')
        self.assertEqual(column_types['TEMP'], 'FLOAT')

    def test_normalize_columns(self):
        data_path = os.path.join(self.DATA_DIR, 'example.sas7bdat')
        run.run_import(data_path, self.con, normalize=True)

        tables = self.query_many(
            "select name from sqlite_master where type = 'table'")
        self.assertEqual(tables, [{'name': 'example'}])

        columns = self.query_many(
            "SELECT name FROM PRAGMA_TABLE_INFO('example') ORDER BY name")
        names = [col['name'] for col in columns]
        self.assertEqual(
            names, ['begin', 'capital', 'enddate', 'index', 'info', 'year', 'year_formatted'])

    def test_missing_src(self):
        with self.assertRaises(FileNotFoundError):
            run.run_import('nonexistent.sas7bdat', self.con)

    def test_existing_table(self):
        data_path = os.path.join(self.DATA_DIR, 'example.sas7bdat')
        run.run_import(data_path, self.con)
        with self.assertRaises(ValueError):
            run.run_import(data_path, self.con)


if __name__ == '__main__':
    unittest.main()
