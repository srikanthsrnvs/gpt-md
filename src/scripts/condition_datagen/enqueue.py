import os
import argparse
import pandas as pd
import sys
import signal

from redis import Redis
from rq import Queue
from dotenv import load_dotenv

load_dotenv()

def remove_all_jobs(queue):
    while not queue.is_empty():
        queue.dequeue()

def enqueue_prompts(prompts):
    redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
    queue = Queue(connection=redis_conn)
    for prompt in prompts:
        queue.enqueue("worker.process_prompt", prompt)

def extract_short_descriptions_from_csv(file_path, column_name, num_rows=None):
    df = pd.read_csv(file_path, nrows=num_rows)
    short_descriptions = df[column_name].tolist()
    return short_descriptions

if __name__ == "__main__":
    redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
    queue = Queue(connection=redis_conn)
    try:
        parser = argparse.ArgumentParser(description="Enqueue prompts from CSV")
        parser.add_argument('--num_rows', type=int, default=None, help='Number of rows to read from the CSV file')

        args = parser.parse_args()

        file_path = '../../data/conditions.csv'
        column_name = 'SHORT DESCRIPTION'  # Adjust if your column has a different name

        short_descriptions = extract_short_descriptions_from_csv(file_path, column_name, args.num_rows)
        prompts = [f"What is {short_description}?" for short_description in short_descriptions]


        # Set up a signal handler to clean up the Redis queue if the script is terminated
        def handle_signal(signum, frame):
            print("Signal received, removing all jobs from the Redis queue")
            remove_all_jobs(queue)
            sys.exit(1)

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        enqueue_prompts(prompts)

    except Exception as e:
        print(f"An exception occurred: {e}")
        print("Removing all jobs from the Redis queue")
        remove_all_jobs(queue)
        sys.exit(1)
