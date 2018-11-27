import argparse
import sqlite3
from sas7bdat import SAS7BDAT


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('src', help='path to the source *.sas7bdat file')
parser.add_argument('table', help='name of the destination table')
parser.add_argument('--db', default='sas.db',
                    help='name of the SQLite file to use/create')

args = parser.parse_args()

con = sqlite3.connect(args.db)


def columns_from_fields(fields):
    return ', '.join(col + " string" for col in fields)


with SAS7BDAT(args.src, skip_header=True) as reader:
    column_names = [col.decode('utf-8') for col in reader.column_names]
    columns = columns_from_fields(column_names)
    with con:
        con.execute("DROP TABLE IF EXISTS " + args.table)
        con.execute("CREATE TABLE {} ({})".format(args.table, columns))

    # continue

    for row in reader:
        with con:
            col_placeholders = ', '.join('?' for key in column_names)
            con.execute("INSERT INTO {} ({}) VALUES ({})".format(
                args.table, ', '.join(column_names), col_placeholders), tuple(row))
