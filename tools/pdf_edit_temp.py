from pathlib import Path
import fitz

src = Path(r"c:\Users\aazin\AppData\Roaming\Cursor\User\workspaceStorage\f56cbdee70247d30ebac7a5ee5a74e4a\pdfs\4726ae9b-4f33-4793-890d-bba0bf23349a\1_HDNS 样本.pdf")
dst = src.with_name("HDNS_edited.pdf")

doc = fitz.open(str(src))
for i, page in enumerate(doc):
    w = page.rect.width
    h = page.rect.height
    page.draw_rect(fitz.Rect(0, 0, w, 96), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
    if i == 1:
        page.draw_rect(fitz.Rect(0, 96, w, h - 42), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)

doc.save(str(dst))
doc.close()
print(dst)
