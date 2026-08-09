#!/usr/bin/env python3
"""Draw the hub favicon and write favicon.png / favicon.ico at the repo root.

The mark is three document rules on the accent gold tile — the same accent the
hub UI uses. Pure stdlib: the PNG is assembled by hand and wrapped in an ICO
container (browsers have accepted PNG-payload ICOs since Vista).

Run: python3 scripts/gen_favicon.py
"""
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GOLD = (182, 130, 53, 255)     # #b68235 — hub accent
INK = (25, 24, 22, 255)        # #191816 — hub ink
CLEAR = (0, 0, 0, 0)

SIZE = 64                      # drawn at 64px, downscaled for the small entries
RADIUS = 14
BARS = [(14, 18, 36), (14, 30, 36), (14, 42, 24)]   # x, y, width
BAR_H = 6


def draw(size: int) -> list:
    """Return `size` rows of RGBA tuples, supersampled 4x for smooth edges."""
    ss = 4
    n = size * ss
    r = RADIUS * (n / SIZE)
    scale = n / SIZE

    def inside_tile(x, y):
        # rounded square: clamp to the corner circle centres
        cx = min(max(x, r), n - r)
        cy = min(max(y, r), n - r)
        return (x - cx) ** 2 + (y - cy) ** 2 <= r * r

    def inside_bar(x, y):
        for bx, by, bw in BARS:
            x0, y0 = bx * scale, by * scale
            x1, y1 = (bx + bw) * scale, (by + BAR_H) * scale
            br = (BAR_H / 2) * scale
            cx = min(max(x, x0 + br), x1 - br)
            cy = min(max(y, y0 + br), y1 - br)
            if (x - cx) ** 2 + (y - cy) ** 2 <= br * br:
                return True
        return False

    rows = []
    for py in range(size):
        row = []
        for px in range(size):
            acc = [0, 0, 0, 0]
            for sy in range(ss):
                for sx in range(ss):
                    x = px * ss + sx + 0.5
                    y = py * ss + sy + 0.5
                    c = CLEAR
                    if inside_tile(x, y):
                        c = INK if inside_bar(x, y) else GOLD
                    for i in range(4):
                        acc[i] += c[i]
            row.append(tuple(v // (ss * ss) for v in acc))
        rows.append(row)
    return rows


def png_bytes(rows: list) -> bytes:
    h = len(rows)
    w = len(rows[0])
    raw = b"".join(
        b"\x00" + b"".join(struct.pack("BBBB", *px) for px in row) for row in rows
    )

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def ico_bytes(pngs: dict) -> bytes:
    """pngs: {size: png_bytes}. ICO with PNG-compressed entries."""
    entries, blobs = b"", b""
    offset = 6 + 16 * len(pngs)
    for size in sorted(pngs):
        data = pngs[size]
        entries += struct.pack(
            "<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(data), offset
        )
        blobs += data
        offset += len(data)
    return struct.pack("<HHH", 0, 1, len(pngs)) + entries + blobs


pngs = {s: png_bytes(draw(s)) for s in (16, 32, 48)}
(ROOT / "favicon.ico").write_bytes(ico_bytes(pngs))
(ROOT / "favicon.png").write_bytes(png_bytes(draw(180)))   # apple-touch-icon
print(f"favicon.ico ({(ROOT / 'favicon.ico').stat().st_size} B, 16/32/48) + favicon.png (180px)")
