---
Title: NGINX
Description: Reverse Proxy Service
---

[Nginx](https://www.nginx.com/), stylized as NGIИX, is a web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache.

## Table of contents

- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [Integration](#integration)
- [Related Tutorials](#related-tutorials)

## Folder Structure

```
nginx
├── docker-compose.yml  # Service configuration
├── nginx.conf          # NGINX configuration
├── README.md
└── template            # Template and Script to manage nginx.conf dynamically - WORK IN PROGRESS
    ├── nginx.conf.j2
    └── template.py
```

## Docker-compose

```yaml
version: "3"
services:
  nginx:
    image: nginx
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ../Certbot-Godaddy/config:/etc/letsencrypt # Only needed for HTTPS configuration
    restart: unless-stopped

# This network configuration must be added to all services behind NGINX
# NGIX must be on the same network of the services it will be routing requests
networks:
  default:
    external:
      name: apps
```

## Integration

> TODO: Network diagram

## Related Tutorials

> TODO:

- Tutorial adding a service do nginx.conf
  - deny external access
- How to use nginx templating
