import psycopg2
import os, sys, time


env_db_host: str = "APP_DB_HOST"
env_db_host_file: str = "APP_DB_HOST_FILE"
env_db_port: str = "APP_DB_PORT"
env_db_username: str = "APP_DB_USERNAME"
env_db_password: str = "APP_DB_PASSWORD"
env_db_password_file: str = "APP_DB_PASSWORD_FILE"
env_db_dbname: str = "APP_DB_DBNAME"
env_db_ssl_mode: str = "APP_DB_SSL_MODE"
env_db_ssl_root_cert_file: str = "APP_DB_SSL_ROOT_CERT_FILE"
env_db_loop_interval: str = "APP_LOOP_INTERVAL_SECONDS"


def float_try_parse(value):
    try:
        return float(value), True
    except ValueError:
        return value, False


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    db_host = os.environ.get(env_db_host)
    db_host_file = os.environ.get(env_db_host_file)
    db_port = os.environ.get(env_db_port, "5432")
    db_username = os.environ.get(env_db_username)
    db_password = os.environ.get(env_db_password)
    db_password_file = os.environ.get(env_db_password_file)
    db_dbname = os.environ.get(env_db_dbname)
    db_ssl_mode = os.environ.get(env_db_ssl_mode)
    db_ssl_root_cert_file = os.environ.get(env_db_ssl_root_cert_file)
    loop_interval = os.environ.get(env_db_loop_interval, "5")

    if None in (db_username, db_dbname):
        print_error("username and db name are required")
        exit(1)

    builder = [
        f"port={db_port}",
        f"user={db_username}",
        f"dbname={db_dbname}",
    ]

    if db_host:
        builder.append(f"host={db_host}")
    else:
        with open(db_host_file) as f:
            host: str = f.read()
        builder.append(f"host={host}")

    if db_password:
        builder.append(f"password={db_password}")
    elif db_password_file:
        with open(db_password_file) as f:
            dbpassword: str = f.read()
        builder.append(f"password={dbpassword}")
    else:
        print_error("password is required")
        exit(1)

    if db_ssl_mode:
        builder.append(f"sslmode={db_ssl_mode}")
    
    if db_ssl_root_cert_file:
        builder.append(f"sslrootcert={db_ssl_root_cert_file}")

    db_conn: str = " ".join(builder)
    
    # validate int
    loop_iterval, valid = float_try_parse(loop_interval)
    if not valid:
        print_error(f"env {env_db_loop_interval} must be a valid integer")
        exit(1)
        
    print(f"connection string: `{db_conn}`")
    conn = None
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(db_conn)

        while True:
            # Open a cursor to perform database operations
            cur = conn.cursor()

            # Execute a query
            cur.execute("SELECT NOW(), VERSION();")

            row = cur.fetchone()
            print("db connected!")
            print(f"result:  {(row[0].isoformat(), row[1])}")

            try:
                # sleep
                time.sleep(loop_iterval)
            except KeyboardInterrupt:
                print(f"cancelled by user")
                break
    except psycopg2.OperationalError as e:
        print_error(f"database connection failed.\n{e}")
    except Exception as e:
        print_error(f"unhandled error: {e}")
    finally:
        if conn is not None:
            conn.close()
            print(f"db disconected.")

if __name__ == "__main__":
    main()
