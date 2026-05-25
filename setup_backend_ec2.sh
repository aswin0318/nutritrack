#!/bin/bash
set -e

echo "Starting Native Backend Setup for NutriTrack..."

# 1. Update OS and Install Dependencies
sudo dnf update -y
sudo dnf install -y python3 python3-pip python3-devel gcc postgresql15-devel git

# 2. Setup Application Directory
echo "Setting up backend application directory..."
sudo mkdir -p /opt/nutritrack-backend
sudo mkdir -p /etc/nutritrack

# Assuming this script is run from the project root (nutritrack)
sudo cp -r backend/* /opt/nutritrack-backend/
sudo chown -R ec2-user:ec2-user /opt/nutritrack-backend

# 3. Create Python Virtual Environment and Install Dependencies
echo "Installing Python dependencies..."
cd /opt/nutritrack-backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Setup Environment File Placeholder
echo "Setting up .env placeholder..."
sudo cat << 'EOF' | sudo tee /etc/nutritrack/.env
APP_NAME=NutriTrack360
APP_ENV=production
APP_DEBUG=false
APP_VERSION=1.0.0
# Hardcoded for AMI baking
DATABASE_URL=postgresql+asyncpg://nutritrack:nutritrack_secret@nutritrack-prod-rds.c6tememgel1n.us-east-1.rds.amazonaws.com:5432/nutritrack360
JWT_SECRET_KEY=change_me
CORS_ORIGINS="*"
EOF
sudo chmod 600 /etc/nutritrack/.env

# 5. Create Systemd Service
echo "Creating Systemd service..."
sudo cat << 'EOF' | sudo tee /etc/systemd/system/nutritrack-backend.service
[Unit]
Description=NutriTrack Backend API (Uvicorn)
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/opt/nutritrack-backend
EnvironmentFile=/etc/nutritrack/.env
ExecStart=/opt/nutritrack-backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 6. Enable and Start the Service
sudo systemctl daemon-reload
sudo systemctl enable nutritrack-backend.service

echo "Backend Setup Complete! You can now create an AMI from this instance."
echo "NOTE: The environment variables are fully baked with your RDS endpoint!"
