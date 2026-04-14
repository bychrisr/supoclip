# SupoClip — Frontend Spec

## Visão Geral

Frontend da aplicação SupoClip, ferramenta de clipping de vídeos com AI. A interface permite ao usuário inserir vídeos do YouTube ou arquivos locais, customizar legendas e configurações de fonte, processar o conteúdo via API backend, e baixar os clips gerados.

O frontend segue uma arquitetura client-heavy, com a maioria das páginas e componentes marcados como `"use client"`. A aplicação faz uso intensivo de shadcn/ui como base de componentes, com customizações para o tema stone e estilo New York.

## Stack

| Tecnologia | Versão | Observação |
|-----------|-------|------------|
| Next.js | 15 | App Router |
| React | 19 | — |
| TailwindCSS | 4 | Tema com tokens OKLCH |
| shadcn/ui | — | Radix primitives |
| Better Auth | — | Autenticação |
| TypeScript | — | — |
| Lucide React | — | Ícones |

## Estrutura de Arquivos

```
frontend/src/
├── app/
│   ├── page.tsx                    # Dashboard + Create
│   ├── globals.css                 # Tokens de design
│   ├── sign-in/page.tsx
│   ├── sign-up/page.tsx
│   ├── list/page.tsx               # All generations
│   ├── settings/page.tsx
│   ├── admin/page.tsx
│   └── tasks/[id]/
│       ├── page.tsx                 # Task detail
│       └── edit/page.tsx            # Clip editor
├── components/
│   ├── ui/                       # shadcn/ui components
│   ├── landing-page.tsx
│   ├── feedback-button.tsx
│   ├── dynamic-video-player.tsx
│   └── auth/
│       ├── sign-in.tsx
│       └── sign-up.tsx
└── lib/
    ├── utils.ts                    # cn() helper
    ├── auth-client.ts
    └── ...
```

## Design System

### Cores (Light Mode)

O tema utiliza OKLCH para定義 de cores, com base stone:

```
--primary: oklch(0.216 0.006 56.043)      # Stone 900
--secondary: oklch(0.97 0.001 106.424)    # Stone 100
--accent: oklch(0.97 0.001 106.424)     # Stone 100
--background: oklch(1 0 0)              # White
--foreground: oklch(0.147 0.004 49.25)  # Stone 147
--muted: oklch(0.97 0.001 106.424)      # Stone 100
--muted-foreground: oklch(0.553 0.013 58.071)  # Stone 556
--destructive: oklch(0.577 0.245 27.325)  # Red
--border: oklch(0.923 0.003 48.717)   # Stone 235
--input: oklch(0.923 0.003 48.717)    # Stone 235
--ring: oklch(0.709 0.01 56.259)       # Stone 450
```

### Cores (Dark Mode)

```
--primary: oklch(0.923 0.003 48.717)   # Stone 500
--background: oklch(0.147 0.004 49.25) # Stone 147
--foreground: oklch(0.985 0.001 106.423)  # White
```

### Tipografia

- Fontes primárias: Geist Sans, Geist Mono (via Next.js font loader)
- Fontes customizáveis pelo usuário para legendas de vídeo
- Escalas: texto-base 16px, headings 2xl a 5xl

### Espaçamento

- Container principal: `max-w-6xl` a `max-w-7xl`
- Padding padrão: `px-4` a `px-6`
- Gap entre seções: `gap-4` a `gap-10`

### Border Radius

- Padrão: `0.625rem` (10px)
- Buttons: `rounded-md` ou `rounded-xl` para CTAs maiores
- Cards: `rounded-xl`
- Inputs: `rounded-md`

## Componentes UI

### shadcn/ui Components

| Componente | Arquivo | Descrição |
|-----------|--------|----------|
| Button | button.tsx | CVA com variants (default, destructive, outline, secondary, ghost, link) |
| Input | input.tsx | Input básico com estilos de focus |
| Card | card.tsx | Card com Header, Content, Footer, Title, Description |
| Badge | badge.tsx | Tags e status badges |
| Alert | alert.tsx | Mensagens de erro/sucesso |
| Select | select.tsx | Dropdown via Radix Select |
| Slider | slider.tsx | Controle de tamanho de fonte |
| Switch | switch.tsx | Toggle para opões |
| Avatar | avatar.tsx | Foto de perfil do usuário |
| Progress | progress.tsx | Barra de progresso |
| Skeleton | skeleton.tsx | Loading states |
| Popover | popover.tsx | Feedback button |
| Separator | separator.tsx | Divisores visuais |
| Textarea | textarea.tsx | Input de texto longo |
| Label | label.tsx | Labels de formulário |
| AlertDialog | alert-dialog.tsx | Confirmações de delete |
| Sonner | sonner.tsx | Toast notifications |

