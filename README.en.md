# Tealun Dev PDCA

[中文](README.md) | English

Less "I think I did it" from your AI agent, more "here is the proof I did it".

Tealun Dev PDCA organises AI-assisted development as a PDCA loop (Plan, Do, Check, Act): five skills, each owning one stage, handing work to one another so the loop closes, plus a read-only `explainer` that translates AI-written code into explanations people who do not read code can follow. You can sync them into the local skill folders of your agent tools, install them as a Claude Code plugin, or build a single suite package (`dev-pdca`) for platforms that accept only one skill per upload. It is for people who already use Codex, Claude Code, Cursor, Gemini, Kimi, OpenCode, or a shared `.agents/skills` folder. You keep your tools; the agent gets a few steadier ways of working.

## The problems it targets

If you build projects with AI agents, you have probably seen these:

- You ask for a file change. It says done, but nothing was written, read back, or checked.
- You ask for a plan. It quickly writes a pile of documents, but requirements, architecture and acceptance criteria are still scattered.
- You ask for a code audit. It picks at style, while real security, data and deployment risks go unproven.
- You ask for a bug fix. It edits without reproducing, and afterwards you have to work out whether it got better by luck.
- A problem gets settled in one conversation, and the next session makes the same mistake from scratch.
- The AI has written a lot of code, and you cannot tell what parts it has or what a change would affect.

Each of these is a missing stage: acting before thinking it through, not checking the result, not tracing a failure to its cause, not keeping what was learned. So this repository splits development into five skills along PDCA, plus `explainer` to help you understand the code.

## The PDCA development loop

| Stage | Skill | What it does |
| --- | --- | --- |
| Plan | `planner` | Settles requirements, architecture, acceptance criteria and stage gates before code is written |
| Do | `tasker` | Every change starts with a done-definition and an executable check, and ends with evidence |
| Check | `auditor` | Audits before a merge, a release or on request, reporting only findings with evidence |
| Check → fix | `bugfixer` | When a check fails or a symptom appears: reproduce, prove the cause, make the smallest fix, add a regression test |
| Act | `evolver` | Turns verified lessons into tests, rules and ledger records that feed the next plan |
| Understand (any stage) | `explainer` | Read-only: explains the project's parts, feature flows, change impact and each commit in plain language with analogies and Mermaid diagrams, citing file paths, saved under `docs/explainer/` and updated incrementally |

The skills hand off to each other: when a check fails during execution, `tasker` routes to `bugfixer` and resumes once the fix is verified; changes touching security or deployment go through `auditor` first; after a second correction in one cycle and again at its close, `evolver` checks for a lesson worth keeping and proposes recording it for the next `planner` round. `explainer` has no PDCA slot of its own: use it before `tasker` or `bugfixer` change an area you do not understand, and to refresh the project map after a feature or an audit. Each skill works on its own; the full set is what closes the loop.

The point is not to make the agent talk more. It is to make it guess less, skip fewer steps, and turn the result of every stage into evidence you can check.

## Quick start

Each of the three routes installs the whole set at once. Pick the one that fits your platform:

- Claude Code: the plugin marketplace is recommended. Two commands to install, one to update.
- claude.ai (web and desktop): download the plugin package from the latest Release and upload it.
- Codex, Cursor, Gemini, Kimi, OpenCode, or a shared `.agents/skills` folder: use the sync script.
- WorkBuddy and other platforms that accept a single skill zip: use the `dev-pdca` suite package.

With the first two routes the six skills are installed separately and each triggers from its own description, which gives the sharpest triggering from a cold start. The suite package puts all six inside one skill; its entry routes requests and keeps the hand-off rules in force for the whole session.

In Claude Code, do not use both routes, or each skill appears twice (`tasker` and `dev-pdca:tasker`). The sync script also writes to `~/.claude/skills` whenever it detects Claude; if you installed the plugin, you can delete those six folders under `~/.claude/skills` after running the script.

### Option 1: Claude Code plugin marketplace

In a Claude Code session:

```text
/plugin marketplace add tealun/tealun-dev-pdca
/plugin install dev-pdca@tealun
```

The same from a terminal:

```bash
claude plugin marketplace add tealun/tealun-dev-pdca
claude plugin install dev-pdca@tealun
```

Start a new session afterwards and all six skills load. Plugin skills carry a prefix, so to call one by hand you type `/dev-pdca:tasker`, `/dev-pdca:bugfixer` and so on. Automatic selection works the same as before.

To update: `/plugin marketplace update tealun`. You can also turn on auto-update for this marketplace under Marketplaces in `/plugin`.

### claude.ai: one-click install

