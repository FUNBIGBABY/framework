#!/bin/bash
# Valorie Framework domain script

set -e

echo "🚀 Starting deployment..."

# install Nginx
echo "📦 Installing Nginx..."
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx -y

# set Nginx
echo "⚙️  Configuring Nginx..."
sudo cp nginx-valorie.conf /etc/nginx/sites-available/valorie
sudo ln -sf /etc/nginx/sites-available/valorie /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# test
sudo nginx -t

# restart Nginx
sudo systemctl restart nginx

echo ""
echo "✅ Nginx configured successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Make sure DNS is configured (expert.valorie.ai and *.valorie.ai)"
echo "2. Get SSL certificates:"
echo "   sudo certbot --nginx -d expert.valorie.ai"
echo "   sudo certbot certonly --manual --preferred-challenges dns -d '*.valorie.ai' -d valorie.ai"
echo "3. Open ports 80 and 443 in GCP firewall"
echo "4. Update frontend code and rebuild Docker"
echo ""