/*
Title: PiHole
Description: DNS Service
*/

## Table of contents
- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [Integration](#integration)
- [NGINX](#nginx)
- [Related Tutorials](#related-tutorials)

## Folder Structure

```
pihole
├── docker-compose.yml    # Service configuration
├── etc-dnsmasq.d
└── etc-pihole            # Block lists (managed by application)
```

## Docker-compose

```yaml
version: "3"

# More info at https://github.com/pi-hole/docker-pi-hole/ and https://docs.pi-hole.net/
services:
  pihole:
    container_name: pihole
    image: pihole/pihole:latest
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "67:67/udp"
      - "8010:80/tcp"
      - "8443:443/tcp"
    environment:
      ServerIP: ${SERVER_IP}
      VIRTUAL_HOST: ${CUSTOM_DOMAIN}
      TZ: ${TZ}
      WEBPASSWORD: ${PASSWORD}
    volumes:
      - './etc-pihole/:/etc/pihole/'
      - './etc-dnsmasq.d/:/etc/dnsmasq.d/'
    # Recommended but not required (DHCP needs NET_ADMIN)
    #   https://github.com/pi-hole/docker-pi-hole#note-on-capabilities
    cap_add:
      - NET_ADMIN
    restart: unless-stopped
```

```
# .env
SERVER_IP=192.168.0.104
CUSTOM_DOMAIN=hole.EXAMPLE.COM
TZ=America/Sao_Paulo
PASSWORD='password'

```
## Integration
> TODO: Network diagram

## NGINX

### HTTP
```perl
# PiHole
server {
    listen       80;
    server_name  hole.EXAMPLE.COM;
        
    location / {
        proxy_pass http://pihole/admin/;
   }
}
```

### HTTPS
```perl
# PiHole
server {
    listen       80;
    server_name  hole.EXAMPLE.COM;
    return 301 https://$server_name$request_uri;
    }

server {
    listen 443 ssl http2;
    server_name  hole.EXAMPLE.COM;
    ssl_certificate /etc/letsencrypt/live/EXAMPLE.COM/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/EXAMPLE.COM/privkey.pem;
    ssl_session_cache builtin:1000;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    
    location / {
        proxy_pass http://pihole/admin/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
   }
}
```

## Related Tutorials

> TODO:
 - Use PiHole as internal DNS
 - Add block lists