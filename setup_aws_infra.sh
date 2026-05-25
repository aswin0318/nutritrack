#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting AWS Infrastructure Setup for NutriTrack..."

# --- Configuration Variables ---
PROJECT="nutritrack"
ENV="prod"
REGION="us-east-1"
AZ1="${REGION}a"
AZ2="${REGION}b"
KEY_PAIR_NAME="us-east"
KEY_FILE="${KEY_PAIR_NAME}.pem"

# --- 0. Create Key Pair ---
echo "Creating Key Pair ($KEY_PAIR_NAME)..."
if ! aws ec2 describe-key-pairs --key-names "$KEY_PAIR_NAME" --region $REGION >/dev/null 2>&1; then
    # Remove existing local file to prevent 'Permission denied' if it was previously set to read-only
    rm -f "$KEY_FILE" 2>/dev/null || chmod 600 "$KEY_FILE" 2>/dev/null || true
    aws ec2 create-key-pair --key-name "$KEY_PAIR_NAME" --query 'KeyMaterial' --output text --region $REGION > "$KEY_FILE"
    chmod 400 "$KEY_FILE" 2>/dev/null || true
    echo "Key pair created and saved to $KEY_FILE"
else
    echo "Key pair $KEY_PAIR_NAME already exists, skipping creation."
fi

# --- 1. Create VPC ---
echo "Creating VPC..."
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text --region $REGION)
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames '{"Value":true}' --region $REGION
aws ec2 create-tags --resources $VPC_ID --tags Key=Name,Value=$PROJECT-$ENV-vpc --region $REGION
echo "VPC Created: $VPC_ID"

# --- 2. Create Subnets ---
echo "Creating Subnets..."
# Public Subnets (For Bastion, External ALB, NAT)
PUB_SUB1=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone $AZ1 --query 'Subnet.SubnetId' --output text --region $REGION)
PUB_SUB2=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --availability-zone $AZ2 --query 'Subnet.SubnetId' --output text --region $REGION)
aws ec2 modify-subnet-attribute --subnet-id $PUB_SUB1 --map-public-ip-on-launch --region $REGION
aws ec2 modify-subnet-attribute --subnet-id $PUB_SUB2 --map-public-ip-on-launch --region $REGION
aws ec2 create-tags --resources $PUB_SUB1 --tags Key=Name,Value=$PROJECT-$ENV-pub-sub-$AZ1 --region $REGION
aws ec2 create-tags --resources $PUB_SUB2 --tags Key=Name,Value=$PROJECT-$ENV-pub-sub-$AZ2 --region $REGION

# Private App Subnets (For Frontend, Backend, Internal ALB)
APP_SUB1=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.11.0/24 --availability-zone $AZ1 --query 'Subnet.SubnetId' --output text --region $REGION)
APP_SUB2=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.12.0/24 --availability-zone $AZ2 --query 'Subnet.SubnetId' --output text --region $REGION)
aws ec2 create-tags --resources $APP_SUB1 --tags Key=Name,Value=$PROJECT-$ENV-app-sub-$AZ1 --region $REGION
aws ec2 create-tags --resources $APP_SUB2 --tags Key=Name,Value=$PROJECT-$ENV-app-sub-$AZ2 --region $REGION

# Private DB Subnets (For RDS)
DB_SUB1=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.21.0/24 --availability-zone $AZ1 --query 'Subnet.SubnetId' --output text --region $REGION)
DB_SUB2=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.22.0/24 --availability-zone $AZ2 --query 'Subnet.SubnetId' --output text --region $REGION)
aws ec2 create-tags --resources $DB_SUB1 --tags Key=Name,Value=$PROJECT-$ENV-db-sub-$AZ1 --region $REGION
aws ec2 create-tags --resources $DB_SUB2 --tags Key=Name,Value=$PROJECT-$ENV-db-sub-$AZ2 --region $REGION

