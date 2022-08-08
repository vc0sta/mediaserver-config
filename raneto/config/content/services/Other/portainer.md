/*
Title: Portainer
Description: Container Management Service
*/

[Portainer](https://www.portainer.io) is a self-service container service delivery platform. It is the definitive container management GUI for Kubernetes, Docker and Swarm.

## Table of contents
- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [NGINX](#nginx)


## Folder structure

```
portainer
├── data                # Service data
└── docker-compose.yml  # Service configuration
```

## Docker-compose
```yaml
version: '2'
services:
  portainer:
    image: portainer/portainer-ce
    command: -H unix:///var/run/docker.sock 
    container_name: portainer
    restart: unless-stopped
    ports:
      - 9000:9000
      # - 8000:8000
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock  # Portainer needs to connect to your host docker.sock
      - ./data:/data
```
## NGINX

### HTTP
```perl
# Portainer
server {
   listen       80;
   server_name  admin.EXAMPLE.COM;
    
   location / {
       proxy_pass http://portainer:9000;
   }
}
```
### HTTPS
```perl
# Portainer
server {
   listen       80;
   server_name  admin.EXAMPLE.COM;
    return 301 https://$server_name$request_uri;
    }

server {
    listen 443 ssl http2;
    server_name  admin.EXAMPLE.COM;
        ssl_certificate /etc/letsencrypt/live/EXAMPLE.COM/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/EXAMPLE.COM/privkey.pem;
    ssl_session_cache builtin:1000;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

   location / {
       proxy_pass http://portainer:9000;
       proxy_set_header   Upgrade            $http_upgrade;
       proxy_set_header   Connection         "upgrade";
   }
}
```