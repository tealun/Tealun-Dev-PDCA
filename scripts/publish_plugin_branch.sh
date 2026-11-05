#!/usr/bin/env bash
# Commit the contents of a built plugin folder to a branch that holds nothing else,
# then push it. Appends one commit per change; never rewrites the branch's history.
# Works in a detached worktree and creates no local branch, so it can run again in
# the same clone (the first commit of a new branch simply has no parent).
# Usage: scripts/publish_plugin_branch.sh <built-plugin-dir> <branch> [remote]
set -euo pipefail

src=$(cd "$1" && pwd)
branch=$2
remote=${3:-origin}
version=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['version'])" "$src/.claude-plugin/plugin.json")
source_sha=$(git rev-parse --short HEAD)
work=$(mktemp -d)
trap 'git worktree remove --force "$work" >/dev/null 2>&1 || true' EXIT

git config user.name >/dev/null || git config user.name "github-actions[bot]"
git config user.email >/dev/null || git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

parent=()
if git ls-remote --exit-code --heads "$remote" "$branch" >/dev/null; then
  git fetch --quiet "$remote" "refs/heads/$branch"
  git worktree add --quiet --detach "$work" FETCH_HEAD
  parent=(-p "$(git -C "$work" rev-parse HEAD)")
else
  git worktree add --quiet --detach "$work"
fi

# Replace everything except .git with the built plugin.
find "$work" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
git -C "$work" rm -rq --cached --ignore-unmatch .
cp -a "$src/." "$work/"
git -C "$work" add -A
tree=$(git -C "$work" write-tree)

if [ ${#parent[@]} -gt 0 ] && [ "$tree" = "$(git -C "$work" rev-parse 'HEAD^{tree}')" ]; then
  echo "$branch already holds tealun-dev-pdca $version; nothing to commit"
  exit 0
fi
commit=$(git -C "$work" commit-tree "$tree" ${parent[@]+"${parent[@]}"} -m "tealun-dev-pdca $version (built from $source_sha)")
git -C "$work" push --quiet "$remote" "$commit:refs/heads/$branch"
echo "pushed tealun-dev-pdca $version to $branch: $(git -C "$work" rev-parse --short "$commit")"
