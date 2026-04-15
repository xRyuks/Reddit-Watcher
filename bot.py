import requests
import os
from datetime import datetime
from pathlib import Path

SUBREDDIT = "Python"
PHRASE = os.getenv("PHRASE", "python").strip().lower()
MATCHES_FILE = Path(__file__).with_name("matches.txt")

def fetch_new_posts(subreddit: str, limit: int = 20):
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    headers = {
        "User-Agent": "linux:github-reddit-watcher:v1.0 (by xRyuks)"
    }
    
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["children"]

def log_match(title: str, permalink: str):
    line = f"[{datetime.now().isoformat()}] {title} -> https://www.reddit.com{permalink}\n"
    with open(MATCHES_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def main():
    try:
        posts = fetch_new_posts(SUBREDDIT, limit=20)
    except requests.RequestException as exc:
        print(f"Failed to fetch posts from r/{SUBREDDIT}: {exc}")
        return

    print(f"Fetched {len(posts)} posts from r/{SUBREDDIT}")
    match_count = 0
    
    for post in posts:
        title = post["data"]["title"]
        if PHRASE in title.lower():
            print("---- MATCH ----")
            print("Title:", title)
            print("URL  :", "https://www.reddit.com" + post["data"]["permalink"])
            log_match(title, post["data"]["permalink"])
            match_count += 1
            print()

    if match_count == 0:
        print(f'No matches found for "{PHRASE}"')
    else:
        print(f"Logged {match_count} matches to {MATCHES_FILE.name}")
            
if __name__ == "__main__":
    main()