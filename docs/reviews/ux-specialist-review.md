# UX Specialist Review - SupoClip

**Projeto:** SupoClip  
**Data:** 2026-04-14  
**Versão:** 1.0  
**Autor:** @ux-design-expert (Uma) — FASE 6 Brownfield Discovery

---

## Gate Status: **APPROVED**

Os débitos UX-001 a UX-010 foram validados e confirmados. Recomenda-se aprovação com ajustes de priorização baseados em impacto real no usuário.

---

## 1. Débitos Validados

| ID | Débito | Severidade Original | Severidade Ajustada | Impacto UX | Horas | Status |
|----|---------|---------------------|---------------------|------------|-------|--------|
| UX-001 | Quase todas as páginas com "use client" — sem Server Components | MEDIA | **ALTA** | Performance, SEO, Time to Interactive | 4h | VALIDATED |
| UX-002 | Inconsistent loading states — task edit não tem skeleton | BAIXA | **BAIXA** | Percepção de lentidão | 1h | VALIDATED |
| UX-003 | Empty state faltando em task edit page | BAIXA | **BAIXA** | Usabilidade | 1h | VALIDATED |
| UX-004 | Botões icon sem aria-label (edit, delete clip) | MEDIA | **ALTA** | Acessibilidade WCAG A | 2h | VALIDATED |
| UX-005 | Phone preview hidden em mobile | BAIXA | **BAIXA** | Usabilidade mobile | 0.5h | VALIDATED |
| UX-006 | Color contrast stone-500 em backgrounds claros | MEDIA | **MEDIA** | Acessibilidade WCAG AA | 2h | VALIDATED |
| UX-007 | Inconsistent button styles entre páginas | BAIXA | **BAIXA** | Consistência visual | 1h | VALIDATED |
| UX-008 | Error handling direto com alert() | MEDIA | **ALTA** | UX, Acessibilidade, Confiabilidade | 2h | VALIDATED |
| UX-009 | Direct fetch calls sem loading robusto | BAIXA | **BAIXA** | Percepção de feedback | 1h | VALIDATED |
| UX-010 | Landing page heavy em client-side animations | MEDIA | **MEDIA** | Performance | 1h | VALIDATED |

### Ajustes Realizados

| ID | Ajuste | Justificativa |
|----|--------|----------------|
| UX-001 | Severidade MEDIA → ALTA | Impacto direto em Core Web Vitals (LCP, TTI). Server Components reduzem JavaScript enviado em ~40-60%. |
| UX-004 | Severidade MEDIA → ALTA | WCAG Exigência mínima (Critério 1.4.11). Usuários de screen reader não identificam botões icon. |
| UX-008 | Severidade MEDIA → ALTA | 12 instâncias de alert() em tasks/[id]/page.tsx. Impacta experiência + acessibilidade + confiabilidade. |
| UX-001 | Esforço 2h → 4h | Requer análise por página + refatoração de estados client para server + testes. |

---

## 2. Débitos Adicionados

| ID | Débito | Severidade | Impacto UX | Horas | Prioridade |
|----|---------|------------|------------|-------|------------|
| UX-011 | Ausência de toast/notification para operações bem-sucedidas | BAIXA | Feedback positivo perdido | 1h | P2 |
| UX-012 | Empty state genérico sem actionable content na task list | MEDIA | Usabilidade, conversão | 1h | P1 |
| UX-013 | Sem validação inline em formulários (sign-in/sign-up) | BAIXA | DX, mas UX impacta borderline cases | 1h | P2 |
| UX-014 | Loading states não bloqueiam interação durante submit | MEDIA | Duplo clique, dados duplicados | 1h | P1 |
| UX-015 | Falta de keyboard navigation em task detail page | ALTA | Acessibilidade WCAG A | 2h | P0 |

---

## 3. Recomendações de Design por Componente/Área

### 3.1 Server Components (UX-001)

**Solução proposta:**

1. **Pages candidatas a Server Components:**
   - `/tasks/[id]` — pode ser Server com client islands para estados interativos
   - `/tasks/[id]/edit` — same approach
   - `/list` — Server com client para paginação/lista

2. **Estratégia de migração:**
   - Extrair `fetch` para Server Component
   - Manter estados interativos em Client Islands
   - Usar `loading.tsx` para skeleton states

3. **Estimativa:**
   - 4 páginas × 1h = 4h (inclui testes)

### 3.2 Acessibilidade - Aria Labels (UX-004)

**Solução proposta:**

```tsx
// Botões icon devem ter aria-label
<Button
  variant="ghost"
  size="icon"
  aria-label="Delete clip"
  onClick={...}
>
  <Trash2 className="h-4 w-4" />
</Button>

<Button
  variant="ghost"
  size="icon"
  aria-label="Edit task title"
  onClick={...}
>
  <Pencil className="h-4 w-4" />
</Button>
```

**Convenção adotada:**
- `{Verb} {Object}` — e.g., "Delete clip", "Edit title", "Toggle selection"
- Sem texto visível = aria-label obrigatório

### 3.3 Error Handling (UX-008)

**Solução proposta:**

Substituir `alert()` por Toast component (sonner já instalado):

```tsx
import { toast } from "sonner";

toast.success("Task updated successfully");
toast.error("Failed to delete task", {
  description: error.message,
});
```

