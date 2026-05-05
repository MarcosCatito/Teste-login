# GitHub Actions Setup Guide

## 🚀 CI/CD Pipeline Configuration

Este projeto inclui uma configuração completa de GitHub Actions para automação de testes, qualidade de código, segurança e deploy.

---

## 📁 Estrutura dos Workflows

```
.github/workflows/
├── backend-ci.yml          # CI para Backend Flask
├── frontend-ci.yml         # CI para Frontend React
├── deploy.yml              # Deploy para Produção/Staging
├── security.yml            # Scans de Segurança
├── code-quality.yml        # Qualidade de Código
└── integration-tests.yml   # Testes de Integração
```

---

## 🔧 Configuração dos Workflows

### 1. Backend CI (`backend-ci.yml`)

**Triggers:**
- Push para branches: `main`, `develop`, `feature/*`
- Pull Requests para: `main`, `develop`
- Mudanças em: `backend/**`

**Jobs:**
- **test**: Testes unitários, linting, formatação
- **security-scan**: Safety e Bandit scans
- **build-docker**: Build e push de imagem Docker

### 2. Frontend CI (`frontend-ci.yml`)

**Triggers:**
- Push para branches: `main`, `develop`, `feature/*`
- Pull Requests para: `main`, `develop`
- Mudanças em: `frontend/**`

**Jobs:**
- **test**: Testes unitários, ESLint, build
- **security-scan**: npm audit, Snyk scan
- **build-docker**: Build e push de imagem Docker
- **performance-test**: Lighthouse CI

### 3. Deploy (`deploy.yml`)

**Triggers:**
- Push para `main`
- Manual workflow dispatch

**Jobs:**
- **test-and-deploy**: Build, deploy, smoke tests
- **rollback**: Rollback automático em caso de falha

### 4. Security (`security.yml`)

**Triggers:**
- Schedule diário (2 AM UTC)
- Push para `main`
- Pull Requests para `main`

**Jobs:**
- **security-scan**: Trivy vulnerability scanner
- **backend-security**: Safety e Bandit
- **frontend-security**: npm audit
- **dependency-check**: OWASP Dependency Check
- **secrets-scan**: TruffleHog e Gitleaks

### 5. Code Quality (`code-quality.yml`)

**Triggers:**
- Push para `main`, `develop`
- Pull Requests para `main`, `develop`

**Jobs:**
- **backend-quality**: Black, isort, flake8, mypy
- **frontend-quality**: ESLint, Prettier, bundle size
- **documentation-check**: Build de documentação
- **performance-benchmark**: Testes de performance

### 6. Integration Tests (`integration-tests.yml`)

**Triggers:**
- Push para `main`, `develop`
- Pull Requests para `main`, `develop`

**Jobs:**
- **setup-test-environment**: Setup do ambiente Docker
- **api-integration-tests**: Testes de API
- **e2e-tests**: Playwright E2E tests
- **load-tests**: Locust load tests
- **cleanup**: Limpeza do ambiente
- **notify-results**: Notificação de resultados

---

## 🔐 Configuração de Secrets

### Secrets Necessários no GitHub

```bash
# Docker Hub
DOCKER_USERNAME=seu_usuario_docker
DOCKER_PASSWORD=sua_senha_docker

# Deploy Servers
STAGING_HOST=seu_staging_host
STAGING_USER=seu_staging_user
STAGING_SSH_KEY=sua_chave_ssh_staging

PRODUCTION_HOST=seu_production_host
PRODUCTION_USER=seu_production_user
PRODUCTION_SSH_KEY=sua_chave_ssh_production

# Security Scans
SNYK_TOKEN=seu_snyk_token
GITLEAKS_LICENSE=sua_licensa_gitleaks

# Notificações
SLACK_WEBHOOK=seu_slack_webhook
```

### Como Configurar Secrets:

1. Vá para o repositório no GitHub
2. Settings → Secrets and variables → Actions
3. Clique "New repository secret"
4. Adicione cada secret acima

---

## 🚀 Como Usar

### 1. Ativação Automática

Os workflows são ativados automaticamente quando:
- Faz push para as branches configuradas
- Abre pull requests
- Agendamento (security scans)

