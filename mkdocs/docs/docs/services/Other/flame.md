---
Title: Flame
Description: Homepage Service
Sort: 1
---

[Flame](https://github.com/pawelmalak/flame) is a self-hosted startpage for your server. Its design is inspired (heavily) by SUI. Flame is very easy to setup and use. With built-in editors, it allows you to setup your very own application hub in no time - no file editing necessary.

## Table of contents

- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [NGINX](#nginx)
- [Related Tutorials](#related-tutorials)

## Folder Structure

```
flame
├── data
└── docker-compose.yml
```

## Docker-compose

```yaml
version: "2.1"
services:
  flame:
    image: pawelmalak/flame:multiarch
    container_name: flame
    volumes:
      - ./data:/app/data
    ports:
      - 5005:5005
    restart: unless-stopped
```

## NGINX

### HTTP

```perl
# Flame
server {
    listen 80 default_server;
    server_name home.EXAMPLE.COM home;

    location / {
        proxy_pass http://flame:5005;
    }
}

```

### HTTPS

```perl
# Flame
server {
    listen 80 default_server;
    server_name home.EXAMPLE.COM home;
    return 301 https://$server_name$request_uri;
}

map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
}

server {
        listen                  443 ssl;
        server_name  home.EXAMPLE.COM;
        ssl_certificate /etc/letsencrypt/live/EXAMPLE.COM/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/EXAMPLE.COM/privkey.pem;

        if ($host != $server_name) {
            return 301 https://home.EXAMPLE.COM$request_uri;
        }

        location /socket {
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_http_version 1.1;
            proxy_pass http://flame:5005/socket;
        }

        location / {
            proxy_pass http://flame:5005;
        }
}
```

## Related Tutorials

> TODO:

- Add applications on homepage
- Configure Weather
