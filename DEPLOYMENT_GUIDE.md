# Cricket Game CI/CD Deployment Guide

This guide will walk you through setting up a complete CI/CD pipeline for the Cricket Game application using Jenkins, SonarQube, AWS services, Docker, and Kubernetes.

## Prerequisites

- AWS Account with appropriate permissions
- GitHub account
- Basic knowledge of Docker, Kubernetes, and AWS services

## Step 1: AWS Infrastructure Setup

### 1.1 Install Required Tools

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### 1.2 Configure AWS Credentials

```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region (us-west-2)
```

### 1.3 Deploy Infrastructure with Terraform

```bash
cd terraform
terraform init
terraform plan -var="db_password=YourSecurePassword123!"
terraform apply -var="db_password=YourSecurePassword123!"
```

## Step 2: GitHub Repository Setup

### 2.1 Push Code to GitHub

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Add GitHub remote
git remote add origin https://github.com/yourusername/cricket-game.git
git branch -M main
git push -u origin main
```

### 2.2 Set GitHub Secrets

In your GitHub repository, go to Settings > Secrets and variables > Actions, and add:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `SONAR_TOKEN`

## Step 3: SonarQube Setup

### 3.1 Deploy SonarQube on EC2

```bash
# Launch EC2 instance (t3.medium or larger)
# SSH into the instance and run:

sudo apt update
sudo apt install -y docker.io docker-compose

# Create docker-compose.yml for SonarQube
cat > docker-compose.yml << EOF
version: '3'
services:
  sonarqube:
    image: sonarqube:community
    depends_on:
      - db
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonar
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: sonar
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_extensions:/opt/sonarqube/extensions
      - sonarqube_logs:/opt/sonarqube/logs
    ports:
      - "9000:9000"
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
      POSTGRES_DB: sonar
    volumes:
      - postgresql:/var/lib/postgresql
      - postgresql_data:/var/lib/postgresql/data

volumes:
  sonarqube_data:
  sonarqube_extensions:
  sonarqube_logs:
  postgresql:
  postgresql_data:
EOF

sudo docker-compose up -d
```

### 3.2 Configure SonarQube

1. Access SonarQube at `http://your-ec2-ip:9000`
2. Login with admin/admin, change password
3. Create a new project for "cricket-game"
4. Generate a token for CI/CD integration

## Step 4: Jenkins Setup

### 4.1 Deploy Jenkins on EC2

```bash
# Launch another EC2 instance for Jenkins
sudo apt update
sudo apt install -y openjdk-11-jdk

# Add Jenkins repository
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

sudo apt update
sudo apt install -y jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Install Docker for Jenkins
sudo apt install -y docker.io
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### 4.2 Configure Jenkins

1. Access Jenkins at `http://your-jenkins-ec2-ip:8080`
2. Install suggested plugins plus:
   - SonarQube Scanner
   - AWS Steps
   - Kubernetes
   - Docker Pipeline
3. Configure tools:
   - Add NodeJS 18 installation
   - Configure SonarQube server
   - Add AWS credentials
   - Configure Docker

### 4.3 Create Jenkins Pipeline

1. Create a new Pipeline job
2. Configure to use SCM (GitHub repository)
3. Specify `Jenkinsfile` as the pipeline script

## Step 5: Kubernetes Setup

### 5.1 Configure EKS Access

```bash
aws eks update-kubeconfig --region us-west-2 --name cricket-game-cluster
```

### 5.2 Install AWS Load Balancer Controller

```bash
# Create IAM policy and service account
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/install/iam_policy.json

aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam_policy.json

# Install AWS Load Balancer Controller
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=cricket-game-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

### 5.3 Deploy Application

```bash
# Update the deployment.yaml with your ECR repository URL
sed -i 's|YOUR_ECR_REPO|YOUR_ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/cricket-game|g' k8s/deployment.yaml

# Deploy to Kubernetes
kubectl apply -f k8s/
```

## Step 6: Domain and SSL Setup

### 6.1 Purchase Domain

1. Purchase a domain from Route 53 or your preferred registrar
2. Create a hosted zone in Route 53

### 6.2 Configure SSL Certificate

```bash
# Request SSL certificate
aws acm request-certificate \
    --domain-name cricket-game.yourdomain.com \
    --validation-method DNS \
    --region us-west-2
```

### 6.3 Update Ingress

Update the ingress configuration in `k8s/service.yaml` with your domain and certificate ARN.

## Step 7: Monitoring Setup

### 7.1 Install Monitoring Stack

```bash
chmod +x scripts/setup-monitoring.sh
./scripts/setup-monitoring.sh
```

### 7.2 Access Monitoring

```bash
# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Access Prometheus
kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090
```

## Step 8: Security Enhancements

### 8.1 Enable Pod Security Standards

```bash
kubectl label namespace cricket-game pod-security.kubernetes.io/enforce=restricted
kubectl label namespace cricket-game pod-security.kubernetes.io/audit=restricted
kubectl label namespace cricket-game pod-security.kubernetes.io/warn=restricted
```

### 8.2 Configure Network Policies

```yaml
# Create network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cricket-game-network-policy
  namespace: cricket-game
spec:
  podSelector:
    matchLabels:
      app: cricket-game
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: TCP
      port: 3001
  egress:
  - {}
```

## Step 9: Backup and Recovery

### 9.1 Setup Automated Backups

```bash
# Install Velero for Kubernetes backups
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts/
helm install velero vmware-tanzu/velero \
    --namespace velero \
    --create-namespace \
    --set configuration.provider=aws \
    --set configuration.backupStorageLocation.bucket=cricket-game-backups \
    --set configuration.backupStorageLocation.config.region=us-west-2
```

## Step 10: Go Live!

### 10.1 Final Deployment

1. Push your code to the main branch
2. Jenkins will automatically trigger the CI/CD pipeline
3. Monitor the deployment in Jenkins and Kubernetes
4. Verify the application is accessible via your domain

### 10.2 Post-Deployment Checklist

- [ ] Application is accessible via HTTPS
- [ ] Health checks are passing
- [ ] Monitoring is working
- [ ] Backups are configured
- [ ] Security scans are clean
- [ ] Performance testing completed

## Maintenance

### Daily Tasks
- Monitor application health and performance
- Check for security vulnerabilities
- Review logs for errors

### Weekly Tasks
- Update dependencies
- Review security scan results
- Check backup integrity

### Monthly Tasks
- Update Kubernetes cluster
- Review and optimize costs
- Security audit

## Troubleshooting

### Common Issues

1. **Pod not starting**: Check logs with `kubectl logs -n cricket-game deployment/cricket-game-deployment`
2. **Health checks failing**: Verify the health endpoint is working
3. **Image pull errors**: Check ECR permissions and image exists
4. **Ingress not working**: Verify AWS Load Balancer Controller is running

### Support Commands

```bash
# Check pod status
kubectl get pods -n cricket-game

# View pod logs
kubectl logs -f deployment/cricket-game-deployment -n cricket-game

# Check ingress status
kubectl get ingress -n cricket-game

# View cluster events
kubectl get events -n cricket-game --sort-by='.lastTimestamp'
```

## Cost Optimization

1. Use Spot instances for non-production workloads
2. Enable cluster autoscaling
3. Set up cost monitoring alerts
4. Regularly review resource utilization

## Security Best Practices

1. Regularly update base images
2. Use least privilege access
3. Enable audit logging
4. Implement network segmentation
5. Regular security scans

Your Cricket Game is now live and accessible to the public with a complete CI/CD pipeline!
