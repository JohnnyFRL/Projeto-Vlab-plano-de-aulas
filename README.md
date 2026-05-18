# Vlab — Plano de Aulas

API RESTful para gerenciamento de planos de aula com sugestões automáticas via Inteligência Artificial.

Projeto desenvolvido como parte do desafio técnico VLAB.

---

## Stack

- **Python 3.11**
- **Flask** — framework web
- **Flask-SQLAlchemy** — ORM para PostgreSQL
- **PostgreSQL** — banco de dados relacional
- **Marshmallow** — validação de dados
- **OpenAI API** — sugestões pedagógicas com IA
- **Docker** — containerização

---

## Arquitetura

O projeto segue uma arquitetura em camadas, com responsabilidades bem definidas:

```
routes       → apenas mapeamento de URLs
controllers  → request/response e status HTTP
services     → regras de negócio e logs
repositories → acesso ao banco de dados
models       → definição das tabelas
schemas      → validação de entrada
utils        → logger e error handlers
```

---

## Estrutura de pastas

```
Backend/
├── app/
│   ├── controllers/
│   │   └── lesson_plan_controller.py
│   ├── services/
│   │   ├── lesson_plan_service.py
│   │   └── ai_service.py
│   ├── repositories/
│   │   └── lesson_plan_repository.py
│   ├── routes/
│   │   ├── lesson_plan_routes.py
│   │   └── health_routes.py
│   ├── models/
│   │   └── lesson_plan.py
│   ├── schemas/
│   │   └── lesson_plan_schema.py
│   ├── config/
│   │   └── settings.py
│   ├── utils/
│   │   ├── logger.py
│   │   └── error_handlers.py
│   ├── app.py
│   └── extensions.py
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── run.py
```

---

## Como rodar localmente

### Pré-requisitos

- Python 3.11+
- PostgreSQL rodando localmente
- (Opcional) Chave da OpenAI para o endpoint de IA

### 1. Clone e entre na pasta

```bash
git clone <url-do-repositorio>
cd Projeto-Vlab-plano-de-aulas/Backend
```

### 2. Ative o ambiente virtual

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o .env

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais:

```
FLASK_ENV=development
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vlab_db
DB_USER=postgres
DB_PASSWORD=sua_senha
OPENAI_API_KEY=sk-sua-chave
```

### 5. Crie o banco

```bash
psql -U postgres -c "CREATE DATABASE vlab_db;"
```

### 6. Suba o servidor

```bash
python run.py
```

O servidor estará disponível em `http://localhost:5000`.

---

## Como rodar com Docker

### Pré-requisitos

- Docker Desktop instalado e rodando

### 1. Configure o .env

```bash
cp .env.example .env
# edite com suas credenciais
```

### 2. Suba os containers

```bash
docker compose up --build
```

O comando sobe o banco PostgreSQL e o backend automaticamente. Aguarde o log `Running on http://0.0.0.0:5000` antes de fazer requisições.

Para rodar em background:

```bash
docker compose up --build -d
```

Para parar:

```bash
docker compose down
```

---

## Endpoints

### Health Check

```
GET /health
```

**Resposta:**
```json
{ "status": "ok" }
```

---

### Criar plano de aula

```
POST /lesson-plans
```

**Body:**
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

**Resposta:** `201 Created`
```json
{
  "id": 1,
  "title": "Introdução ao OSPF",
  "discipline": "Redes de Computadores",
  "objective": "Compreender o funcionamento do protocolo OSPF",
  "summary": "Aula sobre roteamento dinâmico com foco em OSPF",
  "planned_date": "2025-09-15",
  "contents": "Conceitos de área, DR/BDR, métricas de custo",
  "support_resources": "Slides PDF, Cisco Packet Tracer",
  "tags": "redes,ospf,routing",
  "created_at": "2025-05-17T10:00:00"
}
```

---

### Listar planos

```
GET /lesson-plans
```

**Query params disponíveis:**

| Param | Descrição | Exemplo |
|---|---|---|
| `page` | Página atual | `?page=1` |
| `limit` | Itens por página | `?limit=10` |
| `search` | Busca por título | `?search=ospf` |
| `discipline` | Filtro por disciplina | `?discipline=Redes` |
| `tag` | Filtro por tag | `?tag=routing` |
| `planned_date` | Filtro por data | `?planned_date=2025-09-15` |
| `sort` | Ordenação | `?sort=title` |

**Resposta:** `200 OK`
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

**Resposta:** `200 OK` ou `404 Not Found`

---

### Atualizar plano

```
PUT /lesson-plans/1
```

**Body (todos os campos são opcionais):**
```json
{
  "tags": "redes,ospf,avancado",
  "contents": "Conteúdo atualizado com mais detalhes"
}
```

---

### Deletar plano

```
DELETE /lesson-plans/1
```

**Resposta:**
```json
{ "message": "Lesson plan deleted successfully." }
```

---

### Smart Assist — Sugestões com IA

```
POST /lesson-plans/ai-suggestions
```

**Body:**
```json
{
  "title": "Introdução ao OSPF",
  "discipline": "Redes",
  "summary": "Conceitos básicos de roteamento dinâmico"
}
```

**Resposta:** `200 OK`
```json
{
  "contents": [
    "Roteamento dinâmico vs estático",
    "Eleição de DR e BDR",
    "LSA e propagação de rotas",
    "Convergência OSPF"
  ],
  "recommended_tags": [
    "ospf",
    "routing",
    "redes",
    "ccna"
  ],
  "support_resources": [
    "Cisco OSPF Configuration Guide",
    "Vídeo: OSPF no Packet Tracer",
    "RFC 2328 — OSPF Version 2"
  ]
}
```

**Resposta em caso de falha:** `503 Service Unavailable`
```json
{
  "error": "Unable to generate AI suggestions right now. Please try again later."
}
```

---

## Logs

O sistema registra as principais operações no terminal:

```
2025-05-17T10:00:00 [INFO] app.services.lesson_plan_service — Lesson plan created successfully: id=1 title='Introdução ao OSPF'
2025-05-17T10:01:00 [INFO] app.services.ai_service — AI suggestion generated: Title='Introdução ao OSPF', Discipline='Redes', TokenUsage=320, Latency=1.8s
2025-05-17T10:02:00 [ERROR] app.services.ai_service — OpenAI request failed: Connection timeout
```
