import os
from redis import Redis
from rq import Queue
from dotenv import load_dotenv

load_dotenv()

def enqueue_prompts(prompts):
    redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
    queue = Queue(connection=redis_conn)
    for prompt in prompts:
        queue.enqueue("worker.process_prompt", prompt)

if __name__ == "__main__":
    prompts = [
        "What is the capital of France?",
        "What is the tallest mountain in the world?",
        # Add more prompts here
    ]
    enqueue_prompts(prompts)