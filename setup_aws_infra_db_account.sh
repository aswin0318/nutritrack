#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting AWS Infrastructure Setup for Database Account..."

PROJECT="nutritrack"
ENV="prod"
REGION="us-east-1"
AZ1="${REGION}a"
AZ2="${REGION}b"
APP_VPC_CIDR="10.0.0.0/16" # Used for Security Group Ingress

# --- 1. Create DB VPC ---
echo "Creating DB VPC..."
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.1.0.0/16 --query 'Vpc.VpcId' --output text --region $REGION)
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames '{"Value":true}' --region $REGION
aws ec2 create-tags --resources $VPC_ID --tags Key=Name,Value=$PROJECT-$ENV-db-vpc --region $REGION
echo "DB VPC Created: $VPC_ID"

# --- 2. Create DB Subnets ---
echo "Creating DB Subnets..."
DB_SUB1=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.1.1.0/24 --availability-zone $AZ1 --query 'Subnet.SubnetId' --output text --region $REGION)
DB_SUB2=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.1.2.0/24 --availability-zone $AZ2 --query 'Subnet.SubnetId' --output text --region $REGION)
aws ec2 create-tags --resources $DB_SUB1 --tags Key=Name,Value=$PROJECT-$ENV-db-sub-$AZ1 --region $REGION
aws ec2 create-tags --resources $DB_SUB2 --tags Key=Name,Value=$PROJECT-$ENV-db-sub-$AZ2 --region $REGION

# --- 3. Route Table ---
echo "Creating Route Table..."
RT_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text --region $REGION)
aws ec2 associate-route-table --subnet-id $DB_SUB1 --route-table-id $RT_ID --region $REGION > /dev/null
aws ec2 associate-route-table --subnet-id $DB_SUB2 --route-table-id $RT_ID --region $REGION > /dev/null
aws ec2 create-tags --resources $RT_ID --tags Key=Name,Value=$PROJECT-$ENV-db-rt --region $REGION

# --- 4. Security Group ---
echo "Creating DB Security Group..."
DB_SG=$(aws ec2 create-security-group --group-name $PROJECT-db-sg --description "SG for cross-account RDS" --vpc-id $VPC_ID --query 'GroupId' --output text --region $REGION)
# Allow Postgres port from the Application VPC CIDR (10.0.0.0/16)
aws ec2 authorize-security-group-ingress --group-id $DB_SG --protocol tcp --port 5432 --cidr $APP_VPC_CIDR --region $REGION > /dev/null
aws ec2 create-tags --resources $DB_SG --tags Key=Name,Value=$PROJECT-$ENV-db-sg --region $REGION

# --- 5. DB Subnet Group ---
echo "Creating DB Subnet Group..."
aws rds create-db-subnet-group \
    --db-subnet-group-name "$PROJECT-cross-vpc-db-subnet-group" \
    --db-subnet-group-description "Subnet group for NutriTrack RDS in DB Account" \
    --subnet-ids "$DB_SUB1" "$DB_SUB2" \
    --region $REGION > /dev/null

echo "======================================================"
echo "DB Account Infrastructure Setup Complete!"
echo "DB VPC ID: $VPC_ID"
echo "DB Route Table ID: $RT_ID"
echo "DB Subnets: $DB_SUB1, $DB_SUB2"
echo "DB Security Group ID: $DB_SG"
echo "DB Subnet Group: $PROJECT-cross-vpc-db-subnet-group"
echo "======================================================"
echo "Next Steps:"
echo "1. Log into your App Account and initiate a VPC Peering Request to this VPC ($VPC_ID)."
echo "2. Accept the peering request in this DB Account."
echo "3. Update this DB Route Table ($RT_ID) to route 10.0.0.0/16 to the Peering Connection."
echo "4. Update your App Private Route Table to route 10.1.0.0/16 to the Peering Connection."
