#!/usr/bin/env bash
set -euo pipefail

# ── Files/dirs that live only in dev — never synced to main ──────────────────
DEV_ONLY=(
  DEVELOPMENT.md
  .pre-commit-config.yaml
  tests
)
# ─────────────────────────────────────────────────────────────────────────────

# Check prerequisites
if ! command -v gh &>/dev/null; then
  echo "Error: gh CLI not found. Install it from https://cli.github.com/" >&2
  exit 1
fi

# Must be run from dev
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" != "dev" ]; then
  echo "Error: must be run from the dev branch (currently on '$current_branch')" >&2
  exit 1
fi

# Fetch latest remote state
echo "Fetching latest remote state..."
git fetch origin main dev --quiet

is_dev_only() {
  local file="$1"
  for pattern in "${DEV_ONLY[@]}"; do
    if [[ "$file" == "$pattern" || "$file" == "$pattern/"* ]]; then
      return 0
    fi
  done
  return 1
}

# Parse changed files between main and dev
declare -a to_checkout=()  # added or modified on dev
declare -a to_delete=()    # deleted on dev (exists on main)

while IFS=$'\t' read -r status file rest; do
  case "$status" in
    R*)
      # Rename: file=old name, rest=new name
      is_dev_only "$file"  || to_delete+=("$file")
      is_dev_only "$rest"  || to_checkout+=("$rest")
      ;;
    D*)
      is_dev_only "$file"  || to_delete+=("$file")
      ;;
    *)
      # A, M, C, etc.
      is_dev_only "$file"  || to_checkout+=("$file")
      ;;
  esac
done < <(git diff --name-status origin/main..dev)

n_add=${#to_checkout[@]}
n_del=${#to_delete[@]}

if [ "$n_add" -eq 0 ] && [ "$n_del" -eq 0 ]; then
  echo "Nothing to sync — dev and main are already in sync (excluding dev-only files)."
  exit 0
fi

echo ""
echo "Files to sync to main:"
for f in "${to_checkout[@]}"; do printf "  + %s\n" "$f"; done
for f in "${to_delete[@]}";   do printf "  - %s\n" "$f"; done
echo ""

# Create a branch off main
branch="sync/dev-to-main-$(date +%Y%m%d-%H%M%S)"
git checkout -b "$branch" origin/main --quiet
echo "Created branch: $branch"

# Apply changes
for f in "${to_checkout[@]}"; do
  git checkout dev -- "$f"
done

for f in "${to_delete[@]}"; do
  git rm -f "$f" --quiet 2>/dev/null || true
done

# Commit
if [ "$n_add" -gt 0 ] && [ "$n_del" -eq 0 ]; then
  commit_msg="Sync $n_add production file(s) from dev"
elif [ "$n_del" -gt 0 ] && [ "$n_add" -eq 0 ]; then
  commit_msg="Remove $n_del production file(s) (synced from dev)"
else
  commit_msg="Sync production files from dev ($n_add updated, $n_del removed)"
fi

git add -A
git commit -m "$commit_msg" --quiet

# Push
git push -u origin "$branch" --quiet
echo "Pushed to origin/$branch"

# Build PR body
pr_body="## Changes"$'\n\n'

if [ "$n_add" -gt 0 ]; then
  pr_body+="**Updated/added:**"$'\n'
  for f in "${to_checkout[@]}"; do pr_body+="- \`$f\`"$'\n'; done
  pr_body+=$'\n'
fi

if [ "$n_del" -gt 0 ]; then
  pr_body+="**Removed:**"$'\n'
  for f in "${to_delete[@]}"; do pr_body+="- \`$f\`"$'\n'; done
  pr_body+=$'\n'
fi

pr_body+="_Synced from \`dev\` — dev-only files excluded._"

# Open PR
pr_url=$(gh pr create \
  --base main \
  --head "$branch" \
  --title "$commit_msg" \
  --body "$pr_body")

echo ""
echo "PR created: $pr_url"

# Return to dev
git checkout dev --quiet
echo "Back on dev."
