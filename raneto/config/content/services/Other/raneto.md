/*
Title: Raneto
Description: Documentation Service
*/

[Raneto](http://raneto.com/) is an open source Knowledgebase platform that uses static Markdown files to power your Knowledgebase.

## Table of contents
- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [NGINX](#nginx)
- [Customization](#customization)
- [Related Tutorials](#related-tutorials)
## Folder structure

```
.
├── config
│   ├── content          # Markdown files - %base_dir%
│   └── images           # Image files    - %image-dir%
├── default              # Themes
│   ├── public
│   └── templates
└── docker-compose.yml   # Service configuration
```

## Docker-compose

```yaml
---
version: "2.1"
services:
  raneto:
    image: lscr.io/linuxserver/raneto:latest
    container_name: raneto
    environment:                             
      - PUID=1000
      - PGID=1000
      - TZ=America/Sao_Paulo                 # Set this variable to get the right timezone on your posts
    volumes:
      - ./config:/config                     # All documents are here
      - ./default:/app/raneto/themes/default # Used only for custom theme
    ports:
      - 3000:3000
    restart: unless-stopped
```

## NGINX

### HTTP

```perl
# Raneto
server {
    listen       80;
    server_name  docs.EXAMPLE.COM;

    location / {
        proxy_pass http://raneto:3000;
    }
    
}
```

### HTTPS
```perl
# Raneto
server {
    listen       80;
    server_name  docs.EXAMPLE.COM;
    return 301 https://$server_name$request_uri;
    }

server {
    listen 443 ssl http2;
    server_name  docs.EXAMPLE.COM;
    ssl_certificate /etc/letsencrypt/live/EXAMPLE.COM/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/EXAMPLE.COM/privkey.pem;
    ssl_session_cache builtin:1000;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

    location / {
        proxy_pass http://raneto:3000;
    }
}
```

## Customization

You can customize your theme either by modifying the HTML templates, or by modifying CSS styles, JS scripts in public folder.

```
.
├── public
│   ├── favicon.ico
│   ├── images -> /config/images
│   ├── lib
│   ├── scripts
│   └── styles
└── templates
    ├── edit.html
    ├── error.html
    ├── home.html
    ├── layout.html
    ├── login.html
    ├── page.html
    └── search.html
```

## Related Tutorials

- [Writing Documentation](%base_url%/tutorials/write-documentation.md)