# Projeto VLAB — Backend

API RESTful para gerenciamento de planos de aula com sugestões via IA.

---

## Requisitos

- Python 3.11+
- PostgreSQL rodando localmente
- Chave da OpenAI (para o endpoint de IA)

---

## Como rodar

### 1. Ative o ambiente virtual

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o .env

Copie o `.env.example` para `.env` e preencha:

```
FLASK_ENV=development
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vlab_db
DB_USER=postgres
DB_PASSWORD=sua_senha
OPENAI_API_KEY=sk-sua-chave
```

### 4. Crie o banco de dados (se não existir)

```bash
psql -U postgres -c "CREATE DATABASE vlab_db;"
```

### 5. Suba o servidor

```bash
python run.py
```

O servidor sobe em `http://localhost:5000`.

---

## Endpoints

### Health check
```
GET /health
```

---

### Criar plano
```
POST /lesson-plans
Content-Type: application/json

{
  "title": "Introdução ao OSPF",
  "discipline": "Redes de Computadores",
  "objective": "Entender o funcionamento do protocolo OSPF",
  "summary": "Aula sobre roteamento dinâmico com foco em OSPF",
  "planned_date": "2025-09-15",
  "contents": "Conceitos de área, DR/BDR, métricas",
  "support_resources": "Slides PDF, Cisco Packet Tracer",
  "tags": "redes,ospf,routing"
}
```

---

### Listar planos (com filtros, busca, paginação, ordenação)
```
GET /lesson-plans
GET /lesson-plans?page=1&limit=5
GET /lesson-plans?search=ospf
GET /lesson-plans?discipline=Redes
GET /lesson-plans?tag=routing
GET /lesson-plans?planned_date=2025-09-15
GET /lesson-plans?sort=title
GET /lesson-plans?discipline=Redes&tag=ospf&search=OSPF
```

Resposta:
```json
{
  "data": [...],
  "total": 12,
  "page": 1,
  "pages": 3,
  "per_page": 5
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
Content-Type: application/json

{
  "tags": "redes,ospf,avancado",
  "contents": "Conteúdo atualizado"
}
```

---

### Deletar plano
```
DELETE /lesson-plans/1
```

---

### Sugestões com IA (Smart Assist)
```
POST /lesson-plans/ai-suggestions
Content-Type: application/json

{
  "title": "Introdução ao OSPF",
  "discipline": "Redes",
  "summary": "Conceitos básicos de roteamento dinâmico"
}
```

Resposta:
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

---

## Estrutura do projeto

```
backend/
├── app/
│   ├── controllers/        # request/response, status codes
│   ├── services/           # regra de negócio + IA
│   ├── repositories/       # acesso ao banco
│   ├── routes/             # apenas rotas
│   ├── models/             # modelos SQLAlchemy
│   ├── schemas/            # validação marshmallow
│   ├── config/             # configurações de ambiente
│   ├── app.py              # App Factory
│   └── extensions.py       # db, cors
├── .env
├── .env.example
├── requirements.txt
└── run.py
```
