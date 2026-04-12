# -*- coding: utf-8 -*-
"""Add language switcher + i18n chrome to product-*.html and accessory-*.html."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TOP_BAR_REPLACEMENT = """  <div class="top-bar">
    <div class="container top-bar-inner">
      <p class="top-welcome"><span data-i18n="top.welcome">Chào mừng đến với</span> <strong>HDNS Pro instruments</strong></p>
      <div class="top-contact">
        <a class="top-phone" href="tel:+84981729869"><span data-i18n="top.phone">Điện thoại:</span> +84 981 729 869</a>
        <span class="top-zalo-label">Zalo:</span>
        <img class="top-zalo-qr" src="images/zalo-qr.png" width="44" height="44" alt="Mã QR Zalo — HDNS Pro instruments" data-i18n-alt="top.zaloAlt" />
        <span class="top-wechat-label" data-i18n="top.wechatLabel">WeChat:</span>
        <img class="top-wechat-qr" src="images/wechat-qr.png" width="44" height="44" alt="" data-i18n-alt="top.wechatAlt" />
        <a class="top-wa" href="https://wa.me/84981729869" target="_blank" rel="noopener noreferrer" data-i18n="top.whatsappShort">WhatsApp</a>
        <div class="lang-switcher" role="group" aria-label="Language switcher">
          <button type="button" class="lang-btn" data-lang="vi" aria-pressed="true">VI</button>
          <button type="button" class="lang-btn" data-lang="en" aria-pressed="false">EN</button>
          <button type="button" class="lang-btn" data-lang="zh" aria-pressed="false">中文</button>
        </div>
      </div>
    </div>
  </div>"""

# Two observed top-bar blocks (product vs compact accessory formatting)
TOP_BAR_VARIANTS = [
    """  <div class="top-bar">
    <div class="container top-bar-inner">
      <p class="top-welcome">Chào mừng đến với <strong>HDNS Pro instruments</strong></p>
      <div class="top-contact">
        <a class="top-phone" href="tel:+84981729869">Điện thoại: +84 981 729 869</a>
        <span class="top-zalo-label">Zalo:</span>
        <img class="top-zalo-qr" src="images/zalo-qr.png" width="44" height="44" alt="Zalo" />
      </div>
    </div>
  </div>""",
    """<div class="top-bar">
