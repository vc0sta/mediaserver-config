/*
Title: Deluge
Description: Torrent Service
*/

[Deluge](http://deluge-torrent.org/) is a lightweight, Free Software, cross-platform BitTorrent client.

## Table of contents
- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [Integration](#integration)
- [NGINX](#nginx)
- [Related Tutorials](#related-tutorials)

## Folder Structure

```
deluge
├── config                 # Service data
└── docker-compose.yml     # Service configuration
```
## Docker-compose
```yaml
---
version: "2.1"
services:
  deluge:
    image: ghcr.io/linuxserver/deluge
    container_name: deluge
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
      - DELUGE_LOGLEVEL=info
    volumes:
      - './config:/config'
      - ${STORAGE_PATH}/downloads:/downloads
    ports:
      - 58846:58846
      - 8112:8112
    restart: unless-stopped
```

```
# .env

STORAGE_PATH=/mnt/storage
TZ=America/Sao_Paulo
```
## Integration

> TODO: Volume mapping diagram
## NGINX

### HTTP

```perl
# Deluge
server {
    listen       80;
    server_name  torrent.EXAMPLE.COM;
    
    location / {
        proxy_pass http://deluge:8112;
    }
}
```

### HTTPS

```perl
# Deluge
server {
    listen       80;
    server_name  torrent.EXAMPLE.COM;
    return 301 https://$server_name$request_uri;
    }

server {
    listen 443 ssl http2;
    server_name  torrent.EXAMPLE.COM;
        ssl_certificate /etc/letsencrypt/live/EXAMPLE.COM/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/EXAMPLE.COM/privkey.pem;
    ssl_session_cache builtin:1000;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

    location / {
        proxy_pass http://deluge:8112;
    }
}
```

## Related Tutorials

> TODO:
 - Login First time
 - Configure Scheduling

