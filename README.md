<<<<<<< HEAD
# 📦 FileVault API

API de armazenamento de arquivos com metadados, construída para uso em ambiente local (self-hosted), com upload, download e listagem de arquivos.

---

## 🧱 Stack

| Camada          | Tecnologia |
|-----------------|------------|
| Backend         | Python 3.11 |
| Framework       | FastAPI |
| Banco de dados  | PostgreSQL |
| Storage         | Sistema de arquivos local |
| Autenticação    | Bearer Token (simples) |
| Deploy externo  | Cloudflare Tunnel |

---

## 🧭 Arquitetura

```
APP → Cloudflare Tunnel → API → PostgreSQL + Storage local
```

---

## 📁 Estrutura de pastas

```
filevault/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── controllers/
│   │   └── files_controller.py
│   ├── services/
│   │   └── file_service.py
│   ├── repositories/
│   │   └── file_repository.py
│   └── utils/
│       └── security.py
│
├── uploads/
├── init.sql
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🗄️ Banco de dados

```sql
CREATE TABLE files (
  id UUID PRIMARY KEY,
  filename TEXT,
  path TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Autenticação

Todas as requisições exigem:

Authorization: Bearer <TOKEN>

Configuração no .env:

AUTH_TOKEN=meu-token-secreto

---

## 📡 Endpoints

### 📤 Upload de arquivo

POST /upload

Form-data:
- file: arquivo

---

### 📄 Listar arquivos

GET /files

---

### 📥 Download de arquivo

GET /files/{id}

---

## ⚙️ Configuração (.env)

DB_HOST=localhost
DB_PORT=5432
DB_NAME=filesdb
DB_USER=postgres
DB_PASSWORD=postgres

UPLOAD_DIR=./uploads
AUTH_TOKEN=meu-token-secreto

---

## ▶️ Como rodar

### 🐳 Docker (recomendado)

docker-compose up --build

API disponível em:
http://localhost:8000

---

### 💻 Local (sem Docker)

pip install -r requirements.txt
uvicorn app.main:app --reload

---

## 📂 Storage

Arquivos são armazenados em:

/uploads

Formato:

<uuid>.<extensão>

---

## 🌐 Cloudflare Tunnel

cloudflared tunnel create filevault
cloudflared tunnel route dns filevault api.seudominio.com
cloudflared tunnel run filevault

---

## ⚠️ Regras do sistema

- Upload máximo: 10MB
- Consistência entre arquivo e banco
- Falha no banco → arquivo é removido
- API protegida por token fixo

---

## 🎯 Objetivo

MVP simples para:

- Upload de arquivos
- Integração API + PostgreSQL + filesystem
- Uso em VM local (self-hosted)
- Exposição via Cloudflare Tunnel

---

## 🚀 Melhorias futuras

- Interface web
- Versionamento de arquivos
- Logs estruturados
- Rate limiting
- Preview de arquivos
- CDN
=======
# 🌊 Agente Mirim — API Backend

API REST para o aplicativo **Agente Mirim**, desenvolvida em Python com FastAPI.
Responsável por armazenar arquivos de mídia (imagens, vídeos, PDFs) e fornecer
dados de missões, conteúdos e medalhas para o app Android.

---

## 🧱 Stack

| Camada       | Tecnologia          |
|--------------|---------------------|
| Backend      | Python 3.11         |
| Framework    | FastAPI + Uvicorn   |
| Banco        | PostgreSQL 15       |
| Storage      | Filesystem local    |
| Auth         | Bearer Token fixo   |
| Deploy       | Cloudflare Tunnel   |

---

## 📁 Estrutura de pastas

```
agentemirim-api/
├── app/
│   ├── main.py                  # Entry point da aplicação
│   ├── config.py                # Configurações via .env
│   ├── database.py              # Conexão async com PostgreSQL
│   ├── models/
│   │   ├── file_model.py        # Tabela: files
│   │   ├── content_model.py     # Tabela: contents
│   │   ├── mission_model.py     # Tabela: missions
│   │   └── medal_model.py       # Tabela: medals
│   ├── controllers/
│   │   ├── files_controller.py
│   │   ├── contents_controller.py
│   │   ├── missions_controller.py
│   │   └── medals_controller.py
│   ├── services/
│   │   ├── file_service.py
│   │   ├── content_service.py
│   │   ├── mission_service.py
│   │   └── medal_service.py
│   ├── repositories/
│   │   ├── file_repository.py
│   │   ├── content_repository.py
│   │   ├── mission_repository.py
│   │   └── medal_repository.py
│   └── utils/
│       └── security.py
├── uploads/
├── init.sql
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🗄️ Banco de dados

```sql
-- Arquivos de mídia
files (id, filename, path, content_type, size_bytes, created_at)

-- Conteúdos educativos
contents (id, title, description, file_id, order_index, category, created_at)

-- Missões
missions (id, title, description, difficulty, points, order_index, created_at)

-- Medalhas
medals (id, name, description, image_url, condition, created_at)
```

---

## 📡 Endpoints

### 🔐 Autenticação
Todas as rotas exigem o header:
```
Authorization: Bearer <AUTH_TOKEN>
```

### 📤 Arquivos
| Método | Rota            | Descrição              |
|--------|-----------------|------------------------|
| POST   | /upload         | Faz upload de arquivo  |
| GET    | /files          | Lista todos os arquivos|
| GET    | /files/{id}     | Download do arquivo    |
| DELETE | /files/{id}     | Remove arquivo         |

### 📚 Conteúdos
| Método | Rota               | Descrição                    |
|--------|--------------------|------------------------------|
| GET    | /contents          | Lista conteúdos (com filtro) |
| GET    | /contents/{id}     | Detalhe de um conteúdo       |
| POST   | /contents          | Cria novo conteúdo           |
| PUT    | /contents/{id}     | Atualiza conteúdo            |
| DELETE | /contents/{id}     | Remove conteúdo              |

### 🎯 Missões
| Método | Rota               | Descrição            |
|--------|--------------------|----------------------|
| GET    | /missions          | Lista missões        |
| GET    | /missions/{id}     | Detalhe da missão    |
| POST   | /missions          | Cria missão          |
| PUT    | /missions/{id}     | Atualiza missão      |
| DELETE | /missions/{id}     | Remove missão        |

### 🏅 Medalhas
| Método | Rota             | Descrição           |
|--------|------------------|---------------------|
| GET    | /medals          | Lista medalhas      |
| GET    | /medals/{id}     | Detalhe da medalha  |
| POST   | /medals          | Cria medalha        |

---

## ▶️ Como rodar

### 🐳 Docker (recomendado)
```bash
cp .env.example .env
# edite o .env se necessário
docker-compose up --build
```
API disponível em: `http://localhost:8000`
Docs interativas: `http://localhost:8000/docs`

### 💻 Local (sem Docker)
```bash
pip install -r requirements.txt
cp .env.example .env
# certifique-se que o PostgreSQL está rodando e a tabela criada (init.sql)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 Exemplos de requisição (curl)

```bash
TOKEN="meu-token-secreto"
BASE="http://localhost:8000"

# Upload de arquivo
curl -X POST "$BASE/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@imagem_enchente.jpg"

# Listar arquivos
curl "$BASE/files" -H "Authorization: Bearer $TOKEN"

# Download de arquivo
curl "$BASE/files/<uuid>" -H "Authorization: Bearer $TOKEN" -O

# Criar conteúdo
curl -X POST "$BASE/contents" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Enchentes","description":"O que fazer em enchentes","category":"enchentes","order_index":1}'

# Listar missões
curl "$BASE/missions" -H "Authorization: Bearer $TOKEN"

# Listar medalhas
curl "$BASE/medals" -H "Authorization: Bearer $TOKEN"
```

---

## 🌐 Cloudflare Tunnel

```bash
cloudflared tunnel create agentemirim
cloudflared tunnel route dns agentemirim api.agentemirim.com
cloudflared tunnel run agentemirim
```

---

## ⚠️ Regras do sistema

- Upload máximo: **10 MB**
- Tipos permitidos: `jpg, jpeg, png, gif, mp4, pdf`
- Falha no banco → arquivo removido do disco automaticamente
- Token fixo via `.env` (trocar antes de produção)

---

## 🚀 Próximos passos (integração com o app)

1. Configurar `AUTH_TOKEN` no Android (BuildConfig ou SharedPreferences)
2. Usar `Retrofit` para consumir os endpoints
3. Substituir dados mockados do Firestore pelos endpoints `/contents` e `/missions`
4. Fazer upload de mídias via `POST /upload` antes de criar um conteúdo
>>>>>>> 080f082 (Primeiro commit)
