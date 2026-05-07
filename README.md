# Sistema de login simples e registo

Este Projeto A consistio numa aplicação web simples de login e registo, com backend em Flask e frontend em React. Pode conter alguns erros e até algumas funções podem não funcionar correctamente. 

Já foram implementadas algumas alterações ao código original, como por exemplo a adição de um sistema de segurança mais robusto, com proteção contra ataques comuns, validação de inputs, rate limiting e brute force protection.

# Para a sua excução

É necessário ter o Python e o Node.js instalados no computador.
É executado por meio do app.py.

# Sistema de Login e Registro - Versão Simplificada

## Visão Geral

Sistema completo de login e registro com pipelines CI/CD **simplificadas e independentes** para backend e frontend.

### Arquitetura
- **Backend**: Flask com SQLite
- **Frontend**: React com componentes modulares
- **CI/CD**: GitHub Actions simplificados (2 pipelines apenas)
- **Deploy**: Docker containers
- **Segurança**: Múltiplas camadas de proteção

---

## Estrutura do Projeto

```
Teste-login/
├── backend/                 # Aplicação Flask
│   ├── app.py              # Aplicação principal
│   ├── database.py          # Operações DB
│   ├── security.py          # Módulo de segurança
│   ├── test_security.py     # Testes de segurança
│   ├── Dockerfile           # Container Docker
│   └── requirements.txt     # Dependências Python
├── frontend/                # Aplicação React
│   ├── src/
│   │   ├── components/      # Componentes modulares
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── SuccessPage.js
│   │   │   └── styles.css
│   │   ├── App.js          # Componente principal
│   │   └── App.test.js     # Testes de integração
│   ├── tests/
│   │   └── login.spec.js   # Testes E2E
│   ├── Dockerfile           # Container Docker
│   ├── package.json        # Dependências Node
│   └── lighthouserc.json   # Config Lighthouse
├── .github/
│   └── workflows/
│       ├── backend.yml        # Pipeline Backend (🔥)
│       └── frontend.yml       # Pipeline Frontend (🎨)
├── docker-compose.yml         # Orquestração Docker
├── .env                     # Variáveis de ambiente
├── PIPELINES_SIMPLIFICADAS.md  # Documentação pipelines
└── README.md               # Este arquivo
```

---

## Instalação Rápida

### 1. Pré-requisitos
```bash
# Docker Desktop
# Node.js 18+
# Python 3.9+
# Git
```

### 2. Clonar e Configurar
```bash
git clone https://github.com/MarcosCatito/Teste-de-login.git
cd Teste-login

# Configurar ambiente
cp .env.example .env
# Editar .env com suas configurações
```

### 3. Iniciar com Docker
```bash
# Iniciar tudo
docker-compose up --build

# Apenas backend
docker-compose up backend

# Apenas frontend
docker-compose up frontend
```

### 4. Acessar Aplicações
- **Frontend**: http://localhost:80
- **Backend**: http://localhost:5000

---

## Pipelines CI/CD Simplificadas

### Backend Pipeline (`.github/workflows/backend.yml`)

**Triggers**: Push para `main`, `develop`, `feature/*` | Mudanças em `backend/**`

**Jobs**:
1. **test** 🧪
   - ✅ Linting (flake8, black, isort)
   - ✅ Unit tests (pytest)
   - ✅ Security tests
   - ✅ Safety check
   - ✅ Bandit scan
   - ✅ Database tests

2. **build** 🏗️
   - ✅ Docker build
   - ✅ Security scan (Trivy)
   - ✅ Push para Docker Hub

3. **deploy** 🚀
   - ✅ Deploy automático
   - ✅ Notificações

### Frontend Pipeline (`.github/workflows/frontend.yml`)

**Triggers**: Push para `main`, `develop`, `feature/*` | Mudanças em `frontend/**`

**Jobs**:
1. **test** 🧪
   - ✅ Linting (ESLint, Prettier)
   - ✅ Unit tests (Jest)
   - ✅ Build verification
   - ✅ Accessibility tests
   - ✅ Security audit (npm audit)

2. **build** 🏗️
   - ✅ Docker build
   - ✅ Security scan (Trivy)
   - ✅ Push para Docker Hub

3. **deploy** 🚀
   - ✅ Deploy automático
   - ✅ Notificações

4. **performance** 📊 (PRs apenas)
   - ✅ Lighthouse CI
   - ✅ Performance scores

---

## Configuração de Segurança

### Secrets Necessários (Apenas 4 essenciais)
```bash
# Docker Hub (Obrigatório)
DOCKER_USERNAME=seu_usuario
DOCKER_PASSWORD=sua_senha

# Deploy (Opcional)
PRODUCTION_HOST=seu_servidor
PRODUCTION_USER=seu_usuario
PRODUCTION_SSH_KEY=sua_chave_ssh
```

### Camadas de Proteção
1. **Input Sanitization** - Limpeza de dados
2. **Rate Limiting** - 10 req/minuto
3. **Brute Force Protection** - 5 tentativas
4. **SQL Injection Prevention** - Prepared statements
5. **XSS Protection** - Sanitização HTML
6. **CORS Security** - Origins permitidos

