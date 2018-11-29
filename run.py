import argparse
import pandas as pd
import sqlite3
from pathlib import Path

# https://docs.python.org/3.7/library/sqlite3.html#sqlite3.Connection.row_factory


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_db(name=':memory:'):
    con = sqlite3.connect(name)
    con.row_factory = dict_factory
    return con


def get_args():
    parser = argparse.ArgumentParser(description='Import SAS data into a SQLite3 table.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('src', help='path to the source *.sas7bdat file')
    parser.add_argument(
        '--db', help='name of the SQLite file to use/create - defaults to name of the SAS file')
    parser.add_argument(
        '--table', help='name of the destination table - defaults to the dataset name from the SAS file')

    return parser.parse_args()


def run_import(src, con, chunksize=100, table=None):
    reader = pd.read_sas(src, chunksize=chunksize)

    dataset_name = reader.name
    table = table or dataset_name
    print("Writing to {} table...".format(table))

    for i, chunk in enumerate(reader):
        # throw an error if the table exists when writing the first chunk
        if_exists = 'fail' if i == 0 else 'append'
        chunk.to_sql(table, con, if_exists=if_exists)
    reader.close()

    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM ' + table)
    count = cur.fetchone()['COUNT(*)']
    print("Wrote {} rows.".format(count))


if __name__ == '__main__':
    args = get_args()

    db = args.db or Path(args.src).stem + '.db'
    print("Writing to {}...".format(db))
    con = create_db(name=db)

    run_import(args.src, con, table=args.table)
