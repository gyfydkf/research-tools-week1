"""Count words in a UTF-8 text file and export reproducible results."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]")


def tokenize(text: str) -> list[str]:
    """Return lowercase Latin tokens and individual Chinese characters."""
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def count_words(text: str) -> Counter[str]:
    """Count normalized tokens."""
    return Counter(tokenize(text))


def save_csv(rows: list[tuple[str, int]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["word", "count"])
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="统计 UTF-8 文本的词频")
    parser.add_argument("input", type=Path, help="输入文本文件")
    parser.add_argument("--top", type=int, default=10, help="显示前 N 项")
    parser.add_argument("--csv", type=Path, help="可选的 CSV 输出路径")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.top <= 0:
        raise SystemExit("--top 必须为正整数")

    text = args.input.read_text(encoding="utf-8")
    counts = count_words(text)
    rows = counts.most_common(args.top)

    print(f"input: {args.input}")
    print(f"tokens: {sum(counts.values())}")
    print(f"unique: {len(counts)}")
    print("top words:")
    for word, count in rows:
        print(f"  {word:<12} {count}")

    if args.csv:
        save_csv(rows, args.csv)
        print(f"csv: {args.csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
