## Context

See `proposal.md` for motivation and `specs/livros/spec.md` for observable behavior. The Reflex application is organized primarily in `biblioteca_nova/biblioteca_nova.py`, with HTTP integration in `biblioteca_nova/api.py`. The existing category flow is the local reference for application-session gating and UI states. The user confirmed workspace 151966, branch `v1`, as the development target. Its Xano contract was pulled read-only and inspected; no credentials or pulled files are added to the repository.

## Goals / Non-Goals

**Goals:**
- Reuse the current authentication/session and API-client patterns.
- Make the actual Xano workspace contract the source of truth for request paths, payloads and response shapes.
- Validate any XanoScript included in this change with the installed Xano Developer MCP and the supported Xano tooling.
- Keep local verification possible without mutating remote data.

**Non-Goals:**
- Guess endpoint paths, table names, authorization rules or response formats.
- Push schema or endpoint changes to a remote Xano workspace as part of implementation.
- Design physical copies, loans, reservations or role-based permissions.

## Decisions

1. **Use the verified Xano contract as the source of truth.** `GET /livro` returns a list; `POST /livro` creates a record; `GET`, `PUT` and `DELETE /livro/{livro_id}` operate on a record. The `livro` table contains `id`, `titulo`, `autor`, nullable `ano_publicacao`, nullable `quantidade_disponivel`, and nullable integer `categoria_id`. There is no ISBN field. Create/update return a record, delete returns null. Seven relevant XanoScript files passed Developer MCP validation. No Xano files or credentials are copied into the repository.
   - The `categorias` table/API uses `id` and `nome`; category description is not in its schema. `GET /categorias` returns a list, while create/update return a record. Existing category selection only needs the ID and name.
   - The inspected endpoints do not declare endpoint authentication and both tables specify `auth = false`. Per the user's explicit decision, this change protects the application UI with its existing session only; it does not claim server-side authorization.
   - Alternative considered: infer REST paths from the base URL and domain model. Rejected because the real paths, payloads, and response shapes differ from the initial domain-model assumptions.
2. **Keep a narrow API adapter in `biblioteca_nova/api.py`.** Follow the existing request/error conventions. Use the confirmed book fields and paths, and normalize IDs/numeric values before exposing them to Reflex state. Keep UI state and presentation in the existing Reflex page/module unless inspection shows a small separate module is needed.
   - Alternative considered: call `requests` directly from UI event handlers. Rejected because it would duplicate HTTP, error and authentication behavior.
3. **Use local mocked HTTP responses for deterministic checks.** Exercise list/create/update/delete success, malformed/error responses, and preservation of form state without writing to Xano. Real integration checks require an explicitly designated development/sandbox workspace and test records.
   - Alternative considered: run CRUD checks against the configured remote API by default. Rejected because that would create or delete user data.
4. **Require category selection in the UI, not in Xano.** The user approved this behavior even though `categoria_id` is nullable and the schema has no declared relationship. Do not claim that Xano enforces the constraint.
   - Alternative considered: allow uncategorized books. Not selected by the user.
5. **Require title and author in the UI.** The user approved this validation even though the Xano schema marks both text fields nullable.
   - Alternative considered: accept empty title/author because Xano permits null values. Not selected by the user.

## Risks / Trade-offs

- [Xano permits unauthenticated access and nullable categories] → Keep the selected UI-only session gate and required category form behavior explicit; do not send remote changes.
- [The Xano contract does not contain ISBN and has additional numeric fields] → Follow the contract and updated spec; do not send ISBN or invent fields.
- [The current app module may make UI changes difficult to isolate] → Preserve existing routes and auth behavior; extract a small component/state helper only if it reduces coupling without broad refactoring.
- [Local checks cannot prove remote permissions or data behavior] → Mark local mocked verification and any real sandbox verification separately; do not claim a remote test unless it was actually run.

## Migration Plan

No production migration is planned. After review and implementation, validate against mocked HTTP responses first. If the real Xano workspace needs schema or endpoint changes, prepare and validate those changes locally, then pause for explicit review before any remote push. Roll back by reverting only the implementation commit(s); do not remove or rewrite pre-existing history.

## Open Questions

- The selected workspace exposes the required book endpoints; Xano authorization is not configured in the inspected files and remains outside this UI-only change.
- The user approved the workspace and the decisions to follow its fields, require category only in the UI, and accept the existing UI-only session gate.
- A separate explicit approval and safe test data are still required for any end-to-end mutation test; no such test is planned by default.
