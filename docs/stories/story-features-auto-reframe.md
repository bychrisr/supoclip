# Story: Auto Reframe with Object Tracking

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P0
- **Estimate:** 40h

## Problem

O auto-reframe atual usa face detection estático, que não acompanha objetos em movimento. Quando o speaker sai do frame ou há múltiplos objetos relevantes, o cropping falha. Isso limita a qualidade dos clips para conteúdodinâmico como demos, tutoriais com objetos, e vídeos com movimento.

## Solution

Implementar object tracking usando MediaPipe para detectar e seguir objetos relevantes durante o vídeo. O sistema deve:
- Detectar faces e objetos em movimento via MediaPipe
- Rastrear o objeto principal ao longo do vídeo
- Ajustar o cropping dinamicamente para manter o objeto em frame
- Suportar múltiplos objetos (priorizar faces > objetos größten)
- Fallback para face detection quando tracking falha

## Scope

- In: Video input com movimento
- Out: Re-frameed video com tracking

## Tasks

1. [ ] Research MediaPipe object tracking options
2. [ ] Implement MediaPipe pose/object detection integration
3. [ ] Create object tracking class for video processing
4. [ ] Integrate tracking com existing cropper service
5. [ ] Add smart object selection (face > largest object)
6. [ ] Implement dynamic frame adjustment
7. [ ] Add fallback to face detection
8. [ ] Add tracking quality metrics
9. [ ] Write integration tests

## Acceptance Criteria

- [ ] Object tracking mantém objeto em frame durante todo o vídeo
- [ ] Suporta mínimo 30fps de tracking
- [ ] Fallback automático para face detection
- [ ] Performance: < 2x processing time overhead
- [ ] Tests: 90% coverage no tracking module

## Dependencies

- FASE 1: Animated captions, Multiple aspect ratios
- MediaPipe (already in project)
- Cropper service (existing)