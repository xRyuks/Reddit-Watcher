# Reddit Bot

A small Python script that fetches recent posts from `r/Python`, looks for a configurable phrase in post titles, and logs matches to `matches.txt`.

## Requirements

- Python 3.11+
- `requests`

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python bot.py
```

By default, the bot searches for `python` in recent post titles from `r/Python`.

To search for a different phrase:

```bash
PHRASE="django" python bot.py
```

## Notes

- `matches.txt` is generated at runtime and is ignored by Git.
- `.venv/`, `__pycache__/`, and editor-specific files are also ignored.
