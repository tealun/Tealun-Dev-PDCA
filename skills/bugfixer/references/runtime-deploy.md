# Runtime, Configuration, CI, and Deployment Bugs

Use this reference when local code and running behavior disagree, configuration is ignored, or pipelines/processes fail.

## Configuration Boundaries

- Identify which process reads each value: IDE/tool metadata, client runtime, backend runtime, platform console, provider app, or tenant authorization store.
- Keep public examples as placeholders and private values in the correct ignored/server/platform plane.
- Prefer validated config getters over scattered raw environment reads.
- Inspect import paths and precedence when sample configuration becomes active.
- For SaaS integrations, separate provider-level application settings from per-tenant credentials and authorization.
- When an interactive shell can find a CLI binary but the app cannot, compare the process manager or server panel user, `PATH`, virtualenv, working directory, and restart state. Prefer an absolute executable config and verify from the app process or logs.

## Production Version Path

1. Reproduce from an external client.
2. Compare a known old route and the failing new route.
3. Check commit/build/version identity when available.
4. Confirm build directory and start command match the actual service.
5. Confirm the process or container restarted after files/build changed.
6. Confirm reverse proxy target and port.
7. Re-run the external URL; a protected route returning `401` may prove registration.
8. Verify runtime working directory for filesystem-dependent behavior.

Interpret route comparisons carefully:

- Old route `401`, new route `404` — likely stale version or missing route in the running target.
- Both `404` — wrong prefix, service, or proxy target.
- New route `500` — route exists; inspect logs, environment, database, and migrations.

## Deploy Sync and Process Managers

- Trust executable include/exclude rules over comments.
- Verify source path, target path, path triggers, authentication, permissions, and sync logs.
- Protect `.env`, uploads, logs, certificates, dependencies, and other runtime-owned files from destructive sync.
- Confirm source-only deploys rebuild generated output.
- Ensure exactly one system owns restart: deploy workflow or process manager, not both.
- For server panels, verify project/run directory, lockfile install command, build output, start entry, port, proxy, environment, and database assets.
- Treat shell probes such as `command -v` or `whereis` as host evidence only; confirm the managed service reads the same environment or configure absolute paths such as `LIBREOFFICE_PATH`.

If the configured project directory lacks `package.json` or source, debug sync before install/start.

## CI Log Triage

Read the first non-zero command and nearby output; do not infer from the step title.

- Compiler file/line/type errors — typecheck failure.
- Linter rule ids and locations — lint failure.
- Failed test names/assertions — test failure.
- Passing tests followed by threshold output — coverage failure.
- Failure before project commands — install failure.
- Vulnerability tooling after install/test — audit failure.

Fix and rerun the actual failing subcommand.

## Windows HTTP Checks

PowerShell may alias `curl` to `Invoke-WebRequest`. Use `curl.exe -i <url>` or `Invoke-WebRequest -Uri "<url>"` when exact HTTP status matters.

## Verification

- Config — prove the intended process reads the intended plane without leaking private values.
- Deployment — build, restart, version identity, proxy target, then external request.
- Sync — inspect actual rules and confirm intended files arrive while protected runtime files remain.
- CI — rerun the exact failing command and show its failure mode changed to passing.
- Process manager — verify configured path, install/build/start commands, port, environment, and health URL.

Files uploaded or a build completed does not prove the running service is current.
