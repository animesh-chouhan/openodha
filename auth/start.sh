#!/usr/bin/bash

export APP_ENV="DEV"

gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:9000 --access-logfile - 
