import run
import sqlite3
import unittest


class TestRun(unittest.TestCase):
    def test_import(self):
        con = sqlite3.connect(':memory:')

        run.run_import('example.sas7bdat', con)

        cur = con.cursor()
        cur.execute('SELECT COUNT(*) FROM example')
        count = cur.fetchone()[0]
        self.assertEqual(count, 20)

    def test_missing_src(self):
        con = sqlite3.connect(':memory:')
        with self.assertRaises(FileNotFoundError):
            run.run_import('nonexistent.sas7bdat', con)


if __name__ == '__main__':
    unittest.main()
