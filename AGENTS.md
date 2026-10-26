# humanizer

Родитель: [hub/projects/non-work/agents-ai](https://github.com/gavrilovdm/hub/blob/main/domains/projects/non-work/agents-ai/AGENTS.md)

Связи: используется [vacancy-parser](https://github.com/gavrilovdm/vacancy-parser) (`apps/content`, git-зависимость по тегу) и плейбуком hub [write-text](https://github.com/gavrilovdm/hub/blob/main/playbooks/write-text.md)

## Что это

Правила, по которым текст от модели не выдаёт ИИ (`RULES.md`), и их проверка в
коде: `humanize` правит типографику, `ai_signs` и `bot_emoji` находят то, что
надо переписать. Без зависимостей. Репо публичный.

## Команды

```bash
uv sync
uv run pytest -q
uv run ruff check . && uv run ruff format --check . && uv run mypy src
uv run humanizer check FILE   # или fix
```

## Структура

- `RULES.md` — канон правил в словах; правишь правило — правь и его, и код.
- `src/humanizer/__init__.py` — `humanize`, `typography_problems`, `ai_signs`, `bot_emoji`, `check`
- `src/humanizer/cli.py` — `humanizer check|fix`

## Соглашения и подводные камни

- Публичный API используют другие репо. Переименование функции или смена текста
  сообщений ломает vacancy-parser (его тесты ищут подстроки сообщений):
  новый тег `vX.Y.Z` и обновление `rev` там — одним PR в vacancy-parser.
- Сообщения о проблемах по-русски: они уходят в русские промпты переделки.
- Новое правило: строка в `RULES.md` + регулярка + тест. Ложные срабатывания
  дороже пропусков: каждое — лишняя переделка текста моделью.
