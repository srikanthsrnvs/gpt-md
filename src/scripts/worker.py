import os
import openai
from redis import Redis
from rq import Queue, Worker
from dotenv import load_dotenv
from db import save_completion

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_completion(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def process_prompt(prompt):
    completion = generate_completion(prompt)
    save_completion(prompt, completion)

if __name__ == "__main__":
    redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
    queue = Queue(connection=redis_conn)
    worker = Worker([queue], connection=redis_conn)
    worker.work()
