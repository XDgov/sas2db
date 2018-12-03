# sas2db [![PyPI version](https://badge.fury.io/py/sas2db.svg)](https://badge.fury.io/py/sas2db)

Imports [SAS](https://en.wikipedia.org/wiki/SAS_(software)) files to SQL databases. Supports both `*.sas7bdat` and XPORT (`*.xpt`) files.

## Installation

1. Install [Python 3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/).
1. Install the package.

    ```sh
    pip3 install sas2db
    ```

## Usage

### SQLite3

`sas2db` supports [SQLite3](https://www.sqlite.org/) with no additional dependencies or setup, so we'll start with that. To import from SAS to SQLite3:

1. Run the conversion.

    ```sh
    sas2db path/to/src.sas7bdat
    ```

1. A `src.db` (matching your input file name) will be created.
1. Run SQL! Example:

    ```
    $ sqlite3 src.db
    sqlite> .tables
    mydata
    sqlite> SELECT COUNT(*) FROM mydata;
    200
    ```

For more options:

```sh
sas2db -h
```

### Other databases

Aside from SQLite3, `sas2db` supports other databases like PostgreSQL and MySQL. This support comes from [SQLAlchemy](https://www.sqlalchemy.org/) under the hood, so see [their list of supported "dialects"](https://docs.sqlalchemy.org/en/latest/dialects/index.html).

To use another database:

1. Ensure that the destination database is installed, running, created, and accessible from wherever you will be doing the import.
1. Install the corresponding driver.
    * On the [Dialects](https://docs.sqlalchemy.org/en/latest/dialects/index.html) page, click your preferred database, then under "DBAPI Support", click one of the options.
    * The first DBAPI option is probably fine, though you may have to try multiple.
1. Run `sas2db`, passing the [database URL](https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) to the `--db` argument.

Example for PostgreSQL:

```sh
# create the database
createdb -U postgres sas_import
# install driver
pip3 install psycopg2
# run the import
sas2db --db postgresql+psycopg2://postgres@localhost:5432/sas_import path/to/src.sas7bdat
```

## Development

1. Install [Pipenv](https://pipenv.readthedocs.io/en/latest/).
1. Clone/download the repository.
1. From the project directory, run

    ```sh
    pipenv install
    pipenv shell
    ```

1. Run PostgreSQL. Example in Docker:

    ```sh
    docker run --rm -it -p 5432:5432 --name pg postgres
    ```

1. Create `sas2db` database in PostgreSQL for testing. Example in Docker:

    ```sh
    docker exec -it pg createdb -U postgres sas2db
    ```

1. Run tests:

    ```sh
    python -m unittest
    ```

To use the script:

```sh
python3 sas2db/run.py path/to/src.sas7bdat
```

[data.gov has data sets you can test with.](https://catalog.data.gov/dataset?res_format=Zipped+SAS7BDAT) Information about data types:

* Documentation
    * [SQLite types](https://www.sqlite.org/datatype3.html#affinity_name_examples)
    * [SAS data types](http://support.sas.com/documentation/cdl/en/fedsqlref/67364/HTML/default/viewer.htm#n19bf2z7e9p646n0z224cokuj567.htm)
    * [SAS formats](http://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/viewer.htm#a001263753.htm)
* SAS to Python type parsing
    * [sas7bdat](https://bitbucket.org/jaredhobbs/sas7bdat/src/d712283fd4a7319c7dffe44b17f25d7917e63724/sas7bdat.py#lines-454:490)
    * [Pandas](https://github.com/pandas-dev/pandas/blob/0409521665bd436a10aea7e06336066bf07ff057/pandas/io/sas/sas7bdat.py#L659-L685)