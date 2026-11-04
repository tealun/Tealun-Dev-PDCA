# Commit and Push Closeout

Loaded from Tasker's Conditional References when the user requests a commit or push, or multi-phase M/L work reaches a checkpoint.

When the user explicitly requests a commit or push, treat delivery verification as part of the acceptance gate:

- Capture `git status --short` before staging and classify every tracked or untracked change as task-owned, user-owned, generated, or unrelated.
- Stage exact task-owned paths; preserve user-owned and unrelated worktree changes unless the user explicitly includes them.
- After committing, read back the commit ID and stat, then confirm the local branch points at that commit.
- After pushing, compare the remote branch SHA with the local commit SHA. Report any remaining uncommitted paths separately from the pushed artifact.
- If the requested repository path is corrected during the task, stop mutation, restate the concrete path mapping, and repeat the workspace identity check before continuing.

For multi-phase `M/L` work, use checkpoint commits at meaningful phase boundaries after that phase's targeted checks pass; do not defer all persistence until final closeout. Before each checkpoint, classify and remove only exact, known generated test/cache/log artifacts that are inside the task scope. Preserve runtime business data, backups, user files, and unrelated changes; when retention is uncertain, leave the path untouched and report it. Re-run `git status --short` after cleanup and after each checkpoint.
