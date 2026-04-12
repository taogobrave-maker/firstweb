# -*- coding: utf-8 -*-
"""Wrap Vickers spec table cell text with data-i18n spans (product-81..85)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Order: longer phrases first to avoid partial overlap
LEFT = [
    ("Hiển thị ngay sau mỗi lần đo: số lần đo, trung bình, độ lệch chuẩn, phạm vi đo", "spec.statsDisplay"),
    ("Chuyển đổi: Brinell, Rockwell, Rockwell bề mặt", "spec.hardnessConversion"),
    ("Máy in tích hợp (số liệu & thống kê), cổng RS232", "spec.integratedPrinter"),
    ("Thời gian duy trì lực thử", "spec.dwellTime"),
    ("Lựa chọn lực thử", "spec.testForceSelect"),
    ("Điều khiển lực thử", "spec.loadControl"),
    ("Độ phóng đại thị kính", "spec.eyepieceMag"),
    ("Bàn xoay ống kính", "spec.lensTurret"),
    ("Chiều cao mẫu tối đa", "spec.maxSampleHeight"),
    ("Chiều rộng mẫu tối đa", "spec.maxSampleWidth"),
    ("Chiều dài đường chéo", "spec.diagonalLength"),
    ("Giá trị độ cứng", "spec.hardnessValue"),
    ("Phạm vi hành trình", "spec.travelRange"),
    ("Độ chia nhỏ nhất", "spec.minStep"),
    ("Nhiệt độ làm việc", "spec.operatingTemp"),
    ("Tổng độ phóng đại", "spec.totalMag"),
    ("Thang Vickers", "spec.vickersScale"),
    ("Bộ mã hóa tương tự", "spec.analogEncoder"),
    ("Bộ mã hóa số", "spec.digitalEncoder"),
    ("Độ phân giải", "spec.resolution"),
    ("Phạm vi đo", "spec.measureRange"),
    ("Kênh quang học", "spec.opticalChannel"),
    ("Độ chính xác", "spec.accuracy"),
    ("Lực thử", "spec.testForce"),
    ("Kích thước", "spec.dimensions"),
    ("Nguồn điện", "spec.powerSupply"),
    ("Khối lượng", "spec.weight"),
    ("Nguồn sáng", "spec.lightSource"),
    ("Kính lọc", "spec.filter"),
    ("Hiển thị", "spec.displayMode"),
    ("Vật kính", "spec.objective"),
    ("Độ ẩm", "spec.humidity"),
    ("Bàn XY", "spec.xyTable"),
]

RIGHT = [
    ("Tự động (nạp tải / duy trì / gỡ tải)", "spec.val.autoLoadUnload"),
    ("Chiều dài đường chéo, giá trị quy đổi độ cứng, lực thử N, kg", "spec.val.displayDiagonal"),
    ("Hai kênh: thị kính / camera", "spec.val.twincam"),
    ("Xanh lá và xanh dương", "spec.val.greenBlue"),
    ("10%~90% không ngưng tụ", "spec.val.humidityRange"),
    ("Bàn chọn lực xoay", "spec.val.rotaryDial"),
    ("4 chữ số (D1, D2)", "spec.val.fourDigits"),
    ("5 chữ số", "spec.val.fiveDigits"),
    ("Đèn halogen", "spec.val.halogen"),
    ("Tùy chọn", "spec.val.optional"),
    ("Thủ công", "spec.val.manual"),
    ("Tự động", "spec.val.auto"),
]


def wrap_p(html: str, text: str, key: str) -> str:
    needle = ">%s</p>" % text
    repl = '><span data-i18n="%s">%s</span></p>' % (key, text)
    while needle in html:
        html = html.replace(needle, repl, 1)
    return html


def wrap_model_strong(html: str) -> str:
    if 'data-i18n="spec.modelHeader"' in html:
        return html
    old = ">Model</strong>"
    new = '><span data-i18n="spec.modelHeader">Model</span></strong>'
    if old in html:
        html = html.replace(old, new, 1)
    return html


def process(path: Path) -> bool:
    html = path.read_text(encoding="utf-8", errors="replace")
    orig = html
    html = wrap_model_strong(html)
    for text, key in LEFT:
        html = wrap_p(html, text, key)
    for text, key in RIGHT:
        html = wrap_p(html, text, key)
    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    n = 0
    for name in ("product-81.html", "product-82.html", "product-83.html", "product-84.html", "product-85.html"):
        p = ROOT / name
        if p.exists() and process(p):
            print("wrapped", name)
            n += 1
    print("done", n)


if __name__ == "__main__":
    main()
