---
Title: Bazarr
Description: Subtitles Service
---

[Bazarr](https://www.bazarr.media/) is a companion application to Sonarr and Radarr. It can manage and download subtitles based on your requirements. You define your preferences by TV show or movie and Bazarr takes care of everything for you.

## Table of contents

- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [NGINX](#nginx)
- [Related Tutorials](#related-tutorials)

## Folder Structure

```
bazarr
├── config                     # Service data
├── docker-compose.yml         # Service configuration
└── update_libseccomp_rpi4.sh  # Script to install libseccomp on Raspberry Pi 4
```

> **Note:** I do not remember why I needed to install libseccomp, but I kept the commands I've used in _update_libseccomp_rpi4.sh_ file.

## Docker-compose

```yaml
version: "2.1"
services:
  bazarr:
    image: ghcr.io/linuxserver/bazarr
    container_name: bazarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
    volumes:
      - ./config:/config
      - ${STORAGE_PATH}/Movies:/movies
      - ${STORAGE_PATH}/Series:/tv
    ports:
      - 6767:6767
    restart: unless-stopped
```

## NGINX

### HTTP

```perl
# Bazarr
server {
    listen       80;
    server_name  subtitles.EXAMPLE.COM;

    location / {
        proxy_pass http://bazarr:6767;
    }
}
```

### HTTPS

```perl
# Bazarr
server {
    listen       80;
    server_name  subtitles.EXAMPLE.COM;
    return 301 https://$server_name$request_uri;
    }

server {
    listen 443 ssl http2;
    server_name  subtitles.EXAMPLE.COM;
        ssl_certificate /etc/letsencrypt/live/EXAMPLE.COM/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/EXAMPLE.COM/privkey.pem;
    ssl_session_cache builtin:1000;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

    location / {
        proxy_pass http://bazarr:6767;
	allow 192.168.77.0/24;
        deny all;


    }
}
```

## Related Tutorials

> TODO: Configure Subtitle Profiles
