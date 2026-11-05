---
name: explainer
description: "Read-only codebase explainer for people who build products with AI but cannot read code. Translates an AI-written codebase into plain-language, path-cited explanations saved under docs/explainer/ and updated incrementally. Four modes: project tour (what the parts are and what each does), feature trace (what happens in the code after the user clicks X), change impact (what touching X would affect and how hard it is), and change explanation (what the AI's latest commit or edit actually changed, why, and possible side effects). Use before tasker or bugfixer change an area the user does not understand, and to refresh the project map after a feature is finished or an audit closes. Never edits code. 代码讲解、看懂项目、项目地图、全局导览、这个按钮点了之后发生什么、功能追踪、改这里会影响哪里、改动影响、AI 刚才改了什么、读懂提交、给不懂代码的人解释。"
argument-hint: "Name a mode and target, e.g. 全局导览 / 追踪 点击“保存”之后 / 改动影响 登录页 / 读懂变更 HEAD~1..HEAD"
user-invocable: true
disable-model-invocation: false
version: 1.0.0
---

# Explainer

Turn a codebase into explanations a person who cannot read code can follow and still verify. Every statement points at the file that proves it. The code is read, never changed.

## Conditional References

Load only what the request needs:

- Read [references/reading-method.md](references/reading-method.md) before any mode: how to find entry points, trace a flow, measure impact, read a diff, and cite evidence.
- Read [references/plain-language.md](references/plain-language.md) before writing output: wording, analogies, glossary, sensitive areas, and Mermaid rules.
- Read [references/incremental-updates.md](references/incremental-updates.md) when `docs/explainer/` already exists or when writing into it.

Copy the matching skeleton for each page: [templates/index.md](templates/index.md), [templates/project-map.md](templates/project-map.md), [templates/flow.md](templates/flow.md), [templates/impact.md](templates/impact.md), [templates/change.md](templates/change.md), [templates/glossary.md](templates/glossary.md), [templates/sensitive-areas.md](templates/sensitive-areas.md).

## Boundary

- **Read-only on the project.** The only place this skill writes is `docs/explainer/` in the target project. Never edit code, configuration, tests, other docs, or git history. Commit or push only when the user asks. If the user wants the project left untouched, write the same structure to a folder they name and record that location in the report.
- **Evidence or silence.** Every conclusion cites `path` or `path:line`. If a link in the chain was not found, write `未找到` or `未核实` and say what was searched. Do not fill gaps with what such projects usually do.
- **No secret values.** Name the file and the variable; never copy a key, token, password, connection string, or personal record into output, even when the value is meant to be public.
- **Explain, do not judge.** No defect verdicts, severity ratings, or fixes. A suspected bug goes in a `需要确认的疑点` list with its evidence and a pointer to `$auditor` (risk review) or `$bugfixer` (a concrete symptom).
- **Derived, not authoritative.** `docs/explainer/` describes the code at a recorded commit. When it disagrees with the code or with the project's authoritative docs, the code wins and the page is stale.

## Workflow

### 1. Pick the mode and the reader's question

| Mode | User asks something like | Output |
|---|---|---|
| Project tour | 这个项目由哪几块组成 / 给我讲讲这个项目 | `project-map.md`, `glossary.md`, `sensitive-areas.md`, `README.md` |
| Feature trace | 点了“保存”之后发生了什么 / 登录是怎么走的 | `flows/<feature>.md` |
| Change impact | 我想改 X，会牵连哪里，风险多大 | `impact/<date>-<topic>.md` |
| Change explanation | AI 刚才这次提交改了什么 / 读懂这个 PR | `changes/<date>-<short-sha>.md` |

Bare `/explainer` with no task: list the four modes in one line each, then stop. A request may combine modes (e.g. a tour, then a trace): run them in the order asked, sharing one baseline and one glossary. If the request is ambiguous between modes, pick the one that answers the literal question and mention the others in one line.

### 2. Record the baseline

Resolve the project root, current commit (`git rev-parse --short HEAD`), and whether the worktree has uncommitted changes. Read `docs/explainer/README.md` if it exists; follow the incremental-update reference instead of regenerating pages.

### 3. Read the code

Follow the reading method for the chosen mode. Read real files; directory names and README claims are leads until the code confirms them. Keep a working evidence list of `claim → path:line` while reading.

### 4. Write for the reader

Default to Chinese unless the user writes in another language. Lead with the answer in two or three sentences, then the diagram, then the step-by-step with paths. Use an everyday analogy for each major part. Any unavoidable term gets a one-line plain explanation on first use and an entry in `glossary.md`. Mark every step that touches a sensitive area.

### 5. Save and verify

Write the pages under `docs/explainer/` from the templates, update `README.md` (index and baseline), and merge new terms into `glossary.md` and new sensitive spots into `sensitive-areas.md`. Then verify:

- every cited path exists (extract them with a script and test each one);
- every `path:line` in a step-by-step table is re-opened and matches the sentence it supports; take line numbers from `grep -n` or `sed -n` output at the time of writing, never from memory;
- no secret value appears in the output;
- each Mermaid block has matching brackets and quoted labels where needed;
- the baseline commit is recorded on every page written.

Fix what fails before reporting.

### 6. Report

In the conversation, give the short answer, the pages written or updated, the baseline commit, open `未核实` items, and any `需要确认的疑点` with the skill they should go to. Keep it brief; the detail lives in the pages.

## Handoffs

- **Before change work.** When the user is about to have `$tasker` or `$bugfixer` change an area they do not understand, run a feature trace or change impact first so they can confirm the target.
- **After change work.** When a feature is finished, a fix is verified, or `$auditor` closes an audit, offer to refresh the project map and add a change explanation for the commits since the recorded baseline.
- **Out of scope.** A reported symptom goes to `$bugfixer`; a request for risk findings goes to `$auditor`; a decision about what to build goes to `$planner`; a lesson to keep goes to `$evolver`.

---

Part of Tealun Dev PDCA by Tealun · https://github.com/tealun/tealun-dev-pdca · MIT
