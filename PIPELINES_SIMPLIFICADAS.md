# Pipelines Simplificadas - Backend e Frontend

## 🎯 Estrutura Simplificada

Agora o projeto tem apenas **2 pipelines principais**:
- **backend.yml** - Pipeline completa para o backend Flask
- **frontend.yml** - Pipeline completa para o frontend React

---

## 📁 Estrutura Final

```
.github/workflows/
├── backend.yml          # Pipeline do Backend Flask
└── frontend.yml         # Pipeline do Frontend React
```

---

## 🔧 Pipeline do Backend (`backend.yml`)

### Triggers
- **Push**: `main`, `develop`, `feature/*`
- **Pull Request**: `main`, `develop`
- **Paths**: `backend/**`

### Jobs

#### 1. **test** 🧪
- ✅ **Linting**: flake8, black, isort
- ✅ **Unit Tests**: pytest com coverage
- ✅ **Security Tests**: test_security.py
- ✅ **Safety Check**: scan de dependências
- ✅ **Bandit Scan**: análise de segurança
- ✅ **Database Tests**: operações DB

#### 2. **build** 🏗️
- ✅ **Docker Build**: cria imagem Docker
- ✅ **Security Scan**: Trivy na imagem
- ✅ **Push**: Docker Hub
- ✅ **Labels**: metadados da imagem

#### 3. **deploy** 🚀
- ✅ **Deploy**: para produção
- ✅ **Notificação**: status do deploy

---

## 🎨 Pipeline do Frontend (`frontend.yml`)

### Triggers
- **Push**: `main`, `develop`, `feature/*`
- **Pull Request**: `main`, `develop`
- **Paths**: `frontend/**`

### Jobs

#### 1. **test** 🧪
- ✅ **Linting**: ESLint, Prettier
- ✅ **Unit Tests**: Jest com coverage
- ✅ **Build**: npm run build
- ✅ **Accessibility**: axe-core tests
- ✅ **Security**: npm audit

#### 2. **build** 🏗️
- ✅ **Docker Build**: cria imagem Docker
- ✅ **Security Scan**: Trivy na imagem
- ✅ **Push**: Docker Hub
- ✅ **Labels**: metadados da imagem

#### 3. **deploy** 🚀
- ✅ **Deploy**: para produção
- ✅ **Notificação**: status do deploy

#### 4. **performance** 📊 (PRs apenas)
- ✅ **Lighthouse CI**: performance scores
- ✅ **Relatórios**: artefatos de performance

---

## 🔐 Secrets Necessários

Apenas **4 secrets** essenciais:

```bash
# Docker Hub
DOCKER_USERNAME=seu_usuario
DOCKER_PASSWORD=sua_senha

# Opcionais para deploy
PRODUCTION_HOST=seu_servidor
PRODUCTION_USER=seu_usuario
PRODUCTION_SSH_KEY=sua_chave_ssh
```

---

## 🚀 Como Funciona

### 1. **Desenvolvimento**
```bash
# Backend
cd backend
python -m pytest test_security.py -v --cov=.

# Frontend  
cd frontend
npm test -- --coverage --watchAll=false
```

### 2. **CI/CD Automático**
```bash
# Push para branch
git push origin feature/nova-feature

# Pipelines rodam automaticamente:
# - Backend: se mudanças em backend/**
# - Frontend: se mudanças em frontend/**
```

### 3. **Deploy Automático**
```bash
# Push para main
git push origin main

# Resultado:
# - Backend: imagem Docker criada e pushada
# - Frontend: imagem Docker criada e pushada
# - Deploy: automático para produção
```

---

## 📊 Logs e Monitoramento

### Logs Relevantes

#### Backend Pipeline
```
📥 Checkout code
🐍 Set up Python
📦 Install dependencies
🔍 Lint with flake8
🎨 Check code formatting with black
📚 Check import sorting with isort
🧪 Run unit tests
🔒 Run security tests
🛡️ Run safety check
🕵️ Run bandit security scan
📊 Test database operations
📈 Upload coverage to Codecov
📤 Upload security reports
🏗️ Build and push backend image
🔍 Run security scan on image
📤 Upload Trivy scan results
🚀 Deploy backend
📢 Notify deployment
```

#### Frontend Pipeline
```
📥 Checkout code
🟢 Set up Node.js
📦 Install dependencies
🔍 Run ESLint
🎨 Run Prettier check
🧪 Run unit tests
🏗️ Build application
🌐 Run accessibility tests
📈 Upload coverage to Codecov
🛡️ Run npm audit
📤 Upload security reports
🏗️ Build and push frontend image
🔍 Run security scan on image
📤 Upload Trivy scan results
🚀 Deploy frontend
📢 Notify deployment
📊 Performance results
```

---

## 🎯 Benefícios da Simplificação

### ✅ **Manutenibilidade**
- Menos arquivos para manter
- Lógica mais clara
- Debug mais fácil

### ✅ **Performance**
- Pipelines mais rápidas
- Menos dependencies
- Execução paralela

### ✅ **Flexibilidade**
- Deploy independente
- Testes isolados
- Escalabilidade

### ✅ **Segurança**
- Scans específicos
- Menos superfície de ataque
- Foco no essencial

---

## 🔧 Configuração de Desenvolvimento

### 1. **Ambiente Local**
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
```

### 2. **Frontend Local**
```bash
cd frontend
npm install
npm start
```

### 3. **Docker Local**
```bash
# Build e subir
docker-compose up --build

# Apenas backend
docker-compose up backend

# Apenas frontend
docker-compose up frontend
```

---

## 📋 Checklist de Deploy

### Antes do Deploy
- [ ] Testes unitários passando
- [ ] Testes de segurança OK
- [ ] Build sem erros
- [ ] Imagens Docker criadas
- [ ] Secrets configurados

### Durante o Deploy
- [ ] Pipelines executando
- [ ] Logs sendo gerados
- [ ] Notificações enviadas

### Pós-Deploy
- [ ] Aplicações rodando
- [ ] Health checks OK
- [ ] Monitoramento ativo
- [ ] Backup recente

---

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. **Pipeline Falha**
```bash
# Ver logs no GitHub Actions
# Verificar secrets
# Testar localmente
```

#### 2. **Build Erros**
```bash
# Limpar cache
docker system prune -a
npm cache clean --force
pip cache purge
```

#### 3. **Deploy Falha**
```bash
# Verificar conexão
# Checar permissões
# Validar configuração
```

---

## 🚀 Próximos Passos

### 1. **Configurar Secrets**
- Adicionar secrets no GitHub
- Testar conexão Docker Hub
- Validar chaves SSH

### 2. **Testar Pipelines**
- Fazer push para testar
- Verificar resultados
- Ajustar configuração

### 3. **Monitorar**
- Configurar alertas
- Criar dashboard
- Definir métricas

---

## 📈 Métricas Importantes

### Backend
- **Build Time**: < 5 minutos
- **Test Coverage**: > 80%
- **Security Score**: 0 vulnerabilidades
- **Deploy Success**: > 95%

### Frontend
- **Build Time**: < 3 minutos
- **Bundle Size**: < 1MB
- **Lighthouse**: > 90 em todos
- **Deploy Success**: > 95%

---

**Versão**: 2.0 - Simplificada  
**Data**: 2026  
**Status**: ✅ Produção Ready