---

## Testes Completos

### Backend Tests
```bash
cd backend
python -m pytest test_security.py -v --cov=.
```

### Frontend Tests
```bash
cd frontend
npm test -- --coverage --watchAll=false
```

### E2E Tests
```bash
cd frontend
npx playwright test
```

### Integration Tests
```bash
docker-compose -f docker-compose.test.yml up -d
python integration_tests.py
```

---

## Monitoramento e Logs

### Logs Relevantes com Emojis
```
📥 Checkout code
🐍 Set up Python/Node.js
📦 Install dependencies
🔍 Linting checks
🎨 Formatting checks
🧪 Unit tests
🔒 Security tests
🛡️ Safety scans
🏗️ Docker build
🚀 Deploy
📢 Notifications
```

### Métricas Importantes
- **Build Time**: < 5 min (backend), < 3 min (frontend)
- **Test Coverage**: > 80%
- **Security Score**: 0 vulnerabilidades críticas
- **Performance**: Lighthouse > 90

---

## Deploy em Produção

### 1. Configurar Ambiente
```bash
# Servidor de produção
# Docker instalado
# Chaves SSH configuradas
# Secrets no GitHub configurados
```

### 2. Deploy Automático
```bash
# Push para main
git push origin main

# Resultado automático:
# 🔥 Backend pipeline executa
# 🎨 Frontend pipeline executa
# 🏗️ Docker images criadas
# 🚀 Deploy automático
```

### 3. Verificação
```bash
# Status dos serviços
docker-compose ps

# Logs de produção
docker-compose logs -f

# Health checks
curl http://your-domain.com/health
```

---

## Troubleshooting

### Problemas Comuns

#### 1. Docker Issues
```bash
# Limpar cache
docker system prune -a

# Reconstruir
docker-compose build --no-cache

# Verificar logs
docker-compose logs
```

#### 2. Pipeline Failures
```bash
# Ver GitHub Actions
# Checkar secrets
# Testar localmente
```

#### 3. Deploy Issues
```bash
# Verificar conexão
# Checar permissões
# Validar configuração
```

---

## Checklist Completo

### Desenvolvimento
- [x] Ambiente configurado
- [x] Dependências instaladas
- [x] Testes locais passando
- [x] Docker build funcionando
- [x] Pipelines simplificadas

### Produção
- [x] Secrets documentados
- [x] Pipelines testadas
- [x] Deploy automatizado
- [x] Monitoramento ativo
- [x] Documentação completa

---

## Funcionalidades Implementadas

### Sistema de Login
- Registro de novos usuários
- Login de usuários existentes
- Validação de inputs
- Página de sucesso
- Sistema de tokens JWT

### Segurança
- Sanitização de inputs
- Rate limiting
- Brute force protection
- SQL injection prevention
- XSS protection
- CORS security

### CI/CD Simplificado
- **Apenas 2 pipelines** (backend + frontend)
- Testes automatizados
- Build automatizado
- Deploy automatizado
- Security scans
- Performance monitoring

### Docker
- Containers otimizados
- Multi-stage builds
- Security scanning
- Health checks
- Volume persistence

---

## Roadmap Futuro

### V1.1
- [ ] Refresh tokens
- [ ] 2FA integration
- [ ] OAuth providers
- [ ] Audit logs

### V1.2
- [ ] Microservices
- [ ] Redis cache
- [ ] Load balancer
- [ ] CDN integration

### V2.0
- [ ] GraphQL API
- [ ] Real-time notifications
- [ ] Advanced analytics
- [ ] Mobile apps

---

## Suporte e Documentação

### Documentação Disponível
- [Pipelines Simplificadas](./PIPELINES_SIMPLIFICADAS.md) - Detalhes completos
- [Docker Setup](./DOCKER_README.md) - Configuração Docker
- [GitHub Actions](./GITHUB_ACTIONS_README.md) - CI/CD completo

### Recursos
- [GitHub Repository](https://github.com/MarcosCatito/Teste-de-login)
- [Docker Hub](https://hub.docker.com/)
- [Issues e Suporte](https://github.com/MarcosCatito/Teste-de-login/issues)

---

## Como Contribuir

### Fluxo de Contribuição
1. Fork do repositório
2. Criar feature branch
3. Desenvolver com testes
4. Abrir Pull Request
5. Aguardar review

### Padrões de Código
- Seguir estrutura de código
- Manter testes atualizados
- Documentar mudanças
- Respeitar CI/CD

---

## Conclusão

Sistema **enterprise-ready** com:
- **Pipelines simplificadas** (apenas 2)
- **Deploy automatizado**
- **Segurança completa**
- **Documentação detalhada**
- **Docker otimizado**
- **Testes completos**

**Versão**: 2.0 - Simplificada  
**Status**: Produção Ready  
**Última Atualização**: 2026
#   T e s t e - l o g i n  
 