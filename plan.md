# Development Plan — FaizZab ISO & DPDPA Toolkit Generator (FARM)

## 1) Objectives
- Deliver a secure multi-tenant PWA where clients can **see exact toolkit manifest**, pay ₹4,999, complete **guided onboarding**, get **admin verification**, then receive a **branded, org-specific toolkit** (DOCX/XLSX/PDF/ZIP) with strong document-control metadata.
- Prove the **core document-generation engine** works end-to-end (templating → validation → outputs) before building the full app.
- Preserve key compliance/marketing constraints: no certification guarantees, no “auto-compliance”, DPDPA legal disclaimer, ISO copyright respect.
- **Current status update:** Phase 1 (POC) and Phase 2 (MVP) are **complete and tested end-to-end**. Focus now shifts to **production hardening** (real auth + payments), **content expansion toward 50–75 docs/toolkit**, and **new standards**.

---

## 2) Implementation Steps

### Phase 1 — Core POC (Isolation): Document Generation + Validation (blocker)
**Goal:** deterministic generation works reliably with real files.

**User stories**
1. As an admin, I want to provide a client profile + brand + scope so the generator produces org-specific docs.
2. As a client, I want my logo/name/locations to appear correctly in every generated document.
3. As a QA reviewer, I want an automatic check that no placeholders remain and mandatory sections aren’t blank.
4. As a client, I want a ZIP download containing a complete toolkit matching the manifest.
5. As the platform, I want immutable generated outputs with a reproducible generation log.

**Steps**
- Research best practices: python-docx templating, header/footer images, table styling, XLSX generation, deterministic PDF rendering.
- Implement standalone Python POC (no DB, no auth):
  - Inputs: `client.json` (org + brand + roles + doc-control settings), `manifest.json`, template specs.
  - Generate: 1 DOCX + 1 XLSX + 1 PDF + ZIP + manifest/index.
  - Validations: no unresolved placeholders, logo present, unique doc IDs, required fields present, files openable, ZIP completeness.
  - Output `generation_report.json` with warnings/errors.
- Iterate until POC passes for multiple sample clients.

**Exit criteria**
- DOCX opens in Word, XLSX opens in Excel, PDF renders, ZIP complete, validations pass.

**Status: COMPLETE ✅**
- Implemented `toolkit_engine` using `python-docx`, `openpyxl`, `reportlab`, `zipfile`.
- POC script validates outputs and detects unresolved placeholders.

---

### Phase 2 — V1 App Development (MVP around proven core; minimal mocks)
**Goal:** end-to-end purchase → onboarding → admin approval → generation → download, for 3 standards (ISO 27001, DPDPA, ISO 9001).

**User stories**
1. As a visitor, I want to browse toolkits and see the exact manifest before paying.
2. As a client admin, I want to create an org profile + upload a logo and save onboarding as draft.
3. As a client admin, I want to pay and only then receive entitlement to proceed (server-verified).
4. As an admin, I want to review onboarding, request corrections, then approve for generation.
5. As a client admin, I want to download individual files and a full ZIP, with clear versioning and disclaimers.

**Backend (FastAPI + MongoDB)**
- Data model + tenant isolation (org_id scoping) for core entities: Users, Orgs, Standards/Toolkits, Onboarding schema + submissions, Orders/Payments, Entitlements, Invoices, GenerationJobs, GeneratedArtifacts, Downloads, AuditLogs, AdditionalRequirements/Quotations.
- Public catalogue APIs: toolkit list/detail incl **full manifest** + onboarding section preview + disclaimers.
- Commerce APIs:
  - Order create → payment verification → entitlement grant (server-side).
  - Coupon validation and price breakdown.
  - Invoice record generation.
- Onboarding engine:
  - Modular sections A–I with conditional visibility.
  - Draft save, completion percentage, final submit + declaration.
- Admin verification workflow:
  - Review queue, comments, request correction, approve/reject.
  - **Hard gate:** generation only after approved onboarding.
- Generation pipeline:
  - Integrate generator; create DOCX/XLSX/PDF + ZIP; store artifacts; log jobs.
- Security baseline:
  - RBAC, audit logs, tenant-isolated downloads (403 cross-org).

**Frontend (React + PWA)**
- Public pages: landing + catalogue, toolkit detail manifest view, login.
- Client area: dashboard, organization profile + logo upload, checkout (simulated payment), onboarding wizard, downloads, invoices, additional requests.
- Admin area: executive dashboard, review queue + detail, approve/correct/reject, generation monitor, commerce/content/clients/audit dashboards, additional requests quoting.
- PWA manifest added.

**End of Phase testing (1 round E2E)**
- catalogue → purchase → onboarding submit → admin approve → generate → download ZIP; verify tenant isolation with 2 orgs.

