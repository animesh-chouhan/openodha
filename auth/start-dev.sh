#!/usr/bin/bash

export APP_ENV="DEV"

source venv/bin/activate
uvicorn main:app --port 9000 --reload