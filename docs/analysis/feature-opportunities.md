# Feature Opportunities - SupoClip

## Web Research Results

This document compiles web research on the AI video clipping competitive landscape, focusing on OpusClip (the market leader) and alternatives. The goal is to identify feature opportunities for SupoClip.

---

### OpusClip Current State

**Pricing (March 2026)**

| Plan | Price | Credits | Key Features |
|-------|-------|---------|--------------|
| Free | $0/mo | 60 min/mo | Watermark, 1080p, 3-day storage |
| Starter | $15/mo | 150 min/mo | No watermark, virality score, auto-captions |
| Pro | $29/mo ($14.50 annual) | 300 min/mo | AI B-Roll, social scheduler, XML export, team workspace, 100GB |
| Business | Custom | Custom | API access, SSO, unlimited seats |

**Key Features**
- ClipAnything AI: multimodal analysis (speech, visuals, emotion) - handles any video genre (podcasts, interviews, gaming, vlogs)
- Virality Score (0-100) for clip prioritization
- Auto-reframe to 9:16, 1:1, 16:9
- Animated captions with emojis and keyword highlighting
- Active Speaker Detection with face tracking
- AI B-Roll generation (Pro: 50 clips/day)
- Direct publishing to YouTube, TikTok, Instagram, LinkedIn, Facebook
- Social media scheduling
- XML export for Premiere Pro & DaVinci Resolve
- Team workspaces (up to 4 users on Pro)
- Processing time: 2-5 minutes per video, typically generating 10-25 clips

**Limitations**
- Credit-based pricing (1 credit = 1 minute of source video)
- Per-minute pricing becomes expensive for long-form content
- API access requires Business plan (custom pricing, closed beta)
- Free plan: watermark, 3-day storage expiry, 9:16 only
- Trustpilot complaints: processing failures, hidden credit mechanics, cancellation difficulties

---

### Competitive Landscape

**Major Competitors**

| Tool | Starting Price | Best For | Key Differentiator |
|------|----------------|----------|-------------------|
| Ssemble | $7.50/mo | High-volume clippers | Per-video pricing (not per-minute), API on all plans |
| Vizard | $14.50/mo | Teams | Collaboration features, brand kits, 20 seats |
| Reap | $9.99/mo | Multilingual | AI dubbing in 80+ languages, 98+ caption languages |
| Choppity | $7.50/mo | Face-tracking | Advanced hook detection, extensive caption customization |
| CapCut | Free | Basic editing | Free option, full editor + AI clipping |
| Descript | $12/mo | Transcript editing | Edit video by editing text |
| 2Short.ai | $9.90/mo | YouTube-focused | YouTube URL only, simple interface |

**Open Source Alternatives**

| Tool | Price | Key Feature |
|------|-------|-------------|
| SupoClip (this repo) | Free, open-source | Self-hosted, unlimited usage |
| ClipPro | Free | Whisper + Gemini AI, GPU accelerated, FFmpeg cuts |
| OpenClip (AIONIX) | Free | Local-first, YouTube URL → download → auto-clip |
| ViralCutter | Free | Gemini AI, face tracking, translation |
| ClipsAI | Free | Python library, transcript-based clipping |
| Reelify AI | Free (90 hours/mo) | 90 hours free processing, local Mac app |

**Pricing Comparison**

For a 60-minute video:
- Ssemble Pro: ~$0.75 (3 credits × $0.25)
- OpusClip Pro: ~$2.90 (60 credits × $0.048)
- Vizard Creator: ~$14.50+

**Key Market Observations**
1. Credit-based pricing (per-minute) is dominant but unfavorable for long-form content
2. Per-video pricing models (Ssemble) offer 3-4x better value
3. Open-source alternatives are emerging with local processing
4. Enterprise features (API, SSO, team management) are only available at top tiers or custom pricing
5. AI dubbing/translation is becoming a differentiator (Reap leads)

---

### Opportunities for SupoClip

Based on competitive analysis, here are feature opportunities:

**1. Flexible Pricing Models**
- Consider per-video pricing (like Ssemble) instead of per-minute
- Offer tiered plans with different credit systems
- Annual billing discounts (OpusClip offers 17%)

**2. Enhanced AI Features**
- Virality scoring similar to OpusClip (Hook/Flow/Value/Trend analysis)
- Multimodal clip detection (speech + visuals + emotion)
- AI B-Roll suggestions and insertion

**3. Enterprise Features**
- API access at accessible pricing (Ssemble offers it on all plans)
- Team workspaces with role-based permissions
- Brand templates and custom assets

**4. Publishing & Distribution**
- Direct social media publishing (YouTube, TikTok, Instagram, LinkedIn)
- Scheduling calendar for automated posting
- Multi-platform export optimization

**5. Video Processing**
- Fillers words and pause removal
- Multiple aspect ratio support (9:16, 1:1, 16:9)
- Speaker diarization and face tracking
- Video enhancement (speech enhancement, auto-censor)

**6. Localization**
- Multi-language transcription (100+ languages)
- AI dubbing and translation
- Localized caption styles

**7. Open-Source Differentiators**
- Self-hosted option for privacy-sensitive users
- No watermarks (vs OpusClip free tier)
- Unlimited processing (vs 60 min/mo on free tier)
- Customizable AI prompts
- Winner learning from analytics

---

### Summary

The AI video clipping market is maturing with 10+ serious competitors. Key gaps that SupoClip can address:

1. **Pricing**: Offer more generous free tier or per-video model
2. **API Access**: Make it accessible without enterprise pricing
3. **Self-Hosting**: Position as privacy-first alternative to cloud-only tools
4. **Localization**: Add multilingual support and dubbing
5. **Team Features**: Build collaboration tools at accessible price points

---

*Research completed: April 2026*
*Sources: Ssemble, Toolradar, AI Productivity, OrbitarAI, CreatorStackClub, Vizard Blog, Clipotato, GitHub repositories (ClipPro, OpenClip, ViralCutter, ClipsAI)*