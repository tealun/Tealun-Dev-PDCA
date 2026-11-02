# Plain Language, Sensitive Areas, and Diagrams

The reader builds products with AI and does not read code. They need to know what each part does, where it lives, and what is risky to touch, and they need to be able to hand any sentence to someone else to check.

## Writing

- Default to Chinese. Short sentences. Lead with the answer.
- Describe behavior from the user's side first ("你点保存后，页面会先……"), then where it happens in code.
- One analogy per major part, chosen from everyday life and kept consistent across pages: e.g. the worker is the front desk that takes every request; the database is the archive room; a migration is a renovation plan for the archive shelves; an environment variable is a sealed envelope handed to the program at start.
- Do not stack analogies on one sentence and do not let an analogy replace the citation.
- Prefer verbs the reader knows: 保存、读取、发出、收到、检查、拒绝、记下.

## Terms

- Avoid a term when a plain phrase works ("网址路径" over "route" when it reads naturally).
- When a term is unavoidable, use it with a one-line explanation on first use on each page: `Worker（运行在云端、接收所有请求的一段程序）`.
- Every term used goes into `glossary.md`: term, plain explanation, where it appears in this project (one path). Merge with existing entries; keep the glossary sorted.

## Sensitive areas

Mark these wherever they appear, with ⚠️ and the category:

| Category | Look for |
|---|---|
| 密钥与凭证 | env files, secret bindings, API keys, tokens, signing secrets, OAuth client secrets, `.env*`, config files with credentials |
| 支付 | payment SDKs, checkout, subscription, billing, webhooks from payment providers, price and plan tables |
| 用户数据 | tables or stores with personal data (email, name, phone, address, content users wrote), export/delete flows, logs that record user data |
| 数据库结构 | schema files, migrations, ORM models, row-level security, seed and backfill scripts |
| 登录与权限 | sign-in, sessions, tokens, role checks, admin-only paths, share links |

Rules:

- Record location and variable or table names only. Never print a value. If a value is hard-coded in source, say "此处写死了一个密钥（值不在此复述）" with `path:line` and list it under `需要确认的疑点` for `$auditor`.
- `sensitive-areas.md` is the single list for the project; flows, impact and change pages link to it and flag the hops that touch it.

## Mermaid

- Use `flowchart` for how parts connect (project map) and `sequenceDiagram` for a feature trace. A change page may use a small `flowchart` of what touches what.
- Keep each diagram to about 15 nodes. Split rather than cram.
- Node labels are plain Chinese names of the part ("网页前端", "云端接口", "数据库"). Put paths in the table under the diagram, keyed by the same names.
- Quote labels containing spaces, parentheses, slashes, colons or non-ASCII punctuation: `A["网页前端 (React)"]`. Use simple ASCII node IDs.
- Mark sensitive nodes with a ⚠️ prefix in the label; do not rely on color alone.
- Only draw an arrow you can cite. A guessed connection is not drawn.
