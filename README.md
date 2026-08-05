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

## Publish new docs

```bash
./sync.sh
```

## Add a new section

1. `mkdir my-section` and drop HTML files in it.
2. (Optional) add a title/icon/description for it in `SECTIONS` inside
   `scripts/gen_manifest.py`, and a source rsync line in `sync.sh`.
3. `./sync.sh`
