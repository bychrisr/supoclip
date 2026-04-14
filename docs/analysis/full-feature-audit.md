# Full Feature Audit - SupoClip Competition

**[Versão Completa]** — Análise exaustiva de OpusClip, Real Oficial, VidRush vs SupoClip atual

---

## PARTE 1: OPUSCLIP (Líder - 16M usuários, $50M funding)

### 1.1 Core Video Processing

| Feature | Descrição | Status SupoClip |
|---------|-----------|-----------------|
| ClipAnything | Modelo AI multimodal proprietário para clipping por áudio, visual, emoção, gênero | P0 - Requer extensão |
| ReframeAnything | Reframe automático com object tracking para qualquer aspect ratio | P1 - 9:16 já funciona |
| Video input sources | YouTube, Google Drive, Vimeo, Zoom, Rumble, Twitch, Facebook, LinkedIn, Twitter/X, Loom, Riverside, Frame.io, StreamYard + URLs MP4 públicas | P0 - YouTube + upload só |
| Face detection/cropping | Crop automático centralizado em rosto | DONE - MediaPipe + OpenCV |
| Word-synced subtitles | Transcrição com timestamps por palavra | DONE - AssemblyAI |
| Multiple aspect ratios | 9:16, 16:9, 1:1, 4:5 | P1 - Só 9:16 atualmente |
| Video trimming | Ajuste manual de início/fim dos clips | DONE - API existe |
| Clip splitting | Dividir clip em timestamp específico | DONE - API existe |
| Clip merging | Mesclar clips selecionados | DONE - API existe |
| Transition effects | Transições entre clipes | DONE - Backend suporta |
| Background processing | Processamento assíncrono com queue | DONE - ARQ worker |

### 1.2 AI Features

| Feature | Descrição | Status SupoClip |
|---------|-----------|-----------------|
| Virality Score | Score proprietário que prediz performance (0-100) | DONE - hook/engagement/value/shareability |
| AI segment selection | Seleciona 3-7 segmentos virais automaticamente | DONE - Pydantic AI |
| Emotion detection | Detecção de tom emocional | P1 - No escopo do AI |
| Humor detection | Detecção de humor no conteúdo | P1 - No escopo do AI |
| Genre classification | Classificação por gênero do conteúdo | P1 - No escopo do AI |
| Audio-based clipping | Cortar por picos de áudio | DONE - Já funciona |
| Visual-based clipping | Cortar por relevância visual | P0 - Requer extensão |
| Transcript caching | Cache de transcrição para reuse | DONE - .transcript_cache.json |
| Multi-language transcription | 26+ línguas suportadas | P2 - Só inglês otimizado |
| Custom AI prompts | Prompts customizáveis para seleção | P1 - Prompt fixo atualmente |

### 1.3 Export/Output

| Feature | Descrição | Status SupoClip |
|---------|-----------|-----------------|
| Platform presets | Presets por plataforma (TikTok, Reels, Shorts) | DONE - Export endpoint |
| Resolution options | 720p, 1080p, 4K | P1 - Só 1080p |
| Format export | MP4, MOV | P2 - Só MP4 |
| Adobe Premiere XML | Export para Premiere Pro | P3 - Não prioritário |
| DaVinci Resolve XML | Export para DaVinci Resolve | P3 - Não prioritário |
| Direct social posting | Publicação direta para redes | P0 - NÃO EXISTE |
| Download links | Links de download para clips | DONE - Serve endpoint |
| Custom output directory | Diretório de saída configurável | DONE - OUTPUT_DIR env |

### 1.4 Scheduling & Automation

| Feature | Descrição | Status SupoClip |
|---------|-----------|-----------------|
| Social Scheduler | Agendamento para YT/TikTok/IG/LinkedIn/FB/X | P0 - NÃO EXISTE |
| Calendar view | Visualização calendário de posts | P0 - NÃO EXISTE |
| Queue management | Fila de processamento | DONE - ARQ |
| Webhooks | Notificações assíncronas | P2 - Planejado |
| Zapier integration | Integração com 5K+ apps | P2 - Não implementado |
| Make.com integration | Integração com automação | P2 - Não implementado |
| Bulk processing | Processamento em massa | P1 - Editing em massa |
| Auto-resume | Retry automático em falha | P2 - Manual resume |

