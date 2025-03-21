import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

"""
Use the connection to the database to load the staging table
from S3 buckets

Arg(s):
    cur: cursor to the database
    conn: connection object to the database
"""
def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

"""
Transform data in staging tables and insert them into tables used for analytics

Arg(s):
    cur: cursor to the database
    conn: connection object to the database
"""
def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()