# Auto-Deploy Flask App - ECS DevOps

A complete DevOps pipeline for deploying a Flask application to AWS Elastic Container Service (ECS) using containerization and CI/CD practices.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Setup](#docker-setup)
- [AWS Infrastructure](#aws-infrastructure)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

This project demonstrates a production-ready Flask application deployed on AWS ECS using modern DevOps practices. It includes containerization with Docker, automated CI/CD pipelines, infrastructure as code, and comprehensive monitoring.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│  GitHub Actions  │───▶│   AWS ECR       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│      Users      │───▶│   Load Balancer  │───▶│   ECS Service   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │  ECS Tasks      │
                                                │  (Flask App)    │
                                                └─────────────────┘
```

## ✨ Features

- **Flask Web Application**: RESTful API with health checks and logging
- **Containerization**: Docker-based deployment with multi-stage builds
- **AWS ECS**: Scalable container orchestration with Fargate
- **CI/CD Pipeline**: Automated testing, building, and deployment
- **Infrastructure as Code**: AWS resources provisioned using Terraform
- **Load Balancing**: Application Load Balancer for high availability
- **Auto Scaling**: Automatic scaling based on CPU and memory metrics
- **Monitoring**: CloudWatch integration for logs and metrics
- **Security**: IAM roles, security groups, and SSL/TLS encryption

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**
- **Docker** and **Docker Compose**
- **AWS CLI** configured with appropriate permissions
- **Terraform** (version 1.0+)
- **Git**

### AWS Permissions Required

Your AWS user/role needs permissions for:
- ECS (Elastic Container Service)
- ECR (Elastic Container Registry)
- VPC and networking
- IAM roles and policies
- CloudWatch logs and metrics
- Application Load Balancer

## 🚀 Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/Yaswanthkumarreddyundela/flask-ecs-devops.git
cd flask-ecs-devops
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
AWS_REGION=us-east-1
```

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### 5. Run Tests

```bash
python -m pytest tests/
```

## 🐳 Docker Setup

### Build Docker Image

```bash
docker build -t flask-ecs-app .
```

### Run with Docker Compose

```bash
docker-compose up --build
```

### Docker Commands

```bash
# Build image
docker build -t flask-ecs-app:latest .

# Run container
docker run -p 5000:5000 flask-ecs-app:latest

# Push to ECR (after setting up ECR repository)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag flask-ecs-app:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/flask-ecs-app:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/flask-ecs-app:latest
```

## 🏗️ Terraform Infrastructure

This project uses Terraform to provision and manage AWS infrastructure as code.

### Infrastructure Components

The Terraform configuration includes:
- **VPC**: Virtual Private Cloud with public/private subnets
- **Security Groups**: Network access control for ECS tasks and load balancer
- **Application Load Balancer**: Traffic distribution and health checks
- **ECS Cluster**: Fargate-based container orchestration
- **ECS Service**: Service definition with auto-scaling configuration
- **ECR Repository**: Container image registry
- **IAM Roles**: Service permissions and task execution roles
- **CloudWatch Log Groups**: Centralized logging configuration

### Terraform Setup

1. **Initialize Terraform**:
   ```bash
   cd terraform/
   terraform init
   ```

2. **Review and modify variables**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your specific values
   ```

3. **Plan infrastructure**:
   ```bash
   terraform plan
   ```

4. **Apply infrastructure**:
   ```bash
   terraform apply
   ```

5. **Destroy infrastructure** (when needed):
   ```bash
   terraform destroy
   ```

### Terraform Variables

Key variables to configure in `terraform.tfvars`:

```hcl
aws_region          = "us-east-1"
project_name        = "flask-ecs-app"
environment         = "production"
app_port           = 5000
app_count          = 2
fargate_cpu        = 256
fargate_memory     = 512
health_check_path  = "/health"
```

### State Management

- **Remote State**: Configure S3 backend for state management
- **State Locking**: DynamoDB table for state locking
- **Workspaces**: Use Terraform workspaces for multiple environments

Example backend configuration:
```hcl
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "flask-ecs-devops/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

## ☁️ AWS Infrastructure

### Manual ECS Operations

If you need to perform manual ECS operations outside of Terraform:

1. **Create ECS Cluster**:
   ```bash
   aws ecs create-cluster --cluster-name flask-app-cluster
   ```

2. **Create Task Definition**:
   - Review and modify `task-definition.json`
   - Register the task definition:
   ```bash
   aws ecs register-task-definition --cli-input-json file://task-definition.json
   ```

3. **Create ECS Service**:
   ```bash
   aws ecs create-service \
     --cluster flask-app-cluster \
     --service-name flask-app-service \
     --task-definition flask-app-task \
     --desired-count 2 \
     --launch-type FARGATE \
     --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
   ```

### Infrastructure Components

All AWS resources are provisioned and managed through Terraform:

- **VPC**: Virtual Private Cloud with public/private subnets
- **Security Groups**: Network access control
- **Load Balancer**: Application Load Balancer for traffic distribution
- **ECS Cluster**: Container orchestration platform
- **ECR Repository**: Container image registry
- **IAM Roles**: Service permissions and policies

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

### Workflow Overview

1. **Code Push**: Developer pushes code to GitHub
2. **Testing**: Automated tests run on pull requests
3. **Build**: Docker image is built and tagged
4. **Push**: Image is pushed to AWS ECR
5. **Deploy**: ECS service is updated with new image
6. **Verify**: Health checks confirm successful deployment

### GitHub Actions Workflow

The `.github/workflows/deploy.yml` file defines the CI/CD pipeline:

- **Test Stage**: Run unit tests and linting
- **Build Stage**: Create Docker image
- **Deploy Stage**: Push to ECR and update ECS service

### Environment Variables (GitHub Secrets)

Set these secrets in your GitHub repository:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
ECR_REPOSITORY
ECS_CLUSTER
ECS_SERVICE
```

## 🚢 Deployment

### Manual Deployment

1. **Build and push Docker image**:
   ```bash
   ./scripts/build-and-push.sh
   ```

2. **Update ECS service**:
   ```bash
   aws ecs update-service \
     --cluster flask-app-cluster \
     --service flask-app-service \
     --force-new-deployment
   ```

### Automated Deployment

Push to the `main` branch to trigger automatic deployment via GitHub Actions.

## 📊 Monitoring

### CloudWatch Integration

- **Application Logs**: Centralized logging via CloudWatch Logs
- **Metrics**: Custom application metrics and AWS service metrics
- **Alarms**: Automated alerts for critical issues

### Health Checks

The application includes health check endpoints:

- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system status

### Scaling Policies

Auto Scaling policies based on:
- CPU utilization (>70% scale up, <30% scale down)
- Memory utilization
- Request count per target

## 🔧 Troubleshooting

### Common Issues

1. **ECS Service Not Starting**:
   - Check CloudWatch logs for container errors
   - Verify task definition parameters
   - Ensure security groups allow required traffic

2. **Load Balancer Health Checks Failing**:
   - Verify application is listening on correct port
   - Check health check endpoint response
   - Review security group rules

3. **Docker Build Failures**:
   - Check Dockerfile syntax
   - Verify base image availability
   - Review build context and .dockerignore

### Debugging Commands

```bash
# View ECS service events
aws ecs describe-services --cluster flask-app-cluster --services flask-app-service

# Check task logs
aws logs get-log-events --log-group-name /ecs/flask-app --log-stream-name <stream-name>

# List running tasks
aws ecs list-tasks --cluster flask-app-cluster --service-name flask-app-service
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write unit tests for new features
- Update documentation as needed
- Use meaningful commit messages
- Follow Terraform best practices for infrastructure changes
- Test infrastructure changes in a separate environment before applying to production


## 🙏 Acknowledgments

- AWS Documentation for ECS and Fargate
- Flask documentation and community
- Docker best practices guides
- GitHub Actions documentation

---

**Author**: Yaswanth Kumar Reddy Undela  
**Repository**: [flask-ecs-devops](https://github.com/Yaswanthkumarreddyundela/flask-ecs-devops)
