#!/bin/bash

# Install Nginx if it's not already installed
sudo apt-get update
sudo apt-get install -y nginx

sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

sudo echo "Hello, World!" > /data/web_static/releases/test/index.html

sudo rm -f /etc/nginx/sites-enabled/web_static
sudo ln -s /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data

sudo echo "server {
    listen 80;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current;
    }
}" > /etc/nginx/sites-available/web_static

sudo ln -s /etc/nginx/sites-available/web_static /etc/nginx/sites-enabled/

sudo service nginx restart