<div class="container top-bar-inner">
<p class="top-welcome">Chào mừng đến với <strong>HDNS Pro instruments</strong></p>
<div class="top-contact">
<a class="top-phone" href="tel:+84981729869">Điện thoại: +84 981 729 869</a>
<span class="top-zalo-label">Zalo:</span>
<img alt="Mã QR Zalo — HDNS Pro instruments" class="top-zalo-qr" height="44" src="images/zalo-qr.png" width="44"/>
</div>
</div>
</div>""",
]


def ensure_contact_css(html: str) -> str:
    if "contact-channels.css" in html:
        return html
    needle2 = '<link rel="stylesheet" href="css/product-detail.css" />'
    if needle2 in html:
        return html.replace(
            needle2,
            needle2 + "\n  <link rel=\"stylesheet\" href=\"css/contact-channels.css\" />",
            1,
        )
    needle3 = '<link href="css/product-detail.css" rel="stylesheet"/>'
    if needle3 in html:
        return html.replace(
            needle3,
            needle3 + '\n<link href="css/contact-channels.css" rel="stylesheet"/>',
            1,
        )
    return html


def replace_top_bar(html: str) -> str:
    if "lang-switcher" in html:
        return html
    for old in TOP_BAR_VARIANTS:
        if old in html:
            return html.replace(old, TOP_BAR_REPLACEMENT, 1)
    return html


def patch_nav(html: str) -> str:
    html = html.replace(
        '<nav class="main-nav" aria-label="Chính">',
        '<nav class="main-nav" aria-label="Chính" data-i18n-aria-label="nav.mainAria">',
    )
    html = html.replace(
        '<nav aria-label="Chính" class="main-nav">',
        '<nav aria-label="Chính" class="main-nav" data-i18n-aria-label="nav.mainAria">',
    )
    # Nav links: add data-i18n once per pattern
    pairs = [
        ('<a href="index.html#top">Trang chủ</a>', '<a href="index.html#top" data-i18n="nav.home">Trang chủ</a>'),
        ('<a href="index.html">Trang chủ</a>', '<a href="index.html" data-i18n="nav.home">Trang chủ</a>'),
        ('<a href="index.html#san-pham" class="is-active">Sản phẩm</a>', '<a href="index.html#san-pham" class="is-active" data-i18n="nav.products">Sản phẩm</a>'),
        ('<a class="is-active" href="index.html#san-pham">Sản phẩm</a>', '<a class="is-active" href="index.html#san-pham" data-i18n="nav.products">Sản phẩm</a>'),
        ('<a href="index.html#gioi-thieu">Giới thiệu</a>', '<a href="index.html#gioi-thieu" data-i18n="nav.about">Giới thiệu</a>'),
        ('<a href="index.html#lien-he">Liên hệ</a>', '<a href="index.html#lien-he" data-i18n="nav.contact">Liên hệ</a>'),
    ]
    for a, b in pairs:
        if b not in html:
            html = html.replace(a, b)
    html = html.replace(
        '<a href="index.html#san-pham">Sản phẩm</a>',
        '<a href="index.html#san-pham" data-i18n="nav.products">Sản phẩm</a>',
    )
    return html


def patch_header_hotline(html: str) -> str:
    if 'data-i18n="header.hotline"' in html:
        return html
    return html.replace(
        '<span class="header-hotline-label">Hotline</span>',
        '<span class="header-hotline-label" data-i18n="header.hotline">Hotline</span>',
    )


def patch_brand(html: str) -> str:
    html = html.replace(
        '<span class="brand-tagline" lang="vi">',
        '<span class="brand-tagline" data-i18n="brand.tagline" lang="vi">',
    )
    html = html.replace(
        '<span class="brand-sub">Thiết bị đo độ cứng &amp; kiểm tra vật liệu</span>',
        '<span class="brand-sub" data-i18n="brand.tagline">Thiết bị đo độ cứng &amp; kiểm tra vật liệu</span>',
    )
    return html


def patch_breadcrumb(html: str) -> str:
    html = html.replace(
        '<nav class="breadcrumb" aria-label="Đường dẫn">',
        '<nav class="breadcrumb" aria-label="Đường dẫn" data-i18n-aria-label="breadcrumb.aria">',
    )
    html = html.replace(
        '<nav aria-label="Đường dẫn" class="breadcrumb">',
        '<nav aria-label="Đường dẫn" class="breadcrumb" data-i18n-aria-label="breadcrumb.aria">',
    )
    return html


def patch_footer(html: str) -> str:
    if 'data-i18n="footer.copyPrefix"' in html:
        return html
    old = '''<p class="footer-copy">© <span id="year"></span> HDNS Pro instruments. Bảo lưu mọi quyền.</p>'''
    new = '''<p class="footer-copy"><span data-i18n="footer.copyPrefix">©</span> <span id="year"></span> HDNS Pro instruments. <span data-i18n="footer.copySuffix">Bảo lưu mọi quyền.</span></p>'''
    if old in html:
        return html.replace(old, new)
    old2 = """<p class="footer-copy">© <span id="year"></span> HDNS Pro instruments. Bảo lưu mọi quyền.</p>"""
    # same
    return html.replace(old2, new)


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    orig = text
    text = ensure_contact_css(text)
    text = replace_top_bar(text)
    text = patch_breadcrumb(text)
    text = patch_nav(text)
    text = patch_header_hotline(text)
    text = patch_brand(text)
    text = patch_footer(text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
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
