# Reading Method

How to read a codebase for each mode, and how to cite what was read.

## Evidence rules

- A claim is a sentence a reader could check. Each one cites `path` (a whole file or folder) or `path:line` / `path:start-end` (a specific behavior).
- Cite the place that does the thing, not the place that mentions it. A route table proves a URL exists; the handler proves what it does.
- Names, comments, README text, and folder names are leads. Confirm them in code before stating them as fact.
- When a link cannot be found, write `未找到：<what was searched, where>`. When something was found but not followed to the end, write `未核实：<what remains>`. Never bridge a gap with a typical pattern.
- Use repository-relative paths with `/`. Line numbers come from the recorded baseline commit.
- A config key cites its file and key: `wrangler.jsonc`（`SUPABASE_URL`）, or `path:line` when the line is stable. A URL or route is written as text, not as a path citation.
- Parts that were not read go under `未找到 / 未核实` as `未读：<folder> — <why>`.

## Fingerprint the project (all modes)

Read before concluding anything:

1. Package and build manifests: `package.json` (and workspaces), `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile`, `composer.json`, `pubspec.yaml`.
2. Runtime and deploy config: `wrangler.*`, `vercel.json`, `netlify.toml`, `Dockerfile`, `docker-compose.*`, `fly.toml`, `Procfile`, CI workflows.
3. Project instructions and docs index: `README.md`, `CLAUDE.md`, `AGENTS.md`, `docs/README.md`.
4. Top-level folders: list them with file counts; skip `node_modules`, build output, vendored code, lockfiles, generated files.

From these, name the parts: what the user sees (web pages, app screens, emails), what answers requests (server, worker, API), where data lives (database, storage, cache), what runs on a schedule or in the background, and outside services (payment, login, email, AI, analytics).

## Mode: project tour

1. Find the entry points: the server or worker `main`/`fetch` handler, the web app's root component and router, scheduled jobs, CLI scripts.
2. For each part, open its entry file and one representative file. Record: what it is for in one sentence, its folder, the files that prove it.
3. Draw how the parts talk to each other: which calls which, over what (HTTP request, database read/write, queue, webhook). Only draw an arrow you can cite.
4. Sweep for sensitive areas (see `plain-language.md`): search for env and secret access, payment SDKs and webhooks, auth/session code, user-data tables, schema and migration files.
5. Stop at the level a non-coder needs: 4–10 parts. Large monorepos group packages by role, not one box per package.

## Mode: feature trace

Trace one user action from the screen to the data and back:

```text
what the user does → UI element → event handler → request sent
  → route → validation / login check → business logic → data read/write
  → outside services → response → what the user sees
```

1. Find the trigger: search the UI for the visible text of the button or page, then the handler bound to it. When the same user goal has several entries (a quick-add bar, a form on a list page, a calendar), list them all, trace the one the user named or else the most central one (present on most screens, described first in the project's README, or covered by end-to-end tests), and state the choice and reason at the top of the page. Other entries get a short route at the end.
2. Follow each hop by reading the called function, not by guessing from its name. Record `path:line` per hop.
3. Note branches that change what the user sees: not logged in, validation fails, network error, empty result. One line each. A branch you saw but did not follow (an alternate version, a feature flag, a fallback) goes under `未核实` with the condition that selects it.
4. Note every hop that crosses a sensitive area.
5. If the chain leaves the repository (a third-party API, a database trigger defined elsewhere), say so and stop there.

## Mode: change impact

1. Pin down X: the file(s), function(s), table, or screen the user means. If several candidates fit, list them and pick the one the user named; ask only if none fits.
2. Find who depends on X: search for imports, calls, route references, table/column names, config keys, CSS class names, and tests that mention it.
3. Classify each dependent: same feature / other feature / shared by many / data stored long-term / outside contract (public API, webhook, email, mobile app).
4. Rate how hard the change is, from evidence only:
   - **低** — used in one place, no sensitive area, covered by tests or easy to check by hand.
   - **中** — used by several features, or no tests, or changes what is stored.
   - **高** — touches a sensitive area, a database structure, a shared base piece used widely, or a contract other systems rely on.
   State the reasons; the rating is a summary of them, not a verdict on code quality.
5. List what to check after the change, in user terms (screens to open, actions to try).

## Mode: change explanation

1. Resolve the range: `HEAD~1..HEAD` by default, a named commit, a PR, a branch against its base, or uncommitted work (`git diff` plus untracked files).
2. Read `git log --stat` for the range, then the diff file by file. Group files by purpose, not by folder.
3. For each group: what changed in behavior a user would notice, why (from commit message, PR text, linked issue, or code comments; if none, write `原因未说明`), and what else reads or depends on the changed parts.
4. Possible side effects are statements of reach, not defects: "this also changes what the weekly email shows" with a citation. Anything that looks wrong goes to `需要确认的疑点`.
5. Flag changes to sensitive areas, dependencies, config, database structure, and deleted files explicitly.

## Scale

- Prefer search over reading whole trees. Read the files on the path; skim neighbors only to confirm a role.
- When a part is too large to read in the session, describe it from its entry file and say what was not read.
- When a trace runs past about 15 steps, split it into phases the user would recognize (e.g. 提交 → 确认 → 保存), each with its own table; summarize repetitive middle hops with a citation range.
