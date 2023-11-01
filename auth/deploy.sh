#!/usr/bin/bash

docker build -t openodha-auth:latest .
docker tag openodha-auth:latest animeshchouhan/openodha-auth:latest
docker login
docker push animeshchouhan/openodha-auth:latest