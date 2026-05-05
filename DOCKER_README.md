# Docker Setup Guide

## 🐋 Docker Configuration for Login System

PT: Este projeto incluí configuração completa do Docker para deployment em desenvolvimento e produção.

EN: This project includes complete Docker configuration for both development and production deployment.

---

## 📁 Estrutura dos ficheiros do Docker 

```
Teste-login/
├── docker-compose.yml          # Orchestration file
├── .env.example              # Environment variables template
├── backend/
│   ├── Dockerfile            # Backend container config
│   └── .dockerignore         # Backend ignore file
├── frontend/
│   ├── Dockerfile            # Frontend container config
│   ├── .dockerignore         # Frontend ignore file
│   └── nginx.conf           # Nginx configuration
└── DOCKER_README.md         # This file
```

---

## 🚀 Início Rápido

### 1. Pré-requisitos

```bash
# Install Docker
# Windows/Mac: Download from docker.com
# Linux: 
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
# Windows/Mac: Included with Docker Desktop
# Linux:
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod 755 /usr/local/bin/docker-compose
```

### 2. Configuração do Environment

```bash
# Copy environment file
cp .env.example .env

# Edit with your values
nano .env
```

### 3. Construir e Executar

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Acessar as Aplicações

- **Frontend**: http://localhost:80
- **Backend**: http://localhost:5000

---

## 🏗️ Container Details

### Backend Container

**Image**: Custom Flask image  
**Base**: `python:3.9-slim`  
**Port**: 5000  
**Features**:
- Multi-stage build
- Non-root user
- Health checks
- Volume mounting for development
- Environment variables

### Frontend Container

**Image**: Custom React + Nginx  
**Base**: `node:18-alpine` (build) + `nginx:alpine` (runtime)  
**Port**: 80  
**Features**:
- Multi-stage build
- Optimized production build
- Nginx reverse proxy
- Static asset caching
- Security headers
- Health checks

---

## 🔧 Modo Desenvolvimento vs Produção

### Modo Desenvolvimento

```bash
# Use volume mounts for live reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Modo Produção

```bash
# Configuração de produção
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

## 📋 Comandos do Docker

### Comandos Básicos

```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Remove containers and networks
docker-compose down --remove-orphans

# Remove everything (including volumes)
docker-compose down -v
```

### Comandos de Monitorização

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs
docker-compose logs -f

# View resource usage
docker stats
```

### Comandos de Manutenção

```bash
# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Restart service
docker-compose restart backend
docker-compose restart frontend

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# View container details
docker-compose inspect backend
docker-compose inspect frontend
```

---

## 🔒 Configuração de Segurança

### Variáveis de Ambiente

```bash
# Em produção, use segredos fortes:
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
```

### Segurança de Rede

- Containers communicate via private network
- Only necessary ports exposed
- Nginx security headers configured
- CORS properly configured

### File Permissions

- Non-root user in backend container
- Proper file ownership
- Restricted volume permissions

---

## 🗄️ Opções da Base de Dados

### SQLite (Padrão)

```yaml
# Uses SQLite file in volume
volumes:
  - backend_data:/app/data
```

### PostgreSQL (Production)

```yaml
# Uncomment in docker-compose.yml
database:
  image: postgres:13-alpine
  environment:
    POSTGRES_DB: login_db
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: ${DB_PASSWORD}
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

### MySQL (Alternative)

```yaml
# Alternative database
database:
  image: mysql:8.0
  environment:
    MYSQL_DATABASE: login_db
    MYSQL_USER: app_user
    MYSQL_PASSWORD: ${DB_PASSWORD}
    MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
  volumes:
    - mysql_data:/var/lib/mysql
```

---

## 🌐 Deployment em Produção

### Docker Compose em Produção

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    environment:
      - FLASK_ENV=production
      - DEBUG=False
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M

  frontend:
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 256M
        reservations:
          memory: 128M

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
```

### Docker Swarm  

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml login-system

# Scale services
docker service scale login-system_backend=3
```

### Kubernetes    

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: login-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: login-backend
  template:
    metadata:
      labels:
        app: login-backend
    spec:
      containers:
      - name: backend
        image: login-backend:latest
        ports:
        - containerPort: 5000
```

---

## 🔍 Resolução de Problemas

### Problemas Comuns

#### Conflitos de Portas

```bash
# Check port usage
netstat -tulpn | grep :80
netstat -tulpn | grep :5000

# Change ports in docker-compose.yml
ports:
  - "8080:80"  # Change host port
```

#### Problemas de Permissões

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Reset permissions
docker-compose down
sudo rm -rf backend_data
docker-compose up -d
```

#### Problemas de Build

```bash
# Clear Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

#### Container Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Check container status
docker-compose ps

# Debug container
docker-compose run --rm backend bash
```

### Verificações de Saúde

```bash
# Verificar estado de saúde
docker-compose ps

# Verificação manual de saúde
curl http://localhost:5000/
curl http://localhost:80/

# Logs de saúde do container
docker inspect login-backend | grep Health
docker inspect login-frontend | grep Health
```

---

## 📊 Monitorização e Registo

### Gestão de Registos

```bash
# Centralized logging
docker-compose logs --tail=100

# Log rotation
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Metrics Collection  

```yaml
# Add to docker-compose.yml
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## 🔄 Integração com CI/CD

### GitHub Actions

```yaml
# .github/workflows/docker.yml
name: Docker Build and Deploy
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build Docker images
      run: |
        docker-compose build
    - name: Push to registry
      run: |
        docker-compose push
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('Test') {
            steps {
                sh 'docker-compose run --rm backend python -m pytest'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
```

---

## 📝 Boas Práticas  

### Image Optimization

1. **Use multi-stage builds**
2. **Minimize layers**
3. **Use .dockerignore**
4. **Choose minimal base images**
5. **Remove build dependencies**

### Security

1. **Use non-root users**
2. **Scan images for vulnerabilities**
3. **Use secrets management**
4. **Regular updates**
5. **Network segmentation**

### Performance

1. **Use volume mounts for development**
2. **Implement health checks**
3. **Set resource limits**
4. **Use load balancing**
5. **Optimize Dockerfile**

---

## 🆘 Suporte

### Obter Ajuda

```bash
# Docker help
docker --help
docker-compose --help

# Version information
docker --version
docker-compose --version

# System information
docker system info
docker system df
```

### Recursos

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Security Guide](https://docs.docker.com/engine/security/)

---

**Version**: 1.0  
**Last Updated**: 2026  
**Compatible**: Docker 20.10+, Docker Compose 2.0+
