#!/bin/bash

# Define a function to remove all jobs from the Redis queue
remove_jobs() {
    echo "Removing all jobs from the Redis queue"
    redis-cli del rq:queue:default
}

# Set up a trap to handle termination signals (SIGINT, SIGTERM)
trap remove_jobs INT TERM

# Run enqueue_jobs.py
read -p "Enter the number of rows to process (or press Enter for all rows): " num_rows
python enqueue_jobs.py --num_rows "${num_rows:-}"

# Get the number of enqueued jobs
num_jobs=$(redis-cli llen rq:queue:default)

# Display the number of enqueued jobs
echo "Enqueued $num_jobs jobs"

# Ask the user if they want to continue
read -p "Do you want to continue? (Y/N): " continue_answer

if [[ $continue_answer =~ ^[Yy]$ ]]; then
    # Ask the user for the number of workers
    read -p "Enter the number of workers: " num_workers

    # Start the workers with a progress bar using tqdm
    python -m tqdm --unit "job" --total $num_jobs --interval 1 -- \
        ./start_workers.sh $num_workers
else
    echo "Exiting without starting workers"
    remove_jobs
fi

# Remove the trap when the script finishes
trap - INT TERM
