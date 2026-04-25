# 🌊 Agente Mirim — API de Arquivos v2.0

API REST para o aplicativo **Agente Mirim** — educação sobre prevenção de desastres naturais.
Responsável por armazenar e servir arquivos de mídia (imagens, vídeos, PDFs).

---

## 🧱 Stack

| Camada    | Tecnologia              |
|-----------|-------------------------|
| Backend   | Python 3.11 + FastAPI   |
| Banco     | PostgreSQL 15           |
| Storage   | Filesystem local        |
| Auth      | Bearer Token (seguro)   |
| Deploy    | Docker + Cloudflare Tunnel |

---

## 📁 Estrutura

```
app/
├── main.py                  # Entry point
├── config.py                # Configurações (.env)
├── database.py              # Conexão PostgreSQL async
├── models/models.py         # Tabela: files
├── repositories/repository.py
├── services/service.py
├── controllers/controller.py
└── utils/security.py        # Autenticação Bearer (timing-safe)
```

---

## 📡 Endpoints

| Método   | Rota              | Descrição                    | Auth |
|----------|-------------------|------------------------------|------|
| `GET`    | `/health`         | Health check                 | ❌   |
| `POST`   | `/files/upload`   | Upload de arquivo            | ✅   |
| `GET`    | `/files/`         | Lista todos os arquivos      | ✅   |
| `GET`    | `/files/{id}`     | Download de arquivo por ID   | ✅   |
| `DELETE` | `/files/{id}`     | Remove arquivo               | ✅   |

### 🔐 Autenticação
```
Authorization: Bearer <AUTH_TOKEN>
```

### 📎 Tipos de arquivo aceitos
`jpg` · `jpeg` · `png` · `gif` · `webp` · `mp4` · `pdf`

---

## ▶️ Como rodar

```bash
cp .env.example .env
# edite AUTH_TOKEN e DB_PASSWORD no .env
docker compose up --build -d
```

API: `http://localhost:8000`
Docs: `http://localhost:8000/docs`

---

## ⚙️ Variáveis de ambiente (.env)

| Variável        | Descrição                          | Padrão         |
|-----------------|------------------------------------|----------------|
| `DB_HOST`       | Host do PostgreSQL                 | `db`           |
| `DB_PORT`       | Porta do PostgreSQL                | `5432`         |
| `DB_NAME`       | Nome do banco                      | `agentemirim_db` |
| `DB_USER`       | Usuário do banco                   | `postgres`     |
| `DB_PASSWORD`   | Senha do banco                     | —              |
| `UPLOAD_DIR`    | Diretório de uploads               | `/data/uploads`|
| `AUTH_TOKEN`    | Token de autenticação (mín. 16 chars) | —           |
| `MAX_UPLOAD_MB` | Limite de upload em MB (0 = sem limite) | `0`       |

---

## 🧪 Exemplos curl

```bash
BASE="https://api.digitalvs.com.br"
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

---

## 🔐 Segurança implementada

- Comparação de token com `secrets.compare_digest` (proteção contra timing attack)
- Validação de extensão de arquivo na inicialização
- Validação de arquivo vazio
- Rollback automático: se o banco falhar após salvar no disco, o arquivo é removido
- API não sobe se `AUTH_TOKEN` não estiver configurado ou for menor que 16 chars
- Handler global para erros 500 (não expõe stack trace)

---

## 🗄️ Banco de dados

```sql
CREATE TABLE files (
    id           UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    filename     TEXT    NOT NULL,
    path         TEXT    NOT NULL,
    content_type TEXT    NOT NULL DEFAULT 'application/octet-stream',
    size_bytes   BIGINT  NOT NULL DEFAULT 0,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```