# --- 3. Internet Gateway ---
echo "Creating Internet Gateway..."
IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text --region $REGION)
aws ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID --region $REGION
aws ec2 create-tags --resources $IGW_ID --tags Key=Name,Value=$PROJECT-$ENV-igw --region $REGION

# --- 4. Public Route Table ---
echo "Creating Public Route Table..."
PUB_RT=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text --region $REGION)
aws ec2 create-route --route-table-id $PUB_RT --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID --region $REGION > /dev/null
aws ec2 associate-route-table --subnet-id $PUB_SUB1 --route-table-id $PUB_RT --region $REGION > /dev/null
aws ec2 associate-route-table --subnet-id $PUB_SUB2 --route-table-id $PUB_RT --region $REGION > /dev/null
aws ec2 create-tags --resources $PUB_RT --tags Key=Name,Value=$PROJECT-$ENV-pub-rt --region $REGION

# --- 5. NAT Gateways (One per AZ for HA) ---
echo "Allocating EIPs and Creating NAT Gateways..."
EIP1=$(aws ec2 allocate-address --domain vpc --query 'AllocationId' --output text --region $REGION)
EIP2=$(aws ec2 allocate-address --domain vpc --query 'AllocationId' --output text --region $REGION)

NAT1=$(aws ec2 create-nat-gateway --subnet-id $PUB_SUB1 --allocation-id $EIP1 --query 'NatGateway.NatGatewayId' --output text --region $REGION)
NAT2=$(aws ec2 create-nat-gateway --subnet-id $PUB_SUB2 --allocation-id $EIP2 --query 'NatGateway.NatGatewayId' --output text --region $REGION)
aws ec2 create-tags --resources $NAT1 --tags Key=Name,Value=$PROJECT-$ENV-nat-$AZ1 --region $REGION
aws ec2 create-tags --resources $NAT2 --tags Key=Name,Value=$PROJECT-$ENV-nat-$AZ2 --region $REGION

echo "Waiting for NAT Gateways to become available (this takes a few minutes)..."
aws ec2 wait nat-gateway-available --nat-gateway-ids $NAT1 $NAT2 --region $REGION

# --- 6. Private Route Tables ---
echo "Creating Private Route Tables..."
PRI_RT1=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text --region $REGION)
PRI_RT2=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text --region $REGION)

# Route 0.0.0.0/0 to NAT Gateways
aws ec2 create-route --route-table-id $PRI_RT1 --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NAT1 --region $REGION > /dev/null
aws ec2 create-route --route-table-id $PRI_RT2 --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NAT2 --region $REGION > /dev/null

# Associate AZ1 Subnets to PRI_RT1
aws ec2 associate-route-table --subnet-id $APP_SUB1 --route-table-id $PRI_RT1 --region $REGION > /dev/null
aws ec2 associate-route-table --subnet-id $DB_SUB1 --route-table-id $PRI_RT1 --region $REGION > /dev/null

# Associate AZ2 Subnets to PRI_RT2
aws ec2 associate-route-table --subnet-id $APP_SUB2 --route-table-id $PRI_RT2 --region $REGION > /dev/null
aws ec2 associate-route-table --subnet-id $DB_SUB2 --route-table-id $PRI_RT2 --region $REGION > /dev/null

aws ec2 create-tags --resources $PRI_RT1 --tags Key=Name,Value=$PROJECT-$ENV-pri-rt-$AZ1 --region $REGION
aws ec2 create-tags --resources $PRI_RT2 --tags Key=Name,Value=$PROJECT-$ENV-pri-rt-$AZ2 --region $REGION

# --- 7. Security Groups ---
echo "Creating Security Groups..."

# Bastion SG
BASTION_SG=$(aws ec2 create-security-group --group-name $PROJECT-bastion-sg --description "SG for Bastion Host" --vpc-id $VPC_ID --query 'GroupId' --output text --region $REGION)
aws ec2 authorize-security-group-ingress --group-id $BASTION_SG --protocol tcp --port 22 --cidr 0.0.0.0/0 --region $REGION > /dev/null
aws ec2 create-tags --resources $BASTION_SG --tags Key=Name,Value=$PROJECT-$ENV-bastion-sg --region $REGION

