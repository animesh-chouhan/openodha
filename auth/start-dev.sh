#!/usr/bin/bash

source venv/bin/activate
uvicorn main:app --port 9000 --reload