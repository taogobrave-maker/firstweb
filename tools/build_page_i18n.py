# -*- coding: utf-8 -*-
"""Extract per-page strings and emit js/page-i18n-data.js (PAGE_I18N) via JSON."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# English / Chinese overrides: docTitle, bcCurrent, dtTitle, intro (HTML fragments)
PAGE_EN = {
    "product-81": {
        "docTitle": "SVD-430TS — Digital touchscreen Vickers hardness tester | HDNS Pro instruments",
        "bcCurrent": "SVD-430TS — Digital touchscreen Vickers hardness tester",
        "dtTitle": "SVD-430TS — Digital touchscreen Vickers hardness tester",
        "intro": (
            "<strong>HDNS Vickers 400 series</strong><br/>"
            "SVD-430TS digital touchscreen Vickers hardness tester.<br/><br/>"
            "<strong>Applications:</strong><br/>"
            "- Carburized layers, ceramics, steel, non-ferrous metals<br/>"
            "- Thin sheets, foil, plating, small parts<br/>"
            "- Material hardness, heat treatment, case depth and hardening depth"
        ),
    },
    "product-82": {
        "docTitle": "SVD-432TS — Digital Vickers, auto turret | HDNS Pro instruments",
        "bcCurrent": "SVD-432TS — Digital Vickers, auto turret",
        "dtTitle": "SVD-432TS — Digital Vickers, auto turret",
        "intro": (
            "<strong>HDNS Vickers 400 series</strong><br/>"
            "SVD-432TS digital touchscreen Vickers hardness tester with automatic turret.<br/><br/>"
            "<strong>Applications:</strong><br/>"
            "- Carburized layers, ceramics, steel, non-ferrous metals<br/>"
            "- Thin sheets, foil, plating, small parts<br/>"
            "- Material hardness, heat treatment, case depth and hardening depth"
        ),
    },
    "product-83": {
        "docTitle": "SVD-450TS — Digital touchscreen Vickers hardness tester | HDNS Pro instruments",
        "bcCurrent": "SVD-450TS — Digital touchscreen Vickers hardness tester",
        "dtTitle": "SVD-450TS — Digital touchscreen Vickers hardness tester",
        "intro": (
            "<strong>HDNS Vickers 400 series</strong><br/>"
            "SVD-450TS digital touchscreen Vickers hardness tester.<br/><br/>"
            "<strong>Applications:</strong><br/>"
            "- Carburized layers, ceramics, steel, non-ferrous metals<br/>"
            "- Thin sheets, foil, plating, small parts<br/>"
            "- Material hardness, heat treatment, case depth and hardening depth"
        ),
    },
    "product-84": {
        "docTitle": "SVD-452TS — Digital Vickers, auto turret | HDNS Pro instruments",
        "bcCurrent": "SVD-452TS — Digital Vickers, auto turret",
        "dtTitle": "SVD-452TS — Digital Vickers, auto turret",
        "intro": (
            "<strong>HDNS Vickers 400 series</strong><br/>"
            "SVD-452TS digital touchscreen Vickers hardness tester with automatic turret.<br/><br/>"
            "<strong>Applications:</strong><br/>"
            "- Carburized layers, ceramics, steel, non-ferrous metals<br/>"
            "- Thin sheets, foil, plating, small parts<br/>"
            "- Material hardness, heat treatment, case depth and hardening depth"
        ),
    },
    "product-85": {
        "docTitle": "SVD-4052 — Low-load digital Vickers, auto turret | HDNS Pro instruments",
        "bcCurrent": "SVD-4052 — Low-load digital Vickers, auto turret",
        "dtTitle": "SVD-4052 — Low-load digital Vickers, auto turret",
        "intro": (
            "<strong>HDNS low-load Vickers series</strong><br/>"
            "SVD-4052 low-load digital touchscreen Vickers hardness tester with automatic turret.<br/><br/>"
            "<strong>Applications:</strong><br/>"
            "- Carburized layers, ceramics, steel, non-ferrous metals<br/>"
            "- Thin sheets, foil, plating, small parts<br/>"
            "- Material hardness, heat treatment, case depth and hardening depth"
        ),
    },
    "product-122": {
        "docTitle": "RLD-550 fully automatic high-precision Rockwell hardness tester | HDNS Pro instruments",
        "bcCurrent": "RLD-550 fully automatic high-precision Rockwell hardness tester",
        "dtTitle": "RLD-550 fully automatic high-precision Rockwell hardness tester",
        "intro": (
            "<p><strong>Model:</strong> RLD-550 high-precision fully automatic Rockwell hardness tester.</p>"
            "<p>Closed-loop servo loading with force feedback; optional Brinell mode on RLD-550B. "
            "See the specification table below for loads, standards and options.</p>"
        ),
    },
}

PAGE_ZH = {
    "product-81": {
        "docTitle": "SVD-430TS — 数显触摸屏维氏硬度计 | HDNS Pro instruments",
        "bcCurrent": "SVD-430TS — 数显触摸屏维氏硬度计",
        "dtTitle": "SVD-430TS — 数显触摸屏维氏硬度计",
        "intro": (
            "<strong>HDNS 维氏 400 系列</strong><br/>"
            "SVD-430TS 数显触摸屏维氏硬度计。<br/><br/>"
            "<strong>适用范围：</strong><br/>"
            "- 渗碳层、陶瓷、钢材、有色金属<br/>"
            "- 薄板、箔材、镀层、小型零件<br/>"
            "- 材料硬度、热处理、渗碳层深与淬硬层深"
        ),
    },
    "product-82": {
        "docTitle": "SVD-432TS — 数显维氏硬度计（自动转塔）| HDNS Pro instruments",
        "bcCurrent": "SVD-432TS — 数显维氏硬度计（自动转塔）",
        "dtTitle": "SVD-432TS — 数显维氏硬度计（自动转塔）",
        "intro": (
            "<strong>HDNS 维氏 400 系列</strong><br/>"
            "SVD-432TS 数显触摸屏维氏硬度计，配置自动物镜转塔。<br/><br/>"
            "<strong>适用范围：</strong><br/>"
            "- 渗碳层、陶瓷、钢材、有色金属<br/>"
            "- 薄板、箔材、镀层、小型零件<br/>"
            "- 材料硬度、热处理、渗碳层深与淬硬层深"
        ),
    },
    "product-83": {
        "docTitle": "SVD-450TS — 数显触摸屏维氏硬度计 | HDNS Pro instruments",
        "bcCurrent": "SVD-450TS — 数显触摸屏维氏硬度计",
        "dtTitle": "SVD-450TS — 数显触摸屏维氏硬度计",
        "intro": (
            "<strong>HDNS 维氏 400 系列</strong><br/>"
            "SVD-450TS 数显触摸屏维氏硬度计。<br/><br/>"
            "<strong>适用范围：</strong><br/>"
            "- 渗碳层、陶瓷、钢材、有色金属<br/>"
            "- 薄板、箔材、镀层、小型零件<br/>"
            "- 材料硬度、热处理、渗碳层深与淬硬层深"
        ),
    },
    "product-84": {
        "docTitle": "SVD-452TS — 数显维氏硬度计（自动转塔）| HDNS Pro instruments",
        "bcCurrent": "SVD-452TS — 数显维氏硬度计（自动转塔）",
        "dtTitle": "SVD-452TS — 数显维氏硬度计（自动转塔）",
        "intro": (
            "<strong>HDNS 维氏 400 系列</strong><br/>"
            "SVD-452TS 数显触摸屏维氏硬度计，配置自动物镜转塔。<br/><br/>"
            "<strong>适用范围：</strong><br/>"
            "- 渗碳层、陶瓷、钢材、有色金属<br/>"
            "- 薄板、箔材、镀层、小型零件<br/>"
            "- 材料硬度、热处理、渗碳层深与淬硬层深"
        ),
    },
    "product-85": {
        "docTitle": "SVD-4052 — 小负荷数显维氏硬度计（自动转塔）| HDNS Pro instruments",
        "bcCurrent": "SVD-4052 — 小负荷数显维氏硬度计（自动转塔）",
        "dtTitle": "SVD-4052 — 小负荷数显维氏硬度计（自动转塔）",
        "intro": (
            "<strong>HDNS 小负荷维氏系列</strong><br/>"
            "SVD-4052 小负荷数显触摸屏维氏硬度计，配置自动物镜转塔。<br/><br/>"
            "<strong>适用范围：</strong><br/>"
            "- 渗碳层、陶瓷、钢材、有色金属<br/>"
            "- 薄板、箔材、镀层、小型零件<br/>"
            "- 材料硬度、热处理、渗碳层深与淬硬层深"
        ),
    },
    "product-122": {
        "docTitle": "RLD-550 全自动高精度洛氏硬度计 | HDNS Pro instruments",
        "bcCurrent": "RLD-550 全自动高精度洛氏硬度计",
        "dtTitle": "RLD-550 全自动高精度洛氏硬度计",
        "intro": (
            "<p><strong>型号：</strong>RLD-550 高精度全自动洛氏硬度计。</p>"
            "<p>采用闭环伺服加载与力值反馈；RLD-550B 可选布氏模式。"
            "载荷、标准与功能详见下方参数表。</p>"
        ),
    },
}

ACCESSORY_EN = {
    "96": "Rockwell indenter tip HRB 1/16″ — HDNS-006 probe for Rockwell HRB scale.",
    "97": "Accessory — see images and notes on this page.",
}
ACCESSORY_ZH = {
    "96": "洛氏压头 HRB 1/16″ — HDNS-006，用于洛氏 HRB 标尺。",
    "97": "配件产品 — 详见页面图片与说明。",
}


def slug_from_name(name: str) -> str:
    return name.replace(".html", "")


def extract_intro(html: str) -> str:
    """Intro HTML inside xiangxi_con: text/images before spec table or main data table."""
    m = re.search(
        r'<div class="xiangxi_con"[^>]*>\s*([\s\S]*?)\s*<div\s+class="spec-table-wrap"',
        html,
        re.IGNORECASE,
    )
    if m:
        return m.group(1).strip()
    m = re.search(
        r'<div class="xiangxi_con"[^>]*>\s*<p[^>]*>([\s\S]*?)</p>\s*<table',
        html,
        re.IGNORECASE,
    )
    if m:
        inner = m.group(1).strip()
        inner = re.sub(r"<br\s*/?>", "<br/>", inner, flags=re.I)
        return inner
    m = re.search(
        r'<div class="xiangxi_con"[^>]*>\s*<p[^>]*>([\s\S]*?)</p>',
        html,
        re.IGNORECASE,
    )
    if m:
        inner = m.group(1).strip()
        inner = re.sub(r"<br\s*/?>", "<br/>", inner, flags=re.I)
        return inner
    return ""


def build_bundle(path: Path, html: str, slug: str) -> dict:
    title_m = re.search(r"<title>([^<]+)</title>", html, re.I)
    doc_title = title_m.group(1).strip() if title_m else ""

    bc_m = re.search(r'<span class="bc-current"[^>]*>([^<]+)</span>', html)
    bc = bc_m.group(1).strip() if bc_m else ""

    dt_m = re.search(r"<dt>\s*<strong>\s*([^<]+)\s*</strong>\s*</dt>", html, re.S)
    dt = re.sub(r"\s+", " ", dt_m.group(1).strip()) if dt_m else ""

    intro_vi = extract_intro(html)

    vi = {
        "docTitle": doc_title,
        "bcCurrent": bc,
        "dtTitle": dt,
        "intro": intro_vi,
    }
    en = {**vi}
    zh = {**vi}

    if slug in PAGE_EN:
        en.update(PAGE_EN[slug])
    if slug in PAGE_ZH:
        zh.update(PAGE_ZH[slug])

    if path.name.startswith("accessory-"):
        num = slug.replace("accessory-", "")
        if num in ACCESSORY_EN:
            en["intro"] = ACCESSORY_EN[num]
        if num in ACCESSORY_ZH:
            zh["intro"] = ACCESSORY_ZH[num]

    return {"vi": vi, "en": en, "zh": zh}


def main():
    products = sorted(ROOT.glob("product-*.html"))
    accessories = sorted(ROOT.glob("accessory-*.html"))
    page_i18n = {}

    for path in list(products) + list(accessories):
        html = path.read_text(encoding="utf-8", errors="replace")
        slug = slug_from_name(path.name)
        page_i18n[slug] = build_bundle(path, html, slug)

    payload = json.dumps(page_i18n, ensure_ascii=False, indent=2)
    js = (
        "/* Auto-built PAGE_I18N — per-page titles and intro; regenerate: python tools/build_page_i18n.py */\n"
        "(function () {\n"
        "  window.PAGE_I18N = window.PAGE_I18N || {};\n"
        f"  Object.assign(window.PAGE_I18N, {payload});\n"
        "})();\n"
    )
    out = ROOT / "js" / "page-i18n-data.js"
    out.write_text(js, encoding="utf-8")
    print("Wrote", out, "pages:", len(page_i18n))


if __name__ == "__main__":
    main()
