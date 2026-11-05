# Audit Method

Use this reference to calibrate depth, coverage, and critical-path analysis.

## Fingerprint and Risk Surfaces

Inspect manifests, directory shape, project instructions, database/schema assets, CI, deployment configuration, and existing audit reports. Identify whether production code implements:

- auth, roles, permissions, tenancy, or sensitive/PII data;
- payment, entitlement, webhook, upload, or public API paths;
- third-party calls, scheduled/async work, database writes, or caching;
- UI and accessibility concerns;
- production infrastructure, secrets, backups, rollback, monitoring, or migrations.

A package name or keyword is only a signal. Count the surface after confirming its use and reachable context. A single consequential path may justify deep analysis even in a small diff.

Use `.audit-config.yml` when present:

```yaml
audit:
  mode: auto
  max_depth: deep
  max_duration_minutes: 20
  output_dir: docs/99_audits
```

`interactive` mode applies only when explicitly requested. Configuration does not override user scope or safety requirements.

## Depth Expectations

| Depth | Coverage | Path work | Typical verification |
|---|---|---|---|
| Quick | requested concern plus core safety/health samples | optional; disclose omission | searches, focused inspection, narrow checks |
| Standard | all applicable dimensions | highest-risk path | targeted tests/build plus static proof |
| Deep | all applicable dimensions, supply chain, tests, ops | every identified high-risk path | broader tests, config/infra inspection, safe runtime checks |

Choose depth from consequence, reachability, and project shape—not commit count or raw match counts. Respect time/access caps and name incomplete dimensions.

## Twelve Dimensions

| # | Dimension | Check |
|---|---|---|
| 1 | Architecture | module boundaries, technology fit, coupling, extensibility, unjustified complexity |
| 2 | Platform integration | SDK/callback contracts, timeout/retry/idempotency, outage degradation |
| 3 | Security | auth/authz, injection, secrets, encryption, redaction, abuse controls |
| 4 | Code efficiency | needless compute/queries, duplication, complexity, measured performance |
| 5 | Runtime smoothness | latency, concurrency, cache, resources, wait/error behavior |
| 6 | Information isolation | tenant/account/role boundaries, RLS, cross-scope access |
| 7 | Data accuracy | invariants, transactions, attribution, aggregation, lifecycle, consistency |
| 8 | Parameter passing | URL/body/header/token boundaries, public versus internal IDs |
| 9 | User experience | key flow, accessibility, empty/loading/error/degraded states |
| 10 | Coding standards | names, layout, lint/types, response/error conventions, documentation fit |
| 11 | Testing | unit/integration/contract/authz/migration tests and CI enforcement |
| 12 | Deploy and operations | config, logs, monitoring, health, rollback, backup, secret rotation |

Always adapt the meaning to the project. Security for a CLI may mean argument/file validation and secret handling, not web sessions.

Conditional dimensions:

- Platform integration only when external platforms/SDKs/callbacks exist.
- Information isolation only for multiple users, tenants, roles, or protected scopes.
- Parameter passing only for HTTP/RPC/CLI/public API entry surfaces.
- User experience only when an interactive UI exists.
- Deploy/operations may be `N/A` for a library that is not independently shipped.

Mark absent surfaces `N/A — <reason>`. Mark ambiguous ones `Not verified — <evidence needed>` rather than inventing a defect.

## Specialist Lenses

These are analysis lenses, not mandatory agents:

- Security: identity, authorization, injection, exposure, isolation, abuse, log redaction.
- Backend/data: contracts, errors, transactions, N+1, idempotency, metrics, migrations, third-party reliability.
- Frontend/UX: state, rendering, leaks, error boundaries, accessibility, degraded and waiting states.
- Architecture/quality: boundaries, duplication, naming/types, documentation drift, maintainability, upgrade traps.
- Test/ops: meaningful coverage, CI enforcement, environment hygiene, monitoring, rollback, backup.

Perform them sequentially unless explicit instructions authorize delegation. Coverage must never depend on multi-agent availability.

## Critical-Path Record

For each selected path, capture:

```markdown
### <path name>
- Goal / protected property:
- Trace and locations:
- Applicable dimensions:
- Confirmed controls:
- Accepted findings:
- Verification gaps:
- Health: Healthy | At risk | Broken | Not verified
```

Stop tracing once the user-visible result and recovery/observability boundary are accounted for. Follow additional branches only when evidence indicates a distinct risk.
