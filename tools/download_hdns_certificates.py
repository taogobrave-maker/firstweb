# -*- coding: utf-8 -*-
"""Download certificate images from hdnskelly.com Photo.aspx?ClassID=43"""
import re
import urllib.request
from pathlib import Path

BASE = "http://www.hdnskelly.com"
PAGE = BASE + "/Photo.aspx?ClassID=43"
OUT = Path(__file__).resolve().parent.parent / "assets" / "certificates-hdnskelly"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    html = fetch(PAGE).decode("utf-8", errors="replace")

    paths = set()
    for m in re.finditer(
        r'(?:href|src)\s*=\s*["\']?(/upload/[^"\'\s>]+)', html, re.I
    ):
        s = m.group(1).split("?")[0]
        if s.startswith("/upload/"):
            paths.add(s)

    # Fallback: known assets from site structure if parse misses
    known = [
        "/upload/20210820140546.png",
        "/upload/20210820140605.png",
        "/upload/20210820113543.jpg",
        "/upload/20210820105400.jpg",
        "/upload/20210820130632.png",
        "/upload/20210820130613.png",
        "/upload/20210820130556.png",
    ]
    for k in known:
        paths.add(k)

    saved = []
    for rel in sorted(paths):
        if not rel.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            continue
        full = BASE + rel
        name = rel.strip("/").replace("/", "_")
        dest = OUT / name
        try:
            data = fetch(full)
            dest.write_bytes(data)
            saved.append(str(dest))
            print("OK", len(data), name)
        except Exception as e:
            print("FAIL", full, e)

    print("---")
    print("Saved", len(saved), "files to", OUT)


if __name__ == "__main__":
    main()
