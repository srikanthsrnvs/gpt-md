import os
import openai
import sys
import re

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "."))

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
            {"role": "system", "content": "You are GPT-MD. An AI trained to pass medical examinations. You are given a question and must output a concise, and accurate answer. If you do not know the answer, you must say so. Do not lie, or hallucinate. You must be extremely detailed in your responses and include common causes, how to diagnose, common symptoms, and treatment options. You must also include any relevant information that may be useful"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1024,
    )

    # Extract the assistant's response
    return response.choices[0].message.content

def extract_code_from_prompt(prompt):
    match = re.search(r"code: '(.+?)'", prompt)
    if match:
        return match.group(1)
    return None


def process_prompt(prompt):
    completion = generate_completion(prompt)
    code = extract_code_from_prompt(prompt)
    if code:
        output_name = code
        save_completion(output_name, completion)
    else:
        save_completion(prompt, completion)

if __name__ == "__main__":
    redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
    queue = Queue(connection=redis_conn)
    worker = Worker([queue], connection=redis_conn)
    worker.work()