**Status: COMPLETE ✅**
- End-to-end tested: backend **100%**, frontend **95%+**, tenant isolation verified.
- Document generation produces ~26 artifacts + ZIP for ISO 27001 (and analogous packs for DPDPA/ISO 9001).
- Cosmetic fix implemented: pre-purchase manifest no longer shows raw placeholders (e.g., classification shown as “Client-defined”).

---

### Phase 3 — Authentication + Hardening + Commerce completeness (Production readiness)
**Goal:** replace simulations with real providers, strengthen security/compliance operations, and improve operational robustness.

**User stories**
1. As a client admin, I want Google sign-in so I don’t manage passwords.
2. As an admin, I want production-grade MFA and secure session controls.
3. As a client admin, I want OTP login backed by a real SMS gateway.
4. As an admin, I want refunds/revocation and immediate entitlement removal.
5. As compliance, I want complete audit trails for logins, downloads, approvals, and generations.

**Steps**
- Replace simulated auth:
  - Emergent-managed Google OAuth for clients.
  - Replace simulated admin MFA (`123456`) with TOTP-based MFA.
  - Replace simulated OTP (`654321`) with SMS provider integration (Twilio/MSG91/etc.), expiry and attempt controls.
- Replace simulated payment with real Razorpay:
  - Order creation, payment capture, webhook signature verification, idempotency, dispute/refund states.
- Security hardening:
  - Rate limiting (OTP/login), secure cookie strategy (if moving away from localStorage), CSP headers.
  - Optional: malware scanning pipeline for uploads.
  - Strengthen audit logs: include IP/user agent; admin impersonation logs if added.
- Operational tooling:
  - Error monitoring hooks; retry strategy for generation; storage quotas.
  - Export reports (CSV) for commerce and operational metrics.

**End of Phase testing (E2E)**
- Test: Google login, real MFA/OTP, payment verification via Razorpay webhooks, entitlement revocation, tenant isolation regression.

---

### Phase 4 — Content governance + Scaling standards/industries + Deepening toolkit completeness
**Goal:** production-ready content lifecycle, expand document depth toward 50–75 artifacts/toolkit, add new standards, and mature add-on workflows.

**User stories**
1. As an admin, I want template/content lifecycle states (Draft→Approved→Published) so no drafts leak.
2. As a client, I want industry-adapted wording without AI hallucinations.
3. As an admin, I want additional requirements → quotation → payment → controlled doc delivery.
4. As a client, I want versioned updates/superseding without changing what I already purchased.
5. As the business, I want configurable pricing (base/discount/coupon/GST/bundles/renewals).

**Steps**
- Content governance system:
  - Template versioning and lifecycle states; publish/supersede/archive.
  - Scheduled reviews and content QA checklists.
- Expand document sets toward the target:
  - Increase per-standard documents to ~50–75 with richer registers, checklists, audit packs, management review packs, evidence indexes, clause-to-document matrices.
  - Add industry add-on blocks (approved content blocks only).
- Add wave-2 standards:
  - ISO/IEC 42001 and ISO/IEC 27701 content packs + onboarding section H variants.
- Pricing engine v2:
  - Admin-configurable pricing, add-ons, renewals/updates, bundles.
- Additional requirements workflow (already present in MVP):
  - Extend to deliver controlled artifacts and link them into the toolkit’s master register.

---

## 3) Next Actions
1. **Production readiness:** swap simulated OTP/MFA/payment to real providers (Phase 3).
2. **Content expansion:** enrich template library for ISO 27001, DPDPA and ISO 9001 toward 50–75 artifacts per toolkit (Phase 4).
3. **Add standards:** implement ISO 42001 + ISO 27701 packs and onboarding variants (Phase 4).
4. **Governance:** add template lifecycle UI + approvals so only published content can be used for generation (Phase 4).
5. **Notifications:** add email/notification templates for key events (OTP, submission updates, approval, generation, quotation) (Phase 3/4).

---

## 4) Success Criteria
- POC: outputs open correctly; ZIP matches manifest; validations catch unresolved placeholders/blank mandatory sections. **(Met ✅)**
- V1: client sees exact manifest pre-payment; entitlements granted only after server-side payment verification; admin approval required before generation. **(Met ✅ — using simulated payments in MVP)**
- Multi-tenant: no cross-org data leakage (API, downloads, storage paths); isolation tests pass. **(Met ✅)**
- Generation: all produced artifacts are versioned/immutable; every job + download is logged. **(Met ✅)**
- Compliance messaging: disclaimers present; no certification/legal-advice claims; DPDPA docs include legal disclaimer. **(Met ✅)**
- Production readiness (next): real OTP/MFA/Razorpay with verified webhooks and robust security controls.
