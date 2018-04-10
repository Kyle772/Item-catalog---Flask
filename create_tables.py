#!/usr/bin/python
import psycopg2 as psql

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE users CASCADE;
        """,
        """
        DROP TABLE items;
        """,
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(16) NOT NULL,
            password_hash VARCHAR NOT NULL,
            user_type INTEGER NOT NULL
        );
        """,
        """
        CREATE TABLE items (
            item_id SERIAL PRIMARY KEY,
            item_name TEXT NOT NULL,
            item_desc TEXT NOT NULL,
            item_image TEXT NOT NULL,
            poster_id INTEGER REFERENCES users(user_id)
        );
        """)
    conn = None
    try:
        connection = psql.connect("dbname=item_catalog")
        # connect to the PostgreSQL server
        cur = connection.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        connection.commit()
    except (Exception, psql.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_tables()
