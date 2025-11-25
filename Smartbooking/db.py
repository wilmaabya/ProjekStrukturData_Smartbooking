import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="proyekbasda",
        user="postgres",
        password="W1lmaaa!"
    )
