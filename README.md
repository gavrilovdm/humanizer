# humanizer

Shared rules for text an LLM writes on a person's behalf, plus a tiny zero-dependency checker.

- `humanize(text)` fixes typography that gives a model away: em/en dashes, smart quotes, `…`.
- `ai_signs(text)` flags what needs a rewrite: marker words (delve, pivotal, seamless…),
  "not X, it's Y", drumroll openers, "…, highlighting" tails, stacked exclamation marks.
- `bot_emoji(text)` flags 🚀 ✨ 🔥 💯 🎯 ✅ 👉.

The rules in words live in [RULES.md](RULES.md) (Russian). Problem messages are in Russian too.

```bash
uvx --from git+https://github.com/gavrilovdm/humanizer@v0.1.1 humanizer fix draft.md
uvx --from git+https://github.com/gavrilovdm/humanizer@v0.1.1 humanizer check draft.md
```
