#!/bin/bash
# Personal-use app domain deployment helper

set -euo pipefail

APP_DOMAIN="${APP_DOMAIN:-}"
SITE_NAME="${SITE_NAME:-framework}"
NGINX_TEMPLATE="${NGINX_TEMPLATE:-nginx-framework.conf}"
NGINX_AVAILABLE="/etc/nginx/sites-available/${SITE_NAME}"
NGINX_ENABLED="/etc/nginx/sites-enabled/${SITE_NAME}"

if [ -z "$APP_DOMAIN" ]; then
    echo "Set APP_DOMAIN to the deployment hostname before running this script."
    echo "Example: APP_DOMAIN=personal.example.com ./deploy.sh"
    exit 1
fi

if [[ ! "$APP_DOMAIN" =~ ^[A-Za-z0-9.-]+$ ]]; then
    echo "APP_DOMAIN must be a hostname without a scheme, path, wildcard, or port."
    exit 1
fi

if [[ ! "$SITE_NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
    echo "SITE_NAME may only contain letters, numbers, dots, underscores, and dashes."
    exit 1
fi

if [ ! -f "$NGINX_TEMPLATE" ]; then
    echo "Nginx template not found: $NGINX_TEMPLATE"
    exit 1
fi

echo "Starting deployment for ${APP_DOMAIN}..."

echo "Installing Nginx and Certbot..."
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx -y

echo "Configuring Nginx site ${SITE_NAME}..."
sed "s#__APP_DOMAIN__#${APP_DOMAIN}#g" "$NGINX_TEMPLATE" | sudo tee "$NGINX_AVAILABLE" >/dev/null
sudo ln -sf "$NGINX_AVAILABLE" "$NGINX_ENABLED"
sudo rm -f /etc/nginx/sites-enabled/default

sudo nginx -t
sudo systemctl restart nginx

echo ""
echo "Nginx configured successfully for ${APP_DOMAIN}."
echo ""
echo "Next steps:"
echo "1. Make sure DNS for ${APP_DOMAIN} points to this server."
echo "2. Get SSL certificates:"
echo "   sudo certbot --nginx -d ${APP_DOMAIN}"
echo "3. Set APP_BASE_DOMAIN=${APP_DOMAIN}, FRONTEND_URL=https://${APP_DOMAIN}, and VITE_APP_BASE_DOMAIN=${APP_DOMAIN} in deployment env."
echo "4. Open ports 80 and 443 in your firewall."
echo "5. Rebuild and restart Docker services as needed."
echo ""