### 1.5 Team/Workspace

| Feature | Descrição | Status SupoClip |
|---------|-----------|-----------------|
| Multi-workspace | Múltiplos workspaces por usuário | P1 - Single user |
| Team seats | Assentos por equipe | P1 - Não implementado |
| Role-based permissions | Permissões por role | P1 - Não implementado |
| Member invitations | Convite de membros | P1 - Não implementado |
| Team analytics | Analytics por equipe | P1 - Não implementado |
| Folder organization | Organização por pastas | P1 - Não implementado |
| Shared templates | Templates compartilhados | P2 - Não implementado |

### 1.6 Billing & Plans

| Feature | Descrição | Status SupoClip |
|---------|-----------|-----------------|
| Free tier | 60 créditos/mês (watermark) | DONE - FREE_PLAN_TASK_LIMIT |
| Starter plan | $15/mês, 150 créditos/mês | P1 - Plan system |
| Pro plan | $29/mês, 3600 créditos/ano | P1 - Plan system |
| Business plan | Custom, API, SSO, storage ilimitado | P1 - Plan system |
| Annual billing | Desconto anual (~50%) | P2 - Stripe config |
| Credit packs | Compra avulsa de créditos | P2 - Billing system |
| Usage tracking | Tracking de uso por usuário | P1 - Parcial |
| Plan upgrade/downgrade | Mudança de plano | P2 - Billing system |
| Invoice generation | Geração de faturas | P2 - Stripe |

### 1.7 Integrações

| Feature | Descrição | Status SupoClip |
|---------|-----------|-----------------|
| YouTube | Fonte de vídeo + upload | DONE - yt-dlp + upload |
| Google Drive | Fonte de vídeo | P0 - Não implementado |
| Vimeo | Fonte de vídeo | P0 - Não implementado |
| Zoom | Fonte de vídeo | P0 - Não implementado |
| Rumble | Fonte de vídeo | P0 - Não implementado |
| Twitch | Fonte de vídeo | P0 - Não implementado |
| Loom | Fonte de vídeo | P0 - Não implementado |
| Riverside | Fonte de vídeo | P0 - Não implementado |
| Frame.io | Fonte de vídeo | P0 - Não implementado |
| StreamYard | Fonte de vídeo | P0 - Não implementado |
| Direct upload | Upload de arquivo MP4 | DONE - Upload endpoint |
| API v2 | API pública REST | P2 - API interna |
| SSO/SAML | Enterprise auth | P2 - Better Auth |
| Discord webhooks | Feedback via Discord | DONE - Discord webhook |

### 1.8 Technical Stack

| Componente | OpusClip | SupoClip |
|------------|----------|----------|
| Frontend | Next.js Pages Router | Next.js 15 App Router (melhor) |
| Backend | Node.js + Django | FastAPI (Python) |
| Database | MongoDB | PostgreSQL (melhor) |
| Cache/Queue | Redis | Redis |
| Video processing | FFmpeg fork | FFmpeg + MoviePy |
| Auth | WorkOS | Better Auth |
| Cloud | GCP | Configurável |
| CDN | Cloudflare + GCS | Configurável |
| AI models | Gemini 1.5 Flash | Multi-provider |

---

## PARTE 2: REAL OFICIAL (Brasil)

### 2.1 Core Features

| Feature | Descrição | Status SupoClip |
|---------|-----------|-----------------|
| BIA (Business Intelligence for Attention) | IA proprietária especializada em podcasts/webinars | P0 - IA genérica |
| Análise de 18 parâmetros | Humor, tom emocional, engajamento | P1 -analytics limitado |
| Monitoramento de lives | Rastreia streams ao vivo (~118 simultâneos) | P0 - NÃO EXISTE |
| Cortes automáticos | ~15 cortes por 30 min de vídeo | DONE - AI selection |
| Output vertical + horizontal | 9:16 + 16:9 | P1 - Só 9:16 |
| Legendas word-synced | Legendas sincronizadas | DONE |
| Tradução de legendas | Tradução automática | P2 - Não implementado |
| Editor profissional | Ajuste enquadramento, legendas | DONE - Clip editing API |
| Brand Kit | Personalização por conta | P1 - Templates básicos |
| Edição em massa | Batch editing | P1 - Parcial |
| Clip duration até 15min | Clipes longos | DONE - CLIP_DURATION config |

