# -*- coding: utf-8 -*-
"""Inject data-page, script order, data-page-i18n, product field labels into subpages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SCRIPT_BLOCK = (
    '  <script src="js/i18n-spec.js"></script>\n'
    '  <script src="js/page-i18n-data.js"></script>\n'
    '  <script src="js/main.js"></script>'
)

RE_MAIN_ONLY = re.compile(
    r'<script\s+src=["\']js/main\.js["\']\s*></script>',
    re.I,
)


def ensure_body_data_page(html: str, slug: str) -> str:
    if re.search(r'<body[^>]*\bdata-page\s*=', html, re.I):
        return html

    def repl(m):
        inner = m.group(1)
        if inner.strip():
            return '<body%s data-page="%s">' % (inner, slug)
        return '<body data-page="%s">' % slug

    return re.sub(r"<body([^>]*)>", repl, html, count=1, flags=re.I)


def replace_scripts(html: str) -> str:
    if "i18n-spec.js" in html:
        return html
    return RE_MAIN_ONLY.sub(SCRIPT_BLOCK.strip(), html, count=1)


def breadcrumb_bc(html: str) -> str:
    return re.sub(
        r'(<span class="bc-current"[^>]*)(>)',
        r'\1 data-page-i18n="bcCurrent"\2',
        html,
        count=1,
    )


def dt_title(html: str) -> str:
    # <dt><strong>... — avoid double attribute
    if 'data-page-i18n="dtTitle"' in html:
        return html
    return re.sub(
        r"(<dt>\s*<strong)(?![^>]*data-page-i18n)",
        r'\1 data-page-i18n="dtTitle"',
        html,
        count=1,
    )


def spec_section_title(html: str) -> str:
    # Vickers: Chi tiết kỹ thuật
    if 'data-i18n="detail.specTitle"' in html:
        return html
    html = re.sub(
        r'(<h2>\s*<strong)(>Chi tiết kỹ thuật</strong>)',
        r'\1 data-i18n="detail.specTitle"\2',
        html,
        count=1,
    )
    # Accessory short title
    html = re.sub(
        r'(<h2>\s*<strong)(>Chi tiết</strong>)',
        r'\1 data-i18n="detail.shortTitle"\2',
        html,
        count=1,
    )
    return html


def accessory_bc_link_v2(html: str) -> str:
    """Single replacement: link content from i18n."""
    if re.search(r'href="product-126\.html"[^>]*data-i18n', html):
        return html
    return re.sub(
        r'(<a\s+href="product-126\.html"[^>]*>)Phụ kiện tùy chọn(</a>)',
        r'\1<span data-i18n="sidebar.accessoriesLink">Phụ kiện tùy chọn</span>\2',
        html,
    )


def product_dd_fields(html: str) -> str:
    pairs = [
        ("Mã sản phẩm：", "product.fieldSku"),
        ("Xuất xứ：", "product.fieldOrigin"),
        ("Ngày đăng：", "product.fieldDate"),
        ("Hotline：", "product.fieldHotline"),
        ("Từ khóa：", "product.fieldKeywords"),
    ]
    for label, key in pairs:
        pat = (
            r'(<dd>\s*<strong>)'
            + re.escape(label)
            + r"(</strong></dd>)"
        )
        rep = r'<dd><strong><span data-i18n="%s">%s</span></strong></dd>' % (
            key,
            label,
        )
        html = re.sub(pat, rep, html, count=1)
    return html


def jqzoom_title(html: str) -> str:
    if 'data-i18n-title="product.zoomTitle"' in html:
        return html
    return re.sub(
        r'(<a[^>]*class="jqzoom"[^>]*)(title="[^"]*")',
        r'\1 data-i18n-title="product.zoomTitle" \2',
        html,
        count=1,
    )


def inject_intro_placeholder(html: str, path: Path) -> str:
    slug = path.stem
    if "product-intro" in html and "data-page-i18n-html" in html:
        return html

    # RLD-550: before spec-table-wrap
    if re.search(r'<div class="spec-table-wrap"', html, re.I):
        html2, n = re.subn(
            r'(<div class="xiangxi_con"[^>]*>)\s*[\s\S]*?(?=\s*<div\s+class="spec-table-wrap")',
            r'\1\n<div class="product-intro" data-page-i18n-html="intro"></div>\n',
            html,
            count=1,
            flags=re.I,
        )
        if n:
            return html2

    # Vickers: first <p>...</p> then <table
    html2, n = re.subn(
        r'(<div class="xiangxi_con"[^>]*>)\s*<p[^>]*>[\s\S]*?</p>(\s*<table)',
        r'\1\n<div class="product-intro" data-page-i18n-html="intro"></div>\2',
        html,
        count=1,
        flags=re.I,
    )
    if n:
        return html2

    # Accessory: first <p> block inside xiangxi_con
    if path.name.startswith("accessory-"):
        html2, n = re.subn(
            r'(<div class="xiangxi_con"[^>]*>)\s*<p[^>]*>[\s\S]*?</p>\s*(</div>)',
            r'\1\n<div class="product-intro" data-page-i18n-html="intro"></div>\n\2',
            html,
            count=1,
            flags=re.I,
        )
        if n:
            return html2

    return html


def prevnext_i18n(html: str) -> str:
    html = re.sub(
        r'(<a class="pn-link[^"]*"[^>]*href="[^"]*">)(← Quay lại danh mục)(</a>)',
        r'\1<span data-i18n="product.navBackCatalog">\2</span>\3',
        html,
        count=1,
    )
    html = re.sub(
        r'(<a class="pn-link[^"]*"[^>]*href="[^"]*">)(← Mục trước)(</a>)',
        r'\1<span data-i18n="product.navPrevShort">\2</span>\3',
        html,
        count=1,
    )
    html = re.sub(
        r'(<a class="pn-link pn-link--next"[^>]*href="[^"]*">)(Mục tiếp →)(</a>)',
        r'\1<span data-i18n="product.navNextShort">\2</span>\3',
        html,
        count=1,
    )
    html = re.sub(
        r'(<a class="pn-link pn-link--next"[^>]*href="[^"]*">)(Sản phẩm tiếp →)(</a>)',
        r'\1<span data-i18n="product.navNext">\2</span>\3',
        html,
        count=1,
    )
    html = re.sub(
        r'(<a class="pn-link"[^>]*href="[^"]*">)(← Sản phẩm trước)(</a>)',
        r'\1<span data-i18n="product.navPrev">\2</span>\3',
        html,
        count=1,
    )
    return html


def process_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8", errors="replace")
    slug = path.stem
    orig = html

    html = ensure_body_data_page(html, slug)
    html = replace_scripts(html)
    html = breadcrumb_bc(html)
    html = dt_title(html)
    html = spec_section_title(html)
    html = accessory_bc_link_v2(html)
    html = product_dd_fields(html)
    html = jqzoom_title(html)
    html = inject_intro_placeholder(html, path)
    html = prevnext_i18n(html)

    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    files = sorted(ROOT.glob("product-*.html")) + sorted(ROOT.glob("accessory-*.html"))
    n = 0
    for f in files:
        if process_file(f):
            print("updated", f.name)
            n += 1
    print("done,", n, "files changed")


if __name__ == "__main__":
    main()
