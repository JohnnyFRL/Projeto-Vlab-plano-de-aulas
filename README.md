# Vlab — Sistema de Gerenciamento de Planos de Aula

Plataforma centralizada para planejamento de aulas e organização de conteúdos pedagógicos. O sistema permite o cadastro, organização e consulta de planos de aula, além de utilizar Inteligência Artificial para sugerir conteúdos complementares, tópicos relacionados e tags com base no tema da aula.

---

## Stack

**Backend**
- Python 3.11
- Flask + Flask-SQLAlchemy + Flask-CORS
- PostgreSQL
- Marshmallow (validação)
- OpenAI API (Smart Assist)

**Frontend**
- React 18
- React Router DOM
- Vite
- CSS Modules

**DevOps**
- Docker + Docker Compose
- GitHub Actions (CI com flake8 e ESLint)

---

## Arquitetura

### Backend

O backend segue uma arquitetura em camadas com responsabilidades bem definidas:

```
routes       → mapeamento de URLs e métodos HTTP
controllers  → leitura de request, status codes e response
services     → regras de negócio e logs
repositories → acesso ao banco de dados
models       → definição das tabelas (SQLAlchemy)
schemas      → validação de entrada (Marshmallow)
utils        → logger centralizado e error handlers globais
```

### Frontend

```
pages        → telas da aplicação (ListPage, FormPage)
components   → componentes reutilizáveis (Layout, Filters, PlanCard, etc.)
services     → chamadas à API do backend
hooks        → lógica de estado e fetching (usePlans)
styles       → design system global (variáveis CSS)
```

---

## Estrutura de pastas

```
Projeto-Vlab-plano-de-aulas/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Backend/
│   ├── app/
│   │   ├── controllers/
│   │   │   └── lesson_plan_controller.py
│   │   ├── services/
│   │   │   ├── lesson_plan_service.py
│   │   │   └── ai_service.py
│   │   ├── repositories/
│   │   │   └── lesson_plan_repository.py
│   │   ├── routes/
│   │   │   ├── lesson_plan_routes.py
│   │   │   └── health_routes.py
│   │   ├── models/
│   │   │   └── lesson_plan.py
│   │   ├── schemas/
│   │   │   └── lesson_plan_schema.py
│   │   ├── config/
│   │   │   └── settings.py
│   │   ├── utils/
│   │   │   ├── logger.py
│   │   │   └── error_handlers.py
│   │   ├── app.py
│   │   └── extensions.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
│
└── Frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Layout.jsx
    │   │   ├── Filters.jsx
    │   │   ├── PlanCard.jsx
    │   │   ├── Pagination.jsx
    │   │   └── Toast.jsx
    │   ├── pages/
    │   │   ├── ListPage.jsx
    │   │   └── FormPage.jsx
    │   ├── services/
    │   │   └── api.js
    │   ├── hooks/
    │   │   └── usePlans.js
    │   ├── styles/
    │   │   └── global.css
    │   ├── App.jsx
    │   └── main.jsx
    ├── eslint.config.js
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## Como rodar localmente

### Pré-requisitos

- Python 3.11+
- Node.js 20+
- PostgreSQL rodando localmente
- Chave da OpenAI (opcional — o sistema funciona sem ela, o Smart Assist retorna um fallback)

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd Projeto-Vlab-plano-de-aulas
```

### 2. Configure o Backend

```bash
cd Backend

# Ative o ambiente virtual
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais
```

Conteúdo do `.env`:
```
FLASK_ENV=development
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vlab_db
DB_USER=postgres
DB_PASSWORD=sua_senha
OPENAI_API_KEY=sk-sua-chave
```

### 3. Crie o banco de dados

```bash
psql -U postgres -c "CREATE DATABASE vlab_db;"
```

### 4. Suba o Backend

```bash
python run.py
```

Servidor disponível em `http://localhost:5000`.

### 5. Configure e suba o Frontend

Em outro terminal:

```bash
cd Frontend
npm install
npm run dev
```

Aplicação disponível em `http://localhost:3000`.

---

## Como rodar com Docker

### Pré-requisitos

- Docker Desktop instalado e rodando

