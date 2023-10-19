#!/usr/bin/bash

gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:9000
# uvicorn main:app --port 9000 --reload