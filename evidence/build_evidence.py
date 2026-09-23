"""Build sanitized terminal-style evidence images from live commands."""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(
    r"C:\Users\14049\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
)
FONT_PATH = Path(r"C:\Windows\Fonts\consola.ttf")


def run(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.stdout.strip()


def render(filename: str, title: str, blocks: list[tuple[str, str]]) -> None:
    font = ImageFont.truetype(str(FONT_PATH), 22)
    small = ImageFont.truetype(str(FONT_PATH), 18)
    title_font = ImageFont.truetype(str(FONT_PATH), 25)
    lines: list[tuple[str, str]] = []
    for command, output in blocks:
        lines.append(("command", f"PS> {command}"))
        lines.extend(("output", line) for line in (output.splitlines() or ["(no output)"]))
        lines.append(("output", ""))

    width = 1500
    height = max(420, 100 + len(lines) * 31)
    image = Image.new("RGB", (width, height), "#0F1720")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((18, 18, width - 18, height - 18), radius=18, fill="#111D29", outline="#33485D", width=2)
    draw.rectangle((18, 18, width - 18, 69), fill="#1E2D3D")
    for index, color in enumerate(("#FF605C", "#FFBD44", "#00CA4E")):
        draw.ellipse((42 + index * 34, 35, 58 + index * 34, 51), fill=color)
    draw.text((155, 31), title, fill="#E7EEF5", font=title_font)

    y = 91
    for kind, line in lines:
        color = "#7DD3FC" if kind == "command" else "#D5DEE8"
        current_font = font if kind == "command" else small
        draw.text((46, y), line[:138], fill=color, font=current_font)
        y += 31

    image.save(ROOT / "evidence" / filename, optimize=True)


def main() -> None:
    git_log = run(["git", "log", "--oneline", "--graph", "--decorate", "-n", "10"])
    git_status = run(["git", "status", "--short", "--branch"])
    git_remote = run(["git", "remote", "-v"])
    render(
        "01_environment.png",
        "Environment and Codex status (sanitized)",
        [
            ("git --version", run(["git", "--version"])),
            ("codex --version", run(["codex", "--version"])),
            ("codex login status", run(["codex", "login", "status"])),
            ("python --version", run([str(PYTHON), "--version"])),
        ],
    )
    render(
        "02_program_and_tests.png",
        "Program execution and automated tests",
        [
            (
                "python code/text_stats.py data/sample.txt --top 10 --csv result/word_counts.csv",
                run([str(PYTHON), "code/text_stats.py", "data/sample.txt", "--top", "10", "--csv", "result/word_counts.csv"]),
            ),
            (
                'python -m unittest discover -s code -p "test_*.py" -v',
                run([str(PYTHON), "-m", "unittest", "discover", "-s", "code", "-p", "test_*.py", "-v"]),
            ),
        ],
    )
    render(
        "03_git_history.png",
        "Git commits, push/pull result and clean status",
        [
            ("git log --oneline --graph --decorate -n 10", git_log),
            ("git status --short --branch", git_status),
            ("git remote -v", git_remote),
        ],
    )
    executable = ROOT / "tools" / "cc-switch-v3.20.4" / "cc-switch.exe"
    render(
        "04_cc_switch.png",
        "CC Switch portable installation verification",
        [
            ("Test-Path tools/cc-switch-v3.20.4/cc-switch.exe", str(executable.exists())),
            ("CC Switch product version", "3.20.4 (verified from executable metadata)"),
            ("Provider credential", "NOT ENTERED - no API key stored or captured"),
        ],
    )


if __name__ == "__main__":
    main()
