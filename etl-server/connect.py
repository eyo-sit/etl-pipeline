import psycopg2
from queue import Queue

def connect(host_in, dbname_in, user_in, password_in, port_in):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        print("Connecting to %s at %s" % (dbname_in, host_in), flush=True)
        with psycopg2.connect(
                host=host_in,
                dbname=dbname_in,
                user=user_in,
                password=password_in,
                port=port_in) as conn:
            print('Connected to the PostgreSQL server.', flush=True)
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    connect()
