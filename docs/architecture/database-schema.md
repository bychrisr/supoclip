# SupoClip - Database Schema

## Visão Geral

Este documento descreve o schema completo do banco de dados PostgreSQL utilizado pelo SupoClip. O banco utiliza UUIDs como identificadores primários, com nomenclatura mista (camelCase para tabelas de autenticação Better Auth, snake_case para tabelas de domínio da aplicação).

**Versão do PostgreSQL:** 15+  
**Extensões:** uuid-ossp  
**Encoding:** UTF-8 (padrão)

---

## Índice de Tabelas

| # | Tabela | Descrição | Domínio |
|---|--------|-----------|---------|
| 1 | `users` | Usuários da aplicação (integrado com Better Auth) | Autenticação |
| 2 | `session` | Sessões ativas de usuários | Autenticação |
| 3 | `account` | Contas de provedores OAuth/credenciais | Autenticação |
| 4 | `verification` | Códigos de verificação de email | Autenticação |
| 5 | `sources` | Fontes de vídeo (YouTube, URL) | Domínio |
| 6 | `tasks` | Tarefas de processamento de clip | Domínio |
| 7 | `generated_clips` | Clipes gerados a partir de tarefas | Domínio |
| 8 | `processing_cache` | Cache de processamento de vídeos | Domínio |
| 9 | `stripe_webhook_events` | Webhooks do Stripe (idempotência) | Billing |

---

## Tabelas de Autenticação (Better Auth)

### 1. users

Tabela principal de usuários, estendida com campos de monetização e preferências.

| Coluna | Tipo | PK | FK | Nullable | Default | Constraints |
|--------|------|-----|-----|----------|---------|-------------|
| id | VARCHAR(36) | ✅ | — | ❌ | uuid_generate_v4() | PRIMARY KEY |
| name | VARCHAR(255) | — | — | ❌ | — | NOT NULL |
| email | VARCHAR(255) | — | — | ❌ | — | UNIQUE, NOT NULL |
| emailVerified | BOOLEAN | — | — | ❌ | false | NOT NULL |
| image | VARCHAR(500) | — | — | ✅ | — | — |
| createdAt | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |
| updatedAt | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |
| first_name | VARCHAR(100) | — | — | ✅ | — | — |
| last_name | VARCHAR(100) | — | — | ✅ | — | — |
| password_hash | VARCHAR(255) | — | — | ✅ | — | — |
| default_font_family | VARCHAR(100) | — | — | ✅ | 'TikTokSans-Regular' | — |
| default_font_size | INTEGER | — | — | ✅ | 24 | — |
| default_font_color | VARCHAR(7) | — | — | ✅ | '#FFFFFF' | — |
| is_admin | BOOLEAN | — | — | ❌ | false | NOT NULL |
| plan | VARCHAR(20) | — | — | ❌ | 'free' | NOT NULL |
| subscription_status | VARCHAR(20) | — | — | ❌ | 'inactive' | NOT NULL |
| stripe_customer_id | VARCHAR(255) | — | — | ✅ | — | UNIQUE |
| stripe_subscription_id | VARCHAR(255) | — | — | ✅ | — | UNIQUE |
| billing_period_start | TIMESTAMP WITH TIME ZONE | — | — | ✅ | — | — |
| billing_period_end | TIMESTAMP WITH TIME ZONE | — | — | ✅ | — | — |
| trial_ends_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | — | — |

**Índices:**
- `idx_users_email` (email) - UNIQUE

**Trigger:** `update_users_updatedAt` (atualiza `updatedAt` automaticamente)

---

### 2. session

Sessões ativas de usuários (Better Auth).

| Coluna | Tipo | PK | FK | Nullable | Default | Constraints |
|--------|------|-----|-----|----------|---------|-------------|
| id | VARCHAR(36) | ✅ | — | ❌ | — | PRIMARY KEY |
| expiresAt | TIMESTAMP WITH TIME ZONE | — | — | ❌ | — | NOT NULL |
| token | VARCHAR(255) | — | — | ❌ | — | UNIQUE, NOT NULL |
| createdAt | TIMESTAMP WITH TIME ZONE | — | — | ❌ | — | NOT NULL |
| updatedAt | TIMESTAMP WITH TIME ZONE | — | — | ❌ | — | NOT NULL |
| ipAddress | VARCHAR(255) | — | — | ✅ | — | — |
| userAgent | TEXT | — | — | ✅ | — | — |
| userId | VARCHAR(36) | — | ✅ | ❌ | — | REFERENCES users(id) ON DELETE CASCADE |

**Índices:**
- `idx_session_token` (token) - UNIQUE
- `idx_session_userId` (userId)

**Trigger:** `update_session_updatedAt`

