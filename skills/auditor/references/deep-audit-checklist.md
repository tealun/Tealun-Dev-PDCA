# Deep Audit Command Checklist

Adapt commands to the detected stack and operating system. Prefer repository-native scripts and tools already installed. Search output creates candidates, not findings.

## Baseline and Shape

```text
git status --short
git branch --show-current
git rev-parse HEAD
rg --files -g "package.json" -g "pyproject.toml" -g "go.mod" -g "Cargo.toml" -g "pom.xml" -g "Dockerfile*" -g "*.yml" -g "*.yaml"
```

Also inspect project instructions, README/docs index, dependency manifests, schema/migration directories, CI, deployment assets, and prior audits. On non-Git projects record paths and observation time instead of inventing a commit range.

## Risk-Surface Discovery

Use case-insensitive, scoped searches and inspect context:

```text
rg -n -i "stripe|paypal|payment|refund|entitlement" <source paths>
rg -n -i "jwt|oauth|oidc|session|permission|role|tenant|rls" <source paths>
rg -n -i "webhook|multipart|upload|callback" <source paths>
rg -n -i "password|phone|address|date_of_birth|national_id|secret|token" <schema/source paths>
rg -n -i "cron|schedule|queue|retry|timeout|circuit" <source/config paths>
```

Exclude generated, dependency, build, fixture, and vendor directories using repository-appropriate globs. Confirm imports, registration, callers, runtime configuration, and reachable paths before treating a match as active.

## Security and Contracts

```text
rg -n "eval\(|exec\(|new Function|dangerouslySetInnerHTML|innerHTML" <source paths>
rg -n -i "select.+\+|insert.+\+|update.+\+|delete.+\+" <data-access paths>
rg -n "req\.(body|query|params)|request\.(json|form)|argv" <entry paths>
rg -n -i "cors|helmet|rate.?limit|csrf|sameSite|secure" <server/config paths>
```

For each candidate trace validation, identity, authorization, data access, error mapping, and logging. Inspect hardcoded values directly; `process.env` or equivalent is not itself a leaked secret.

## Data and Backend

Search for transaction boundaries, writes inside loops, idempotency keys/conflict handling, migrations, constraints, and aggregation definitions. Then run the project's narrow database/service tests when safe.

```text
rg -n -i "transaction|begin|commit|rollback|on conflict|upsert|idempot" <source/database paths>
rg -n "for.*await|Promise\.all|\.map\(async" <service paths>
rg -n -i "count\(|sum\(|avg\(|group by|attribution|metric" <analytics paths>
```

Do not execute migrations, seeds, destructive checks, or production queries merely to audit.

## Frontend and UX

Inspect state ownership, effect cleanup, error boundaries, role-based visibility, accessibility, and loading/empty/error/degraded states.

```text
rg -n "setInterval|setTimeout|addEventListener|subscribe\(" <UI paths>
rg -n "clearInterval|clearTimeout|removeEventListener|unsubscribe" <UI paths>
rg -n -i "loading|empty|error|fallback|aria-|role=" <UI paths>
```

Pair searches with component and route-level inspection. Absence of a keyword is not proof that a state or cleanup is missing.

## Maintainability and Health

```text
rg -n "TODO|FIXME|HACK|XXX|console\.(log|warn|error)" <source paths>
rg -n "@deprecated|DEPRECATED|/internal|/dist/|node_modules/" <source/manifests>
rg -n "Manager|Factory|Wrapper|Abstract|interface |abstract class" <source paths>
```

Treat names and abstractions as leads. Demonstrate needless indirection, coupling, dead reachability, or change cost before accepting a finding.

## Native Verification

Prefer commands already declared by the repository, for example:

- lint/format check;
- typecheck or compiler check;
- focused unit/integration/contract test;
- production build;
- dependency audit using the existing lockfile/toolchain;
- migration syntax or dry-run check on a disposable target when authorized.

Record the exact command, exit code, and material output. A green build proves buildability, not authorization, data accuracy, UX, or deployment health. A failed command caused by missing local tooling is an evidence limit unless the project contract requires that tooling to be present.

## Verification Patterns

- Confirm a defect by reproducing the user-visible behavior or proving a complete reachable path.
- Confirm a fix by rerunning the original proof, then an adjacent regression check.
- Confirm absence only within a named search scope and pattern; avoid repository-wide certainty from one grep.
- Inspect resolved dependency versions and actual imports before reporting advisories.
- Recheck `git status --short` at the end and account for every new file or modification.
