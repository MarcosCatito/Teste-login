# Sistema de login simples e registo

Este Projeto A consistio numa aplicação web simples de login e registo, com backend em Flask e frontend em React. Pode conter alguns erros e até algumas funções podem não funcionar correctamente. 

Já foram implementadas algumas alterações ao código original, como por exemplo a adição de um sistema de segurança mais robusto, com proteção contra ataques comuns, validação de inputs, rate limiting e brute force protection.

# Para a sua excução

É necessário ter o Python e o Node.js instalados no computador.
É executado por meio do app.py.

# Alterações novas ao ficheiro 


Este projeto é um sistema completo de login e registro com as seguintes características:

- **Frontend**: React com componentes modulares
- **Backend**: Flask com SQLite
- **Segurança**: Múltiplas camadas de proteção
- **Testes**: Cobertura completa com Jest
- **Arquitetura**: Componentes separados e reutilizáveis

### Funcionalidades Principais
- ✅ Registro de novos usuários
- ✅ Login de usuários existentes
- ✅ Página de sucesso personalizada
- ✅ Sistema de tokens JWT
- ✅ Proteção contra ataques comuns
- ✅ Validação de inputs
- ✅ Rate limiting e brute force protection

---

## 🏗️ Arquitetura do Sistema

```
Teste-login/
├── frontend/                 # Aplicação React
│   ├── src/
│   │   ├── components/       # Componentes modulares
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── SuccessPage.js
│   │   │   └── styles.css
│   │   ├── App.js           # Componente principal
│   │   └── App.test.js      # Testes de integração
│   └── package.json
├── backend/                  # Aplicação Flask
│   ├── app.py               # Aplicação principal
│   ├── database.py          # Operações DB
│   ├── security.py          # Módulo de segurança
│   ├── migrate.py           # Migrações
│   ├── view_db.py           # Visualização DB
│   ├── test_security.py     # Testes de segurança
│   └── templates/           # Templates HTML
└── DOCUMENTACAO_PROJETO.md  # Este documento
```

---