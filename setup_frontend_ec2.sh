#!/bin/bash
set -e

echo "Starting Native Frontend Setup for NutriTrack..."

# 1. Update OS and Install Dependencies
sudo apt-get update -y
sudo apt-get install -y nginx nodejs npm git

# 2. Build the Frontend
echo "Building Frontend..."
# Assuming this script is run from the project root (nutritrack)
cd frontend
npm install
npm run build

# 3. Deploy built files to Nginx
echo "Deploying to Nginx..."
sudo rm -rf /usr/share/nginx/html/*
sudo cp -r dist/* /usr/share/nginx/html/

# 4. Configure Nginx
echo "Configuring Nginx..."
cat << 'EOF' | sudo tee /etc/nginx/conf.d/nutritrack.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/javascript application/javascript application/json;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API proxy
    location /api/ {
        # Proxies directly to the Internal ALB
        proxy_pass http://internal-nutritrack-prod-int-alb-1445772917.us-east-1.elb.amazonaws.com;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Remove default nginx config to avoid port 80 conflict
sudo rm -f /etc/nginx/conf.d/default.conf || true
sudo rm -f /etc/nginx/sites-enabled/default || true

# 5. Enable Nginx
sudo systemctl enable nginx
sudo systemctl start nginx

echo "Frontend Setup Complete! You can now create an AMI from this instance."
echo "NOTE: The Nginx configuration is fully baked with your Internal ALB endpoint!"
