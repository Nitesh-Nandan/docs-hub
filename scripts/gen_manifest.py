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
}


def doc_meta(path: Path, section: str) -> dict:
    html = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    title = (
        re.sub(r"\s+", " ", m.group(1)).replace("&amp;", "&").strip()
        if m
        else path.stem
    )
    dm = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    d = dm.group(1) if dm else date.fromtimestamp(path.stat().st_mtime).isoformat()
    doc = {"file": f"{section}/{path.name}", "title": title, "date": d}

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
    docs = sorted(
        (doc_meta(f, folder.name) for f in sorted(folder.glob("*.html"))),
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
