#!/usr/bin/env bash
# Swap the active hub UI. Variants live in assets/ui/*.html; the chosen one
# is copied over index.html, committed and pushed.
#   ./switch-ui.sh           → list variants (marks the active one)
#   ./switch-ui.sh terminal  → make assets/ui/terminal.html the live UI
set -euo pipefail
cd "$(dirname "$0")"

if [[ $# -eq 0 ]]; then
  echo "usage: ./switch-ui.sh <variant>"
  echo "variants:"
  for f in assets/ui/*.html; do
    v="$(basename "$f" .html)"
    if cmp -s "$f" index.html; then echo "  * $v  (active)"; else echo "    $v"; fi
  done
  exit 0
fi

src="assets/ui/$1.html"
if [[ ! -f "$src" ]]; then
  echo "no such variant: $1 (run ./switch-ui.sh to list)" >&2
  exit 1
fi

cp "$src" index.html
git add index.html
if git diff --cached --quiet; then
  echo "$1 is already active"
  exit 0
fi
git commit -m "switch hub UI → $1"
git push
echo "published → https://nitesh-nandan.github.io/docs-hub/"
