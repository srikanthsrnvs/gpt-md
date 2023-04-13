import os
import openai
from redis import Redis
from rq import Queue, Worker
from dotenv import load_dotenv
from db import save_completion

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_completion(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace with the GPT-4 model name
        messages=[
            {"role": "system", "content": "You are GPT-MD. An AI trained to pass medical examinations. You are given a question and must output a concise, and accurate answer. If you do not know the answer, you must say so. Do not lie, or hallucinate."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1024,
    )

    # Extract the assistant's response
    return response.choices[0].message.content


def process_prompt(prompt):
    completion = generate_completion(prompt)
    condition_name = prompt.replace("What is ", "").replace("?", "")
    save_completion(condition_name, completion)

if __name__ == "__main__":
    redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
    queue = Queue(connection=redis_conn)
    worker = Worker([queue], connection=redis_conn)
    worker.work()
