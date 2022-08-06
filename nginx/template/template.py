
from jinja2 import Environment, FileSystemLoader

values = {
    "network_cidr": "192.168.77.0/24",
    "domain": ".vcosta.dev",
    "tls_chain": "/etc/letsencrypt/live/vcosta.dev/fullchain.pem",
    "tls_privkey": "/etc/letsencrypt/live/vcosta.dev/privkey.pem",
}


environment = Environment(loader=FileSystemLoader("./"))
template = environment.get_template("nginx.conf.j2")

filename = f"generated_nginx.conf"
content = template.render(values)
with open(filename, mode="w", encoding="utf-8") as message:
    message.write(content)