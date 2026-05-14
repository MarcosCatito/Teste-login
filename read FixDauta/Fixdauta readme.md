# FixDAuto - Estrutura do Projeto

Este documento descreve em maior detalhe a organização do código, a arquitetura, a base de dados e os níveis de estrutura do projeto FixDAuto.
É uma documentação para ajudar a visualizar o fluxo completo e os pontos de integração.

## 1. Visão geral da arquitetura

- `FixDAuto-FE/` → frontend React + Vite
- `FixDAuto-BE/` → backend Spring Boot Java
- `fixdauto-ai/` → serviço AI/ML em Python FastAPI
- `scripts/` → utilitários de deploy e configuração

Fluxo principal:

Frontend → Backend → Banco de Dados
              ↘
               IA/ML



### Objetivo da arquitetura

- O **frontend** é a interface do usuário e chama o backend via API.
- O **backend** processa regras de negócio, autenticação, validações e persistência.
- O **IA/ML** oferece suporte inteligente para chat e diagnósticos.
- O **banco de dados** guarda usuários, ordens, veículos, orçamentos e conversas.

## 2. Estrutura de pastas do projeto

### 2.1 FixDAuto-BE

- `src/main/java/com/fix/dauto/controller/` → endpoints REST que expõem a API para o frontend
- `src/main/java/com/fix/dauto/service/` → lógica de negócio que orquestra operações
- `src/main/java/com/fix/dauto/repository/` → interfaces JPA para leitura e escrita no banco
- `src/main/java/com/fix/dauto/domain/` → entidades JPA que representam tabelas
- `src/main/java/com/fix/dauto/dto/` → objetos de transferência de dados JSON
- `src/main/java/com/fix/dauto/config/` → configurações do Spring, CORS, OpenAPI, cache, etc.
- `src/main/java/com/fix/dauto/security/` → JWT, filtros e detalhes de autenticação
- `src/test/java/com/fix/dauto/` → testes unitários e de integração

### 2.2 FixDAuto-FE

- `src/` → código fonte React, páginas, componentes, rotas e estilos
- `src/utils/` → helpers, constantes e configurações de API
- `src/services/` → chamadas HTTP para o backend
- `package.json` → dependências, scripts e configurações do frontend

### 2.3 fixdauto-ai

- `app/` → código FastAPI, endpoints, modelos e lógica de IA/ML
- `requirements.txt` → dependências Python do serviço de IA
- `Dockerfile` e `docker-compose` → execução do serviço em container
- `scripts/` e `deploy/` → comandos de treino, monitoramento e deploy

### 2.4 Ambientação

- `docker-compose.local.yml` → orquestração local de frontend, backend, banco e IA
- `docker-compose.prod.yml` → orquestração para produção
- `README.md` da raiz → visão geral do projeto

## 3. Níveis de estrutura do sistema

### Nível 1: grandes blocos

- Frontend
- Backend
- Banco de Dados
- IA/ML

### Nível 2: camadas internas por bloco

#### Backend
- Controller
- Service
- Repository
- Domain
- Security

#### Frontend
- UI/Páginas
- Componentes
- Serviços/API
- Utilitários

#### IA/ML
- Endpoints
- Modelos
- Treino e dados

### Nível 3: módulos principais

#### Backend (exemplos)
- `WorkOrderController`
- `UserService`
- `AnswerRepository`
- `Vehicle`
- `QuoteDTO`

#### Frontend (exemplos)
- `pages/WorkOrders`
- `components/WorkOrderForm`
- `services/apiWorkOrder.ts`
- `utils/apiBaseUrl.ts`

#### IA/ML (exemplos)
- `app/api/chat.py`
- `app/data/embeddings.py`
- `app/models/solution_option.py`

### Nível 4-1: fluxos específicos

Aqui estão casos de uso e fluxo de dados detalhados:

- Login
- Criação de ordem de serviço
- Consulta de peças
- Comunicação de chat mecânico
- Geração de orçamento
- Requisição de sugestão AI

#### Exemplo de fluxo: criação de ordem de serviço

1. Frontend envia POST para o backend em `WorkOrderController`
2. Backend valida os dados em `WorkOrderService`
3. Service persiste no banco via `WorkOrderRepository`
4. Se necessário, chama IA/ML para sugestão de solução
5. Backend retorna resposta ao frontend

#### Exemplo de fluxo: chat AI

1. Frontend envia mensagem de chat para o backend
2. Backend processa e chama o serviço IA/ML
3. IA responde com diagnóstico ou solução
4. Backend salva a conversa no banco
5. Frontend exibe a resposta ao usuário

## 4. Base de dados e entidades principais

### Tipos de banco usados
- `SQL Server` para produção
- `H2` para desenvolvimento e testes locais

### Entidades principais

- `User` / `Company` → contas, perfis e empresas
- `Vehicle` → informações do veículo e compatibilidade
- `WorkOrder` → ordens de serviço, status e histórico
- `Quote` → orçamentos, itens e valores
- `Conversation` / `Answer` → chat e respostas automatizadas
- `SolutionOption` → alternativas de solução com inteligência

### Relações básicas

- `User` pertence a `Company`
- `WorkOrder` refere `Vehicle`, `User` e `Company`
- `Quote` pertence a `WorkOrder`
- `Conversation` contém `Answer`
- `SolutionOption` está ligado ao `WorkOrder` e ao chat

## 5. Como executar o projeto

### Com Docker Compose
```bash
cd FixDAuto-main
docker-compose -f docker-compose.local.yml up --build
```

### Manualmente
```bash
cd FixDAuto-BE
mvn clean install
mvn spring-boot:run
```

```bash
cd FixDAuto-FE
npm install
npm run dev
```

```bash
cd fixdauto-ai
pip install -r requirements.txt
./start_dashboard.sh
```

## 6. Rede de dependências e responsabilidades

- O frontend nunca acessa o banco diretamente.
- O backend é o único ponto que fala com o banco.
- O backend também consome o serviço IA/ML.
- O AI/ML processa dados e devolve respostas inteligentes para o backend.

## 7. Desenho do diagrama

Para um desenho visual (papel, draw.io ou diagrams.net), use estas camadas:

1. `Frontend`
2. `Backend`
3. `Banco de Dados`
4. `Serviço AI/ML`

E conecte-as assim:

- Frontend → Backend
- Backend → Banco de Dados
- Backend → IA/ML

Você pode adicionar sub-blocos dentro do backend para:
- Controllers
- Services
- Repositories
- Domain

## 8. Conclusão

A estrutura do projeto é clara e modular:
- Camada de apresentação: `FixDAuto-FE`
- Camada de aplicação: `FixDAuto-BE`
- Camada inteligente: `fixdauto-ai`
- Persistência: `SQL Server / H2`

Esta documentação detalhada ajuda a ver os níveis 1, 2, 3 e 4-1 do sistema e facilita a criação de diagramas e mapas arquiteturais.
