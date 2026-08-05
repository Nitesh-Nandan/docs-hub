# Docs Hub — CLAUDE.md

Personal docs hub published via **GitHub Pages**. Live at
**https://nitesh-nandan.github.io/docs-hub/** · repo `Nitesh-Nandan/docs-hub`.

This repo renders self-contained HTML documents (reports, plans, tools)
generated elsewhere (mostly the `backtest-strategy` lab). It is a **publishing
artifact, not a source repo** — documents are produced in their source repos
and *synced* here.

⚠️ **This repo is PUBLIC** (required for Pages on the free plan). Never commit
account numbers, broker tokens, portfolio values, API keys, or personal data.
Stock analysis and calculators are fine.

---

## How it works

```
docs-hub/
├── index.html            # ACTIVE hub UI — a copy of one assets/ui/ variant
├── assets/ui/*.html      # UI variants (classic, terminal, …); edit these, not index.html
├── switch-ui.sh          # ./switch-ui.sh <variant> → copy to index.html + commit + push
├── data/manifest.js      # AUTO-GENERATED — never edit by hand
├── scripts/gen_manifest.py  # scans section folders → writes data/manifest.js
├── sync.sh               # copy new docs from sources + regen + commit + push
├── ipo-reports/*.html    # section: IPO opportunity reviews (QGLP-A)
├── sip-plans/            # section: SIP & lump-sum decisions
└── calculators/          # section: interactive tools
```

- **Every top-level folder is a section** (except `data/`, `scripts/`,
  `assets/`, dotfolders). The hub home page shows one card per folder;
  clicking it lists that folder's docs; each doc opens in a new tab.
- `gen_manifest.py` extracts per-doc metadata: `<title>`, date
  (`YYYY-MM-DD` in the filename, else file mtime), and — if the HTML embeds
  QGLP-A data (`sym:"X"` + `opp:{score:N, verdict:"…"}` patterns) — stock
  score chips.
- Pages deploys from `main` branch root (legacy build); changes go live
  ~30–60s after push.

## Add a report to an existing section

1. Drop the `.html` file into the section folder (or let `sync.sh` copy it
   from its source dir — see the rsync lines in `sync.sh`).
2. Run `./sync.sh` — it regenerates the manifest, commits, and pushes.

That's it. Never edit `data/manifest.js` manually.

## Add a new section

1. `mkdir <section-name>` (kebab-case) and add HTML files.
2. Optional polish: add an entry in `SECTIONS` inside
   `scripts/gen_manifest.py` (title, emoji icon, description, order).
   Unlisted folders still work with auto-derived names.
3. If docs for it are generated in another repo, add one rsync line in
   `sync.sh` mapping `<source dir>/ → <section>/`.
4. Run `./sync.sh`.

## Conventions & rules

- **Documents must be fully self-contained HTML** — inline CSS/JS, no CDN
  links, no external images. They are opened directly as static files.
- **Filenames**: include the date as `YYYY-MM-DD` (e.g.
  `ipo_RSL_2026-08-05.html`) — the manifest and sorting rely on it. Give
  every doc a meaningful `<title>` tag; that's what the card shows.
- **Don't edit synced reports here.** They're generated in their source repo
  (e.g. `backtest-strategy/strategy_ipo_recross/reports/`). Fix them there,
  then re-run `./sync.sh`. Direct edits here get overwritten by the next sync.
- **Hub UI is swappable**: `index.html` is a byte-for-byte copy of one
  variant in `assets/ui/` (`assets/` is excluded from the manifest scan).
  **Never edit index.html directly** — edit the variant, then run
  `./switch-ui.sh <variant>` to re-copy, commit, and push. Each variant
  must theme via CSS variables with light **and** dark support (manual
  toggle persisted in localStorage), and keep the verdict color convention:
  green = CONVICTION/BET, amber = OPPORTUNITY/SELECTIVE/WATCH, red =
  NOT-AN-OPPORTUNITY/AVOID/BYE.
- Commit messages: short imperative summary; no need for elaborate bodies.

## Common tasks

| Task | Command |
|---|---|
| Publish everything new | `./sync.sh` |
| List / swap the hub UI | `./switch-ui.sh` · `./switch-ui.sh <variant>` |
| Regenerate manifest only | `python3 scripts/gen_manifest.py` |
| Preview locally | `open index.html` (works on file://, no server needed) |
| Check Pages deploy status | `gh api repos/Nitesh-Nandan/docs-hub/pages --jq .status` |
