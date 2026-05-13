# FixDAuto - Estrutura & Arquitetura

## 📁 Estrutura do Projeto

```
FixDAuto/
├── FixDAuto-BE/        → Spring Boot (Java 11) | Port 8080
├── FixDAuto-FE/        → React + Vite (TypeScript) | Port 5173
├── fixdauto-ai/        → FastAPI (Python) | Port 5000
└── scripts/            → Deploy & utilidades
```

## 🏗️ Arquitetura

```
┌─────────────┐  REST  ┌─────────────┐  REST  ┌──────────┐
│ Frontend    │◄──────►│ Backend     │◄──────►│ IA/ML    │
│ (React)     │        │ (Spring)    │        │ (Python) │
└─────────────┘        └─────────────┘        └──────────┘
       │                       │                    │
       └───────────────────────┼────────────────────┘
                               ▼
                    ┌──────────────────┐
                    │ SQL Server/H2    │
                    │ Redis (Cache)    │
                    └──────────────────┘
```

## 🗄️ Backend - Pacotes Java

| Pacote | Função |
|--------|--------|
| `controller/` | Endpoints HTTP REST |
| `service/` | Lógica de negócio |
| `repository/` | Acesso a dados (JPA) |
| `domain/` | Entidades (tabelas DB) |
| `dto/` | Objetos de transferência |
| `config/` | Configurações Spring |
| `security/` | JWT & autenticação |

## 🗃️ Base de Dados

Tabelas principais:
- **users** → Utilizadores (mechanic, supplier, admin)
- **companies** → Oficinas e fornecedores
- **vehicles** → Veículos
- **work_orders** → Ordens de trabalho
- **quotes** → Orçamentos
- **conversations** → Chat (receptionist/mechanic)
- **answers** → Respostas em conversas