### 2.2 Localização

| Feature | Descrição | Status SupoClip |
|---------|-----------|-----------------|
| Interface PT-BR | Português brasileiro nativo | P1 - EN only |
| Multi-idioma | PT/EN/ES | P2 - i18n não implementado |
| Pricing em BRL | Preços em Real | P2 - billing BRL |
| Testimonial Podpah | Validação de mercado BR | N/A |
| Live monitoring BR | Monitoramento de streams BR | P0 - NÃO EXISTE |

### 2.3 Pricing (em BRL)

| Plano | Preço | Créditos | Status SupoClip |
|-------|-------|----------|-----------------|
| Free | R$0 | 60 | DONE |
| Lite | R$59,90 | 600 | P1 |
| Creator | R$99,90 | 1.200 | P1 |
| Viral | R$149,90 | 1.800 | P1 |

---

## PARTE 3: VIDRUSH

### 3.1 Core Features

| Feature | Descrição | Status SupoClip |
|---------|-----------|-----------------|
| Text-to-video generation | Gera vídeo do zero com tópico | N/A - Diferente escopo |
| Faceless video | Vídeos sem aparecer | N/A - Diferente escopo |
| Auto Mode | Geração automática com aprovação de script | P1 - Workflow similar |
| Manual Mode | Revisão de script antes de gerar | P1 - Workflow similar |
| Custom Script upload | Upload de roteiro próprio | P2 - Prompt custom |
| Custom Voiceover upload | Upload de narração própria | P0 - Upload single |
| Reference Video | Imitar estilo de canal existente | P3 - Nice to have |
| Thumbnail Generator | Geração de thumbnail | P2 - Não implementado |
| Video Editor | Editor pós-geração | DONE - Clip editing |
| Queue cloud | Processamento em background | DONE - ARQ |
| Team Seats | Assentos por equipe | P1 - Não implementado |
| Multi-workspace | Múltiplos workspaces | P1 - Não implementado |

### 3.2 Modelos de Geração

| Modelo | Visual | Raciocínio | Custo (créditos/min) |
|--------|--------|------------|----------------------|
| Deep Video v1 Mini | Só imagens | Low | 32 |
| Deep Video v1 Mini | Só imagens | Medium | 40 |
| Deep Video v1 Pro | Vídeo + imagem | Low | 44 |
| Deep Video v1 Pro | Vídeo + imagem | Medium | 55 |

### 3.3 Pricing

| Plano | Mensal | Anual | Créditos | Concurrent |
|-------|--------|-------|----------|------------|
| Starter | $99 | $74 | 2.000 | 1 |
| Creator | $239 | $179 | 6.000 | 2 |
| Pro | $639 | $479 | 18.000 | 3 |
| Scale | $1.750 | $1.313 | 50.000 | 5 |

---

## PARTE 4: SUPOCLIP - ESTADO ATUAL

### 4.1 O que já temos (do CLAUDE.md)

