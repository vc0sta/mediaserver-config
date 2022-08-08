/*
Title: Planka
Description: Kanban Service
*/

[Planka](https://github.com/plankanban/planka) is a Trello-like kanban board built with React and Redux.
## Table of contents
- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [NGINX](#nginx)
- [Related Tutorials](#related-tutorials)
## Folder Structure

```
planka
├── attachments
├── db-data
├── docker-compose.yml
├── project-background-images
└── user-avatars
    └── 54f7e083-9836-4fea-90cf-ed6b809ef016
```
## Docker-compose

```yaml
version: '3'

services:
  planka:
    image: meltyshev/planka:latest
    container_name: planka
    command: >
      bash -c
        "for i in `seq 1 30`; do
          ./start.sh &&
          s=$$? && break || s=$$?;
          echo \"Tried $$i times. Waiting 5 seconds...\";
          sleep 5;
        done; (exit $$s)"
    restart: unless-stopped
    volumes: # These folders are mapped only to persist your data
             # you dont need to change anything in here
      - ./user-avatars:/app/public/user-avatars
      - ./project-background-images:/app/public/project-background-images
      - ./attachments:/app/public/attachments
    ports:
      - 1337:1337
    environment:
      - BASE_URL=https://tasks.EXAMPLE.COM # Change this to the URL you will use for this service
      - DATABASE_URL=postgresql://postgres@postgres/planka
      - SECRET_KEY=notsecretkey  
      - TRUST_PROXY=1
    depends_on:
      - postgres

  postgres:
    image: postgres:alpine
    container_name: planka_db
    restart: unless-stopped
    volumes: # This folder is mapped only to persist your data
             # you dont need to change anything in here
      - ./db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=planka
      - POSTGRES_HOST_AUTH_METHOD=trust
```

## NGINX

### HTTP
```perl
#  Planka
server {
    listen 80;
    server_name tasks.EXAMPLE.COM tasks;
    
    location / {
        proxy_pass http://planka:1337;
    }
}
```

### HTTPS
```perl
#  Planka
server {
    listen 80;
    server_name tasks.EXAMPLE.COM tasks;
    return 301 https://$server_name$request_uri;
}

map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
}

server {
        listen                  443 ssl;
        server_name  tasks.EXAMPLE.COM;
        ssl_certificate /etc/letsencrypt/live/EXAMPLE.COM/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/EXAMPLE.COM/privkey.pem;

        if ($host != $server_name) {
            return 301 https://tasks.EXAMPLE.COM$request_uri;
        }

        location /socket.io {
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_http_version 1.1;
            proxy_pass http://planka:1337/socket.io;
        }

        location / {
            proxy_pass http://planka:1337;
            allow 192.168.77.0/24;
            deny all;
        }
}
```

## Related Tutorial

> TODO: Basic board creation