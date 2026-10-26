"""`humanizer check|fix FILE...` — для агентов и людей, пишущих тексты.

`check` печатает проблемы по абзацам с номером строки и выходит с кодом 1,
если они есть. `fix` применяет `humanize` к файлам на месте и затем делает
`check`: типографику он чинит, остальное остаётся переписать.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path

from humanizer import check, humanize


def paragraphs(text: str) -> Iterator[tuple[int, str]]:
    """Абзацы текста с номером их первой строки (с 1)."""
    start, lines = 0, list[str]()
    for no, line in enumerate(text.splitlines(), 1):
        if line.strip():
            if not lines:
                start = no
            lines.append(line)
        elif lines:
            yield start, "\n".join(lines)
            lines = []
    if lines:
        yield start, "\n".join(lines)


def report(name: str, text: str) -> int:
    """Напечатать проблемы текста; вернуть их число."""
    count = 0
    for line, para in paragraphs(text):
        for problem in check(para):
            print(f"{name}:{line}: {problem}")
            count += 1
    return count


def main(argv: Sequence[str] | None = None) -> int:
    """Точка входа CLI. `-` вместо файла — читать stdin."""
    parser = argparse.ArgumentParser(prog="humanizer", description=__doc__)
    parser.add_argument("command", choices=["check", "fix"])
    parser.add_argument("files", nargs="+", help="файлы или - для stdin")
    args = parser.parse_args(argv)

    total = 0
    for name in args.files:
        if name == "-":
            text = sys.stdin.read()
            if args.command == "fix":
                text = humanize(text)
                sys.stdout.write(text + "\n")
            total += report("<stdin>", text)
            continue
        path = Path(name)
        text = path.read_text(encoding="utf-8")
        if args.command == "fix":
            text = humanize(text) + "\n"
            path.write_text(text, encoding="utf-8")
        total += report(name, text)
    if total:
        print(f"{total} проблем(ы)", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
