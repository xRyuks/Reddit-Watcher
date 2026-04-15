import os
import argparse
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Missing dependency: requests. Install dependencies with 'pip install -r requirements.txt' "
        "or run the bot with '.venv/bin/python bot.py'."
    ) from exc

PHRASE = os.getenv("PHRASE", "python").strip().lower()
MATCHES_FILE = Path(__file__).with_name("matches.txt")


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch subreddit posts and log matching titles.")
    parser.add_argument(
        "subreddit",
        nargs="?",
        default=None,
        help="Subreddit to scan (default: Python)",
    )
    parser.add_argument(
        "--phrase",
        default=None,
        help="Case-insensitive phrase to match in post titles (default: python or $PHRASE)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Number of recent posts to fetch (default: 20)",
    )
    parser.add_argument(
        "--sort",
        choices=["best", "hot", "new", "top", "rising"],
        default=None,
        help="Post category to fetch: best, hot, new, top, or rising (default: new)",
    )
    parser.add_argument(
        "--top-time",
        choices=["now", "today", "this-week", "this-month", "this-year", "all-time"],
        default=None,
        help="Time range for top posts: now, today, this-week, this-month, this-year, all-time",
    )
    return parser.parse_args()

def resolve_subreddit(subreddit: str | None) -> str:
    if subreddit:
        return normalize_subreddit(subreddit)

    entered = input("Enter a subreddit to scan: ").strip()
    return normalize_subreddit(entered or "Python")


def normalize_subreddit(subreddit: str) -> str:
    cleaned = subreddit.strip()

    if cleaned.startswith("http://") or cleaned.startswith("https://"):
        parsed = urlparse(cleaned)
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) >= 2 and parts[0].lower() == "r":
            return parts[1]

    if cleaned.lower().startswith("r/"):
        return cleaned[2:]

    return cleaned


def resolve_phrase(phrase: str | None) -> str:
    if phrase:
        return phrase

    entered = input(f'Enter a phrase/word to match: ').strip()
    return entered or PHRASE


def resolve_limit(limit: int | None) -> int:
    if limit is not None:
        if limit < 1:
            raise SystemExit("--limit must be at least 1")
        return limit

    while True:
        entered = input("How many posts should I search [20]: ").strip()
        if not entered:
            return 20
        if entered.isdigit() and int(entered) > 0:
            return int(entered)
        print("Please enter a positive whole number.")


def resolve_sort(sort: str | None) -> str:
    if sort:
        return sort

    while True:
        entered = input("Choose category [best/hot/new/top/rising] (default: new): ").strip().lower()
        if not entered:
            return "new"
        if entered in {"best", "hot", "new", "top", "rising"}:
            return entered
        print("Please enter 'best', 'hot', 'new', 'top', or 'rising'.")


def resolve_top_time(top_time: str | None, sort: str) -> str | None:
    if sort != "top":
        return None

    if top_time:
        return top_time

    while True:
        entered = input(
            "Choose top time range [now/today/this-week/this-month/this-year/all-time] (default: today): "
        ).strip().lower()
        if not entered:
            return "today"
        if entered in {"now", "today", "this-week", "this-month", "this-year", "all-time"}:
            return entered
        print("Please enter now, today, this-week, this-month, this-year, or all-time.")


def fetch_posts(subreddit: str, limit: int = 20, sort: str = "new", top_time: str | None = None):
    listing = sort
    url = f"https://www.reddit.com/r/{subreddit}/{listing}.json"
    params: dict[str, int | str] = {"limit": limit}

    if listing == "top":
        top_time_map = {
            "now": "hour",
            "today": "day",
            "this-week": "week",
            "this-month": "month",
            "this-year": "year",
            "all-time": "all",
        }
        params["t"] = top_time_map.get(top_time or "today", "day")

    headers = {
            "User-Agent": "macos:github-reddit-watcher:v1.0 (by u/MinamotoGenji)"
    }
    
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["children"]

def log_match(title: str, permalink: str):
    line = f"[{datetime.now().isoformat()}] {title} -> https://www.reddit.com{permalink}\n"
    with open(MATCHES_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def main(subreddit: str, phrase: str, limit: int, sort: str, top_time: str | None):
    phrase = phrase.strip().lower()
    try:
        posts = fetch_posts(subreddit, limit=limit, sort=sort, top_time=top_time)
    except requests.RequestException as exc:
        print(f"Failed to fetch posts from r/{subreddit}: {exc}")
        return

    if sort == "top" and top_time:
        print(f"Fetched {len(posts)} top posts ({top_time}) from r/{subreddit}")
    else:
        print(f"Fetched {len(posts)} {sort} posts from r/{subreddit}")
    match_count = 0
    
    for post in posts:
        title = post["data"]["title"]
        if phrase in title.lower():
            print("---- MATCH ----")
            print("Title:", title)
            print("URL  :", "https://www.reddit.com" + post["data"]["permalink"])
            log_match(title, post["data"]["permalink"])
            match_count += 1
            print()

    if match_count == 0:
        print(f'No matches found for "{phrase}"')
    else:
        print(f"Logged {match_count} matches to {MATCHES_FILE.name}")
            
if __name__ == "__main__":
    args = parse_args()
    selected_subreddit = resolve_subreddit(args.subreddit)
    selected_phrase = resolve_phrase(args.phrase)
    selected_limit = resolve_limit(args.limit)
    selected_sort = resolve_sort(args.sort)
    selected_top_time = resolve_top_time(args.top_time, selected_sort)

    main(
        selected_subreddit,
        selected_phrase,
        selected_limit,
        selected_sort,
        selected_top_time,
    )