
---

## ✅ `docs/rls_model.md`

```markdown
# RLS (Row-Level Security) Model — Consignee Scope

## Objective
Ensure a user can ONLY retrieve shipments belonging to their allowed consignee scope.

Special rule: *Parent can view children*, but children cannot view siblings.

---

## Terminology
- **Consignee Code**: internal code like `0000866`
- **Parent Consignee**: a top-level organization that accounts for child sub-orgs
- **Child Consignee**: sub-org under a parent

In payload, user may send:
- `["0000866,234567"]` (single string containing commas)
- `["0000866", "234567"]` (list)
We must normalize to `["0000866", "234567"]`.

---

## Source of Truth for Scope
**Never trust payload consignee_codes alone.**

In production, scope should come from:
- authenticated identity (JWT claims / API key)
- server-side mapping

For demo:
- payload may supply codes, but MUST be validated against server rules.

---

## Scope Resolution Rules

### Rule 1 — Fail Closed
If no consignee scope resolved:
- deny retrieval (no hits)
- respond with: "Not authorized"

### Rule 2 — Parent Can See Children
If user is authenticated as parent `P`:
Allowed scope = `[P] + children(P)`

### Rule 3 — Child Cannot See Siblings
If user is authenticated as child `C`:
Allowed scope = `[C]` (not siblings, not parent unless explicitly granted)

### Rule 4 — Payload Cannot Expand Scope
If payload includes codes outside allowed scope:
- ignore/unset them
- optionally add a notice
- never query with them

---

## Implementation Plan

### 1) `security/scope.py`
Expose a single function:
- `resolve_allowed_scope(user_identity, payload_codes) -> List[str]`

This returns the effective `allowed_consignee_codes` used everywhere else.

### 2) `security/rls.py`
Build filter strings for Azure AI Search:
- always use `allowed_consignee_codes`
- do not use raw payload codes

Example if index field is collection `consignee_code_ids`:

