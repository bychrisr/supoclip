# Complete Feature Matrix — SupoClip vs Concorrentes

**Data de criação:** 2026-04-14  
**Fonte:** Análise competitiva de OpusClip, Real Oficial e VidRush + baseline SupoClip (CLAUDE.md)  
**Objetivo:** Mapa completo de features para roadmap de desenvolvimento

---

## 1. CORE VIDEO PROCESSING

| Feature | OpusClip | Real Oficial | VidRush | SupoClip | Gap |
|---------|----------|--------------|---------|----------|-----|
| **YouTube import** | ✅ | ✅ | ❌ | ✅ | DONE |
| **Upload direto (MP4)** | ✅ | ✅ | ✅ | ✅ | DONE |
| **URLs múltiplas** | ✅ GDrive, Vimeo, Zoom, Rumble, Twitch, FB, LinkedIn, X, Loom, Riverside, Frame.io, StreamYard | ❌ | ❌ | ❌ | P2 |
| **AI clip selection** | ✅ ClipAnything (áudio, visual, emoção, gênero) | ✅ BIA (18 parâmetros, podcasts BR) | ✅ AI generation | ✅ Pydantic AI | DONE |
| **Auto reframe (ReframeAnything)** | ✅ object tracking | ❌ | ❌ | ❌ | **P1** |
| **Virality scoring** | ✅ score proprietário 0-100 | 🔍 inferred | ❌ | ✅ (hook, engagement, value, shareability) | DONE |
| **Face detection/centered** | ✅ | ✅ | ❌ | ✅ MediaPipe → OpenCV → Haar | DONE |
| **Transcript + captions** | ✅ 97%+ accuracy | ✅ | ✅ | ✅ AssemblyAI | DONE |
| **Animated captions** | ✅ 97%+ accuracy + emoji highlights | ✅ | ❌ | ❌ | **P0** |
| **Brand templates** | ✅ (font, cor, logo, intro/outro) | ✅ Brand Kit | ❌ | ❌ | **P1** |
| **B-roll auto** | ✅ AI B-Roll (50 clips/dia Pro) | ❌ | ✅ (stock video/image API) | ✅ Pexels API | DONE |
| **Transições** | ✅ | ✅ | ❌ | ✅ | DONE |
| **Custom fonts** | ✅ | ✅ | ✅ | ✅ (TTF em backend/fonts/) | DONE |
| **Text-to-video (geração)** | ❌ | ❌ | ✅ | ❌ | N/A (different workflow) |
| **Faceless generation** | ❌ | ❌ | ✅ | ❌ | N/A (different workflow) |
| **Live monitoring** | ❌ | ✅ (118 streams) | ❌ | ❌ | **P1** |

---

## 2. EXPORT & OUTPUT

| Feature | OpusClip | Real Oficial | VidRush | SupoClip | Gap |
|---------|----------|--------------|---------|----------|-----|
| **TikTok export** | ✅ | ✅ | ✅ | ✅ | DONE |
| **YT Shorts** | ✅ | ✅ | ✅ | ✅ | DONE |
| **IG Reels** | ✅ | ✅ | ✅ | ✅ | DONE |
| **LinkedIn** | ✅ | ❌ | ❌ | ❌ | **P2** |
| **Facebook** | ✅ | ❌ | ❌ | ❌ | **P2** |
| **X (Twitter)** | ✅ | ❌ | ❌ | ❌ | **P2** |
| **Snapchat** | 🔍 coming | ❌ | ❌ | ❌ | P3 |
| **Custom aspect ratios** | ✅ (9:16, 1:1, 16:9, outros) | ✅ (9:16 + horizontal) | ❌ | ❌ (9:16 only) | **P0** |
| **XML export (Premiere)** | ✅ | ❌ | ❌ | ❌ | **P2** |
| **XML export (DaVinci)** | ✅ | ❌ | ❌ | ❌ | **P2** |
| **1080p export** | ✅ | ✅ unlimited (Lite+) | ✅ | ✅ | DONE |
| **4K export** | ✅ Pro+ | ❌ | ❌ | ❌ | P3 |
| **Export presets** | ✅ | ✅ | ✅ | ✅ (TikTok, Instagram) | DONE |

---

## 3. WORKFLOW & AUTOMATION

