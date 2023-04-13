import os
import pandas as pd
from redis import Redis
from rq import Queue
from dotenv import load_dotenv

load_dotenv()

def enqueue_prompts(prompts):
    redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
    queue = Queue(connection=redis_conn)
    for prompt in prompts:
        queue.enqueue("worker.process_prompt", prompt)

def extract_short_descriptions_from_csv(file_path, column_name):
    df = pd.read_csv(file_path)
    short_descriptions = df[column_name].tolist()
    return short_descriptions

if __name__ == "__main__":
    file_path = 'data/conditions.csv'
    column_name = 'SHORT DESCRIPTION' # Adjust if your column has a different name

    short_descriptions = extract_short_descriptions_from_csv(file_path, column_name)
    prompts = [f"What is {short_description}?" for short_description in short_descriptions]
    enqueue_prompts(prompts)