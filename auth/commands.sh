# Building and pushing
docker build -t openodha-auth:latest .
docker tag openodha-auth:latest animeshchouhan/openodha-auth:latest
docker login
docker push animeshchouhan/openodha-auth:latest


# Running
docker run -it --rm -p 9000:9000 openodha-auth:latest
docker run -it --rm -p 9000:9000 --add-host=host.docker.internal:host-gateway --name openodha-auth animeshchouhan/openodha-auth:latest
docker start openodha-auth
--add-host=host.docker.internal:host-gateway

# Pulling
docker pull animeshchouhan/openodha-auth:latest


# Debugging
docker container exec -it openodha-auth bash
docker container exec -it openodha-docker-openodha-auth-1 bash

apt-get update
apt-get install -y iputils-ping
apt-get install -y redis
apt-get install -y netcat-traditional
# ping host.docker.internal

# Password files
vim -b <filename>
:set noeol
:wq
