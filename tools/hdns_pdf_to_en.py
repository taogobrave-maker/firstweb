# -*- coding: utf-8 -*-
"""Translate HDNS catalog extracted text to English and build a simple PDF."""
import re
import time
from pathlib import Path

from deep_translator import GoogleTranslator
from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
SRC_TXT = ROOT / "_hdns_extracted.txt"
OUT_DIR = Path(
    r"c:\Users\aazin\AppData\Roaming\Cursor\User\workspaceStorage\f56cbdee70247d30ebac7a5ee5a74e4a\pdfs\976c61a2-9719-48b3-bbdc-9839643a3f8c"
)
OUT_PDF = OUT_DIR / "1_HDNS Sample_EN.pdf"


def split_pages(raw: str):
    parts = re.split(r"\n===== PAGE \d+ =====\n", raw)
    return [p.strip() for p in parts if p.strip()]


def chunk_blocks(text: str, max_chars: int = 3800):
    """Split by blank lines; keep chunks under Google translate practical size."""
    blocks = re.split(r"\n\s*\n+", text)
    chunks = []
    buf = []
    n = 0
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        if n + len(b) + 2 > max_chars and buf:
            chunks.append("\n\n".join(buf))
            buf = [b]
            n = len(b)
        else:
            buf.append(b)
            n += len(b) + 2
    if buf:
        chunks.append("\n\n".join(buf))
    if not chunks and text.strip():
        chunks = [text.strip()]
    return chunks


def translate_text(translator, text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    out = []
    for ch in chunk_blocks(text):
        if not ch.strip():
            continue
        try:
            out.append(translator.translate(ch))
        except Exception as e:
            out.append(
                "[Translation failed: %s]\n%s" % (e, ch[:1200])
            )
        time.sleep(0.35)
    return "\n\n".join(out)


class Doc(FPDF):
    def __init__(self):
        super().__init__()
        self.set_doc_option("core_fonts_encoding", "utf-8")


def main():
    if not SRC_TXT.exists():
        raise SystemExit("Missing %s — run extract_pdf_text.py first" % SRC_TXT)

    raw = SRC_TXT.read_text(encoding="utf-8")
    pages = split_pages(raw)
    translator = GoogleTranslator(source="zh", target="en")

    pdf = Doc()
    pdf.set_auto_page_break(True, margin=14)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.multi_cell(0, 8, "HDNS Kelly Instruments — Product Catalog (English)")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 8)
    pdf.multi_cell(
        0,
        4,
        "Machine-translated from Chinese for reference. "
        "Verify critical specifications against factory documentation.",
    )
    pdf.ln(6)

    for i, page_txt in enumerate(pages, 1):
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, "Page %d / %d" % (i, len(pages)), ln=1)
        pdf.ln(2)
        pdf.set_font("Helvetica", "", 8)
        en = translate_text(translator, page_txt)
        pdf.multi_cell(0, 4, en)
        pdf.ln(4)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT_PDF))
    print(str(OUT_PDF))


if __name__ == "__main__":
    main()
