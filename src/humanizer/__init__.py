"""Признаки текста от ИИ: что править механически и что отдавать на переделку.

Общие правила для всего, что пишут модели от имени человека: посты,
комментарии, письма, статьи. Канон в словах — `RULES.md` в корне репо, здесь —
то, что из него проверяет код. Типографику (`humanize`) код правит сам: смысл
не меняется. Остальное (`ai_signs`, `bot_emoji`) — повод переписать текст, а
не публиковать: замену словам и оборотам должен подобрать автор или модель.

Сообщения о проблемах — по-русски: они уходят и человеку, и в промпт
переделки, где остальной текст тоже русский.
"""

from __future__ import annotations

import re

__all__ = [
    "BOT_EMOJI",
    "ai_signs",
    "bot_emoji",
    "check",
    "humanize",
    "typography_problems",
]

# Признаки — по гайду Википедии «Signs of AI writing» и разбору постов
# LinkedIn за 2026 год (ссылки — в RULES.md).
#: Слова, которые модели пишут непропорционально часто.
_AI_WORDS = re.compile(
    r"\b(delve[sd]?|delving|tapestry|testament|pivotal|crucial|underscor\w*|showcas\w*|"
    r"foster\w*|realm|landscape|intricat\w*|seamless\w*|navigat\w* the|game[- ]changer|"
    r"valuable insights?|resonat\w*|in today'?s|fast-paced|ever-evolving|"
    r"it'?s worth noting|it'?s important to note)\b",
    re.I,
)
#: «It's not X, it's Y» / «not just X but Y» / «X rather than Y».
_NEGATIVE_PARALLEL = re.compile(
    r"\bnot (just|only|merely|about)\b[^.]*\b(but|it'?s)\b|"
    r"\b(isn'?t|is not|wasn'?t)\b[^.]*[.,;]\s*(it'?s|it is)\b|\brather than\b",
    re.I,
)
#: Заходы-барабаны: объявляют, вместо того чтобы сказать.
_DRUMROLL = re.compile(
    r"\b(here'?s (the thing|what|how|why)|the result\?|the key is|"
    r"stop \w+[^.]*\. start\b|let that sink in|game changer)\b",
    re.I,
)
#: Хвост «, highlighting the …» — пустой вывод в конце фразы.
_ING_TAIL = re.compile(
    r",\s*(highlighting|underscoring|emphasizing|showcasing|reflecting|ensuring|fostering)\b",
    re.I,
)
_TYPOGRAPHY = str.maketrans({"“": '"', "”": '"', "„": '"', "‘": "'", "’": "'", " ": " "})
_SMART = re.compile("[“”„‘’ …]")
_DASH = re.compile("[—–]")

#: Эмодзи, которые в живых текстах встретились только у ИИ («game-changer! 🚀»)
#: и в саморекламе (👉). По разбору 216 живых комментариев, 2026-10-09.
BOT_EMOJI = frozenset({"🚀", "✨", "🔥", "💯", "🎯", "✅", "👉"})


def humanize(text: str) -> str:
    """Механически убрать типографику, которая выдаёт модель.

    Длинное и среднее тире — в дефис с пробелами: так тире набирают люди с
    обычной клавиатуры. Кавычки и апострофы — прямые, «…» — три точки.
    Смысл не меняется, поэтому это правка, а не повод отбраковать текст.
    Абзацы (пустые строки) сохраняются.
    """
    out = text.translate(_TYPOGRAPHY).replace("…", "...")
    out = re.sub(r"[ \t]*[—–][ \t]*", " - ", out)
    return re.sub(r"[ \t]{2,}", " ", out).strip()


def typography_problems(text: str) -> list[str]:
    """Типографика, которую убрал бы `humanize`."""
    problems = []
    if _DASH.search(text):
        problems.append("длинное тире (humanize заменит)")
    if _SMART.search(text):
        problems.append("«умные» кавычки или многоточие (humanize заменит)")
    return problems


def ai_signs(text: str) -> list[str]:
    """Признаки текста от ИИ, которые код не исправит сам.

    Каждый — повод переписать фразу. Пустой список — признаков не нашлось,
    а не гарантия, что текст звучит как человек.
    """
    problems = []
    if m := _AI_WORDS.search(text):
        problems.append(f"слово-маркер ИИ: {m.group(0)!r}")
    if _NEGATIVE_PARALLEL.search(text):
        problems.append("конструкция «not X, it's Y»")
    if m := _DRUMROLL.search(text):
        problems.append(f"заход-барабан: {m.group(0)!r}")
    if _ING_TAIL.search(text):
        problems.append("хвост «, highlighting …»")
    if text.count("!") > 1:
        problems.append("много восклицаний")
    return problems


def bot_emoji(text: str) -> list[str]:
    """Эмодзи, которые ставят боты, а не люди (`BOT_EMOJI`)."""
    found = sorted({e for e in BOT_EMOJI if e in text})
    return [f"эмодзи ботов: {' '.join(found)}"] if found else []


def check(text: str) -> list[str]:
    """Все проблемы текста: типографика, признаки ИИ, эмодзи ботов."""
    return typography_problems(text) + ai_signs(text) + bot_emoji(text)
