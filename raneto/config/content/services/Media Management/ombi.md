/*
Title: Ombi
Description: Requests Service
*/

## Table of contents
- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [NGINX](#nginx)

## Folder Structure
```
ombi
├── config
└── docker-compose.yml
```

## Docker-compose
```yaml
---
version: "2.1"
services:
  ombi:
    image: lscr.io/linuxserver/ombi:latest
    container_name: ombi
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/Sao_Paulo
    volumes:
      - ./config:/config
    ports:
      - 3579:3579
    restart: unless-stopped
```
## Integration

> TODO: Services Diagram

## NGINX

### HTTP

```perl
 # Ombi v4 Subdomain
# Replace EXAMPLE.COM with your domain
server {
    listen 80;
    server_name requests.EXAMPLE.COM;
    resolver 1.1.1.1 1.0.0.1 valid=300s;
    resolver_timeout 10s;
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_types text/plain text/css text/xml application/xml text/javascript application/x-javascript image/svg+xml;
    gzip_disable "MSIE [1-6]\.";

    location / {
        proxy_pass http://ombi:3579;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    # This allows access to the actual api
    location /api {
            proxy_pass http://ombi:3579;
    }
    # This allows access to the documentation for the api
    location /swagger {
            proxy_pass http://ombi:3579;
    }
}

```
### HTTPS
```perl

 # Ombi v4 Subdomain
    # Replace EXAMPLE.COM with your domain
    server {
        listen 80;
        server_name requests.EXAMPLE.COM;
        return 301 https://$server_name$request_uri;
    }
    server {
        listen 443 ssl http2;
        server_name requests.EXAMPLE.COM;
        ssl_certificate /etc/letsencrypt/live/EXAMPLE.COM/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/EXAMPLE.COM/privkey.pem;
        ssl_session_cache builtin:1000;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-ECDSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
        ssl_session_tickets off;
        ssl_ecdh_curve secp384r1;
        resolver 1.1.1.1 1.0.0.1 valid=300s;
        resolver_timeout 10s;
        gzip on;
        gzip_vary on;
        gzip_min_length 1000;
        gzip_proxied any;
        gzip_types text/plain text/css text/xml application/xml text/javascript application/x-javascript image/svg+xml;
        gzip_disable "MSIE [1-6]\.";

        location / {
            proxy_pass http://ombi:3579;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        }
        # This allows access to the actual api
        location /api {
                proxy_pass http://ombi:3579;
        }
        # This allows access to the documentation for the api
        location /swagger {
                proxy_pass http://ombi:3579;
        }
    }

```
## Customization
