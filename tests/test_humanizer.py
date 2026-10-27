import time
from pathlib import Path

import pytest

from humanizer import ai_signs, bot_emoji, check, humanize
from humanizer.cli import main, paragraphs


def test_humanize_fixes_typography() -> None:
    text = humanize("We tried it—twice – and it’s “fine”…")
    assert text == 'We tried it - twice - and it\'s "fine"...'


def test_humanize_keeps_paragraphs() -> None:
    assert humanize("One — two.\n\nThree.") == "One - two.\n\nThree."


@pytest.mark.parametrize(
    ("text", "problem"),
    [
        ("We had to delve into the change detection internals for a week.", "маркер"),
        ("It isn't a framework problem. It's a process problem on most teams.", "not X"),
        ("Not just faster builds but a simpler mental model for the whole team.", "not X"),
        ("Here's the thing: signals only help when the state graph is small.", "барабан"),
        ("We moved to signals last year, highlighting how much zone.js cost us.", "хвост"),
        ("Signals are great! We moved last year! Never going back to zone.js now.", "восклиц"),
    ],
)
def test_ai_signs(text: str, problem: str) -> None:
    assert any(problem in p for p in ai_signs(text))


def test_plain_text_passes() -> None:
    assert check("We moved to signals last year and the build got faster.") == []


def test_bot_emoji() -> None:
    assert bot_emoji("Shipped it 🚀") == ["эмодзи ботов: 🚀"]
    assert bot_emoji("Shipped it 😅") == []


def test_paragraphs_have_line_numbers() -> None:
    assert list(paragraphs("a\nb\n\n\nc\n")) == [(1, "a\nb"), (5, "c")]


def test_cli_fix_then_check(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    f = tmp_path / "post.md"
    f.write_text("Fast — and simple.\n\nHere's the thing: it works.\n", encoding="utf-8")
    assert main(["fix", str(f)]) == 1
    assert f.read_text(encoding="utf-8") == "Fast - and simple.\n\nHere's the thing: it works.\n"
    out = capsys.readouterr().out
    assert f"{f}:3: заход-барабан" in out
    assert "тире" not in out


def test_long_text_without_periods_stays_linear() -> None:
    # Было квадратично: 45 000 символов — ~0.8 с, 180 000 — десятки секунд.
    text = "isn't a, " * 20_000 + "not just " + "word, " * 20_000
    started = time.monotonic()
    check(text)
    assert time.monotonic() - started < 1
