#!/usr/bin/env bash
# Aprovisionamiento idempotente del Droplet Ubuntu 24.04 LTS para Módulo 4:
# 1. Instala Docker Engine
# 2. Configura firewall UFW (22, 80, 443 abiertos; puertos internos 8000/50051 cerrados al exterior)
# 3. Instala Caddy con certificado HTTPS/TLS automático (<IP-con-guiones>.sslip.io o dominio propio)

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

echo "[1/4] Actualizando paquetes base e instalando Docker..."
apt-get -o DPkg::Lock::Timeout=120 update -y
apt-get -o DPkg::Lock::Timeout=120 install -y ca-certificates curl gnupg ufw debian-keyring debian-archive-keyring apt-transport-https

if ! command -v docker >/dev/null 2>&1; then
  apt-get -o DPkg::Lock::Timeout=120 install -y docker.io
fi
systemctl enable --now docker

echo "[2/4] Configurando firewall UFW (puertos mínimos 22, 80 y 443)..."
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
ufw status verbose

echo "[3/4] Instalando proxy inverso Caddy para SSL/HTTPS automático..."
if ! command -v caddy >/dev/null 2>&1; then
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor --yes -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list >/dev/null
  apt-get -o DPkg::Lock::Timeout=120 update -y
  apt-get -o DPkg::Lock::Timeout=120 install -y caddy
fi

PUBLIC_IP="$(curl -4 -fsS https://ifconfig.me || hostname -I | awk '{print $1}')"
DEFAULT_SSLIP="$(echo "$PUBLIC_IP" | tr '.' '-').sslip.io"
DOMAIN="${1:-$DEFAULT_SSLIP}"

echo "[4/4] Configurando HTTPS en Caddy para dominio: https://${DOMAIN}"
cat >/etc/caddy/Caddyfile <<EOF
${DOMAIN} {
    encode gzip zstd

    request_body {
        max_size 12MB
    }

    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "SAMEORIGIN"
        Referrer-Policy "strict-origin-when-cross-origin"
    }

    reverse_proxy 127.0.0.1:8000
}
EOF

systemctl enable caddy
systemctl restart caddy

echo "================================================================"
echo " Droplet listo para GitLab CI/CD"
echo " IP pública     : ${PUBLIC_IP}"
echo " Dominio HTTPS  : https://${DOMAIN}"
echo " Proxy inverso  : Caddy (:443 -> 127.0.0.1:8000)"
echo "================================================================"