### Custom Components

| Componente | Arquivo | Descrição |
|-----------|--------|----------|
| LandingPage | landing-page.tsx | Página de marketing completa com scroll animations |
| FeedbackButton | feedback-button.tsx | Botão flutuante de feedback via Popover |
| DynamicVideoPlayer | dynamic-video-player.tsx | Player de vídeo com controles |
| AdminUserToggle | admin/admin-user-toggle.tsx | Toggle admin para usuários |

## Páginas e Fluxos

### Fluxo Principal (Autenticado)

```
Sign In / Sign Up → Dashboard (home) → Create Task → Processing → Task Detail → Download
                              ↘︎ Settings ↘︎ All Generations (list)
```

### Página: Dashboard (`/`)

- Header com logo, badge de plano, botão de sign out, avatar
- Latest task banner (se existir)
- Formulário principal de criação:
  - Source type tabs (YouTube URL / Upload video)
  - Inputs condicionais
  - Seção "Style & Captions" com:
    - Caption template selector
    - AI B-roll toggle (conditional)
    - Wide format toggle
    - Add subtitles toggle
    - Video quality selector
  - Seção "Font Customization" (collapsible):
    - Font family selector
    - Font size slider (12-48px)
    - Color picker com presets
  - Loading state com progresso e steps
  - Error state com Alert
- Live phone preview (desktop only)

### Página: Task Detail (`/tasks/[id]`)

- Header com título editável, status, botões de ação
- Estados:
  - Processing/queued: animated dots + progresso
  - Error: mensagem de erro
  - Empty: "no clips generated"
  - Completed: lista de clips
- Card de Project Settings (font, size, color, template, b-roll)
- Lista de clips com:
  - Video player
  - Virality score breakdown (hook, engagement, value, shareability)
  - Transcript
  - AI Analysis
  - Ações: Download, Export (TikTok/Reels/Shorts), Edit, Delete
- Edit mode inline para trim, split, regenerate
- Alert dialogs para delete (task e clip)

### Página: All Generations (`/list`)

- Header com título
- Lista de tasks com:
  - Título
  - Badge de status (completed, processing, queued, error)
  - Tipo(fonte)
  - Data de criação
  - Quantidade de clips
- Empty state se nenhuma geração
- Loading skeletons

### Página: Settings (`/settings`)

- Default Font Settings:
  - Font family selector
  - Font size slider
  - Color picker com presets
  - Preview
- Billing (se monetization enabled)
- Save button

### Landing Page (`/` quando não autenticado)

- Hero section com CTAs
- "How It Works" com 3 steps
- "Features" com 6 cards
- Open source section com código
- Final CTA + waitlist (se mode enabled)
- Footer

### Páginas de Auth

- Sign In: Email/password form
- Sign Up: Email/password form
- Ambas com validação básica e error states

## Estados e Feedback

### Loading States

- Skeletons para página e lista
- Spinner (Loader2) para ações
- Progress bar com percentage
- Animated dots para processing longo

### Error States

- Alert component com mensagem
- Toast errors via Sonner
- Inline error messages

### Empty States

- All generations: "No generations yet"
- Task detail: "No clips generated"
- Alguns casos sem empty state adequado

### Success States

- Toast via Sonner
- Alert de sucesso em settings
- Redirect automático

## Responsividade

### Breakpoints Utilizados

- `sm: block` — Small (640px+)
- `md: flex` — Medium (768px+)
- `lg: col-span-2` — Large (1024px+)
- `hidden lg:block` — Phone preview only on desktop

### Observações

- Header user info: `hidden sm:block` em mobile
- Phone preview: `hidden lg:block` — só desktop
- Grid layouts: `grid-cols-1 lg:grid-cols-5`
- Cárdas de fonte: grid responsivo com `md:grid-cols-2 lg:grid-cols-4`

