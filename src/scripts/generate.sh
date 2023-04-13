#!/bin/bash

NUM_WORKERS=50

source venv/bin/activate
export $(grep -v '^#' .env | xargs)

for i in $(seq 1 $NUM_WORKERS); do
  echo "Starting worker $i"
  rq worker --name "worker-$i" &
  sleep 1
done

echo "All $NUM_WORKERS workers started"
wait