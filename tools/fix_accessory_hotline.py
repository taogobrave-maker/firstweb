# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD = "<dd><strong>Hotline：</strong><span>+84 981 729 869</span></dd>"
NEW = """<dd><strong><span data-i18n="product.fieldHotline">Hotline：</span></strong><span>+84 981 729 869</span></dd>"""

for f in sorted(ROOT.glob("accessory-*.html")):
    t = f.read_text(encoding="utf-8")
    if OLD in t:
        f.write_text(t.replace(OLD, NEW), encoding="utf-8")
        print("ok", f.name)
