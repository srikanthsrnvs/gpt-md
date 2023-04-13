import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect():
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=5432
    )
    return conn

def save_completion(prompt, completion):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO conditions (name, information) VALUES (%s, %s)", (prompt, completion))
    conn.commit()
    cur.close()
    conn.close()
