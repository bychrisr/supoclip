# Story: Annual Billing with Discount

- **Epic:** epic-features.md
- **Fase:** FASE 3 - Team/Agency
- **Priority:** P2
- **Estimate:** 16h

## Problem

Currently only monthly billing is available. Users on monthly plans have no incentive to commit longer term. Without annual billing:

- Higher customer acquisition cost due to no commitment discount
- Less predictable revenue stream
- Users on monthly plans churn more frequently
- Cannot offer competitive pricing vs annual competitors

## Solution

Implement annual billing option with ~50% discount (equivalent to 2 months free). Annual plans provide stable revenue and better customer retention.

## Scope

- **In:** Existing Stripe integration, plan system
- **Out:** Multi-year discounts, custom enterprise annual contracts

### In Scope
- Annual plan option in pricing page
- Stripe annual subscription products
- Prorated upgrades from monthly to annual
- Annual plan badge in account settings
- Cancellation handling for annual plans
- Renewal reminders before annual end

### Out of Scope
- Multi-year contracts
- Custom enterprise pricing
- Annual billing for credit packs only

## Tasks

1. [ ] Create Stripe annual subscription products
2. [ ] Add annual plan toggle in pricing UI
3. [ ] Implement proration for plan upgrades
4. [ ] Add annual plan indicator in account
5. [ ] Create renewal reminder system
6. [ ] Handle early cancellation refunds
7. [ ] Add annual discount display in checkout
8. [ ] Update billing history to show annual

## Acceptance Criteria

- [ ] Annual plan shows ~50% savings vs monthly
- [ ] Users can switch from monthly to annual
- [ ] Prorated charges applied correctly
- [ ] Account shows annual plan badge
- [ ] Renewal reminder sent 30 days before end
- [ ] Early cancellation calculates refund
- [ ] Billing history reflects annual payments

## Dependencies

- Backend: FastAPI (existing)
- Payment: Stripe (existing integration)
- Frontend: Next.js (existing)
- Plan: story-features-billing.md (transparent billing base)