import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect():
    conn = psycopg2.connect(
        dbname="conditions",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_URL"),
        port=5432
    )
    return conn

def save_completion(prompt, completion):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO completions (prompt, completion) VALUES (%s, %s)", (prompt, completion))
    conn.commit()
    cur.close()
    conn.close()
