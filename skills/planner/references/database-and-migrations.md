# Database And Migrations

Use this reference when planning database schema, migrations, RLS/security policies, production data movement, seed data, or operational commands.

## Baseline And Evolution

Use a two-track model:

- `database/schema.sql`: authoritative baseline for a fresh environment.
- `database/migrate/` or `database/migrations/`: forward-only incremental evolution for existing environments.

Optional but recommended:

- `database/rls.sql`: row-level security policies if tenant/user isolation exists.
- `database/grant_all_to_<role>.sql`: idempotent permission repair for PostgREST/self-hosted roles.
- `database/scripts/migrate.*`: runner that orders and records migrations.
- `database/scripts/check.*`: non-destructive readiness checks.
- `database/scripts/verify.*`: destructive disposable-database verification, clearly marked unsafe for production.

## Migration Rules

- Use plain, reviewable SQL unless the project has a strong migration framework.
- Name files with sortable versions, for example `migrate_v2_93_<topic>.sql` or `migrate_v1_4.sql`.
- Start every migration with a comment block:
  - purpose
  - reason/risk
  - production commands
  - post-steps such as grants and schema reload
- Prefer forward-only migrations. If rollback is needed, document a manual rollback path separately.
- Use idempotent SQL where practical: `IF NOT EXISTS`, `IF EXISTS`, `CREATE OR REPLACE FUNCTION`.
- For existing data, write the evolution as safe phases:
  1. add nullable column/table/function
  2. backfill
  3. validate
  4. add `NOT NULL`/unique/FK constraints
  5. switch application reads/writes
- Never hide destructive operations. Mark them in the file and in execution instructions.

## Production Command Pattern

When users must copy commands into SSH/panel terminals, provide complete commands, not fragments.

Example:

```bash
psql -h /tmp -U postgres -d <db_name> -f /www/wwwroot/<app>/database/migrate/migrate_vX_Y_topic.sql
psql -h /tmp -U postgres -d <db_name> -f /www/wwwroot/<app>/database/grant_all_to_app.sql
psql -h /tmp -U postgres -d <db_name> -c "NOTIFY pgrst, 'reload schema';"
```

Add grants when new tables, sequences, functions, views, or RPCs are created. Reload PostgREST schema cache after schema changes.

## Permissions And RLS

For apps with tenant/user data:

- State whether application code connects through backend only or whether clients can directly access DB APIs.
- Define the service role, app role, admin/migration role, and public/anonymous role separately.
- RLS default should be deny when context is missing.
- Use transaction-scoped context such as `SET LOCAL app.tenant_id = ...` only inside explicit transactions.
- Platform/global tables require an explicit reason if they bypass tenant RLS.
- Cross-tenant sensitive binding tables need special rules; do not casually classify them as global.
- Public lookup tables should avoid PII and expose only the minimum needed to resolve a public identifier.

## Data Model Checklist

For every important table, capture:

- purpose and owner
- primary key and public identifier
- tenant/user ownership fields
- lifecycle status and soft-delete behavior
- timestamps and audit fields
- unique constraints, including partial unique indexes for soft-delete
- foreign keys or invariant validator if FKs are intentionally avoided
- indexes for common queries
- PII/sensitive fields
- seed/backfill strategy
- retention/deletion policy

## Seed And Data Migration

Separate these categories:

- `schema`: structure required for the app to run.
- `seed`: initial reference data for empty environments.
- `backfill`: one-time transformation of existing production data.
- `repair`: safe idempotent script for known inconsistencies.
- `verify`: checks that prove data is consistent.

For backfills:

- Define source tables, target tables, filtering rules, idempotency key, batch size, and resume behavior.
- Include a dry-run query where possible.
- Record counts before/after.
- Log skipped rows and reasons.
- Avoid irreversible deletes; prefer mark-and-review.

## Readiness Before Coding

Database planning is ready when:

- A fresh environment can be initialized from the baseline.
- An existing environment can move forward through migrations.
- Permissions/RLS are defined for every access role.
- Production execution commands are copy-pasteable.
- Unknown external identifiers or API payloads are owned by M0 spike tasks.
- Tests/check scripts distinguish destructive verification from safe production checks.
