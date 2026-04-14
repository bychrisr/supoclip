# Story 1.1: Segurança Crítica

## Epic
[epic-technical-debt.md](epic-technical-debt.md)

## Prioridade
**P0** — Crítico

## Esforço
~42h

## Responsável
@dev + @data-engineer

## Contexto

O SupoClip possui débitos críticos de segurança que devem ser resolvidos imediatamente:
- RLS (Row Level Security) desativado em todas as tabelas
- Rate limiting inexistente
- Credenciais hardcoded

## Débitos Alocados

| ID | Débito | Esforço |
|----|--------|---------|
| DB-029 | Sem políticas RLS em nenhuma tabela | 8h |
| DB-030 | Sem políticas RLS para sources | 4h |
| DB-031 | Sem políticas RLS para generated_clips | 4h |
| DB-019 | Sem tabela de rate limiting/limites | 8h |
| SYS-007 | Falta de rate limiting na API pública | 8h |
| SYS-008 | Credenciais hardcoded no init.sql | 2h |
| SYS-024 | Security Headers ausentes | 4h |

## Tasks

### DB-029: RLS em tasks
- [ ] 1.1.1 Ativar RLS no banco
- [ ] 1.1.2 Criar política RLS para tasks (owner = current_user)
- [ ] 1.1.3 Testar acesso cross-user via Pooler
- [ ] 1.1.4 Validar queries existentes com RLS

### DB-030: RLS em sources
- [ ] 1.1.5 Criar política RLS para sources (owner = current_user)
- [ ] 1.1.6 Validar queries com RLS ativo

### DB-031: RLS em generated_clips
- [ ] 1.1.7 Criar política RLS para generated_clips (via tasks)
- [ ] 1.1.8 Validar queries com RLS ativo

### DB-019 + SYS-007: Rate Limiting
- [ ] 1.1.9 Criar tabela user_limits (user_id, endpoint, limit, used, window_start)
- [ ] 1.1.10 Implementar middleware de rate limiting no backend
- [ ] 1.1.11 Configurar limites por endpoint (/api/tasks: 60/min, /api/clips: 30/min)
- [ ] 1.1.12 Testar rate limiting com curl (múltiplas requisições)

### SYS-008: Credenciais
- [ ] 1.1.13 Remover senha hardcoded do init.sql
- [ ] 1.1.14 Usar variável de ambiente POSTGRES_PASSWORD
- [ ] 1.1.15 Atualizar .env.example com variáveis de banco

### SYS-024: Security Headers
- [ ] 1.1.16 Configurar CSP header no backend
- [ ] 1.1.17 Configurar X-Frame-Options: DENY
- [ ] 1.1.18 Configurar HSTS header
- [ ] 1.1.19 Testar headers com curl -I

## Critérios de Aceite

### Segurança
- [ ] RLS ativo em tasks, sources, generated_clips
- [ ] Acesso cross-user retornando 403
- [ ] Rate limiting retorna 429 após limite
- [ ] Security headers presentes na resposta

### Funcionalidade
- [ ] Usuário consegue criar, editar, deletar próprias tasks
- [ ] Usuário NÃO consegue acessar tasks de outro usuário
- [ ] Rate limiting não quebra funcionalidades legítimas

### Testes
- [ ] Teste: Tentativa de acesso cross-user via API
- [ ] Teste: Rate limit atingido retorna 429
- [ ] Teste: Security headers presentes em todas as respostas

## Definition of Done

1. [ ] Todos os testes passando
2. [ ] Code review aprovado
3. [ ] Documentação atualizada (README.md)
4. [ ] Zero vulnerabilidades de segurança críticas

## Dependencies

- **Bloqueada por:** Nenhuma
- **Bloqueia:** Story 1.3 (Database Quality) para RLS

## Notes

- RLS com PostgreSQL Pooler requer atenção especial — pooler绕过 RLS em algumas configurações
- Rate limiting deve considerar endpoints públicos vs autenticados
- Testar SEMPRE com usuário diferente antes de considerar completo
