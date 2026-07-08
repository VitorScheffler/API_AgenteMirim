# 🌊 Agente Mirim — API de Arquivos

API REST para o app **Agente Mirim** — armazena e serve arquivos de mídia (imagens, vídeos, PDFs).

---

## 🧱 Stack

| Camada  | Tecnologia            |
|---------|-----------------------|
| Backend | Python 3.11 + FastAPI |
| Banco   | PostgreSQL 15         |
| Storage | Filesystem local      |
| Auth    | Bearer Token          |
| Deploy  | Docker + Cloudflare   |

---

## 📁 Estrutura

```
app/
├── __init__.py
├── config.py      # Variáveis de ambiente
├── database.py    # Conexão + model File
├── controller.py  # Endpoints (upload, listar, download, deletar)
├── security.py    # Autenticação Bearer Token
└── main.py        # Inicialização FastAPI
```

---

## 📡 Endpoints

| Método   | Rota              | Descrição              | Auth |
|----------|-------------------|------------------------|------|
| GET      | `/health`         | Health check           | ❌   |
| POST     | `/files/upload`   | Upload de arquivo      | ✅   |
| GET      | `/files/`         | Listar arquivos        | ✅   |
| GET      | `/files/{id}`     | Download por ID        | ✅   |
| DELETE   | `/files/{id}`     | Remover arquivo        | ✅   |

### Autenticação
```
Authorization: Bearer <AUTH_TOKEN>
```

### Tipos aceitos
`jpg` · `jpeg` · `png` · `gif` · `webp` · `mp4` · `pdf`

---

## ▶️ Como rodar

```bash
# 1. Copiar e editar o .env
cp .env.example .env

# 2. Subir os containers
docker compose up --build -d

# 3. Acessar
# API:  http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## ⚙️ Variáveis de ambiente (.env)

| Variável        | Descrição                             | Padrão           |
|-----------------|---------------------------------------|------------------|
| `DB_HOST`       | Host do PostgreSQL                    | `db`             |
| `DB_PORT`       | Porta do PostgreSQL                   | `5432`           |
| `DB_NAME`       | Nome do banco                         | `agentemirim_db` |
| `DB_USER`       | Usuário do banco                      | `postgres`       |
| `DB_PASSWORD`   | Senha do banco                        | —                |
| `UPLOAD_DIR`    | Diretório de uploads                  | `/data/uploads`  |
| `AUTH_TOKEN`    | Token de autenticação (mín. 16 chars) | —                |
| `MAX_UPLOAD_MB` | Limite de upload em MB (0 = sem limite) | `0`            |

---

## 🧪 Exemplos curl

```bash
BASE="https://sua-api.com"
TOKEN="seu-token-aqui"

# Upload
curl -X POST "$BASE/files/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@imagem.jpg"

# Listar
curl "$BASE/files/" \
  -H "Authorization: Bearer $TOKEN"

# Download
curl "$BASE/files/<uuid>" \
  -H "Authorization: Bearer $TOKEN" -O

# Remover
curl -X DELETE "$BASE/files/<uuid>" \
  -H "Authorization: Bearer $TOKEN"
```
