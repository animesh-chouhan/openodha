#!/usr/bin/bash

source venv/bin/activate
# gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
uvicorn main:app --port 9000 --reload