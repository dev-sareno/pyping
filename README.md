# pyping
Python simple program that connect and call simple query to a Postgres database; useful for testing your application if it can reach the database

## SQL
Query to run
```sql
SELECT NOW(), VERSION();
```

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
$ export APP_DB_HOST="localhost"
$ export APP_DB_PORT="5432"
$ export APP_DB_USERNAME="username"
$ #export APP_DB_PASSWORD="password"
$ export APP_DB_PASSWORD_FILE="/var/run/secrets/app/password.txt"
$ export APP_DB_DBNAME="mydb"
$ export APP_DB_SSL_MODE="verify-full"
$ export APP_DB_SSL_ROOT_CERT_FILE="/var/run/secrets/app/password.txt"
$ export APP_LOOP_INTERVAL_SECONDS="3"
$ python main.py
```

## Run Docker
```shell
$ docker run \
    --rm -ti \
    --pull=always \
    -e APP_DB_HOST="localhost" \
    -e APP_DB_PORT="5432" \
    -e APP_DB_USERNAME="username" \
    -e APP_DB_PASSWORD="password" \
    -e APP_DB_DBNAME="mydb" \
    -e APP_LOOP_INTERVAL_SECONDS="3" \
    devsareno/pyping
```