| Feature | OpusClip | Real Oficial | VidRush | SupoClip | Gap |
|---------|----------|--------------|---------|----------|-----|
| **Social Scheduler** | ✅ (YT, TikTok, IG, LinkedIn, FB, X) | ✅ | ❌ | ❌ | **P0** |
| **Auto post (direct)** | ✅ | ✅ | ❌ | ❌ | **P1** |
| **Batch editing** | ✅ | ✅ | ✅ | ❌ | **P1** |
| **Cloud queue (background)** | ✅ | ✅ | ✅ (50-60 min) | ❌ | **P1** |
| **Webhooks** | 🔍 inferred | ❌ | ❌ | ❌ | **P1** |
| **Zapier integration** | ✅ Pro | ❌ | ❌ | ❌ | **P2** |
| **Make.com (Integromat)** | ✅ community | ❌ | ❌ | ❌ | **P2** |
| **API pública** | ✅ closed beta (20+ packs annual) | ❌ | ❌ | ❌ | **P1** |
| **Editor pós-geração** | ✅ | ✅ (profissional) | ✅ (swap clips, edit audio) | ✅ (trim, split, merge) | DONE |

---

## 4. COLLABORATION & TEAMS

| Feature | OpusClip | Real Oficial | VidRush | SupoClip | Gap |
|---------|----------|--------------|---------|----------|-----|
| **Team seats** | ✅ 2-4 (Pro) | ✅ | ✅ 0-10 (por tier) | ❌ | **P1** |
| **Workspaces** | ✅ | ✅ | ✅ | Limited (single user) | **P1** |
| **Team templates** | ✅ | ❌ | ❌ | ❌ | **P2** |
| **Client sub-workspace** | 🔍 coming | ❌ | ❌ | ❌ | **P2** |
| **Member permissions** | 🔍 coming | ❌ | ❌ | ❌ | P2 |

---

## 5. LOCALIZATION & UX

| Feature | OpusClip | Real Oficial | VidRush | SupoClip | Gap |
|---------|----------|--------------|---------|----------|-----|
| **PT-BR localization** | ❌ | ✅ native | ❌ | ❌ | **P0** |
| **PT-BR support** | ❌ | ✅ (BIA optimized) | ❌ | ❌ | **P0** |
| **Multi-language UI** | ✅ 26+ languages | ✅ (EN, PT, ES) | ✅ | ❌ | **P1** |
| **Live monitoring** | ❌ | ✅ (118 streams) | ❌ | ❌ | **P1** |
| **Progress real-time** | ✅ polling 15s | ✅ | ✅ | ✅ SSE | DONE |
| **Dark mode** | ✅ | ✅ | ✅ | ❌ | **P2** |
| **Mobile app** | ❌ | 🔍 | ❌ | ❌ | **P3** |
| **Queue visibility** | ✅ | ✅ | ✅ | ❌ | **P1** |

---

## 6. BILLING & PRICING

| Feature | OpusClip | Real Oficial | VidRush | SupoClip | Gap |
|---------|----------|--------------|---------|----------|-----|
| **Free tier** | ✅ 60 min/mês (watermark) | ✅ 60 credits (signup) | ❌ | ✅ (task limits) | DONE |
| **Paid plans** | ✅ $15-$29/mo | ✅ R$59-149/mo | ✅ $99-1750/mo | ✅ Stripe Pro | DONE |
| **Credits/minute** | ✅ opaque | ✅ ~R$0.10/min | ✅ ~$1.70/min | ❌ | **P0** |
| **PAYG (pay-as-you-go)** | ✅ packs | ✅ credits avulsos | ✅ | ❌ | **P1** |
| **Team seats billing** | ✅ per seat | ❌ | ✅ per seat | ❌ | **P1** |
| **White-label** | ✅ Business | ❌ | ✅ (implied) | ❌ | **P2** |
| **Annual discount** | ✅ (~50% savings) | ❌ | ✅ (20% savings) | ❌ | P2 |

---

## 7. SUPPORT & ONBOARDING

| Feature | OpusClip | Real Oficial | VidRush | SupoClip | Gap |
|---------|----------|--------------|---------|----------|-----|
| **Intercom live chat** | ✅ Pro+ | ❌ | ❌ | ❌ | P2 |
| **Discord community** | ✅ free | ✅ | ❌ | ✅ (feedback webhook) | DONE |
| **Dedicated Slack** | ✅ Business | ❌ | ❌ | ❌ | P2 |
| **Documentation** | ✅ help.opus.pro | ✅ | ✅ docs.vidrush.ai | ❌ | **P1** |
| **API docs** | ✅ developer.opus.pro | ❌ | ❌ | ❌ | P2 |

---

## 8. CUSTOMIZATION & TOOLS