**Nota:** `userId` tem DELETE CASCADE - ao excluir usuário, sessões são removidas.

---

### 3. account

Contas de provedores OAuth e autenticação por senha.

| Coluna | Tipo | PK | FK | Nullable | Default | Constraints |
|--------|------|-----|-----|----------|---------|-------------|
| id | VARCHAR(36) | ✅ | — | ❌ | — | PRIMARY KEY |
| accountId | VARCHAR(255) | — | — | ❌ | — | NOT NULL |
| providerId | VARCHAR(255) | — | — | ❌ | — | NOT NULL |
| userId | VARCHAR(36) | — | ✅ | ❌ | — | REFERENCES users(id) ON DELETE CASCADE |
| accessToken | TEXT | — | — | ✅ | — | — |
| refreshToken | TEXT | — | — | ✅ | — | — |
| idToken | TEXT | — | — | ✅ | — | — |
| accessTokenExpiresAt | TIMESTAMP WITH TIME ZONE | — | — | ✅ | — | — |
| refreshTokenExpiresAt | TIMESTAMP WITH TIME ZONE | — | — | ✅ | — | — |
| scope | TEXT | — | — | ✅ | — | — |
| password | TEXT | — | — | ✅ | — | — |
| createdAt | TIMESTAMP WITH TIME ZONE | — | — | ❌ | — | NOT NULL |
| updatedAt | TIMESTAMP WITH TIME ZONE | — | — | ❌ | — | NOT NULL |

**Índices:**
- `idx_account_userId` (userId)

**Trigger:** `update_account_updatedAt`

**Nota:** Campos de token em TEXT (sem limite) - tokens OAuth podem ser longos.

---

### 4. verification

Códigos de verificação de email (Better Auth).

| Coluna | Tipo | PK | FK | Nullable | Default | Constraints |
|--------|------|-----|-----|----------|---------|-------------|
| id | VARCHAR(36) | ✅ | — | ❌ | — | PRIMARY KEY |
| identifier | VARCHAR(255) | — | — | ❌ | — | NOT NULL |
| value | VARCHAR(255) | — | — | ❌ | — | NOT NULL |
| expiresAt | TIMESTAMP WITH TIME ZONE | — | — | ❌ | — | NOT NULL |
| createdAt | TIMESTAMP WITH TIME ZONE | — | — | ✅ | — | — |
| updatedAt | TIMESTAMP WITH TIME ZONE | — | — | ✅ | — | — |

**Índices:**
- `idx_verification_identifier` (identifier)

**Trigger:** `update_verification_updatedAt`

---

## Tabelas de Domínio (Aplicação)

### 5. sources

Fontes de vídeo para processamento (YouTube ou URL direta).

| Coluna | Tipo | PK | FK | Nullable | Default | Constraints |
|--------|------|-----|-----|----------|---------|-------------|
| id | VARCHAR(36) | ✅ | — | ❌ | uuid_generate_v4() | PRIMARY KEY |
| type | VARCHAR(20) | — | — | ❌ | — | CHECK (type IN ('youtube', 'video_url')) |
| title | VARCHAR(500) | — | — | ❌ | — | NOT NULL |
| url | VARCHAR(1000) | — | — | ✅ | — | — |
| created_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |
| updated_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |

**Índices:**
- `idx_sources_created_at` (created_at)

**Trigger:** `update_sources_updated_at`

**Notas:**
- CHECK constraint no campo `type` ('youtube', 'video_url')
- Campo `url` é nullable (fontes podem ser criadas sem URL ainda)

---

### 6. tasks

Tarefas de processamento de clips de vídeo.

| Coluna | Tipo | PK | FK | Nullable | Default | Constraints |
|--------|------|-----|-----|----------|---------|-------------|
| id | VARCHAR(36) | ✅ | — | ❌ | uuid_generate_v4() | PRIMARY KEY |
| user_id | VARCHAR(36) | — | ✅ | ❌ | — | REFERENCES users(id) ON DELETE CASCADE |
| source_id | VARCHAR(36) | — | ✅ | ✅ | — | REFERENCES sources(id) ON DELETE SET NULL |
| generated_clips_ids | VARCHAR(36)[] | — | — | ✅ | — | Array de UUIDs |
| status | VARCHAR(20) | — | — | ❌ | 'pending' | NOT NULL |
| progress | INTEGER | — | — | ✅ | 0 | CHECK (progress >= 0 AND progress <= 100) |
| progress_message | TEXT | — | — | ✅ | — | — |
| font_family | VARCHAR(100) | — | — | ✅ | 'TikTokSans-Regular' | — |
| font_size | INTEGER | — | — | ✅ | 24 | — |
| font_color | VARCHAR(7) | — | — | ✅ | '#FFFFFF' | — |
| caption_template | VARCHAR(50) | — | — | ✅ | 'default' | — |
| include_broll | BOOLEAN | — | — | ✅ | false | — |
| processing_mode | VARCHAR(20) | — | — | ❌ | 'fast' | NOT NULL |
| started_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | — | — |
| completed_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | — | — |
| cache_hit | BOOLEAN | — | — | ❌ | false | NOT NULL |
| error_code | VARCHAR(80) | — | — | ✅ | — | — |
| stage_timings_json | TEXT | — | — | ✅ | — | — |
| created_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |
| updated_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |

