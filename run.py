import argparse
import sqlite3
from pathlib import Path
from sas7bdat import SAS7BDAT


def get_args():
    parser = argparse.ArgumentParser(description='Import SAS data into a SQLite3 table.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('src', help='path to the source *.sas7bdat file')
    parser.add_argument(
        '--db', help='name of the SQLite file to use/create - defaults to name of the SAS file')
    parser.add_argument(
        '--table', help='name of the destination table - defaults to the dataset name from the SAS file')

    return parser.parse_args()


def sqlite_type(column):
    if column.type == 'number':
        # TODO real vs. integer
        return 'REAL'
    return 'TEXT'


def create_column_defs(columns):
    return ', '.join(col.name.decode('utf-8') + ' ' + sqlite_type(col) for col in columns)


def create_table(con, name, columns):
    column_defs = create_column_defs(columns)
    with con:
        con.execute("DROP TABLE IF EXISTS " + name)
        con.execute("CREATE TABLE {} ({})".format(name, column_defs))


def write_rows(con, table, reader):
    for row in reader:
        with con:
            col_placeholders = ', '.join('?' for col in reader.columns)
            con.execute("INSERT INTO {} VALUES ({})".format(
                table, col_placeholders), tuple(row))


def run_import(src, con, table=None):
    with SAS7BDAT(src, skip_header=True) as reader:
        dataset_name = reader.properties.name.decode('utf-8')
        table = table or dataset_name

        print("Writing {} rows to {} table...".format(
            reader.properties.row_count, table))

        create_table(con, table, reader.columns)
        write_rows(con, table, reader)

        print("Done")


if __name__ == '__main__':
    args = get_args()

    db = args.db or Path(args.src).stem + '.db'
    print("Writing to {}...".format(db))
    con = sqlite3.connect(db)

    run_import(args.src, con, table=args.table)
