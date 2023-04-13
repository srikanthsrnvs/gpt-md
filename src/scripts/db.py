import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn

def save_completion(prompt, completion):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO completions (prompt, completion) VALUES (%s, %s)", (prompt, completion))
    conn.commit()
    cur.close()
    conn.close()