**Índices:**
- `idx_tasks_user_id` (user_id)
- `idx_tasks_source_id` (source_id)
- `idx_tasks_status` (status)
- `idx_tasks_created_at` (created_at)
- `idx_tasks_processing_mode` (processing_mode)
- `idx_tasks_completed_at` (completed_at)

**Trigger:** `update_tasks_updated_at`

**Constraints:**
- CHECK em `progress` (0-100)
- `status` NOT NULL com default 'pending'
- `processing_mode` NOT NULL com default 'fast'

**Notas:**
- `source_id` com ON DELETE SET NULL (mantém task se fonte for deletada)
- `user_id` com ON DELETE CASCADE (exclui tasks ao excluir usuário)
- `generated_clips_ids` é array PostgreSQL (não normalizado - ver débitos)

---

### 7. generated_clips

Clipes individuais gerados a partir de uma tarefa.

| Coluna | Tipo | PK | FK | Nullable | Default | Constraints |
|--------|------|-----|-----|----------|---------|-------------|
| id | VARCHAR(36) | ✅ | — | ❌ | uuid_generate_v4() | PRIMARY KEY |
| task_id | VARCHAR(36) | — | ✅ | ❌ | — | REFERENCES tasks(id) ON DELETE CASCADE |
| filename | VARCHAR(255) | — | — | ❌ | — | NOT NULL |
| file_path | VARCHAR(500) | — | — | ❌ | — | NOT NULL |
| start_time | VARCHAR(20) | — | — | ❌ | — | NOT NULL (MM:SS) |
| end_time | VARCHAR(20) | — | — | ❌ | — | NOT NULL (MM:SS) |
| duration | FLOAT | — | — | ❌ | — | NOT NULL |
| text | TEXT | — | — | ✅ | — | — |
| relevance_score | FLOAT | — | — | ❌ | — | NOT NULL |
| reasoning | TEXT | — | — | ✅ | — | — |
| clip_order | INTEGER | — | — | ❌ | — | NOT NULL |
| virality_score | INTEGER | — | — | ✅ | 0 | — |
| hook_score | INTEGER | — | — | ✅ | 0 | — |
| engagement_score | INTEGER | — | — | ✅ | 0 | — |
| value_score | INTEGER | — | — | ✅ | 0 | — |
| shareability_score | INTEGER | — | — | ✅ | 0 | — |
| hook_type | VARCHAR(50) | — | — | ✅ | — | — |
| created_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |
| updated_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |

**Índices:**
- `idx_generated_clips_task_id` (task_id)
- `idx_generated_clips_clip_order` (clip_order)
- `idx_generated_clips_created_at` (created_at)

**Trigger:** `update_generated_clips_updated_at`

**Notas:**
- `task_id` com ON DELETE CASCADE (exclui clips ao excluir task)
- Campos de tempo em VARCHAR(20) formato MM:SS (não normalizado)
- Scores de virality individualizados (hook, engagement, value, shareability)

---

### 8. processing_cache

Cache de processamento de vídeos para evitar re-processamento.

| Coluna | Tipo | PK | FK | Nullable | Default | Constraints |
|--------|------|-----|-----|----------|---------|-------------|
| cache_key | VARCHAR(255) | ✅ | — | ❌ | — | PRIMARY KEY |
| source_url | TEXT | — | — | ❌ | — | NOT NULL |
| source_type | VARCHAR(20) | — | — | ❌ | — | NOT NULL |
| video_path | TEXT | — | — | ✅ | — | — |
| transcript_text | TEXT | — | — | ✅ | — | — |
| analysis_json | TEXT | — | — | ✅ | — | — |
| created_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |
| updated_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |

**Índices:**
- `idx_processing_cache_source_url` (source_url)

**Trigger:** `update_processing_cache_updated_at` (não existente - ver débitos)

**Notas:**
- PK `cache_key` deve ser chave derivável da URL (hash ou URL normalizada)
- Campos JSON armazenados como TEXT (sem validação)

---

### 9. stripe_webhook_events

Tabela de idempotência para webhooks do Stripe.