1. Open the [latest Release](https://github.com/tealun/tealun-dev-pdca/releases/latest) and download `tealun-dev-pdca-<version>.zip`. The same package is also attached with a `.plugin` suffix; the contents are identical.
2. In claude.ai, open Customize > Plugins > Add > Upload plugin and upload the zip.

Keep one install route per tool, or each skill appears twice. If you uploaded planner, tasker, bugfixer, auditor and evolver as separate skills before, delete those five in your skill settings first, then install the plugin. When a new plugin version is released, download it and upload it again.

### Option 2: sync script

Sync the skills from this repository into the `skills` folders of your local agent tools. Check which targets will be written first, preview with a dry run, then sync for real.

#### Windows

```powershell
git clone https://github.com/tealun/tealun-dev-pdca.git
cd tealun-dev-pdca
.\sync-skills.ps1 --list-targets
$env:DRY_RUN = '1'
.\sync-skills.ps1
Remove-Item Env:\DRY_RUN
.\sync-skills.ps1
```

#### macOS / Linux

```bash
git clone https://github.com/tealun/tealun-dev-pdca.git
cd tealun-dev-pdca
bash ./sync-skills.sh --list-targets
DRY_RUN=1 bash ./sync-skills.sh
bash ./sync-skills.sh
```

#### Sync only some skills

To install only a few skills, put their names at the end of the command:

```powershell
.\sync-skills.ps1 tasker planner
```

macOS / Linux:

```bash
bash ./sync-skills.sh tasker planner
```

After installing, reopen your agent CLI or start a new session so the tool reloads its skill folders.

### Option 3: the dev-pdca suite package

Download [`dev-pdca.zip`](https://github.com/tealun/tealun-dev-pdca/releases/latest/download/dev-pdca.zip) from the latest Release and choose it in the platform's skill import or upload dialog. It holds the entry skill and all six sub-skills, built by CI from the skill sources at each release.

If the platform wants `SKILL.md` at the zip root, run `python3 scripts/build_suite.py` in the repository (Python 3, no third-party packages) and upload `dist/dev-pdca-<version>-flat.zip`.

Once installed there are no skill names to remember. Say what you want done:

```text
Audit this project, focus on deployment risk
Fix this 500 error, reproduce it first
Draft the M0 plan
```

Or name the stage: `/dev-pdca audit this project`, `/dev-pdca bugfixer this error`. `/dev-pdca` on its own lists the whole set.

## Make the agent actually invoke the skills

Installed is not the same as used. If the project instructions never say when to use which skill, the agent tends to fall back on its own habits, and the skills can sit unused for a whole development cycle. The fix is to write the triggers into the project's `CLAUDE.md` or `AGENTS.md`.

Copy this into your project's instruction file:

```markdown
## Companion skills: invoke them, do not just follow their spirit

This project uses Tealun Dev PDCA (planner, tasker, bugfixer, auditor, evolver, explainer). When a trigger below applies, invoke the matching skill through the skill tool (or read its SKILL.md and follow it). Following the general idea without invoking it does not count. In the first reply of every session, state which of the six skills are available; if one is missing, say so.

- **planner: every planning intent, whatever its size.** A feature, a page, a URL or site-structure change, a data or schema change, a refactor, a release, a roadmap, a doc system or process. Invoke it before writing code or content, and record the decisions in the relevant doc first.
- **tasker: every change to files or state.** Set the done definition and an executable check before editing; finish with evidence (command output, screenshots), not a description. Read-only answers are exempt.
- **bugfixer: when the user says something is wrong or still wrong, a screenshot shows a defect, or a check fails.** Reproduce or observe first, prove the cause, fix only that, and verify the original symptom.
- **auditor: before pushing changes to security, deployment, URL parameters or shared state, before a release, and on any audit request.**
- **evolver: after a verified fix of a user-reported problem, after a second correction in a cycle, and at the close of each work cycle.** Record the lesson and its guard in `docs/98_evolution/evolution-ledger.md`.
- **explainer: when the user cannot follow the code about to change, or asks what the project is made of, what happens after a click, what a change would affect, or what the AI just changed.** Read-only; it writes plain-language pages with file paths under `docs/explainer/`. Use it before tasker or bugfixer change an area the user does not understand, and refresh the project map after a feature or an audit.
```

The Chinese version, the instruction file name for each tool, and how to vendor a pinned copy of the skills into your project for cloud sessions where they are missing are in [docs/agent-instructions-snippet.md](docs/agent-instructions-snippet.md).

## How to use them

Go to your project folder and reopen your agent CLI or start a new session. In tools with slash commands, such as Codex, type:

```text
/tasker Check this project's README for broken links and report the verification result.
/auditor Audit this project, starting with the README, install scripts and doc consistency.
/bugfixer Fix this 500 error. Reproduce it before changing anything.
/planner Lay out the M0/M1 plan for this project and look for architecture risks first.
/evolver Record this verified fix in the project rules and the evolution ledger.
/explainer Give me a project tour, then trace what happens after I click "Save".
```

In tools without slash commands, replace `/tasker` with plain words such as "use tasker".

When a skill is loaded, the agent follows that skill's workflow. For example, `tasker` states the scope, the verification method, the evidence and the conclusion, instead of a single "looks fine".

### Automatic selection

Many agents choose a skill from the `description` in its `SKILL.md`, so you do not always have to type `/tasker`:

- "Finish this task and show me the verification result" usually triggers `tasker`.
- "Audit this project", "do a code review", "check security and deployment risks" usually trigger `auditor`.
- Pasting an error, a 500, a regression, or saying "still wrong" or "reproduce it before fixing" usually triggers `bugfixer`.
- "Requirements", "technical design", "M0/M1 plan", "project planning" usually trigger `planner`.
- "Capture the lesson", "prevent this from recurring", "put it in the rules / ledger / retrospective" usually trigger `evolver`.
- "Walk me through this project", "what happens when I click this button", "what would changing this affect", "what did the AI just change" usually trigger `explainer`.

If the agent does not pick the skill, force it with the slash command. In a long-running project it is more reliable to write the triggers into the project instructions, as in "Make the agent actually invoke the skills" above.

Fuller install and troubleshooting steps are in [QUICKSTART.md](QUICKSTART.md) (Chinese).

## Which skill to use

| Your situation | Skill | What it protects |
| --- | --- | --- |
| The project is just starting and requirements, architecture and milestones are unclear | `planner` | Decisions, assumptions, open questions and stage gates are written down, so less is guessed along the way |
| You want the agent to change code, write docs or run checks | `tasker` | Every completion claim needs an artifact and a check, so "said it was done" does not pass for done |
| You want to find risks before a merge, release or hand-over | `auditor` | Only findings with evidence are reported, with severity, confidence and verification gaps kept apart |
| There is already an error, a regression or odd behaviour | `bugfixer` | Reproduce and locate first, make the smallest fix, then add a regression test, instead of guessing the bug from experience |
| The same kind of problem keeps coming back and you want the lesson to stick | `evolver` | Verified lessons become rules, checks, ledger records or input for the next plan |
| You cannot read the AI-written code and want to understand it before changing it | `explainer` | Never edits code; every conclusion cites a file path, and secrets, payments, user data and database structure are flagged separately |

## Where the sync script installs

The sync script detects compatible tools that are installed or configured on your machine and copies the skills into their `skills` folders. It currently covers:

- Claude
- Codex
- Cursor
- Gemini
- Kimi
- Kimi Desktop (Windows)
- OpenCode
- Shared agents (`~/.agents/skills`)

The script copies over the existing content: skills from this repository are written into the target folder, and metadata files that exist only in the target folder are usually kept. Run it with `DRY_RUN=1` first to see where it will write.

## Updating

Installed through the plugin marketplace: run `/plugin marketplace update tealun` in Claude Code.

Installed with the sync script: pull the latest version and run the script again.

macOS / Linux:

```bash
git pull
bash ./sync-skills.sh
```

Windows:

```powershell
git pull
.\sync-skills.ps1
```

## Repository layout

```text
.
├── .claude-plugin/   # Claude Code plugin marketplace manifest (marketplace.json)
├── auditor/          # Evidence-led project audits
├── bugfixer/         # Symptom-driven repairs
├── evolver/          # Turns lessons into lasting guards
├── explainer/        # Read-only plain-language code explanations
├── planner/          # Early project planning
├── tasker/           # General task-execution discipline
├── suite/dev-pdca/   # Suite package entry: PDCA routing rules
├── scripts/          # build_suite.py: builds the dev-pdca suite package
├── docs/             # Instruction snippet, case studies, this repo's evolution ledger
├── sync-skills.ps1   # Windows sync script
└── sync-skills.sh    # macOS / Linux / WSL sync script
```

## Troubleshooting

Check three things first:

1. Does your agent tool support folder-based `SKILL.md` skills?
2. Does `--list-targets` find the target folder?
3. Did you reopen the agent CLI or start a new session after syncing?

More in [SUPPORT.md](SUPPORT.md). To contribute, see [CONTRIBUTING.md](CONTRIBUTING.md). For security issues, follow [SECURITY.md](SECURITY.md).

## License

MIT License. See [LICENSE](LICENSE).
