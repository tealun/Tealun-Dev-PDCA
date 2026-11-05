# Backend, Data, and Persistence Bugs

Use this reference for API, auth, storage, persistence, metrics, database, and migration defects.

## Contract and Backend Checks

- Read the client request, route/controller, DTO/schema, service, repository, and affected tests together.
- For `400`, inspect body shape, enum values, content type, validation errors, and missing/extra fields.
- For `401/403`, inspect token source, request attachment, route privacy, identity, owner, tenant, and role rules.
- For `404`, compare exact method/path, global prefix, route registration, resource id, and deployed version.
- For `500`, use the stack trace and inspect nullability, constraints, lengths, migrations, storage, and unhandled branches.
- Keep authorization, idempotency, concurrency, transactions, and error shape visible in mutation paths.
- Redact tokens, connection strings, and secret-bearing environment values from logs and responses.

## Persistence and Storage

Observe the full write/read chain:

```text
UI state → request payload → contract → service/repository
→ database/storage → response → reload mapper → rendered value
```

Check column type, nullability, defaults, lengths, JSON shape, indexes, storage category, MIME/size rules, returned URL, and cleanup. A save is not verified until readback and reload succeed.

## Generated Artifact Freshness

When the defect is in a generated or downloadable artifact such as a PDF, spreadsheet, export ZIP, image, or report, inspect the artifact lifecycle:

```text
source record/template
→ generation service
→ stored file/object
→ freshness marker, version, or metadata
→ download/preview route
→ user file
```

- Compare the actual stored artifact with source inputs; check mtime, checksum, metadata, and whether the request uses a download endpoint or a direct static URL.
- If render, layout, seal, export, or conversion semantics changed, stale artifacts must be invalidated, regenerated, or versioned. Do not assume new code updates existing files.
- Add a regression that an old artifact version or missing marker is detected as stale and triggers the intended regeneration path.
- Verify with a real representative artifact when possible, especially for spreadsheet, PDF, image, or archive conversions where previews can differ from source files.

## Metrics

Define the metric before changing code:

- `unique visitors` — distinct identities.
- `display count` — qualifying view events, including intended repeats.
- `interactions` — explicit actions.
- positive vote/like — at most the product-defined count per identity and object.

Define owner exclusion, anonymous identity window, logged-in identity, dedupe key, tenant/object scope, filters, event write, query, response field, and displayed label. Verify stale demo/cache values clear after real data loads.

## Database and Migration Lifecycle

- Locate the schema authority and migration package first; do not duplicate assets into backend or frontend code.
- Compare migration files with applied state and confirm the process targets the intended database.
- Run migration tooling from its owning package and validate required dependencies, permissions, and working directory.
- Never accept arbitrary browser-provided filesystem paths or shell commands.
- Protect manual execution with high privilege, throttling, concurrency control, sanitization, redaction, and visible status.
- Re-check pending/applied state after execution; do not equate raw stdout with success.

Execute migrations only on a safe target or explicitly intended window with backup and rollback expectations.

## Verification

- Contract change — client construction check plus targeted server test/typecheck.
- Persistence — write, response, database/storage value, reload, and rendered value.
- Auth — anonymous, logged-in visitor, owner, tenant, and forbidden roles as relevant.
- Metrics — event write, dedupe/query, identity rules, response mapping, and UI label.
- Migration — syntax/static review, applied-state check, build/tests, and safe live verification when authorized.