| Feature | Status | Notas |
|---------|--------|-------|
| YouTube URL input | ✅ DONE | yt-dlp |
| File upload | ✅ DONE | Upload endpoint |
| Transcription | ✅ DONE | AssemblyAI word-level |
| AI segment selection | ✅ DONE | Pydantic AI 3-7 clips |
| Virality scoring | ✅ DONE | hook/engagement/value/shareability |
| Face detection/cropping | ✅ DONE | MediaPipe + OpenCV DNN + Haar |
| Word-synced subtitles | ✅ DONE | AssemblyAI timestamps |
| Custom fonts | ✅ DONE | TTF em backend/fonts/ |
| Transition effects | ✅ DONE | MP4 em backend/transitions/ |
| B-roll overlays | ✅ DONE | Pexels API |
| Caption templates | ✅ DONE | Múltiplos estilos |
| Clip trim | ✅ DONE | PATCH endpoint |
| Clip split | ✅ DONE | POST split endpoint |
| Clip merge | ✅ DONE | POST merge endpoint |
| Export presets | ✅ DONE | tiktok, etc |
| SSE progress | ✅ DONE | Real-time updates |
| Task lifecycle | ✅ DONE | queued→processing→completed |
| Multi-provider LLM | ✅ DONE | Google/OpenAI/Anthropic/Ollama |
| Discord webhooks | ✅ DONE | Feedback |
| Health checks | ✅ DONE | /health endpoints |
| PostgreSQL + Redis | ✅ DONE | Docker compose |
| FastAPI backend | ✅ DONE | Clean architecture |

### 4.2 O que NÃO temos (Gap Analysis)

| Feature | Prioridade | Esforço | Motivo |
|---------|------------|---------|--------|
| Social Scheduler | P0 | Alto | Requer integração APIs externas |
| Direct social posting | P0 | Alto | Requer OAuth apps |
| Multiple video sources | P0 | Médio | GDrive, Vimeo, etc |
| Multiple aspect ratios | P1 | Médio | 16:9, 1:1, 4:5 |
| Team/Workspace | P1 | Alto | Auth + DB changes |
| Webhooks | P2 | Médio | Callback system |
| Zapier/Make | P2 | Médio | REST API + webhook |
| Brand Templates | P1 | Médio | Multi-template system |
| PT-BR localization | P1 | Baixo | i18n setup |
| Multi-language transcription | P2 | Médio | Language configs |
| Translation | P2 | Alto | Translation API |
| Live monitoring | P0 | Muito Alto | Stream ingestion |
| Pricing/Billing | P2 | Alto | Stripe integration |
| API pública | P2 | Médio | REST API external |
| Analytics dashboard | P2 | Médio | Usage tracking |

---

## PARTE 5: MATRIX COMPLETA COMPARATIVA

