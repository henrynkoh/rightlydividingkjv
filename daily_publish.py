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


def remaining_posts():
    t = load_tracking()
    done = {int(k) for k, v in t.items() if v.get("blog_done")}
    with open(POSTS_JSON) as f:
        d = json.load(f)
    all_ns = [p["n"] for p in d["posts"]]
    return [n for n in all_ns if n not in done]


def run_batch(post_numbers, delay=35):
    """
    Run pipeline.py for each post in list.
    Returns (published_count, quota_hit, failed_list).
    """
    published = 0
    failed = []
    quota_hit = False

    for i, n in enumerate(post_numbers):
        # Check video exists
        video_path = SCRIPT_DIR / "videos" / f"post-{n}.mp4"
        if not video_path.exists():
            log(f"  Post #{n}: video missing — trying blog-only mode", YEL)
            mode = ["--blog-only"]
        else:
            mode = []   # full upload: video + blog

        cmd = [sys.executable, str(SCRIPT_DIR / "pipeline.py"), "--post", str(n)] + mode
        log(f"  → Post #{n} {'(blog-only)' if mode else '(video + blog)'}")

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(SCRIPT_DIR))
        output = result.stdout + result.stderr

        if "429" in output or "rateLimitExceeded" in output or "quota" in output.lower():
            log(f"  ✗ Post #{n}: Blogger quota hit — stopping for today", RED)
            quota_hit = True
            break

        if result.returncode == 0 and ("✓" in output or "Published" in output or "blog_done" in output):
            log(f"  ✓ Post #{n}: published", GREEN)
            published += 1
        elif "already published" in output or "already done" in output:
            log(f"  ✓ Post #{n}: already done — skipping")
            published += 1
        else:
            log(f"  ✗ Post #{n}: failed — {output[-200:].strip()}", RED)
            failed.append(n)

        # Delay to avoid quota
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
