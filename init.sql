-- ============================================================
-- Agente Mirim — Script de inicialização do banco de dados
-- Versão 2.0.0 — somente armazenamento de arquivos
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS files (
    id           UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    filename     TEXT    NOT NULL,
    path         TEXT    NOT NULL,
    content_type TEXT    NOT NULL DEFAULT 'application/octet-stream',
    size_bytes   BIGINT  NOT NULL DEFAULT 0,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
