# Story: Google Drive Import

- **Epic:** epic-features.md
- **Fase:** FASE 2 - Differentiation
- **Priority:** P2
- **Estimate:** 16h

## Problem

Muitos criadores de conteúdo armazenam vídeos no Google Drive, especialmente no mercado corporativo/BR onde GDrive é padrão. Importar desses serviços evita upload manual de ficheiros grandes.

## Solution

Implementar OAuth integration com Google Drive para:
1. OAuth login com Google account
2. Browse arquivos no Drive
3. Select archivos de vídeo para import
4. Download e processamento automático

## Scope

- **In:** Google Drive files (mp4, mov, avi)
- **Out:** OneDrive import, Dropbox import

## Tasks

1. [ ] Google OAuth setup (Google Cloud Console)
2. [ ] Google Drive API integration
3. [ ] File picker UI (Google Drive files)
4. [ ] Download + process flow
5. [ ] Disconnect/manage connection UI

## Acceptance Criteria

- [ ] Botão "Import from Google Drive"
- [ ] OAuth flow funcional
- [ ] Lista de videos do Drive mostrada
- [ ] Seleção múltipla de arquivos
- [ ] Download inicia automático
- [ ] Disconnect Google account funcional

## Dependencies

- Google Cloud project setup
- OAuth base (story-security-critical.md)

---

*Story ID: FEATURES-GOOGLE-DRIVE-IMPORT*
*Created: 2026-04-14*