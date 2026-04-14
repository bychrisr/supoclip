# Story: Credit Packs

- **Epic:** epic-features.md
- **Fase:** FASE 3 - Team/Agency
- **Priority:** P2
- **Estimate:** 16h

## Problem

Some users prefer pay-as-you-go without recurring subscriptions. Currently, only subscription plans are available. Without credit packs:

- Barriers for occasional users who don't want subscriptions
- Cannot upsell from free tier with one-time purchases
- No way to handle overage/extra usage
- Limited flexibility in pricing model

## Solution

Implement one-time credit pack purchases that can be used for video processing. Credits never expire and apply to workspace balance.

## Scope

- **In:** Stripe integration, usage tracking
- **Out:** Auto-replenishment subscriptions, credit marketplace

### In Scope
- Credit pack product tiers (100, 500, 1000 credits)
- One-time purchase checkout flow
- Credits added to workspace balance
- Credit balance display in account
- Credit usage in processing (deduct from balance)
- No expiration on purchased credits

### Out of Scope
- Auto-replenishment (subscription on credits)
- Credit resale/marketplace
- Credit transfer between workspaces

## Tasks

1. [ ] Create Stripe one-time products for credit packs
2. [ ] Add credit pack purchase UI
3. [ ] Implement credit balance in workspace
4. [ ] Add credits deduction in processing flow
5. [ ] Create credit balance display component
6. [ ] Add credits to checkout flow
7. [ ] Implement credit purchase history
8. [ ] Add "buy credits" CTA in low balance state

## Acceptance Criteria

- [ ] Users can purchase 100, 500, or 1000 credit packs
- [ ] Credits never expire after purchase
- [ ] Credits deduct automatically on processing
- [ ] Balance shows in account settings
- [ ] Purchase history shows credit transactions
- [ ] Low balance triggers "buy more" prompt
- [ ] Credit packs available in checkout

## Dependencies

- Backend: FastAPI (existing)
- Payment: Stripe (existing integration)
- Frontend: Next.js (existing)
- Plan: story-features-billing.md, story-features-transparent-billing.md