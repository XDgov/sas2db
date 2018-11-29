# sas2sqlite

Convert SAS files to SQLite databases. Supports both `*.sas7bdat` and XPORT (`*.xpt`) files.

## Usage

1. Install Python 3 and [Pipenv](https://pipenv.readthedocs.io/en/latest/).
1. Clone/download the repository.
1. From the project directory, run

    ```sh
    pipenv install
    pipenv shell
    python3 run.py path/to/src.sas7bdat
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
python3 run.py -h
```
