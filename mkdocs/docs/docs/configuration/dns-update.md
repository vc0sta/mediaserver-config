---
Title: DNS Update
Description: DNS
Sort: 3
---

My internet has no fixed IP address, so I had to update it manually everytime the connection is interrupted and a new IP is assigned.

To solve it, I created a little shellscript to check the current IP configuration at GoDaddy (my DNS provider) and the current WAN IP address of my network.

If those values don't match, then I update the DNS with my new IP.

Here is the script:

```bash
#!/usr/bin/bash

# daddy-autoupdate.sh
DOMAIN=vcosta.dev
SUBDOMAINS=(play requests vpn)

DESIRED_IP=$(curl ifconfig.me -s)

for SUBDOMAIN in "${SUBDOMAINS[@]}"
do
  CURRENT_IP=$(/usr/local/bin/daddy show -d ${DOMAIN} -n ${SUBDOMAIN} -t A | grep ${SUBDOMAIN} | cut -d"|" -f 3)

  if [ ! $CURRENT_IP = $DESIRED_IP ];
    then /usr/local/bin/daddy update --domain ${DOMAIN} -t A -n ${SUBDOMAIN} -v ${DESIRED_IP};
      echo $(date +"%Y-%m-%d %H:%M") Updating $SUBDOMAIN.$DOMAIN from $CURRENT_IP to $DESIRED_IP
    fi
done
```

I'm using [daddy](https://github.com/artberri/daddy) to manage my DNS records, it requires to setup a _key/secret_ at **\${HOME}/.daddy.yaml**.

Create a new [API Key](https://developer.godaddy.com/keys), then add it's values like:

```yaml
---
key: 1234567689
secret: 1234567689
```

## Cronjob

Also, I've set up this script to run each 30min using crontab:

```bash
crontab -e

# Then add this line at the end of the file:
*/30 * * * * /home/pi/daddy-autoupdate.sh
```