| Feature | OpusClip | Real Oficial | VidRush | SupoClip | Status |
|---------|----------|--------------|---------|----------|--------|
| **Input Sources** | | | | | |
| YouTube URL | ✅ | ✅ | N/A | ✅ DONE | — |
| File upload (MP4) | ✅ | ✅ | N/A | ✅ DONE | — |
| Google Drive | ✅ | ❓ | N/A | ❌ P0 | Gap |
| Vimeo | ✅ | ❓ | N/A | ❌ P0 | Gap |
| Zoom | ✅ | ❓ | N/A | ❌ P0 | Gap |
| Rumble | ✅ | ❓ | N/A | ❌ P0 | Gap |
| Twitch | ✅ | ❓ | N/A | ❌ P0 | Gap |
| Loom | ✅ | ❓ | N/A | ❌ P0 | Gap |
| Riverside | ✅ | ❓ | N/A | ❌ P0 | Gap |
| Frame.io | ✅ | ❓ | N/A | ❌ P0 | Gap |
| StreamYard | ✅ | ❓ | N/A | ❌ P0 | Gap |
| **Core Processing** | | | | | | |
| AI clip selection | ✅ | ✅ | N/A | ✅ DONE | — |
| Virality scoring | ✅ | ✅ | N/A | ✅ DONE | — |
| Face detection/crop | ✅ | ✅ | N/A | ✅ DONE | — |
| Word-synced subtitles | ✅ | ✅ | N/A | ✅ DONE | — |
| Custom fonts | ✅ | ✅ | N/A | ✅ DONE | — |
| Transitions | ✅ | ✅ | N/A | ✅ DONE | — |
| B-roll overlays | ✅ | ✅ | N/A | ✅ DONE | — |
| Caption templates | ✅ | ✅ | N/A | ✅ DONE | — |
| Multiple aspect ratios | ✅ | ✅ | N/A | ❌ P1 | Gap |
| **AI Features** | | | | | |
| ClipAnything (multi-modal) | ✅ | ❓ | N/A | ❌ P0 | Gap |
| ReframeAnything | ✅ | ❓ | N/A | ❌ P1 | Gap |
| BIA (podcast special) | ❌ | ✅ | N/A | ❌ P0 | Gap |
| Emotion detection | ✅ | ✅ | N/A | ❌ P1 | Gap |
| Humor detection | ✅ | ✅ | N/A | ❌ P1 | Gap |
| Live monitoring | ❌ | ✅ | N/A | ❌ P0 | Gap |
| Text-to-video | ❌ | ❌ | ✅ | N/A | Different scope |
| **Editing** | | | | | | |
| Clip trim | ✅ | ✅ | ✅ | ✅ DONE | — |
| Clip split | ✅ | ✅ | ✅ | ✅ DONE | — |
| Clip merge | ✅ | ✅ | ✅ | ✅ DONE | — |
| Bulk editing | ✅ | ✅ | ❓ | ❌ P1 | Gap |
| Video editor UI | ✅ | ✅ | ✅ | ❌ P2 | Nice to have |
| Thumbnail generator | ❌ | ❌ | ✅ | ❌ P2 | Nice to have |
| **Output** | | | | | | |
| Platform presets | ✅ | ✅ | ✅ | ✅ DONE | — |
| 9:16 vertical | ✅ | ✅ | ✅ | ✅ DONE | — |
| 16:9 horizontal | ✅ | ✅ | ✅ | ❌ P1 | Gap |
| 1:1 square | ✅ | ❓ | ❓ | ❌ P1 | Gap |
| 4:5 portrait | ✅ | ❓ | ❓ | ❌ P1 | Gap |
| Export XML (Premiere) | ✅ | ❓ | ❓ | ❌ P3 | Nice to have |
| Direct social post | ✅ | ✅ | ❓ | ❌ P0 | Gap |
| **Scheduling** | | | | | | | |
| Social Scheduler | ✅ | ❓ | ❓ | ❌ P0 | Gap |
| Calendar view | ✅ | ❓ | ❓ | ❌ P0 | Gap |
| Webhooks | ✅ | ❓ | ❓ | ❌ P2 | Gap |
| Zapier integration | ✅ | ❓ | ❓ | ❌ P2 | Gap |
| Make.com integration | ✅ | ❓ | ❓ | ❌ P2 | Gap |
| **Team** | | | | | | |
| Multi-workspace | ✅ | ❓ | ✅ | ❌ P1 | Gap |
| Team seats | ✅ | ❓ | ✅ | ❌ P1 | Gap |
| Role permissions | ✅ | ❓ | ❓ | ❌ P1 | Gap |
| Member invitations | ✅ | ❓ | ❓ | ❌ P1 | Gap |
| Folder organization | ✅ | ❓ | ❓ | ❌ P1 | Gap |
| **Billing** | | | | | | | |
| Free tier | ✅ (60min) | ✅ (60 credits) | ❌ | ✅ DONE | — |
| Paid plans | ✅ | ✅ | ✅ | ❌ P1 | Gap |
| Credit packs | ✅ | ✅ | ✅ | ❌ P2 | Gap |
| Annual billing | ✅ | ❓ | ✅ | ❌ P2 | Gap |
| PAYG | ❌ | ❓ | ✅ | ❌ P2 | Gap |
| **Localization** | | | | | | | |
| PT-BR interface | ❌ | ✅ | ❌ | ❌ P1 | Gap |
| Multi-language | 26+ langs | ✅ (3) | ❌ | ❌ P2 | Gap |
| Pricing in BRL | ❌ | ✅ | ❌ | ❌ P2 | Gap |
| **Technical** | | | | | | | |
| API v2 | ✅ (closed) | ❓ | ❓ | ❌ P2 | Gap |
| SSO/SAML | ✅ (Enterprise) | ❓ | ❓ | ❌ P2 | Gap |
| Real-time SSE | ✅ (15s poll) | ❓ | ❓ | ✅ DONE | Better |
| Background queue | ✅ | ✅ | ✅ | ✅ DONE | — |
| **Analytics** | | | | | | | |
| Usage tracking | ✅ | ✅ | ✅ | ❌ P2 | Gap |
| Team analytics | ✅ | ❓ | ❓ | ❌ P2 | Gap |
| Virality prediction | ✅ | ❓ | ❓ | ✅ DONE | Equal |

