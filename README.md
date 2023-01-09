# pyping
Python simple program that connect and call simple query to a Postgres database; useful for testing your application if it can reach the database

## Environment
```shell
$ pyenv local 3.8.13
$ python -V
Python 3.8.13
$ python -m venv .venv
$ source ./venv/bin/activate
$ pip install pip --upgrade
$ pip install requirements.txt
```

## Run
```shell
$ export APP_DB_CONNECTION_STRING="postgres://username:password@localhost:5432/mydb"
$ export APP_LOOP_INTERVAL_SECONDS="3"
$ python main.py
```
