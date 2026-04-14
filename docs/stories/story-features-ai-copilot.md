# Story: AI Copilot - Topics Search & Prompt to Clip

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P1
- **Estimate:** 32h

## Problem

Usuários precisam de controle granular sobre clip selection. Pesquisar topics específicos e criar clips via prompts seria diferencial competitivo.

## Solution

Implementar AI copilot para clip creation:
- Topics search no transcript
- Prompt-to-clip natural language
- Pydantic AI para intent parsing
- Relevance scoring por topic/prompt
- Interactive refinement loop

## Scope

- In: Transcript + natural language prompt
- Out: Selected clips matching

## Tasks

1. [ ] Implement topic search no transcript
2. [ ] Create Pydantic AI copilot integration
3. [ ] Implement prompt-to-clip parsing
4. [ ] Add relevance ranking
5. [ ] Create interactive refinement loop
6. [ ] Add search history
7. [ ] Write integration tests

## Acceptance Criteria

- [ ] Topics search retorna relevant segments
- [ ] Natural language prompts funcionam
- [ ] Interactive refinement available
- [ ] Search history persistence
- [ ] Tests: 85% coverage

## Dependencies

- Pydantic AI (existing)
- Transcript (existing)
- Word-synced subtitles (existing)