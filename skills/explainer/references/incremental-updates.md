# Incremental Updates

`docs/explainer/` is a map that follows the code. Update the parts the code changed; do not rewrite the whole map each time.

## Layout

```text
docs/explainer/
  README.md              index, baseline, page list (templates/index.md)
  project-map.md         project tour (templates/project-map.md)
  glossary.md            all terms used by any page (templates/glossary.md)
  sensitive-areas.md     the single list of sensitive spots (templates/sensitive-areas.md)
  flows/<feature>.md     one page per traced feature (templates/flow.md)
  impact/<YYYY-MM-DD>-<topic>.md      one page per impact question (templates/impact.md)
  changes/<YYYY-MM-DD>-<short-sha>.md one page per explained change (templates/change.md)
```

File names use lowercase ASCII words joined by `-` (`flows/create-task.md`); the page title carries the Chinese name. Keep the project's own docs conventions untouched; link to `docs/explainer/README.md` from the project's docs index only when the user asks.

## Baseline

- Every page starts with a meta line: `基线：<short-sha>（<YYYY-MM-DD>）`. Add `含未提交改动` when the worktree was dirty.
- `README.md` holds the page table with each page's baseline, so staleness is visible at a glance.
- Without git, use the date and list the files read; say that diff-based updates are unavailable.

## Update procedure

When `docs/explainer/` exists:

1. Read `README.md`; take the oldest baseline among the pages in scope.
2. List what changed since then: `git diff --stat <baseline>..HEAD` and `git log --oneline <baseline>..HEAD`; include uncommitted work when the user means it.
3. Map changed files to pages: a page is affected when any path it cites changed, was moved, or was deleted, or when a new file joins a part or flow it describes.
4. For each affected page, re-read only the changed code it depends on and edit only the affected sections. Re-check every citation in those sections; line numbers drift.
5. Unaffected pages keep their old baseline. Do not bump a baseline on a page you did not re-verify.
6. Merge new terms into `glossary.md` and new sensitive spots into `sensitive-areas.md`; remove entries whose cited path no longer exists.
7. Record the update in `README.md`'s 更新记录: date, new baseline, pages touched, one line on why.

`impact/` and `changes/` pages are snapshots of a question at a moment. Do not edit old ones to match new code; write a new page and link the old one if useful.

## When to regenerate

Rewrite a page from scratch only when most of its cited paths changed or were removed, the project was restructured, or the user asks. Say so in the update record.
