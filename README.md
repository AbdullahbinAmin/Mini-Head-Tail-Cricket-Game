# 🏏 Mini Cricket Head-Tail Game

[![CI/CD Pipeline](https://github.com/yourusername/cricket-game/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/yourusername/cricket-game/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=cricket-game&metric=alert_status)](https://sonarcloud.io/dashboard?id=cricket-game)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://hub.docker.com/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)

A modern, interactive cricket game built with React and TypeScript, featuring a complete CI/CD pipeline and cloud deployment on AWS.

## 🎮 Game Features

- **Team Selection**: Choose from 4 international teams (India, Australia, England, Pakistan)
- **Player Management**: Each team has 11 unique players with individual scoring
- **Game Modes**: Play against Computer AI or Human Player
- **Toss System**: Realistic coin toss with heads/tails selection
- **Visual Effects**: 
  - ✨ Green glow effect for 6 runs
  - 🌟 Yellow-green effect for 4 runs
  - 🔴 Red effect for OUT
- **Complete Match Flow**: Two innings with target chasing
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **shadcn/ui** for components

### Backend
- **Node.js** with Express 5
- **TypeScript** for type safety
- **SQLite** with Kysely query builder

### DevOps & Infrastructure
- **Docker** for containerization
- **Kubernetes (EKS)** for orchestration
- **AWS** cloud services
- **Jenkins** for CI/CD
- **SonarQube** for code quality
- **Terraform** for infrastructure as code

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/cricket-game.git
cd cricket-game

# Install dependencies
npm install

# Start development server
npm run start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:3001

### Docker Development

```bash
# Build Docker image
docker build -t cricket-game .

# Run container
docker run -p 3001:3001 cricket-game
```

## 🎯 How to Play

1. **Select Game Mode**: Choose between VS Computer or VS Player
2. **Pick Teams**: Select different teams for each player
3. **Toss**: Call heads or tails to win the toss
4. **Choose**: Decide to bat or bowl first
5. **Play**: 
   - **Batting**: Click numbers 1-6 to play shots
   - **Bowling**: Select numbers 1-6 to bowl
   - **OUT**: When batting and bowling numbers match
6. **Win**: Score more runs than your opponent!

## 🏗️ CI/CD Pipeline

Our robust CI/CD pipeline includes:

### 🔍 Code Quality
- **SonarQube** analysis for code quality and security
- **ESLint** and **TypeScript** checking
- **npm audit** for vulnerability scanning

### 🧪 Testing & Security
- Automated unit tests
- **Trivy** container security scanning
- Quality gates before deployment

### 🚀 Deployment
- **AWS EKS** Kubernetes cluster
- **ECR** for container registry
- **ALB** for load balancing
- **Auto-scaling** based on CPU/memory usage

### 📊 Monitoring
- **Prometheus** for metrics collection
- **Grafana** dashboards
- **Health checks** and alerting

## ☁️ AWS Infrastructure

### Core Services
- **EKS Cluster**: Managed Kubernetes service
- **ECR**: Container registry
- **VPC**: Network isolation
- **ALB**: Application Load Balancer
- **RDS**: PostgreSQL database (optional)

### Security
- **IAM** roles and policies
- **Security Groups** for network access
- **SSL/TLS** certificates
- **Private subnets** for worker nodes

## 📋 Deployment Guide

### One-Click Deployment

```bash
# Deploy infrastructure
cd terraform
terraform apply

# Deploy application
./scripts/deploy.sh
```

### Manual Deployment

1. **Setup AWS Infrastructure**
   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```

2. **Configure Jenkins Pipeline**
   - Install required plugins
   - Configure AWS credentials
   - Set up SonarQube integration

3. **Deploy to Kubernetes**
   ```bash
   kubectl apply -f k8s/
   ```

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

## 🔧 Environment Variables

```env
NODE_ENV=production
PORT=3001
DATA_DIRECTORY=/app/data
AWS_REGION=us-west-2
```

## 📁 Project Structure

```
cricket-game/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── lib/           # Utilities
│   │   └── cricket-game.py # Python game (standalone)
├── server/                # Express backend
├── k8s/                   # Kubernetes manifests
├── terraform/             # Infrastructure as code
├── scripts/               # Deployment scripts
├── .github/workflows/     # GitHub Actions
├── Dockerfile            # Container configuration
└── Jenkinsfile           # Jenkins pipeline
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Performance

- **Startup Time**: < 5 seconds
- **Response Time**: < 100ms API calls
- **Scalability**: Auto-scales 2-10 pods
- **Availability**: 99.9% uptime SLA

## 🔒 Security

- Container security scanning with Trivy
- Dependency vulnerability checking
- HTTPS/TLS encryption
- Network policies
- Non-root container execution

## 📈 Monitoring & Observability

Access monitoring dashboards:

```bash
# Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Prometheus
kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090
```

Default credentials: `admin/prom-operator`

## 🐛 Troubleshooting

### Common Issues

**Pod not starting?**
```bash
kubectl logs -n cricket-game deployment/cricket-game-deployment
```

**Health checks failing?**
```bash
kubectl describe pod -n cricket-game
```

**Image pull errors?**
```bash
# Check ECR permissions
aws ecr describe-repositories
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Acknowledgments

- React and TypeScript communities
- AWS for cloud services
- Kubernetes ecosystem
- Open source contributors

---

**⭐ Star this repository if you find it helpful!**

[![Deploy to AWS](https://img.shields.io/badge/Deploy%20to-AWS-FF9900?style=for-the-badge&logo=amazon-aws)](./DEPLOYMENT_GUIDE.md)
[![Live Demo](https://img.shields.io/badge/Live-Demo-00C851?style=for-the-badge&logo=vercel)](https://cricket-game.yourdomain.com)
