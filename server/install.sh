#!/usr/bin/bash

# Install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
rm get-docker.sh


# Run docker commands without sudo
sudo groupadd docker
sudo usermod -aG docker $USER
sudo docker swarm init

# Install other services
sudo apt install redis -y
sudo apt install nginx -y

# Edit redis.conf
# sudo nano /etc/redis/redis.conf
# bind 127.0.0.1 ::1 172.17.0.1
# requirepass redis-passwd
# sudo systemctl restart redis

# Setup nginx
# sudo rm /etc/nginx/sites-enabled/default
# sudo nano /etc/nginx/conf.d/nginx-openodha.conf
# sudo systemctl restart nginx

# Setup cloudflare ssl
# sudo nano /etc/ssl/openodha.pem
# sudo nano /etc/ssl/openodha.key