import psycopg2
import os, sys, time


env_db_connection_string: str = "APP_DB_CONNECTION_STRING"
env_loop_interval: str = "APP_LOOP_INTERVAL_SECONDS"


def float_try_parse(value):
    try:
        return float(value), True
    except ValueError:
        return value, False


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    db_conn = os.environ.get(env_db_connection_string)
    if db_conn is None:
        print_error(f"env {env_db_connection_string} is required")
        exit(1)
    
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
