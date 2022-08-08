/*
Title: Jackett
Description: Tracker Service
*/

[Jackett](https://github.com/Jackett/Jackett) works as a proxy server: it translates queries from apps (Sonarr, SickRage, CouchPotato, Mylar, etc) into tracker-site-specific http queries, parses the html response, then sends results back to the requesting software. This allows for getting recent uploads (like RSS) and performing searches. Jackett is a single repository of maintained indexer scraping & translation logic - removing the burden from other apps.
## Table of contents
- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [NGINX](#nginx)
- [Related Tutorials](#related-tutorials)

## Folder Structure
```
jackett
├── config              # Service data
└── docker-compose.yml  # Service configuration
```
## Docker-compose

```yaml
version: "2.1"
services:
  jackett:
    image: ghcr.io/linuxserver/jackett
    container_name: jackett
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=${TZ}
      - AUTO_UPDATE=true #optional
      - RUN_OPTS=<run options here> #optional
    volumes:
      - ./config:/config
      - ${STORAGE_PATH}/torrents:/downloads
    ports:
      - 9117:9117
    restart: unless-stopped
```
## NGINX

### HTTP

```perl
# Jackett
server {
    listen       80;
    server_name  tracker.vcosta.dev;

    location / {
        proxy_pass http://jackett:9117;
    }
}
```
### HTTPS
```perl
# Jackett
server {
    listen       80;
    server_name  tracker.vcosta.dev;
    return 301 https://$server_name$request_uri;
    }

server {
    listen 443 ssl http2;
    server_name  tracker.vcosta.dev;
        ssl_certificate /etc/letsencrypt/live/vcosta.dev/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/vcosta.dev/privkey.pem;
    ssl_session_cache builtin:1000;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

    location / {
        proxy_pass http://jackett:9117;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_redirect off;
    }
}
```
## Related Tutorials

> TODO: 
  - Add trackers
  - Integrate with Radarr/Sonarr

