---
Title: TLS/SSL Configuration
Description: TLS SSL HTTPS
Sort: 4
---

To renew my TLS certificates, I'm using the scripts from [Certbot-Godaddy](https://github.com/orthrus/Certbot-Godaddy). It's usage is very simple:

Create a new [API Key](https://developer.godaddy.com/keys), and set your credentials at _api-settings.sh_:

```bash
############################################################
# Domain settings
DOMAIN=example.com
EMAIL=letsencrypt@${DOMAIN}
############################################################

############################################################
# GoDaddy API Credentials
GODADDY_API_KEY=""
GODADDY_API_SECRET=""
GODADDY_URL="https://api.godaddy.com/"
############################################################
```

Then run _certbot-godaddy-request.sh_:

```bash
# Give execute permissions to the script
chmod +x certbot-godaddy-request.sh

# Run it
./certbot-godaddy-request.sh
```

Your new certificate should be stored in /etc/letsencrypt/live/**[DOMAIN]**/

To use this certificate, see [NGIX Configuration](%base_url%/services/Network/nginx).
