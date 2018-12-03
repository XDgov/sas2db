# sas2sqlite [![PyPI version](https://badge.fury.io/py/sas2sqlite.svg)](https://badge.fury.io/py/sas2sqlite)

Convert [SAS](https://en.wikipedia.org/wiki/SAS_(software)) files to [SQLite](https://www.sqlite.org/) databases. Supports both `*.sas7bdat` and XPORT (`*.xpt`) files.

## Usage

1. Install [Python 3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/).
1. Install the package.

    ```sh
    pip3 install sas2sqlite
    ```

1. Run the conversion.

    ```sh
    sas2sqlite path/to/src.sas7bdat
    ```

1. A `src.db` (matching your input file name) will be created.
1. Run SQL! Example:

    ```
    $ sqlite src.db
    sqlite> .tables
    mydata
    sqlite> SELECT COUNT(*) FROM mydata;
    200
    ```

For more options:

```sh
sas2sqlite -h
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

1. Create `sas2sqlite` database in PostgreSQL for testing. Example in Docker:

    ```sh
    docker exec -it pg createdb -U postgres sas2sqlite
    ```

1. Run tests:

    ```sh
    python -m unittest
    ```

To use the script:

```sh
python3 sas2sqlite/run.py path/to/src.sas7bdat
```

[data.gov has data sets you can test with.](https://catalog.data.gov/dataset?res_format=Zipped+SAS7BDAT) Information about data types:

* Documentation
    * [SQLite types](https://www.sqlite.org/datatype3.html#affinity_name_examples)
    * [SAS data types](http://support.sas.com/documentation/cdl/en/fedsqlref/67364/HTML/default/viewer.htm#n19bf2z7e9p646n0z224cokuj567.htm)
    * [SAS formats](http://support.sas.com/documentation/cdl/en/lrdict/64316/HTML/default/viewer.htm#a001263753.htm)
* SAS to Python type parsing
    * [sas7bdat](https://bitbucket.org/jaredhobbs/sas7bdat/src/d712283fd4a7319c7dffe44b17f25d7917e63724/sas7bdat.py#lines-454:490)
    * [Pandas](https://github.com/pandas-dev/pandas/blob/0409521665bd436a10aea7e06336066bf07ff057/pandas/io/sas/sas7bdat.py#L659-L685)