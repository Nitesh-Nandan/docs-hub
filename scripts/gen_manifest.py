#!/usr/bin/env python3
"""Scan every section folder for *.html docs and write data/manifest.js.

Any top-level folder (except the ones in SKIP) is a section. Drop HTML files
into a folder, run this script, and the hub index picks them up. No manual
editing of the manifest — ever.
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"data", "scripts", "assets", ".git", ".github", "node_modules"}

# Self-contained HTML docs open full-window on their own.
DIRECT_EXT = {".html", ".htm"}
# Everything else opens through viewer.html, which displays the file as-is and
# adds Copy / Raw / Download. Text lands in a <pre> verbatim (CSV and TSV also
# get a table view), PDFs in an embedded reader, images inline.
TEXT_EXT = {
    ".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml", ".toml", ".ini",
    ".sql", ".py", ".js", ".ts", ".sh", ".css", ".xml", ".log",
}
BINARY_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
INDEX_EXT = DIRECT_EXT | TEXT_EXT | BINARY_EXT

# Optional presentation metadata per section. Folders not listed here still
# work — title is derived from the folder name and order defaults to last.
SECTIONS = {
    "ipo-reports": {
        "title": "IPO Reports",
        "icon": "\U0001F4C8",
        "desc": "QGLP-A opportunity reviews of fresh NSE listings — is it a compounder, and is the upside still on the table?",
        "order": 1,
    },
    "sip-plans": {
        "title": "SIP Plans",
        "icon": "\U0001F5D3",
        "desc": "SIP & lump-sum allocation decisions — where the next rupee goes.",
        "order": 2,
    },
    "calculators": {
        "title": "Calculators",
        "icon": "\U0001F9EE",
        "desc": "Interactive financial calculators and tools.",
        "order": 3,
    },
    "roadmaps": {
        "title": "Roadmaps",
        "icon": "\U0001F5FA",
        "desc": "Long-term plans and milestone roadmaps — where things are headed and by when.",
        "order": 4,
    },
    "interview-prep": {
        "title": "Interview Prep",
        "icon": "\U0001F3AF",
        "desc": "Interview preparation notes, guides and practice material.",
        "order": 5,
    },
    "market-research": {
        "title": "Market Research",
        "icon": "\U0001F50D",
        "desc": "Market and equity research reports — sector views and stock deep-dives.",
        "order": 6,
    },
    "books": {
        "title": "Books",
        "icon": "\U0001F4DA",
        "desc": "Book summaries built as mentoring documents — the author's lens, not just their bullet points.",
        "order": 7,
    },
    "prompts": {
        "title": "Prompts",
        "icon": "\U0001F9ED",
        "desc": "Reusable prompt specs — the instructions that produce the documents in this hub.",
        "order": 8,
    },
}


def doc_meta(path: Path, section: str) -> dict:
    rel = f"{section}/{path.name}"
    suffix = path.suffix.lower()
    html = ""

    # Nothing here is ever rewritten. Standalone HTML docs are linked straight
    # at; everything else goes through viewer.html so it displays in place
    # (instead of downloading) and gets Copy / Raw / Download.
    link = rel if suffix in DIRECT_EXT else f"viewer.html?f={rel}"

    if suffix in (".html", ".htm"):
        html = path.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        title = (
            re.sub(r"\s+", " ", m.group(1)).replace("&amp;", "&").strip()
            if m
            else path.stem
        )
    elif suffix == ".md":
        text = path.read_text(encoding="utf-8", errors="ignore")
        hm = re.search(r"^#\s+(.+)$", text, re.M)
        title = hm.group(1).strip() if hm else path.stem
    else:
        title = path.stem.replace("-", " ").replace("_", " ")

    dm = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    d = dm.group(1) if dm else date.fromtimestamp(path.stat().st_mtime).isoformat()
    doc = {"file": link, "title": title, "date": d, "kind": suffix.lstrip(".")}

    # Enrichment: score chips for docs that embed QGLP-A stock data.
    syms = list(dict.fromkeys(re.findall(r'sym:"([A-Z0-9_]+)"', html)))
    opps = re.findall(r'opp:\{score:([0-9.]+),\s*verdict:"([^"]+)"', html)
    if syms:
        doc["stocks"] = [
            {
                "sym": s,
                "score": float(opps[i][0]) if i < len(opps) else None,
                "verdict": opps[i][1] if i < len(opps) else None,
            }
            for i, s in enumerate(syms)
        ]
    return doc


sections = []
for folder in sorted(
    p
    for p in ROOT.iterdir()
    if p.is_dir() and p.name not in SKIP and not p.name.startswith(".")
):
    files = sorted(
        f
        for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in INDEX_EXT
    )
    docs = sorted(
        (doc_meta(f, folder.name) for f in files),
        key=lambda x: x["date"],
        reverse=True,
    )
    meta = SECTIONS.get(folder.name, {})
    sections.append(
        {
            "id": folder.name,
            "title": meta.get("title", folder.name.replace("-", " ").title()),
            "icon": meta.get("icon", "\U0001F4C4"),
            "desc": meta.get("desc", ""),
            "order": meta.get("order", 99),
            "docs": docs,
        }
    )
sections.sort(key=lambda s: (s["order"], s["title"]))

out = ROOT / "data" / "manifest.js"
out.parent.mkdir(exist_ok=True)
out.write_text("window.MANIFEST = " + json.dumps(sections, indent=1) + ";\n")
print(
    f"{out.relative_to(ROOT)}: {len(sections)} sections, "
    f"{sum(len(s['docs']) for s in sections)} docs"
)
