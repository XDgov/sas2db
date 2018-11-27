import sqlite3
from sas7bdat import SAS7BDAT


FILES = {
    'ssocs': 'ssocs.sas7bdat',
}

con = sqlite3.connect('joined-from-sas.db')


def columns_from_fields(fields):
    return ', '.join(col + " string" for col in fields)


for table, path in FILES.items():
    print("Importing", table, "...", flush=True)
    with SAS7BDAT(path, skip_header=True) as reader:
        column_names = [col.decode('utf-8') for col in reader.column_names]
        columns = columns_from_fields(column_names)
        with con:
            con.execute("DROP TABLE IF EXISTS " + table)
            con.execute("CREATE TABLE {} ({})".format(table, columns))

        # continue

        for row in reader:
            with con:
                col_placeholders = ', '.join('?' for key in column_names)
                con.execute("INSERT INTO {} ({}) VALUES ({})".format(
                    table, ', '.join(column_names), col_placeholders), tuple(row))