| Feature | OpusClip | Real Oficial | VidRush | SupoClip | Gap |
|---------|----------|--------------|---------|----------|-----|
| **Custom script upload** | ❌ | ❌ | ✅ | ❌ | N/A |
| **Custom voiceover upload** | ❌ | ❌ | ✅ | ❌ | N/A |
| **Reference video (estilo)** | ❌ | ❌ | ✅ | ❌ | N/A |
| **Thumbnail generator** | ❌ | ❌ | ✅ | ❌ | **P2** |
| **Translation (captions)** | ❌ | 🔍 coming (Viral) | ❌ | ❌ | **P2** |
| **Thumbnail customization** | ✅ | ❌ | ✅ | ❌ | **P2** |
| **Custom intro/outro** | ✅ Brand templates | ✅ | ❌ | ❌ | **P1** |

---

## 9. OBSERVABILITY & DEVEX

| Feature | OpusClip | Real Oficial | VidRush | SupoClip | Gap |
|---------|----------|--------------|---------|----------|-----|
| **Sentry** | ✅ | ❌ | ✅ | ❌ | P2 |
| **Feature flags** | ✅ Statsig | ❌ | ❌ | ❌ | P2 |
| **Analytics de produto** | ✅ (mp.opus.pro proxy) | ✅ Himetrica | ❌ | ❌ | P2 |
| **Status page** | ✅ trust.opus.pro | ❌ | ❌ | ❌ | P3 |

---

## 10. COMPARATIVE SUMMARY

| Dimensão | OpusClip | Real Oficial | VidRush | SupoClip |
|----------|----------|--------------|---------|----------|
| **Maturidade** | 🏆 Leader (16M users, 8-figure ARR) | 🥈 Challenger (2.4k users, BR focus) | 🥉 Early (no public traction) | 🥉 Early (open source) |
| **Preço entrada** | $15/mo | R$59.90/mo (~$11) | $99/mo | FREE (self-hosted) |
| **Strength** | Features + scale | Localization + pricing | Niche (faceless) | Open source + cost |
| **Gap principal** | — | API + scheduling | Everything | Localization + export |
| **Diferencial** | ReframeAnything + Virality Score | BIA (podcasts BR) + Live monitoring | Text-to-video + faceless | Self-hosted + no vendor lock |

---

## SUMMARY: Features a Implementar

### P0 — CRITICAL (Must Have)

| # | Feature | Justificativa | Concorrente Ref |
|---|---------|---------------|-----------------|
| 1 | **Animated captions** | OpusClip: 97%+ accuracy + emoji highlights. SupoClip tem legendas estáticas syncadas. Sem isso, usuário não consegue competir em qualidade visual. | OpusClip |
| 2 | **Custom aspect ratios** | OpusClip: 9:16, 1:1, 16:9. SupoClip só 9:16. Usuário não consegue criar para LinkedIn/YT em outro formato. Limita muito o output. | OpusClip, Real Oficial |
| 3 | **PT-BR localization** | Real Oficial: native PT-BR + BIA otimizada. Mercado brasileiro é o segundo maior para video clipping. Sem isso, não consegue competir localmente. | Real Oficial |
| 4 | **Social Scheduler** | OpusClip + Real Oficial: post direto para YT/TikTok/IG/LinkedIn/FB/X. SupoClip só exporta. Sem scheduler, usuário precisa manual post em cada plataforma — friction mata adoção. | OpusClip, Real Oficial |
| 5 | **Transparent billing (per-minute)** | OpusClip: credits opaque. Real Oficial: ~R$0.10/min. Usuário quer saber "quanto custa processar 1 minuto de vídeo". Sem transparência, confiança erode. | All |

### P1 — HIGH PRIORITY (Should Have)

