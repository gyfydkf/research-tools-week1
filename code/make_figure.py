"""Create a vector PDF bar chart from the word-frequency CSV."""

from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "result" / "word_counts.csv"
OUTPUT_PATH = ROOT / "report" / "figures" / "result.pdf"


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as stream:
        rows = [(row["word"], int(row["count"])) for row in csv.DictReader(stream)]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    page_w, page_h = 560, 320
    pdf = canvas.Canvas(str(OUTPUT_PATH), pagesize=(page_w, page_h))
    pdf.setTitle("Top word frequencies")
    pdf.setFillColor(colors.HexColor("#17324D"))
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(42, 286, "Top word frequencies in sample.txt")

    left, bottom, chart_w, chart_h = 58, 62, 455, 190
    max_count = max(count for _, count in rows)
    bar_gap = 7
    bar_w = (chart_w - bar_gap * (len(rows) - 1)) / len(rows)

    pdf.setStrokeColor(colors.HexColor("#5D7185"))
    pdf.setLineWidth(0.8)
    pdf.line(left, bottom, left, bottom + chart_h)
    pdf.line(left, bottom, left + chart_w, bottom)

    for tick in range(max_count + 1):
        y = bottom + chart_h * tick / max_count
        pdf.setStrokeColor(colors.HexColor("#D9E2EA"))
        pdf.line(left, y, left + chart_w, y)
        pdf.setFillColor(colors.HexColor("#536678"))
        pdf.setFont("Helvetica", 8)
        pdf.drawRightString(left - 7, y - 3, str(tick))

    palette = ["#1677FF", "#22A06B", "#7A5AF8", "#E66A33"]
    for index, (word, count) in enumerate(rows):
        x = left + index * (bar_w + bar_gap)
        height = chart_h * count / max_count
        pdf.setFillColor(colors.HexColor(palette[index % len(palette)]))
        pdf.roundRect(x, bottom, bar_w, height, 3, fill=1, stroke=0)
        pdf.setFillColor(colors.HexColor("#17324D"))
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawCentredString(x + bar_w / 2, bottom + height + 6, str(count))
        pdf.saveState()
        pdf.translate(x + bar_w / 2 + 2, bottom - 8)
        pdf.rotate(-38)
        pdf.setFont("Helvetica", 7.5)
        pdf.drawRightString(0, 0, word)
        pdf.restoreState()

    pdf.setFillColor(colors.HexColor("#536678"))
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(page_w - 42, 18, "Vector PDF generated from result/word_counts.csv")
    pdf.showPage()
    pdf.save()
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
