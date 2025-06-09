#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
AWS_REGION="us-west-2"
CLUSTER_NAME="cricket-game-cluster"
ECR_REPO="YOUR_ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/cricket-game"
NAMESPACE="cricket-game"

echo -e "${GREEN}🚀 Starting deployment process...${NC}"

# Check if required tools are installed
command -v aws >/dev/null 2>&1 || { echo -e "${RED}❌ AWS CLI is required but not installed. Aborting.${NC}" >&2; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo -e "${RED}❌ kubectl is required but not installed. Aborting.${NC}" >&2; exit 1; }
command -v docker >/dev/null 2>&1 || { echo -e "${RED}❌ Docker is required but not installed. Aborting.${NC}" >&2; exit 1; }

# Build and push Docker image
echo -e "${YELLOW}📦 Building Docker image...${NC}"
docker build -t $ECR_REPO:latest .

echo -e "${YELLOW}🔐 Logging into ECR...${NC}"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO

echo -e "${YELLOW}📤 Pushing image to ECR...${NC}"
docker push $ECR_REPO:latest

# Update kubeconfig
echo -e "${YELLOW}⚙️ Updating kubeconfig...${NC}"
aws eks update-kubeconfig --region $AWS_REGION --name $CLUSTER_NAME

# Apply Kubernetes manifests
echo -e "${YELLOW}🔧 Applying Kubernetes manifests...${NC}"
kubectl apply -f k8s/

# Wait for deployment to be ready
echo -e "${YELLOW}⏳ Waiting for deployment to be ready...${NC}"
kubectl rollout status deployment/cricket-game-deployment -n $NAMESPACE

# Show deployment status
echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${YELLOW}📊 Current status:${NC}"
kubectl get pods -n $NAMESPACE
kubectl get svc -n $NAMESPACE
kubectl get ingress -n $NAMESPACE

echo -e "${GREEN}🎉 Cricket Game is now deployed and running!${NC}"
