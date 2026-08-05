#!/usr/bin/env bash
# Pull fresh docs from source dirs, regenerate the manifest, commit & push.
# Add one rsync line per source → section mapping as new doc types appear.
set -euo pipefail
cd "$(dirname "$0")"

# --- sources ---------------------------------------------------------------
rsync -a --include='*.html' --exclude='*' \
  "$HOME/workspace/2026/100cr/backtest-strategy/strategy_ipo_recross/reports/" ipo-reports/
# rsync -a --include='*.html' --exclude='*'  <sip-plans source dir>/  sip-plans/
# ---------------------------------------------------------------------------

python3 scripts/gen_manifest.py

git add -A
if git diff --cached --quiet; then
  echo "nothing new to publish"
  exit 0
fi
git commit -m "sync docs $(date +%F)"
git push
echo "published → https://nitesh-nandan.github.io/docs-hub/"
