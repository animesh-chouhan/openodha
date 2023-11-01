#!/usr/bin/bash

# Pulling
docker pull animeshchouhan/openodha-auth:latest

# Stopping and Removing
docker container stop openodha-docker-openodha-auth-1
docker container stop openodha-docker-openodha-auth-1

# Starting
docker compose up
