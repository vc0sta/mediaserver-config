/*
Title: Radarr
Description: Movies Service
*/

[Radarr](https://github.com/Radarr/Radarr) - A fork of Sonarr to work with movies à la Couchpotato.

## Table of contents
- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [NGINX](#nginx)
- [Related Tutorials](#related-tutorials)

## Folder Structure
```
radarr
├── config
└── docker-compose.yml
```

## Docker-compose
```yaml
version: "2.1"
services:
  radarr:
    image: ghcr.io/linuxserver/radarr
    container_name: radarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
    volumes:
      - ./config:/config
      - ${STORAGE_PATH}/Movies:/movies
      - ${STORAGE_PATH}/downloads:/downloads
    ports:
      - 7878:7878
    restart: unless-stopped
```

## NGINX

### HTTP

```perl

# Radarr
server {
    listen       80;
    server_name  movies.EXAMPLE.COM;
    

    location / {
        proxy_pass http://radarr:7878;
    }
}
```
### HTTPS
```perl
# Radarr
server {
    listen       80;
    server_name  movies.EXAMPLE.COM;
    return 301 https://$server_name$request_uri;
    }

server {
    listen 443 ssl http2;
    server_name  movies.EXAMPLE.COM;
    ssl_certificate /etc/letsencrypt/live/EXAMPLE.COM/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/EXAMPLE.COM/privkey.pem;
    ssl_session_cache builtin:1000;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

    location / {
        proxy_pass http://radarr:7878;
    }
}
```
## Related Tutorials

> TODO:
 - Create profile
 - Connect to Deluge
 - Telegram Notification