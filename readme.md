# GPT-MD

GPT MD: Un-gated healthcare to fix Shkreli's image problem

This project aims to use GPT-4 to generate a massive health dataset and train a LLaMA transformer for healthcare diagnosis. By doing so, we hope to improve access to quality healthcare information and address the image problem caused by individuals like Martin Shkreli, who have contributed to a negative perception of the industry.

## Features

- Utilizes GPT-4 for generating a large-scale healthcare dataset
- Implements Python RQ and PostgreSQL to handle asynchronous tasks and store generated data
- Trains a LLaMA transformer for healthcare diagnosis based on the generated dataset

## Requirements

- Python 3.7 or higher
- PostgreSQL
- Redis

## Installation

1. Clone the repository and navigate to the project folder.

2. Create a `.env` file containing the following env vars: `POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, REDIS_URL, OPENAI_API_KEY`

3. Run the following command to install the required packages: `chmod +x ./setup.sh && ./setup.sh`

4. Run the `start.sh` script located in the `condition_datagen` folder. This will generate a massive healthcare dataset using GPT-4.

5. To be continued...

