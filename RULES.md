# Как писать, чтобы текст не выдавал ИИ

Канон для всех текстов, которые модель пишет от имени человека: посты,
комментарии, письма, статьи, README для людей. Код в `src/humanizer` проверяет
часть этих правил; остальное — на авторе.

Источники: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
[разбор постов LinkedIn 2026](https://magicpost.in/blog/em-dash-ai-sign-linkedin).

Правила про слова и обороты написаны для английского текста. Типографика
(тире, кавычки) — тоже для английского: в русском длинное тире и «ёлочки» —
норма, `humanize` к русскому тексту не применяй.

## Как звучать

- Сразу к делу, без разгона. Первая строка сама по себе интересна: конкретика,
  а не объявление того, что будет дальше.
- Простые слова, сокращения (I've, it's, we're). Как инженер инженеру, а не
  как пресс-релиз.
- Своё: опыт, деталь, уточнение. Не пересказ и не общая мораль в конце.
- Только факты из материала. Не выдумывай цифры, компании, опыт. Цифра без
  источника хуже, чем никакой.
- Нечего сказать — не пиши.

## Что код правит сам (`humanize`)

- Длинное и среднее тире (—, –) → дефис с пробелами.
- «Умные» кавычки и апострофы (“ ” ‘ ’) → прямые " и '.
- Многоточие одним символом (…) → три точки.

Лучше не писать так вовсе: тире на месте точки или запятой — самый узнаваемый
признак модели в LinkedIn 2026 года.

## Что код находит, а переписать должен автор (`ai_signs`, `bot_emoji`)

- Слова-маркеры: delve, tapestry, testament, pivotal, crucial, underscore,
  showcase, foster, realm, landscape, intricate, seamless, navigate the,
  game-changer, valuable insights, resonate, in today's, fast-paced,
  ever-evolving, it's worth noting, it's important to note.
- «It's not X, it's Y», «not just X but Y», «X rather than Y».
- Заходы-барабаны: «Here's the thing», «Here's what/how/why», «The result?»,
  «The key is», «Stop X. Start Y.», «Let that sink in».
- Хвосты на -ing с выводом: «..., highlighting the importance of ...».
- Больше одного восклицательного знака.
- Эмодзи ботов: 🚀 ✨ 🔥 💯 🎯 ✅ 👉.

## Что код не ловит

- Перечисления по три («fast, simple, and scalable»).
- Списки, где каждый пункт начинается с эмодзи.
- «Great post», «Thanks for sharing», лесть адресату.
- Итоговая мораль и призыв «поставь лайк / напиши в комментариях».
- Одинаковый ритм: все предложения одной длины, все абзацы по две строки.

## Как пользоваться

```bash
uvx --from git+https://github.com/gavrilovdm/humanizer@v0.1.1 humanizer fix draft.md    # типографика на месте + отчёт
uvx --from git+https://github.com/gavrilovdm/humanizer@v0.1.1 humanizer check draft.md  # только отчёт, код 1 при проблемах
```

Из Python: `from humanizer import humanize, check, ai_signs`.