### 1. Configure o .env

```bash
cd Backend
cp .env.example .env
# Edite com suas credenciais
```

### 2. Suba os containers

```bash
cd Backend
docker compose up --build
```

O comando sobe o PostgreSQL e o backend automaticamente. Aguarde a mensagem:
```
backend-1 | * Running on http://0.0.0.0:5000
```

Para rodar em background:
```bash
docker compose up --build -d
```

Para parar:
```bash
docker compose down
```

---

## Endpoints da API

### Health Check

```
GET /health
```
```json
{ "status": "ok" }
```

---

### Criar plano de aula

```
POST /lesson-plans
```

```json
{
  "title": "Introdução ao OSPF",
  "discipline": "Redes de Computadores",
  "objective": "Compreender o funcionamento do protocolo OSPF",
  "summary": "Aula sobre roteamento dinâmico com foco em OSPF",
  "planned_date": "2025-09-15",
  "contents": "Conceitos de área, DR/BDR, métricas de custo",
  "support_resources": "Slides PDF, Cisco Packet Tracer",
  "tags": "redes,ospf,routing"
}
```

Resposta: `201 Created`

---

### Listar planos

```
GET /lesson-plans
```

| Parâmetro | Descrição | Exemplo |
|---|---|---|
| `page` | Página atual | `?page=1` |
| `limit` | Itens por página | `?limit=10` |
| `search` | Busca por título | `?search=ospf` |
| `discipline` | Filtro por disciplina | `?discipline=Redes` |
| `tag` | Filtro por tag | `?tag=routing` |
| `planned_date` | Filtro por data | `?planned_date=2025-09-15` |
| `sort` | Ordenação | `?sort=title` |

Resposta:
```json
{
  "data": [...],
  "total": 20,
  "page": 1,
  "pages": 2,
  "per_page": 10
}
```

---

### Buscar plano por ID

```
GET /lesson-plans/1
```

---

### Atualizar plano

```
PUT /lesson-plans/1
```

Todos os campos são opcionais na atualização.

---

### Deletar plano

```
DELETE /lesson-plans/1
```

```json
{ "message": "Lesson plan deleted successfully." }
```

---

### Smart Assist — Sugestões com IA

```
POST /lesson-plans/ai-suggestions
```

```json
{
  "title": "Introdução ao OSPF",
  "discipline": "Redes",
  "summary": "Conceitos básicos de roteamento dinâmico"
}
```

Resposta `200 OK`:
```json
{
  "contents": [
    "Roteamento dinâmico vs estático",
    "Eleição de DR e BDR",
    "LSA e propagação de rotas"
  ],
  "recommended_tags": [
    "ospf",
    "routing",
    "redes"
  ],
  "support_resources": [
    "Cisco OSPF Configuration Guide",
    "Vídeo: OSPF no Packet Tracer",
    "RFC 2328 — OSPF Version 2"
  ]
}
```

Resposta em caso de falha `503`:
```json
{
  "error": "Unable to generate AI suggestions right now. Please try again later."
}
```

---

## Logs

O sistema registra as principais operações no terminal:

```
2025-05-17T10:00:00 [INFO]  app.services.lesson_plan_service — Lesson plan created successfully: id=1 title='Introdução ao OSPF'
2025-05-17T10:01:00 [INFO]  app.services.lesson_plan_service — Lesson plan updated successfully: id=1
2025-05-17T10:02:00 [INFO]  app.services.lesson_plan_service — Lesson plan deleted successfully: id=1
2025-05-17T10:03:00 [INFO]  app.services.ai_service — AI suggestion generated: Title='Introdução ao OSPF', Discipline='Redes', TokenUsage=320, Latency=1.8s
2025-05-17T10:04:00 [ERROR] app.services.ai_service — OpenAI request failed: Connection timeout
```

---

## CI — Integração Contínua

O projeto possui um pipeline no GitHub Actions que roda automaticamente a cada push ou pull request na branch `main`.

**Jobs:**
- `lint-backend` — roda o `flake8` no código Python do Backend
- `lint-frontend` — roda o `eslint` no código React do Frontend

O status aparece diretamente na aba **Actions** do repositório.