**Impacto:**
- WCAG AA: Toast é announced via ARIA live regions
- UX: Non-blocking, não interrompe fluxo
- 代码: 12 locations para migrar

### 3.4 Loading States (UX-002, UX-014)

**Solução proposta:**

1. **Criar componente reutilizável:**
```tsx
// components/ui/loading-state.tsx
export function LoadingState({ 
  isLoading, 
  skeleton: ReactNode, 
  content: ReactNode 
}) {
  return isLoading ? skeleton : content;
}
```

2. **Bloquear double-submit:**
```tsx
<Button 
  disabled={isLoading}
  onClick={handleSubmit}
>
  {isLoading ? <Loader2 className="animate-spin" /> : "Submit"}
</Button>
```

### 3.5 Empty States (UX-003, UX-012)

**Solução proposta:**

```tsx
// components/ui/empty-state.tsx
export function EmptyState({
  icon: Icon,
  title,
  description,
  action
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center py-12 text-center">
      <Icon className="h-12 w-12 text-muted-foreground mb-4" />
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="text-muted-foreground mb-4">{description}</p>
      {action}
    </div>
  );
}
```

**Conteúdo actionable:**
- Empty task list: "Create your first video task" + CTA button

### 3.6 Color Contrast (UX-006)

**Análise técnica:**

Tokens atuais em `globals.css`:

| Token | Valor | Contraste no Light | Contraste no Dark |
|-------|-------|--------------------|-------------------|
| `--muted-foreground` | `oklch(0.553 0.013 58.071)` | ~4.5:1 ✅ | ~4.5:1 ✅ |
| `--foreground` | `oklch(0.147 0.004 49.25)` | ~14:1 ✅ | N/A |

**Veredicto:** Tokens de cor atendem WCAG AA. O draft mencionava "stone-500" que não existe no código. **Débito pode ser REMOVIDO** — falso positivo.

| ID | Decisão | Justificativa |
|----|---------|----------------|
| UX-006 | **REMOVE** | stone-500 não existe no codebase. Tokens OKLCH atendem WCAG AA. |

---

## 4. Priorização Final

### 4.1 Por Impacto no Usuário

| Prioridade | IDs | Total Esforço | Justificativa |
|------------|-----|---------------|----------------|
| **P0** | UX-004, UX-015 | 4h | WCAG A — barreira para usuários com deficiência |
| **P1** | UX-001, UX-008, UX-012, UX-014 | 8h | Performance + confiabilidade + conversão |
| **P2** | UX-002, UX-003, UX-005, UX-007, UX-009, UX-011, UX-013 | 6.5h | Melhorias incrementais |
| **P3** | UX-010 | 1h | Nice-to-have |

### 4.2 Resumo de Esforço

| Métrica | Valor |
|---------|-------|
| Débitos validados | 10 |
| Débitos ajustados | 4 |
| Débitos adicionados | 5 |
| Débitos removidos | 1 (UX-006) |
| **Total pós-revisão** | **14 débitos** |
| **Esforço total** | **~19.5h** |
| **Esforço P0-P1** | **12h** |

---

## 5. Respostas às Perguntas do @architect

### Q1: UX-001 — Quais páginas são candidatas viáveis para migração?

**Resposta:**
- `/tasks/[id]` — Server Component com islands para `handleDeleteClip`, `handleTrimClip`, etc.
- `/tasks/[id]/edit` — Mesmo padrão
- `/list` — Server para list + client para filtering/pagination

**Impacto estimado:** 4h (1h por página + 1h para pattern)

### Q2: UX-004 — Precisamos de uma convenção para labels?

**Resposta:**
Sim. Convenção adotada: `{Verb} {Object}` (ex: "Delete clip", "Edit title").

### Q3: UX-006 — A revisão de cores proposta atende WCAG AA?

**Resposta:**
Sim. Tokens OKLCH em `globals.css` já atendem WCAG AA. stone-500 não existe no codebase. Débito removido.

### Q4: UX-002, UX-003 — Devem ser componentes reutilizáveis ou inline?

**Resposta:**
Componentes reutilizáveis:
- `components/ui/loading-state.tsx`
- `components/ui/empty-state.tsx`

### Q5: UX-007 — Devem ser tokens CSS ou variants de Button component?

**Resposta:**
Variants de Button component (já existe padrão shadcn/ui). Adicionar variants:
- `variant="ghost-icon"` para icon buttons
- Centralizar em `components/ui/button.tsx`

---

## Parecer Final

### Status: **APPROVED**

**Débitos UX validados com ajustes:**
- 10 validados (4 com severidade ajustada)
- 5 adicionados
- 1 removido (falso positivo)
- Total: 14 débitos, ~19.5h

**Recomendações de próxima fase:**
1. Implementar P0-P1 primeiro (12h de esforço)
2. Criar componente de Toast/Notification antes de resolver UX-008
3. Implementar Server Components gradualmente — não Big Bang
4. Validar acessibilidade com axe-core ou Lighthouse após correções

---

## Próximos Passos

- **FASE 7 (@qa)**: Validar proposta de testes de acessibilidade automatizados
- **FASE 8**: Revisão final + roadmap

---

*Documento revisado por @ux-design-expert (Uma) — FASE 6 Brownfield Discovery*
*Signature: — Uma, desenhando com empatia 💝*
