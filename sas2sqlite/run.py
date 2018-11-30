import argparse
import inflection
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine


def create_db(name=':memory:'):
    return create_engine('sqlite+pysqlite:///' + name)


def get_args():
    parser = argparse.ArgumentParser(description='Import SAS data into a SQLite3 table.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('src', help='path to the source *.sas7bdat file')
    parser.add_argument(
        '--db', help='name of the SQLite file to use/create - defaults to name of the SAS file')
    parser.add_argument('--normalize', action='store_true',
                        help="normalize the table and column names as underscored and lowercased (snake-case)")
    parser.add_argument(
        '--table', help='name of the destination table - defaults to the dataset name from the SAS file')

    return parser.parse_args()


def row_count(con, table):
    result = con.execute('SELECT COUNT(*) FROM ' + table)
    return result.fetchone()['COUNT(*)']


def write_to_db(reader, con, table, normalize=False):
    for i, chunk in enumerate(reader):
        if normalize:
            chunk = chunk.rename(columns=inflection.underscore)
        # throw an error if the table exists when writing the first chunk
        if_exists = 'fail' if i == 0 else 'append'
        chunk.to_sql(table, con, if_exists=if_exists)


def run_import(src, con, chunksize=100, normalize=False, table=None):
    reader = pd.read_sas(src, chunksize=chunksize)

    dataset_name = getattr(reader, 'name', 'sas')
    table = table or dataset_name
    if normalize:
        table = inflection.underscore(table)
    print("Writing to {} table...".format(table))

    write_to_db(reader, con, table, normalize=normalize)
    reader.close()

    count = row_count(con, table)
    print("Wrote {} rows.".format(count))


def main():
    args = get_args()

    db = args.db or Path(args.src).stem + '.db'
    print("Writing to {}...".format(db))
    engine = create_db(name=db)

    with engine.begin() as con:
        run_import(args.src, con, normalize=args.normalize, table=args.table)


if __name__ == '__main__':
    main()
