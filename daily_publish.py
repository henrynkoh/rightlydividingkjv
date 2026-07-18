#!/usr/bin/env python3
"""
daily_publish.py – Automatic daily publisher for "Rightly Dividing KJV"
Runs every day until ALL 344 posts are published to Blogger + YouTube.

- Publishes as many posts as the Blogger API quota allows (~40-50/day)
- On 429 quota error: saves progress, exits cleanly (not as failure)
- On next day's run: picks up exactly where it left off via tracking.json
- When all posts are done: self-reports completion and stops

Run manually:    python3 daily_publish.py
Run scheduled:   python3 daily_publish.py  (via Cowork scheduled task at 8am daily)
"""

import os
import sys
import json
import time
import subprocess
import re
from pathlib import Path
from datetime import datetime

SCRIPT_DIR  = Path(__file__).parent
LOG_FILE    = SCRIPT_DIR / "daily_publish.log"
TRACKING    = SCRIPT_DIR / "tracking.json"
POSTS_JSON  = SCRIPT_DIR / "posts_data.json"

GREEN = "\033[0;32m"; RED = "\033[0;31m"; YEL = "\033[1;33m"
CYN = "\033[0;36m"; NC = "\033[0m"

def log(msg, color=""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(f"{color}{line}{NC}" if color else line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_tracking():
    if TRACKING.exists():
        with open(TRACKING) as f:
            return json.load(f)
    return {}


def count_done():
    t = load_tracking()
    return sum(1 for v in t.values() if v.get("blog_done"))


def total_posts():
    with open(POSTS_JSON) as f:
        d = json.load(f)
    return len(d["posts"])


def html_exists_for_post(post, weeks_meta):
    """Return True only if the source HTML file for this post exists on disk."""
    week_key = post.get("week")
    # String week key (week1–week8): look up in weeks_meta dict
    if isinstance(week_key, str) and week_key in weeks_meta:
        html_file = SCRIPT_DIR / weeks_meta[week_key].get("html_file", "")
        return html_file.exists()
    # Integer week key (week 9–12): post carries its own html_file field
    html_name = post.get("html_file")
    if html_name:
        return (SCRIPT_DIR / html_name).exists()
    return False


def remaining_posts():
    t = load_tracking()
    done = {int(k) for k, v in t.items() if v.get("blog_done")}
    with open(POSTS_JSON) as f:
        d = json.load(f)
    weeks_meta = d.get("weeks", {})
    return [
        p["n"] for p in d["posts"]
        if p["n"] not in done and html_exists_for_post(p, weeks_meta)
    ]


def is_post_done(post_n):
    """Check tracking.json to see if a specific post is actually marked blog_done."""
    t = load_tracking()
    return t.get(str(post_n), {}).get("blog_done", False)


def run_batch(post_numbers, delay=35):
    """
    Run pipeline.py for each post in list.
    Always uses --blog-only mode (Blogger first; YouTube handled separately).
    Success is determined by checking tracking.json after each run.
    Returns (published_count, quota_hit, failed_list).
    """
    published = 0
    failed = []
    quota_hit = False

    for i, n in enumerate(post_numbers):
        # Always blog-only: avoid YouTube quota (6 uploads/day limit)
        # YouTube links can be added later via --yt-id flag
        cmd = [sys.executable, str(SCRIPT_DIR / "pipeline.py"),
               "--post", str(n), "--blog-only"]
        log(f"  → Post #{n} (blog-only)")

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(SCRIPT_DIR))
        output = result.stdout + result.stderr

        # Quota check first
        if "429" in output or "rateLimitExceeded" in output or "quota" in output.lower():
            log(f"  ✗ Post #{n}: Blogger quota hit — stopping for today", RED)
            quota_hit = True
            break

        # Ground truth: check tracking.json (not subprocess output, which can be misleading)
        if is_post_done(n):
            log(f"  ✓ Post #{n}: published", GREEN)
            published += 1
        else:
            snippet = output[-300:].strip().replace("\n", " ")
            log(f"  ✗ Post #{n}: failed — {snippet}", RED)
            failed.append(n)

        # Delay to respect Blogger rate limits
        if i < len(post_numbers) - 1 and not quota_hit:
            time.sleep(delay)

    return published, quota_hit, failed


def main():
    log("=" * 60)
    log("Rightly Dividing KJV — Daily Publisher", CYN)
    log(f"Run date: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}", CYN)
    log("=" * 60)

    total = total_posts()
    done_before = count_done()
    remaining = remaining_posts()

    log(f"Progress: {done_before}/{total} published  ({len(remaining)} remaining)")

    if not remaining:
        log("🎉 ALL POSTS PUBLISHED! Nothing left to do.", GREEN)
        log(f"   Total: {total} posts on Blogger + YouTube")
        log(f"   Blog:  https://rightlydividingkjv.blogspot.com")
        log(f"   Channel: https://www.youtube.com/@ohhenry6524")
        return 0

    log(f"\nStarting today's batch (up to ~45 posts before quota)...\n")

    published, quota_hit, failed = run_batch(remaining, delay=35)

    done_after = count_done()
    newly_done = done_after - done_before

    log("\n" + "=" * 60)
    log(f"TODAY'S SUMMARY", CYN)
    log(f"  Published today:  {newly_done}")
    log(f"  Total done:       {done_after}/{total}")
    log(f"  Remaining:        {total - done_after}")
    if failed:
        log(f"  Failed posts:     {failed}", RED)
    if quota_hit:
        log(f"  Quota hit — will resume tomorrow automatically", YEL)
    if total - done_after == 0:
        log(f"\n🎉 ALL {total} POSTS COMPLETE!", GREEN)
    else:
        days_left = max(1, (total - done_after) // 45)
        log(f"  Est. days to completion: ~{days_left} more day(s)", YEL)
    log("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
