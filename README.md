# Docs Hub

Personal research reports, plans and tools, published via GitHub Pages:
**https://nitesh-nandan.github.io/docs-hub/**

## How it works

- Every top-level folder is a **section** (`ipo-reports/`, `sip-plans/`,
  `calculators/`, …). Any `*.html` file inside a section shows up on the hub
  automatically — each doc is self-contained and opens in a new tab.
- `scripts/gen_manifest.py` scans the folders and writes `data/manifest.js`,
  which `index.html` renders (sections, search, score chips).
- `sync.sh` copies new docs from their source dirs, regenerates the manifest,
  commits and pushes.
- The hub UI itself is **swappable**: `index.html` is a byte-for-byte copy of
  one variant in `assets/ui/` (currently `classic` and `terminal`), managed
  by `switch-ui.sh`.

## Publish new docs

```bash
./sync.sh
```

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

## Add a new section

1. `mkdir my-section` and drop HTML files in it.
2. (Optional) add a title/icon/description for it in `SECTIONS` inside
   `scripts/gen_manifest.py`, and a source rsync line in `sync.sh`.
3. `./sync.sh`

## Handy commands

| Task | Command |
|---|---|
| Publish everything new | `./sync.sh` |
| List / swap the hub UI | `./switch-ui.sh` · `./switch-ui.sh <variant>` |
| Regenerate manifest only | `python3 scripts/gen_manifest.py` |
| Preview locally | `open index.html` (works on `file://`, no server) |