# External ALB SG
EXT_ALB_SG=$(aws ec2 create-security-group --group-name $PROJECT-ext-alb-sg --description "SG for External ALB" --vpc-id $VPC_ID --query 'GroupId' --output text --region $REGION)
aws ec2 authorize-security-group-ingress --group-id $EXT_ALB_SG --protocol tcp --port 80 --cidr 0.0.0.0/0 --region $REGION > /dev/null
aws ec2 authorize-security-group-ingress --group-id $EXT_ALB_SG --protocol tcp --port 443 --cidr 0.0.0.0/0 --region $REGION > /dev/null
aws ec2 create-tags --resources $EXT_ALB_SG --tags Key=Name,Value=$PROJECT-$ENV-ext-alb-sg --region $REGION

# Frontend Instances SG
FRONTEND_SG=$(aws ec2 create-security-group --group-name $PROJECT-frontend-sg --description "SG for Frontend Instances" --vpc-id $VPC_ID --query 'GroupId' --output text --region $REGION)
aws ec2 authorize-security-group-ingress --group-id $FRONTEND_SG --protocol tcp --port 80 --source-group $EXT_ALB_SG --region $REGION > /dev/null
aws ec2 authorize-security-group-ingress --group-id $FRONTEND_SG --protocol tcp --port 22 --source-group $BASTION_SG --region $REGION > /dev/null
aws ec2 create-tags --resources $FRONTEND_SG --tags Key=Name,Value=$PROJECT-$ENV-frontend-sg --region $REGION

# Internal ALB SG
INT_ALB_SG=$(aws ec2 create-security-group --group-name $PROJECT-int-alb-sg --description "SG for Internal ALB" --vpc-id $VPC_ID --query 'GroupId' --output text --region $REGION)
aws ec2 authorize-security-group-ingress --group-id $INT_ALB_SG --protocol tcp --port 80 --source-group $FRONTEND_SG --region $REGION > /dev/null
aws ec2 create-tags --resources $INT_ALB_SG --tags Key=Name,Value=$PROJECT-$ENV-int-alb-sg --region $REGION

# Backend Instances SG
BACKEND_SG=$(aws ec2 create-security-group --group-name $PROJECT-backend-sg --description "SG for Backend Instances" --vpc-id $VPC_ID --query 'GroupId' --output text --region $REGION)
aws ec2 authorize-security-group-ingress --group-id $BACKEND_SG --protocol tcp --port 8000 --source-group $INT_ALB_SG --region $REGION > /dev/null
aws ec2 authorize-security-group-ingress --group-id $BACKEND_SG --protocol tcp --port 22 --source-group $BASTION_SG --region $REGION > /dev/null
aws ec2 create-tags --resources $BACKEND_SG --tags Key=Name,Value=$PROJECT-$ENV-backend-sg --region $REGION

# Database SG
DB_SG=$(aws ec2 create-security-group --group-name $PROJECT-db-sg --description "SG for RDS and Redis" --vpc-id $VPC_ID --query 'GroupId' --output text --region $REGION)
aws ec2 authorize-security-group-ingress --group-id $DB_SG --protocol tcp --port 5432 --source-group $BACKEND_SG --region $REGION > /dev/null
aws ec2 authorize-security-group-ingress --group-id $DB_SG --protocol tcp --port 6379 --source-group $BACKEND_SG --region $REGION > /dev/null
aws ec2 create-tags --resources $DB_SG --tags Key=Name,Value=$PROJECT-$ENV-db-sg --region $REGION

# --- 8. Bastion Host ---
echo "Launching Bastion Host..."
# Fetch latest Amazon Linux 2023 AMI
AMI_ID=$(aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64 --query 'Parameters[0].Value' --output text --region $REGION)

