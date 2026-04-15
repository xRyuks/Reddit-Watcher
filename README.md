# Reddit Bot 2.0

A small Python script that fetches subreddit posts, looks for a configurable phrase in post titles, and logs matches to `matches.txt`.

## Requirements

- Python 3.11+
- `requests`

## Setup

1. Create the virtual environment if needed.
2. Activate it from the project folder:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

From the activated virtual environment:

```bash
python bot.py
```

If you prefer not to activate the environment first, run it directly with:

```bash
.venv/bin/python bot.py
```

By default, the bot searches for `python` in `new` posts from `r/Python`.

Example terminal flow used to run it:

```bash
cd /Users/YOUR_NAME/Desktop/reddit-bot
source .venv/bin/activate
python3 bot.py
```

If you run it without a subreddit argument, it will prompt you to enter one. Press Enter to keep the default `Python`.

After that, it will prompt for:

- A phrase/word to search for (default: `python`)
- How many posts to scan (default: `20`)
- A category: `best`, `hot`, `new`, `top`, or `rising` (default: `new`)
- If category is `top`, a time range: `now`, `today`, `this-week`, `this-month`, `this-year`, `all-time` (default: `today`)

To search a different subreddit:

```bash
python bot.py learnpython
```

To search for a different phrase:

```bash
python bot.py learnpython --phrase "django"
```

You can also change the number of posts scanned:

```bash
python bot.py learnpython --limit 50
```

You can choose a category:

```bash
python bot.py learnpython --sort top
```

You can also choose the time range for top posts:

```bash
python bot.py learnpython --sort top --top-time this-week
```

## Notes

- `matches.txt` is generated at runtime and is ignored by Git.
- `.venv/`, `__pycache__/`, and editor-specific files are also ignored.
- `python3 bot.py` only works if your shell is using the virtual environment's Python; otherwise use `.venv/bin/python bot.py`.