---

## PARTE 6: ROADMAP DE IMPLEMENTAÇÃO

### P0 - Essentials (fazer já - Core Differentiation)

- [ ] **Social Scheduler** — Calendar UI + scheduling backend + post queue
- [ ] **Direct Social Posting** — OAuth apps (TikTok, IG, YT, LinkedIn)
- [ ] **Multiple video sources** — Google Drive, Vimeo, Zoom, Loom, Riverside, Rumble, Twitch, Frame.io
- [ ] **BIA-style podcast AI** — Fine-tuned model for Brazilian podcasts/lives
- [ ] **Live Monitoring** — Stream ingestion (HLS/RTMP) + real-time clip generation

### P1 - Differentiation (próximos 30-60 dias)

- [ ] **Multiple aspect ratios** — 16:9, 1:1, 4:5 support
- [ ] **Brand Templates** — Multi-template system with logo/color/font
- [ ] **Team/Workspace** — Multi-tenant with seats and permissions
- [ ] **PT-BR localization** — Full i18n Portuguese
- [ ] **Face tracking reframe** — Object tracking for auto-reframe
- [ ] **Emotion/humor detection** — Extended AI analysis

### P2 - Nice to Have (60-90 dias)

- [ ] **Webhooks** — Event callback system
- [ ] **Zapier integration** — REST API + Zapier app
- [ ] **Public API** — Open API spec for external developers
- [ ] **Billing/Stripe** — Plan system with subscriptions
- [ ] **Translation** — Auto-translate subtitles
- [ ] **Multi-language transcription** — Extended language support
- [ ] **Adobe Premiere/DaVinci export** — XML export

### P3 - Future (90+ dias)

- [ ] **SSO/SAML** — Enterprise auth (WorkOS/Auth0)
- [ ] **White-label** — Full branding customization
- [ ] **Mobile app** — iOS/Android
- [ ] **AI studio** — Full video generation (VidRush territory)

---

## PARTE 7: ANÁLISE ESTRATÉGICA

### 7.1 Vantagens Competitivas do SupoClip

| Vantagem | Descrição |
|----------|-----------|
| Open Source | Transparência, comunidade, self-hosting option |
| Multi-LLM | Google/OpenAI/Anthropic/Ollama flexibility |
| PostgreSQL | Schema mais robusto que MongoDB da OpusClip |
| Better Auth | Auth moderno com banyak providers |
| Clean Architecture | Codebase manutenível |
| AGPL-3.0 | Libre com commercial options |

### 7.2 Riscos e Gaps Críticos

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Sem Social Scheduler | Usuários não ficam no produto | Priorizar P0 |
| Sem direct posting | Não captura valor do workflow | Priorizar P0 |
| Single user only | Não serve agências | Team workspace P1 |
| Sem monetization | Não valida willingness to pay | Billing P2 |
| Sem API | Builders não conseguem integrar | API pública P2 |

### 7.3 Oportunidades de Mercado

1. **API pay-per-use** — OpusClip API é closed beta com barreira alta
2. **Brasil market** — Real Oficial validou, sem competitor open source
3. **Self-hosted option** — Enterprise que não quer dados em cloud
4. **Agências** — Workspace multi-client que OpusClip não suporta bem
5. **Live clipping** — Feature que nenhum competidor oferece bem

---

## PARTE 8: FONTS

| Documento | Data | Linhas |
|-----------|------|--------|
| opusclip-reverse-engineer-20260311.md | 2026-03-11 | 368 |
| realoficial-reverse-engineer-20260312.md | 2026-03-12 | 266 |
| vidrush-reverse-engineer-20260312.md | 2026-03-12 | 265 |
| CLAUDE.md | — | 247 |

---

*Generated: Full Feature Audit v1.0*
*Analysis date: 2026-04-14*
