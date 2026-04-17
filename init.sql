-- ============================================================
-- Agente Mirim — Script de inicialização do banco de dados
-- ============================================================

-- Extensão para UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ------------------------------------------------------------
-- Tabela: files (arquivos de mídia)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS files (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename     TEXT        NOT NULL,
    path         TEXT        NOT NULL,
    content_type TEXT        NOT NULL DEFAULT 'application/octet-stream',
    size_bytes   BIGINT      NOT NULL DEFAULT 0,
    created_at   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Tabela: contents (conteúdos educativos)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS contents (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT        NOT NULL,
    description TEXT        NOT NULL,
    category    TEXT        NOT NULL DEFAULT 'geral',
    order_index INTEGER     NOT NULL DEFAULT 0,
    file_id     UUID        REFERENCES files(id) ON DELETE SET NULL,
    created_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Tabela: missions (missões educativas)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS missions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT        NOT NULL,
    description TEXT        NOT NULL,
    difficulty  TEXT        NOT NULL DEFAULT 'facil',   -- facil | medio | dificil
    points      INTEGER     NOT NULL DEFAULT 10,
    order_index INTEGER     NOT NULL DEFAULT 0,
    image_file_id UUID      REFERENCES files(id) ON DELETE SET NULL,
    created_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Tabela: medals (medalhas/conquistas)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS medals (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT        NOT NULL,
    description TEXT        NOT NULL,
    condition   TEXT        NOT NULL,   -- ex: "Completar 5 missões"
    image_file_id UUID      REFERENCES files(id) ON DELETE SET NULL,
    created_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Dados iniciais de exemplo (seeds)
-- ------------------------------------------------------------

INSERT INTO contents (title, description, category, order_index) VALUES
    ('O que são enchentes?',   'Enchentes ocorrem quando rios transbordam devido a chuvas intensas. Aprenda como se proteger.', 'enchentes',     1),
    ('Deslizamentos de terra', 'Deslizamentos são comuns em áreas com chuva intensa e solo instável. Veja os sinais de alerta.',  'deslizamentos', 2),
    ('Tempestades severas',    'Tempestades com raios e ventos fortes podem causar grandes danos. Saiba o que fazer.',             'tempestades',   3),
    ('Kit de emergência',      'Monte seu kit de emergência com itens essenciais para situações de desastre.',                    'preparacao',    4),
    ('Números de emergência',  'Conheça os números importantes: Defesa Civil 199, SAMU 192, Bombeiros 193.',                     'geral',         5)
ON CONFLICT DO NOTHING;

INSERT INTO missions (title, description, difficulty, points, order_index) VALUES
    ('Conhecendo os riscos',         'Leia sobre os tipos de desastre e responda 3 perguntas.',      'facil',   10, 1),
    ('Monte seu kit de emergência',  'Liste 5 itens essenciais para um kit de emergência.',           'facil',   15, 2),
    ('Rota de evacuação',            'Desenhe uma rota de saída da sua casa para um local seguro.',   'medio',   25, 3),
    ('Quiz: Enchentes',              'Responda 10 perguntas sobre enchentes e prevenção.',             'medio',   30, 4),
    ('Agente Mirim certificado',     'Complete todas as missões anteriores.',                          'dificil', 50, 5)
ON CONFLICT DO NOTHING;

INSERT INTO medals (name, description, condition) VALUES
    ('Primeira Missão',   'Completou sua primeira missão!',             'Completar 1 missão'),
    ('Explorador',        'Completou 3 missões com sucesso.',           'Completar 3 missões'),
    ('Agente Mirim',      'Completou todas as missões disponíveis.',    'Completar todas as missões'),
    ('Especialista',      'Acertou 100% no quiz de enchentes.',         'Nota máxima no quiz'),
    ('Protetor da Cidade','Compartilhou uma dica com a comunidade.',    'Compartilhar conteúdo')
ON CONFLICT DO NOTHING;