## Acessibilidade

### Pontos Positivos

- uso de Radix primitives (Select, Popover, AlertDialog) com ARIA nativo
- Labels em inputs de formulários
- Focus visible: `focus-visible:ring-ring/50`
- role="alert" em Alert components
- Keyboard navigation em Select e Dialogs

### Pontos de Atenção

-Alguns botões sem aria-label (ex: edit, delete icons)
- Color contrast: stone-500 em backgrounds claros pode ser insuficiente
- Skip links não implementados
- announcement de status em processing via live regionausente
- Loading skeletons sem aria-busy

## Débitos UX/UI Identificados

| ID | Débito | Severidade | Impacto | Prioridade |
|-----|---------|------------|---------|------------|
| UX-001 | Quase todas as páginas com "use client" — sem Server Components | Média | Performance e SEO afetados | Alta |
| UX-002 | Inconsistent loading states — task edit não tem skeleton | Baixa | Experiência de carregamento inconsistente | Média |
| UX-003 | Empty state faltando em task edit page | Baixa | Usuário podeahar confuso | Média |
| UX-004 | Botões icon sem aria-label (edit, delete clip) | Média | Acessibilidade comprometida | Alta |
| UX-005 | Phone previewhidden em mobile | Baixa | Usuário não visualiza preview | Baixa |
| UX-006 | Color contrast stone-500 em backgrounds claros | Média | WCAG AA não cumprido | Alta |
| UX-007 | Inconsistent button styles entre páginas | Baixa | Visual não padronizado | Média |
| UX-008 | Error handling direto com alert() | Média | Experiência ruim | Média |
| UX-009 | Direct fetch calls sem loading robusto emalgumas áreas | Baixa | Estados de erro não tratados | Média |
| UX-010 | Landing page heavy em client-side animations | Média | Performanceem devices lentos | Baixa |

## Recomendações

### Alta Prioridade

1. **Server Components** — Migrar páginas que não dependem de client state para Server Components (list, settings, landing page estática). Isso reduz bundle size e melhora performance e SEO.

2. **Aria Labels em Botões Icon** — adicionar `aria-label` ou `aria-labelledby` em todos os botões de ícone:

```tsx
<Button size="sm" variant="ghost" aria-label="Edit title" onClick={...}>
  <Edit2 className="w-4 h-4" />
</Button>
```

3. **Color Contrast** — revisar cores em backgrounds claros. Substituir stone-500 por stone-600 ou stone-700 em texto corpo.

### Média Prioridade

4. **Loading StatesUniformes** — adicionar Skeleton em task edit page e outras áreas que fazem fetch sem skeleton.

5. **Empty State em Task Edit** — adicionar empty state para quando task não tem clips:

```tsx
{clips.length === 0 && (
  <Card>
    <CardContent className="p-8 text-center">
      <p>Nenhum clip gerado ainda.</p>
    </CardContent>
  </Card>
)}
```

6. **Error Handling** — substituir `alert()` por componente de erro ou toast:

```tsx
// Em vez de:
alert("Error message")

// Usar:
toast.error("Error message")
// ou Alert component
```

7. **Button Consistency** — unificar estilos de botão primário entre páginas (todos `w-full h-12 text-base rounded-xl`).

### Baixa Prioridade

8. **Phone Preview Mobile** — considerar versão simplificada ou collapsible para mobile.

9. **Loading Skeletons aria-busy** — adicionar `aria-busy="true"` skeletons.

10. **Skip Links** — adicionar skip link para navegação keyboard.

## Métricas de ROI (Design System)

### Potencial de Consolidação

| Área | Atual |.after Design System | Redução |
|------|-------|------------------|--------|
| Button variants | inline em cada página | Tokens CSS | ~70% código repetido |
| Cores | hardcoded no CSS | Design tokens | ~40% |
| Espaçamento | varied | Consistent spacing scale | ~30% |
| Loading states | por componente | Componente reutilizável | ~50% |

### Custos Estimados

- Implementação full design system: ~2-3 sprints
- ROI esperado: ~34.6x em manutenção
- Débitos de acessibilidade: ~0.5 sprints

## Histórico

- **Created**: 2026-04-14
- **Fase**: brownfield-discovery FASE 3
- **Analista**: @ux-design-expert