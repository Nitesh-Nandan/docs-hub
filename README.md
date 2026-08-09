# Docs Hub

Personal research reports, plans, books and tools, published via GitHub Pages:
**https://docs.niteshnandan.cloud** (also
https://nitesh-nandan.github.io/docs-hub/)

> ⚠️ **This repo is public.** Never commit account numbers, broker tokens,
> portfolio values, API keys or personal data.

## How it works

- Every top-level folder is a **section** (`ipo-reports/`, `books/`,
  `prompts/`, …). Drop a file in, run `./sync.sh`, and it appears on the hub.
- `scripts/gen_manifest.py` scans the section folders and writes
  `data/manifest.js`, which `index.html` renders (sections, search, sort,
  score chips). **Never edit `data/manifest.js` by hand.**
- `sync.sh` copies new docs from their source dirs, regenerates the manifest,
  commits and pushes.
- The hub UI itself is **swappable**: `index.html` is a byte-for-byte copy of
  one variant in `assets/ui/` (currently `classic` and `terminal`), managed
  by `switch-ui.sh`.

## Publish a new document

Copy the file into the section folder, then sync. That's the whole flow —
no manifest editing, nothing to register.

```bash
cp ~/Downloads/annual-letter_2026-08-09.pdf books/
./sync.sh
```

Live in ~30–60s.

### Supported file types

Files are published **as-is** — never converted, reformatted or rewritten.

| Type | How it opens |
|---|---|
| `.html` | directly, full-window (must be self-contained — inline CSS/JS, no CDN) |
| `.md` `.txt` `.json` `.yaml` `.sql` `.py` `.sh` `.log` … | verbatim in a `<pre>`, nothing parsed |
| `.csv` `.tsv` | table view by default, one click to raw text |
| `.pdf` | embedded reader |
| `.png` `.jpg` `.svg` `.gif` `.webp` | inline |

Everything except `.html` opens through **`viewer.html?f=<path>`**, which adds
**Copy all · Raw file · Download**. Copy gives you the exact source text;
Download works for every type.

To support a new extension, add it to `TEXT_EXT` in
`scripts/gen_manifest.py`. Nothing else needs changing.

### Naming rules

- **Title** — taken from `<title>` for HTML, the first `# heading` for
  Markdown, and the **filename** for everything else (`-` and `_` become
  spaces). So `Annual-Letter_2026.pdf` → "Annual Letter 2026". Name PDFs and
  CSVs the way you want them to read.
- **Date** — a `YYYY-MM-DD` anywhere in the filename, else the file's mtime.
  Include it if you want sort order to survive a re-copy:
  `annual-letter_2026-08-09.pdf`.

## Add a new section

1. `mkdir my-section` (kebab-case) and drop files in it.
2. *Optional polish* — add a title, emoji icon, description and order in
   `SECTIONS` inside `scripts/gen_manifest.py`. Unlisted folders still work,
   with a name derived from the folder and a generic 📄 icon.
3. *Optional* — if docs for it are generated in another repo, add one rsync
   line in `sync.sh` mapping `<source dir>/ → <section>/`.
4. `./sync.sh`

Current sections: `ipo-reports`, `sip-plans`, `calculators`, `roadmaps`,
`interview-prep`, `market-research`, `books`, `prompts`.

## Switch the hub UI

```bash
./switch-ui.sh            # list variants, shows which is active
./switch-ui.sh classic    # make assets/ui/classic.html the live UI
./switch-ui.sh terminal   # make assets/ui/terminal.html the live UI
```

The script copies the variant over `index.html`, commits and pushes — live
in ~60s. **Never edit `index.html` directly**: change the variant file in
`assets/ui/`, then re-run `./switch-ui.sh <variant>` (it stages both files).

To add a new look, drop `assets/ui/<name>.html` (self-contained, renders
`data/manifest.js`) and run `./switch-ui.sh <name>`.

## Handy commands

| Task | Command |
|---|---|
| Publish everything new | `./sync.sh` |
| Add one file | `cp <file> <section>/ && ./sync.sh` |
| Regenerate manifest only | `python3 scripts/gen_manifest.py` |
| List / swap the hub UI | `./switch-ui.sh` · `./switch-ui.sh <variant>` |
| Preview locally | `open index.html` |
| Check Pages deploy status | `gh api repos/Nitesh-Nandan/docs-hub/pages --jq .status` |

**Local preview caveat:** `open index.html` works on `file://`, but the
viewer can't load text files there — browsers block the fetch. Use
`python3 -m http.server 8000` and open `http://localhost:8000` to test
`.md` / `.csv` viewing locally, or just check it on the published site.

## Don't edit synced reports here

Documents rsynced from a source repo (e.g.
`backtest-strategy/strategy_ipo_recross/reports/`) are regenerated there.
Fix them at the source and re-run `./sync.sh` — direct edits in this repo get
overwritten by the next sync.
