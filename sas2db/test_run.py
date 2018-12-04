import os
import unittest
from . import run
from sqlalchemy import MetaData, Table, types


class TestRun(unittest.TestCase):
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

    # https://stackoverflow.com/a/11180583/358804
    def run(self, result=None):
        self.engine = run.create_db()
        with self.engine.begin() as con:
            self.con = con
            super(TestRun, self).run(result)

    def query_one(self, query):
        result = self.con.execute(query)
        return result.fetchone()

    def query_many(self, query):
        result = self.con.execute(query)
        return result.fetchall()

    def create_pg_db(self, base_con, name):
        engine = run.create_db(base_con + 'postgres')
        with engine.begin() as con:
            # https://stackoverflow.com/a/8977109/358804
            con.execute('COMMIT')
            con.execute('DROP DATABASE IF EXISTS ' + name)
            con.execute('CREATE DATABASE ' + name)

    def table_info(self, name):
        # https://docs.sqlalchemy.org/en/latest/core/reflection.html
        meta = MetaData()
        return Table(name, meta, autoload=True, autoload_with=self.engine)

    def test_import_sas(self):
        data_path = os.path.join(self.DATA_DIR, 'example.sas7bdat')
        run.run_import(data_path, self.con)

        count = self.query_one('SELECT COUNT(*) FROM example')['COUNT(*)']
        self.assertEqual(count, 20)

        table = self.table_info('example')
        self.assertIsInstance(table.columns.begin.type, types.FLOAT)
        self.assertIsInstance(table.columns.enddate.type, types.DATETIME)
        self.assertIsInstance(table.columns.Info.type, types.TEXT)
        self.assertIsInstance(table.columns.year.type, types.FLOAT)
        self.assertIsInstance(table.columns.Capital.type, types.FLOAT)
        self.assertIsInstance(table.columns.YearFormatted.type, types.FLOAT)

    def test_import_xport(self):
        data_path = os.path.join(self.DATA_DIR, 'test.xpt')
        run.run_import(data_path, self.con)

        count = self.query_one('SELECT COUNT(*) FROM sas')['COUNT(*)']
        self.assertEqual(count, 6)

        table = self.table_info('sas')
        self.assertIsInstance(table.columns.VIT_STAT.type, types.TEXT)
        self.assertIsInstance(table.columns.ECON.type, types.TEXT)
        self.assertIsInstance(table.columns.COUNT.type, types.FLOAT)
        self.assertIsInstance(table.columns.TEMP.type, types.FLOAT)

    def test_normalize_columns(self):
        data_path = os.path.join(self.DATA_DIR, 'example.sas7bdat')
        run.run_import(data_path, self.con, normalize=True)

        tables = self.query_many(
            "select name from sqlite_master where type = 'table'")
        self.assertEqual(tables, [('example',)])

        table = self.table_info('example')
        names = [col.name for col in table.columns]
        self.assertEqual(
            sorted(names), ['begin', 'capital', 'enddate', 'index', 'info', 'year', 'year_formatted'])

    def test_import_pg(self):
        base_con = 'postgresql+psycopg2://postgres@localhost:5432/'
        temp_db = 'sas2db'
        self.create_pg_db(base_con, temp_db)

        engine = run.create_db(base_con + temp_db)
        con = engine.connect()
        # TODO clean this up
        self.engine = engine
        self.con = con

        with con.begin() as trans:
            data_path = os.path.join(self.DATA_DIR, 'example.sas7bdat')
            # PostgreSQL is weird with capitalized table names, so just avoid the problem by normalizing
            run.run_import(data_path, con, normalize=True)

        count = self.query_one('SELECT COUNT(*) FROM example')[0]
        self.assertEqual(count, 20)

        table = self.table_info('example')
        self.assertIsInstance(table.columns.begin.type, types.Float)
        self.assertIsInstance(table.columns.enddate.type, types.TIMESTAMP)
        self.assertIsInstance(table.columns.info.type, types.TEXT)
        self.assertIsInstance(table.columns.year.type, types.Float)
        self.assertIsInstance(table.columns.capital.type, types.Float)
        self.assertIsInstance(table.columns.year_formatted.type, types.Float)

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
