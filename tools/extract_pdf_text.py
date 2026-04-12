# -*- coding: utf-8 -*-
import fitz
from pathlib import Path
import sys

p = Path(
    r"c:\Users\aazin\AppData\Roaming\Cursor\User\workspaceStorage\f56cbdee70247d30ebac7a5ee5a74e4a\pdfs\976c61a2-9719-48b3-bbdc-9839643a3f8c\1_HDNS 样本.pdf"
)
out = Path(__file__).resolve().parent / "_hdns_extracted.txt"
doc = fitz.open(str(p))
lines = []
for i in range(len(doc)):
    t = doc[i].get_text()
    lines.append(f"\n===== PAGE {i+1} =====\n")
    lines.append(t)
doc.close()
out.write_text("".join(lines), encoding="utf-8")
print(str(out))
