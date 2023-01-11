import psycopg2
import os, sys, time


env_db_host: str = "APP_DB_HOST"
env_db_port: str = "APP_DB_PORT"
env_db_username: str = "APP_DB_USERNAME"
env_db_password: str = "APP_DB_PASSWORD"
env_db_dbname: str = "APP_DB_DBNAME"
env_loop_interval: str = "APP_LOOP_INTERVAL_SECONDS"


def float_try_parse(value):
    try:
        return float(value), True
    except ValueError:
        return value, False


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    db_host = os.environ.get(env_db_host)
    db_port = os.environ.get(env_db_port, "5432")
    db_username = os.environ.get(env_db_username)
    db_password = os.environ.get(env_db_password)
    db_dbname = os.environ.get(env_db_dbname)
    if None in (db_host, db_username, db_password, db_dbname):
        print_error(f"env variables {db_host}, {db_username}, {db_password}, and {db_dbname} are required")
        exit(1)

    db_conn: str = f"postgres://{db_username}:{db_password}@{db_host}:{db_port}/{db_dbname}"
    
    loop_iterval_str = os.environ.get(env_loop_interval)
    loop_iterval: int = 0
    if loop_iterval_str is None:
        print_error(f"env {env_loop_interval} is required")
        exit(1)
    else:
        # validate int
        val, valid = float_try_parse(loop_iterval_str)
        if not valid:
            print_error(f"env {env_loop_interval} must be a valid integer")
            exit(1)
        loop_iterval = val
        

    while True:
        conn = None
        try:
            # Connect to your postgres DB
            conn = psycopg2.connect(db_conn)

            # Open a cursor to perform database operations
            cur = conn.cursor()

            # Execute a query
            cur.execute("SELECT NOW(), VERSION();")

            row = cur.fetchone()
            print(f"result:\n{row}")
        except psycopg2.OperationalError as e:
            print_error(f"database connection failed.\n{e}")
            continue
        except Exception as e:
            print_error(f"unhandled error: {e}")
            continue
        finally:
            if conn is not None:
                conn.close()
                print(f"db disconected")

            try:
                # sleep
                time.sleep(loop_iterval)
            except KeyboardInterrupt:
                print(f"cancelled by user")
                break

if __name__ == "__main__":
    main()
