# AWS Deployment Guide

NutriTrack360 is designed to be deployed on AWS using a highly available, secure architecture.

## Target Architecture

1. **Networking**: Custom VPC with 2 public subnets, 2 private application subnets, and 2 private database subnets across two Availability Zones.
2. **Compute**:
   - Frontend: Hosted on S3 + CloudFront, or containerized via ECS Fargate.
   - Backend: Containerized via ECS Fargate or Auto Scaling EC2 instances.
3. **Database**: Amazon RDS for PostgreSQL (Multi-AZ).
4. **Caching**: Amazon ElastiCache for Redis.
5. **Load Balancing**: Application Load Balancer (ALB) routing traffic to backend services.
6. **Security**: AWS WAF, Security Groups restricting inter-service communication.

## Deployment Steps (High Level)

1. **Infrastructure as Code**: Use Terraform or CloudFormation to provision the VPC, Subnets, RDS, and ElastiCache.
2. **Container Registry**: Push Docker images to Amazon ECR.
3. **Compute Provisioning**: Define ECS Task Definitions and Services for the Backend container.
4. **Secrets Management**: Store database credentials and JWT secrets in AWS Secrets Manager.
5. **CI/CD**: Configure GitHub Actions to automatically build and push images to ECR, and update ECS services on merge to `main`.
