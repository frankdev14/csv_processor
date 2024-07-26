#!/bin/bash

# Environment variable for enable debug mode and activate an sleep into the task
export DEBUG_MODE=false

# Activate virtual environment if you have
# Change this if you are using a virtual env for your virtualenv and put your venv path
source /home/frank/Development/bmat_task/bmat_api/bin/activate

# Run the FastAPI application with Uvicorn
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
