/*
Title: Jellyfin
Description: Media Service
*/

[Jellyfin](https://jellyfin.github.io/) is a Free Software Media System that puts you in control of managing and streaming your media. It is an alternative to the proprietary Emby and Plex, to provide media from a dedicated server to end-user devices via multiple apps. Jellyfin is descended from Emby's 3.5.2 release and ported to the .NET Core framework to enable full cross-platform support. There are no strings attached, no premium licenses or features, and no hidden agendas: just a team who want to build something better and work together to achieve it.

## Table of contents
- [Folder Structure](#folder-structure)
- [Docker-compose](#docker-compose)
- [NGINX](#nginx)
- [Related Tutorials](#related-tutorials)

## Folder Structure

```
jellyfin
├── cache/              # Server data
├── config/             # Cache
├── css/                # Styles
└── docker-compose.yml  # Service configuration
```
## Docker-compose

```yaml
version: "3.5"
services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    volumes:
      - "./config:/config"         
      - "./cache:/cache"           
      - "./css:/jellyfin/jellyfin-web/assets/css"
      - ${STORAGE_PATH}:/media  # STORAGE_PATH is defined at .env file shown below
    restart: "unless-stopped"
    environment:
      - JELLYFIN_PublishedServerUrl=https://play.EXAMPLE.COM # Change this to your URL
      - UID=1000
      - GID=1000
    ports:
      - 8096:8096
      - 1900:1900
      - 7359:7359
```

```sh
# .env
STORAGE_PATH=/mnt/storage
```
## NGINX

### HTTP

> TODO: add HTTP config example
### HTTPS
```perl
# Jellyfin
# Uncomment the commented sections after you have acquired a SSL Certificate
server {
    listen 80;
    listen [::]:80;
    server_name play.EXAMPLE.COM;

    # Uncomment to redirect HTTP to HTTPS
     return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name play.EXAMPLE.COM;

    # use a variable to store the upstream proxy
    # in this example we are using a hostname which is resolved via DNS
    # (if you aren't using DNS remove the resolver line and change the variable to point to an IP address e.g `set $jellyfin 127.0.0.1`)
    set $jellyfin jellyfin;
    resolver 127.0.0.11 valid=30;

    ssl_certificate /etc/letsencrypt/live/EXAMPLE.COM/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/EXAMPLE.COM/privkey.pem;
    #include /etc/letsencrypt/options-ssl-nginx.conf;
    #ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    add_header Strict-Transport-Security "max-age=31536000" always;
    ssl_trusted_certificate /etc/letsencrypt/live/EXAMPLE.COM/chain.pem;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security / XSS Mitigation Headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";

    # Content Security Policy:x
    # See: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
    # Enforces https content and restricts JS/CSS to origin
    # External Javascript (such as cast_sender.js for Chromecast) must be whitelisted.
    #add_header Content-Security-Policy "default-src https: data: blob: http://image.tmdb.org; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' https://www.gstatic.com/cv/js/sender/v1/cast_sender.js https://www.youtube.com blob:; worker-src 'self' blob:; connect-src 'self'; object-src 'none'; frame-ancestors 'self'";

add_header Content-Security-Policy "default-src https: data: blob:; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/accentlist.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/base.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/bottombarprogress.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/fixes.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/jf_font.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/overlayprogress.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/rounding.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/rounding_circlehover.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/smallercast.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/rounding_circlehover.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/cornerindicator/indicator_floating.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/cornerindicator/indicator_corner.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/effects/glassy.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/effects/pan-animation.css https://ctalvio.github.io/Monochromic/backdrop-hack_style.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/effects/hoverglow.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/effects/scrollfade.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/episodelist/episodes_compactlist.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/episodelist/episodes_grid.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/fields/fields_border.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/fields/fields_noborder.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/header/header_transparent.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/header/header_transparent-dashboard.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/login/login_frame.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/login/login_minimalistic.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/login/login_frame.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/presets/monochromic_preset.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/presets/kaleidochromic_preset.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/presets/novachromic_preset.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/titlepage/title_banner.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/titlepage/title_banner_logo.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/titlepage/title_simple.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/titlepage/title_simple-logo.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/type/light.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/type/dark.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/type/colorful.css https://cdn.jsdelivr.net/gh/CTalvio/Ultrachromic/type/dark_withaccent.css https://fonts.googleapis.com/css2; script-src 'self' 'unsafe-inline' https://www.gstatic.com/cv/js/sender/v1/cast_sender.js worker-src 'self' blob:; connect-src 'self'; object-src 'none'; frame-ancestors 'self'";

    location = / {
        return 302 http://$host/web/;
    }

    location / {
        # Proxy main Jellyfin traffic
        proxy_pass http://$jellyfin:8096;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Protocol $scheme;
        proxy_set_header X-Forwarded-Host $http_host;

        # Disable buffering when the nginx proxy gets very resource heavy upon streaming
        proxy_buffering off;
    }

    # location block for /web - This is purely for aesthetics so /web/#!/ works instead of having to go to /web/index.html/#!/
    location = /web/ {
        # Proxy main Jellyfin traffic
        proxy_pass http://$jellyfin:8096/web/index.html;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Protocol $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
    }

    location /socket {
        # Proxy Jellyfin Websockets traffic
        proxy_pass http://$jellyfin:8096;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Protocol $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
    }
}
```
## Related Tutorials

> TODO: Tutorial on how to change CSS styling