| # | Feature | Justificativa | Concorrente Ref |
|---|---------|---------------|-----------------|
| 6 | **Auto reframe (ReframeAnything)** | OpusClip feature proprietária. Object tracking para reframing automático. Competidor diferencial forte. | OpusClip |
| 7 | **Virality scoring (enhanced)** | OpusClip: score proprietário. SupoClip já tem 4 sub-scores (hook, engagement, value, shareability) mas não expõe como feature UX. Agregar valor. | OpusClip |
| 8 | **Brand templates** | OpusClip: font/color/logo/intro/outro. Real Oficial: Brand Kit. Sem isso, usuário não mantém consistência visual entre clips. | OpusClip, Real Oficial |
| 9 | **API pública** | OpusClip: closed beta (20+ packs). Demanda huge de developers/SaaS builders. API-first desde dia 1 é diferencial vs OpusClip. | OpusClip |
| 10 | **Webhooks** | Necessário para automação + integração com sistemas externos. OpusClip provavelmente tem internamente. | OpusClip |
| 11 | **Workspaces + Team seats** | OpusClip: 2-4 seats. VidRush: 0-10 per tier. SupoClip: single user only. Agency market exige isso. | OpusClip, VidRush |
| 12 | **Real-time queue visibility** | User quer ver posição na fila, tempo estimado. VidRush: 50-60 min queue visible. | VidRush, Real Oficial |
| 13 | **Live monitoring** | Real Oficial: 118 streams. Nicho podcasts/lives. Diferencial técnico interessante. | Real Oficial |
| 14 | **Multi-language UI** | OpusClip: 26+. Basic i18n infrastructure needed para global market. | OpusClip |
| 15 | **Batch editing** | Real Oficial + VidRush: edição em massa. Usuário quer editar múltiplos clips de uma vez. | Real Oficial, VidRush |

### P2 — MEDIUM PRIORITY (Nice to Have)

| # | Feature | Justificativa | Concorrente Ref |
|---|---------|---------------|-----------------|
| 16 | **LinkedIn export** | OpusClip. Mercado profissional. Usuários B2B querendo distribuir para LinkedIn. | OpusClip |
| 17 | **XML export (Premiere/DaVinci)** | OpusClip. Pro users querem editar em timeline profissional. | OpusClip |
| 18 | **Zapier integration** | OpusClip Pro. Automação business. | OpusClip |
| 19 | **Make.com integration** | OpusClip community. Alternativa ao Zapier. | OpusClip |
| 20 | **Thumbnail generator** | VidRush. Usuário quer thumbnail além do clip. | VidRush |
| 21 | **Dark mode** | All three have it. Basic UX expectation. | All |
| 22 | **Documentation (public)** | OpusClip: help.opus.pro. VidRush: docs.vidrush.ai. Usuário precisa saber como usar. | All |
| 23 | **Translation (captions)** | Real Oficial: coming no Viral. Usuário quer traduzir captions para outros idiomas. | Real Oficial |
| 24 | **Custom intro/outro** | OpusClip: via Brand Templates. Usuário quer watermark/CTA no clip. | OpusClip |
| 25 | **White-label** | OpusClip Business + VidRush. Agencies querem marca própria. | OpusClip |

### P3 — LOW PRIORITY (Future)

| # | Feature | Justificativa | Concorrente Ref |
|---|---------|---------------|-----------------|
| 26 | **Mobile app** | Long-term. Not core para MVP. | — |
| 27 | **Snapchat export** | OpusClip: coming. Nicho menor. | OpusClip |
| 28 | **4K export** | OpusClip Pro+. Demanda niche. | OpusClip |
| 29 | **Status page** | Ops requirement. | OpusClip |

---

## ROADMAP SUGGESTION

### Fase 1: MVP Competitivo (P0)
- Animated captions
- Custom aspect ratios (1:1, 16:9)
- PT-BR localization
- Social scheduler (initial: schedule + export, not direct post)
- Per-minute transparent billing

### Fase 2: Feature Parity (P1)
- API pública
- Webhooks
- Workspaces + Team seats
- Brand templates
- Auto reframe
- Enhanced virality scoring
- Multi-language i18n
- Live monitoring (stretch)

### Fase 3: Ecosystem (P2)
- XML export
- LinkedIn export
- Zapier/Make
- Thumbnail generator
- Batch editing
- Dark mode

### Fase 4: Scale (P3)
- Mobile app
- White-label
- 4K export

---

## NOTES

1. **SupoClip's advantage:** Open source + self-hosted = no vendor lock-in. Can compete on transparency (per-minute billing) + localization (PT-BR) where OpusClip fails.

2. **Real Oficial insight:** BIA specialized for podcasts is the moat. For SupoClip, consider fine-tuning AI model for BR content (podcasts, lives) as differentiation.

3. **VidRush is NOT a direct competitor** — different workflow (generation vs clipping). But their team/multi-workspace features are relevant.

4. **OpusClip's moat:** Not just features — it's scale (16M users) + proprietary models (ClipAnything, ReframeAnything) + distribution (PLG). Hard to compete head-on. Go niche (PT-BR) or go open-source (self-hosted).

---

*Document generated from competitor analysis. Update when new competitive intelligence is available.*