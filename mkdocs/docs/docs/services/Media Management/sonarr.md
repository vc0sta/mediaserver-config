---
Title: Sonarr
Description: Series Service
---

[Sonarr](https://sonarr.tv/) (formerly NZBdrone) is a PVR for usenet and bittorrent users. It can monitor multiple RSS feeds for new episodes of your favorite shows and will grab, sort and rename them. It can also be configured to automatically upgrade the quality of files already downloaded when a better quality format becomes available.

## Table of contents

- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [NGINX](#nginx)
- [Related Tutorials](#related-tutorials)

## Folder Structure

```
sonarr
├── config
└── docker-compose.yml
```

## Docker-compose

```yaml
version: "2.1"
services:
  sonarr:
    image: ghcr.io/linuxserver/sonarr
    container_name: sonarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
    volumes:
      - ./config:/config
      - ${STORAGE_PATH}/Series:/tv
      - ${STORAGE_PATH}/downloads:/downloads
    ports:
      - 8989:8989
    restart: unless-stopped
```

## NGINX

### HTTP

```perl
# Sonarr
server {
    listen       80;
    server_name  series.EXAMPLE.COM;

    location / {
        proxy_pass http://sonarr:8989;
    }
}
```

### HTTPS

```perl
# Sonarr
server {
    listen       80;
    server_name  series.EXAMPLE.COM;
    return 301 https://$server_name$request_uri;
    }

server {
    listen 443 ssl http2;
    server_name  series.EXAMPLE.COM;
        ssl_certificate /etc/letsencrypt/live/vcosta.dev/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/vcosta.dev/privkey.pem;
    ssl_session_cache builtin:1000;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

    location / {
        proxy_pass http://sonarr:8989;
    }
}
```

## Related Tutorials

> TODO:

    - Connect to Deluge
    - Connect to Jackett
    - Connect to Jellyfin