BASTION_ID=$(aws ec2 run-instances --image-id $AMI_ID --count 1 --instance-type t2.micro --key-name $KEY_PAIR_NAME --security-group-ids $BASTION_SG --subnet-id $PUB_SUB1 --query 'Instances[0].InstanceId' --output text --region $REGION)
aws ec2 create-tags --resources $BASTION_ID --tags Key=Name,Value=$PROJECT-$ENV-bastion --region $REGION
echo "Bastion Host Launched: $BASTION_ID"

# --- 9. RDS Postgres ---
echo "Creating RDS Subnet Group and RDS Instance..."
aws rds create-db-subnet-group \
    --db-subnet-group-name "$PROJECT-db-subnet-group" \
    --db-subnet-group-description "Subnet group for NutriTrack RDS" \
    --subnet-ids "$DB_SUB1" "$DB_SUB2" \
    --region $REGION > /dev/null

echo "Skipping RDS Instance creation (Please set this up manually using the Subnet Group: $PROJECT-db-subnet-group and SG: $DB_SG)"

# --- 10. Load Balancers ---
echo "Creating External and Internal ALBs..."

# External ALB
EXT_ALB_ARN=$(aws elbv2 create-load-balancer \
    --name "$PROJECT-$ENV-ext-alb" \
    --subnets "$PUB_SUB1" "$PUB_SUB2" \
    --security-groups "$EXT_ALB_SG" \
    --scheme internet-facing \
    --type application \
    --query 'LoadBalancers[0].LoadBalancerArn' --output text --region $REGION)

# Target Group for External ALB
EXT_TG_ARN=$(aws elbv2 create-target-group \
    --name "$PROJECT-$ENV-frontend-tg" \
    --protocol HTTP --port 80 \
    --vpc-id $VPC_ID \
    --target-type instance \
    --query 'TargetGroups[0].TargetGroupArn' --output text --region $REGION)

# Listener for External ALB
aws elbv2 create-listener \
    --load-balancer-arn $EXT_ALB_ARN \
    --protocol HTTP --port 80 \
    --default-actions Type=forward,TargetGroupArn=$EXT_TG_ARN \
    --region $REGION > /dev/null

# Internal ALB
INT_ALB_ARN=$(aws elbv2 create-load-balancer \
    --name "$PROJECT-$ENV-int-alb" \
    --subnets "$APP_SUB1" "$APP_SUB2" \
    --security-groups "$INT_ALB_SG" \
    --scheme internal \
    --type application \
    --query 'LoadBalancers[0].LoadBalancerArn' --output text --region $REGION)

# Target Group for Internal ALB
INT_TG_ARN=$(aws elbv2 create-target-group \
    --name "$PROJECT-$ENV-backend-tg" \
    --protocol HTTP --port 8000 \
    --vpc-id $VPC_ID \
    --target-type instance \
    --query 'TargetGroups[0].TargetGroupArn' --output text --region $REGION)

# Listener for Internal ALB
aws elbv2 create-listener \
    --load-balancer-arn $INT_ALB_ARN \
    --protocol HTTP --port 80 \
    --default-actions Type=forward,TargetGroupArn=$INT_TG_ARN \
    --region $REGION > /dev/null

echo "======================================================"
echo "Infrastructure Setup Initiated Successfully!"
echo "VPC ID: $VPC_ID"
echo "Public Subnets: $PUB_SUB1, $PUB_SUB2"
echo "Private App Subnets: $APP_SUB1, $APP_SUB2"
echo "Private DB Subnets: $DB_SUB1, $DB_SUB2"
echo "External ALB ARN: $EXT_ALB_ARN"
echo "Internal ALB ARN: $INT_ALB_ARN"
echo "Frontend Target Group: $EXT_TG_ARN"
echo "Backend Target Group: $INT_TG_ARN"
echo "======================================================"
echo "Next Steps:"
echo "1. Create an AMI and Launch Template for Frontend using SG: $FRONTEND_SG"
echo "2. Create an AMI and Launch Template for Backend using SG: $BACKEND_SG"
echo "3. Create Auto Scaling Groups for both, attaching them to their respective Target Groups."