### 2. Deploy Manual

Para deploy manual:

1. Vá para Actions tab
2. Selecione "Deploy to Production"
3. Clique "Run workflow"
4. Escolha o ambiente (staging/production)

### 3. Monitoramento

- **Actions tab**: Ver status dos workflows
- **Security tab**: Ver vulnerabilidades encontradas
- **Insights**: Ver métricas de CI/CD

---

## 📊 Relatórios e Artefatos

### Relatórios Gerados

- **Coverage Reports**: Codecov integration
- **Security Reports**: Trivy, Safety, Bandit
- **Quality Reports**: ESLint, Prettier, Black
- **Performance Reports**: Lighthouse, Locust
- **E2E Reports**: Playwright HTML reports

### Artefatos

- **Test results**: XML e JSON reports
- **Coverage data**: HTML e XML
- **Security scans**: SARIF files
- **Build artifacts**: Docker images

---

## 🔧 Configuração Local

### Testes Locais

```bash
# Backend tests
cd backend
python -m pytest test_security.py -v --cov=.

# Frontend tests
cd frontend
npm test -- --coverage --watchAll=false

# Integration tests
docker-compose -f docker-compose.test.yml up -d
python integration_tests.py
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Docker Build Falha
```bash
# Limpar cache Docker
docker system prune -a
docker-compose build --no-cache
```

#### 2. Testes Timeout
```yaml
# Aumentar timeout nos workflows
timeout-minutes: 30
```

#### 3. Secrets Não Encontrados
```bash
# Verificar se secrets existem
gh secret list
```

#### 4. Permissões SSH
```bash
# Gerar chave SSH correta
ssh-keygen -t rsa -b 4096 -C "github-actions"
```

---

## 📈 Métricas e Monitoramento

### KPIs do Pipeline

- **Build Time**: Tempo médio de build
- **Test Coverage**: Percentual de cobertura
- **Security Score**: Pontuação de segurança
- **Performance Score**: Pontuação de performance
- **Success Rate**: Taxa de sucesso dos deploys

### Dashboard

Configurar dashboard para monitorar:
- GitHub Actions insights
- Codecov coverage
- Security alerts
- Performance metrics

---

## 🔄 Fluxo de Trabalho

### Branch Strategy

```
main (produção)
├── develop (desenvolvimento)
│   ├── feature/login-improvements
│   ├── feature/security-enhancements
│   └── feature/ui-updates
└── hotfix/critical-bug-fix
```

### Processo

1. **Feature Branch**: Criar branch a partir de `develop`
2. **Development**: Desenvolver com testes locais
3. **PR**: Abrir PR para `develop`
4. **CI**: Rodar testes automáticos
5. **Review**: Code review manual
6. **Merge**: Merge para `develop`
7. **Release**: Merge para `main` (deploy automático)

---

## 🚀 Best Practices

### 1. Performance

- Usar caches de dependências
- Paralelizar jobs quando possível
- Otimizar Docker builds
- Usar actions reutilizáveis

### 2. Segurança

- Usar secrets para dados sensíveis
- Scans de segurança regulares
- Dependências atualizadas
- Reviews de segurança

### 3. Qualidade

- Testes unitários e de integração
- Code coverage mínimo 80%
- Linting e formatação automática
- Documentação atualizada

### 4. Monitoramento

- Logs detalhados
- Notificações de falhas
- Métricas de performance
- Alertas críticos

---

## 📝 Exemplos de Uso

### 1. Adicionar Novo Workflow

```yaml
name: Custom Workflow
on: [push, pull_request]
jobs:
  custom-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Custom step
        run: echo "Custom workflow"
```

### 2. Configurar Cache

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### 3. Notificações

```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 🆘 Suporte

### Recursos

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub](https://hub.docker.com/)
- [Codecov](https://codecov.io/)
- [Snyk](https://snyk.io/)

### Comunidade

- GitHub Community Forum
- Stack Overflow
- Discord communities

---

**Versão**: 1.0  
**Last Updated**: 2026  
**Compatible**: GitHub Actions (latest)