| Coluna | Tipo | PK | FK | Nullable | Default | Constraints |
|--------|------|-----|-----|----------|---------|-------------|
| id | VARCHAR(255) | ✅ | — | ❌ | — | PRIMARY KEY |
| type | VARCHAR(255) | — | — | ❌ | — | NOT NULL |
| created_at | TIMESTAMP WITH TIME ZONE | — | — | ✅ | CURRENT_TIMESTAMP | — |

**Índices:** Nenhum adicional

**Notas:**
- `id` deve ser o `id` do evento Stripe (para idempotência)
- Sem campo `updated_at` - tabela de log, não atualizável

---

## Relacionamentos

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USERS (1)                                      │
│                          ┌───────────────┐                                  │
│                          │ id (PK)       │                                  │
│                          └───────┬───────┘                                  │
│                                  │ 1:N                                      │
│         ┌───────────────────────┼───────────────────────┐                  │
│         │                       │                       │                  │
│         ▼                       ▼                       ▼                  │
│    ┌─────────┐           ┌─────────────┐         ┌──────────┐             │
│    │ session │           │   account   │         │  tasks   │             │
│    │ userId  │           │   userId    │         │ user_id  │             │
│    └─────────┘           └─────────────┘         └────┬─────┘             │
│                                                        │ 1:N                │
│                                                        ▼                    │
│                                                ┌─────────────┐             │
│                                                │   sources   │             │
│                                                │  (task)     │             │
│                                                └─────────────┘             │
│                                                 : (tasks.source_id)         │
│                                                        │ 1:N                │
│                                                        ▼                    │
│                                                ┌───────────────┐           │
│                                                │generated_clips│           │
│                                                │   task_id     │           │
│                                                └───────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Cardinalidade

| De | Para | Tipo | ON DELETE |
|-----|------|------|-----------|
| users | session | 1:N | CASCADE |
| users | account | 1:N | CASCADE |
| users | tasks | 1:N | CASCADE |
| tasks | sources | N:1 | SET NULL |
| tasks | generated_clips | 1:N | CASCADE |

---

## Índices Existentes

| Índice | Tabela | Coluna(s) | Única |
|--------|--------|-----------|-------|
| idx_users_email | users | email | ✅ |
| idx_session_token | session | token | ✅ |
| idx_session_userId | session | userId | ❌ |
| idx_account_userId | account | userId | ❌ |
| idx_verification_identifier | verification | identifier | ❌ |
| idx_tasks_user_id | tasks | user_id | ❌ |
| idx_tasks_source_id | tasks | source_id | ❌ |
| idx_tasks_status | tasks | status | ❌ |
| idx_tasks_created_at | tasks | created_at | ❌ |
| idx_tasks_processing_mode | tasks | processing_mode | ❌ |
| idx_tasks_completed_at | tasks | completed_at | ❌ |
| idx_sources_created_at | sources | created_at | ❌ |
| idx_processing_cache_source_url | processing_cache | source_url | ❌ |
| idx_generated_clips_task_id | generated_clips | task_id | ❌ |
| idx_generated_clips_clip_order | generated_clips | clip_order | ❌ |
| idx_generated_clips_created_at | generated_clips | created_at | ❌ |

---

## Triggers

Todos os triggers atualizam automaticamente `updated_at`/`updatedAt` antes de UPDATE:

| Trigger | Tabela | Função |
|---------|--------|--------|
| update_users_updatedAt | users | update_updatedAt_column() |
| update_tasks_updated_at | tasks | update_updated_at_column() |
| update_sources_updated_at | sources | update_updated_at_column() |
| update_generated_clips_updated_at | generated_clips | update_updated_at_column() |
| update_session_updatedAt | session | update_updatedAt_column() |
| update_account_updatedAt | account | update_updatedAt_column() |
| update_verification_updatedAt | verification | update_updatedAt_column() |

---

## Camadas de Dados no Backend

O projeto utiliza **raw SQL via asyncpg** (não ORM completo):

- **Frontend (Next.js):** Prisma Client para tipagem e migrations
- **Backend (FastAPI):** Raw SQL via `src/repositories/` (asyncpg)
- **Worker (ARQ):** Raw SQL via asyncpg para processamentos

---

## Notas de Implementação

### Nomenclatura Mista
- Tabelas Better Auth: camelCase (users, session, account, verification)
- Tabelas de Domínio: snake_case (tasks, sources, generated_clips)
- Campos: mix de ambos dentro de cada tabela

### Campos Timestamps
- Compatibilidade Prisma: `createdAt`, `updatedAt` (camelCase)
- Domínio aplicação: `created_at`, `updated_at` (snake_case)
- Ambos armazenam TIMESTAMP WITH TIME ZONE

### Encoding de Strings
- VARCHAR com tamanhos específicos (não TEXT ilimitado)
- Exceptions: token, scope, text, reasoning, progress_message, stage_timings_json