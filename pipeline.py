#!/usr/bin/env python3
"""
pipeline.py – Full Automation for "Rightly Dividing KJV" Content System
Channel: @ohhenry6524 | Blog: rightlydividingkjv.blogspot.com

Steps per post (fully automated):
  1. Upload video to YouTube via Data API v3
  2. Extract post HTML from week file
  3. Replace video placeholder with iframe embed
  4. Publish post to Blogger via API v3
  5. Save tracking data (YouTube ID + Blogger URL)
  6. Update GitHub Pages index.html and git push

Usage:
  python pipeline.py --post 141                         # single post (uses post-141.mp4)
  python pipeline.py --post 141 --video my_video.mp4    # custom video file
  python pipeline.py --posts 141 142 143                # multiple posts in sequence
  python pipeline.py --week 6                           # all posts in week 6
  python pipeline.py --week 6 --blog-only               # publish to Blogger NOW, no video needed
  python pipeline.py --all --blog-only                  # publish ALL 232 posts to Blogger now
  python pipeline.py --post 141 --yt-id dQw4w9WgXcQ    # attach existing YouTube video ID
  python pipeline.py --setup                            # verify credentials only
  python pipeline.py --status                           # show completion status
"""

import os
import sys
import json
import time
import argparse
import re
import subprocess
from pathlib import Path
from datetime import datetime

# ─── COLOR OUTPUT ────────────────────────────────────────────────────────────
try:
    from colorama import Fore, Style, init
    init()
    def ok(msg):  print(Fore.GREEN  + "✓ " + Style.RESET_ALL + msg)
    def err(msg): print(Fore.RED    + "✗ " + Style.RESET_ALL + msg)
    def inf(msg): print(Fore.YELLOW + "→ " + Style.RESET_ALL + msg)
    def hdr(msg): print(Fore.CYAN   + "\n══ " + msg + " ══" + Style.RESET_ALL)
except ImportError:
    def ok(msg):  print("✓ " + msg)
    def err(msg): print("✗ " + msg)
    def inf(msg): print("→ " + msg)
    def hdr(msg): print("\n══ " + msg + " ══")

# ─── PATHS ───────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
CONFIG_FILE  = SCRIPT_DIR / "config.json"
POSTS_FILE   = SCRIPT_DIR / "posts_data.json"
TRACKING_FILE= SCRIPT_DIR / "tracking.json"

# ─── LOAD CONFIG & DATA ──────────────────────────────────────────────────────
def load_config():
    if not CONFIG_FILE.exists():
        err(f"config.json not found. Copy config.template.json → config.json and fill in values.")
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return json.load(f)

def load_posts():
    with open(POSTS_FILE) as f:
        data = json.load(f)
    return {p["n"]: p for p in data["posts"]}, data

def load_tracking():
    if TRACKING_FILE.exists():
        with open(TRACKING_FILE) as f:
            return json.load(f)
    return {}

def save_tracking(tracking):
    with open(TRACKING_FILE, "w") as f:
        json.dump(tracking, f, indent=2)

# ─── GOOGLE AUTH ─────────────────────────────────────────────────────────────
def get_google_credentials(cfg, scopes):
    """Get / refresh Google OAuth credentials (opens browser on first run)."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
    except ImportError:
        err("Google libraries not installed. Run: pip install -r requirements.txt")
        sys.exit(1)

    token_file = SCRIPT_DIR / "token.json"
    creds = None

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            inf("Refreshing Google token...")
            creds.refresh(Request())
        else:
            inf("Opening browser for Google OAuth (first time only)...")
            secrets = SCRIPT_DIR / cfg["youtube"]["client_secrets_file"]
            if not secrets.exists():
                err(f"client_secrets.json not found at {secrets}")
                err("Download from: console.cloud.google.com → APIs & Services → Credentials")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(secrets), scopes)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as f:
            f.write(creds.to_json())
        ok("Google credentials saved to token.json")

    return creds

# ─── STEP 1: YOUTUBE UPLOAD ──────────────────────────────────────────────────
def upload_to_youtube(post, video_path, cfg):
    """Upload video to YouTube and return the video ID."""
    hdr(f"STEP 1: YouTube Upload – Post #{post['n']}")

    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        err("google-api-python-client not installed.")
        sys.exit(1)

    SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
              "https://www.googleapis.com/auth/youtube"]
    creds = get_google_credentials(cfg, SCOPES)

    youtube = build("youtube", "v3", credentials=creds)

    title = f"{post['title']} | KJV Right Division | {post['verse']}"[:100]

    # week label works for both "week8" (string) and 9 (integer)
    wk = post["week"]
    week_label = f"Week {str(wk).replace('week', '')}"

    description = f"""📖 {post['title']}
"{post['verse']}" KJV

In this study we rightly divide the Word of Truth (2 Tim 2:15) and see exactly what this passage means for the Body of Christ in the Age of Grace.

📚 Full study: {cfg['blogger']['blog_url']}
🌐 All 344 posts: {cfg['github']['pages_url']}
📋 Archive: {cfg['github']['pages_url']}archive-index.html

#KJV #RightDivision #BibleStudy #Dispensational #GraceAge #2Timothy215"""

    tags = [
        "KJV", "Right Division", "Dispensational", "Bible Study",
        "2 Timothy 2:15", "Grace Age", "Body of Christ",
        week_label,
        post["verse"].split(" ")[0] if " " in post["verse"] else post["verse"]
    ]

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27",  # Education
        },
        "status": {
            "privacyStatus": cfg["publishing"].get("default_visibility", "public"),
            "selfDeclaredMadeForKids": False,
        }
    }

    inf(f"Uploading: {video_path.name}")
    inf(f"Title: {title}")

    media = MediaFileUpload(str(video_path), resumable=True,
                            chunksize=1024*1024*5)  # 5MB chunks

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"\r  Uploading... {pct}%", end="", flush=True)

    print()
    video_id = response["id"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    # Upload thumbnail if available
    thumb_folder = SCRIPT_DIR / cfg["publishing"].get("thumbnail_folder", "thumbnails")
    thumb = thumb_folder / f"post-{post['n']}.jpg"
    if not thumb.exists():
        thumb = thumb_folder / f"post-{post['n']}.png"
    if thumb.exists():
        inf(f"Uploading thumbnail: {thumb.name}")
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(str(thumb))
        ).execute()
        ok("Thumbnail uploaded")

    ok(f"YouTube upload complete: {video_url}")
    return video_id, video_url

# ─── STEP 2: EXTRACT POST HTML ───────────────────────────────────────────────
def extract_post_html(post, posts_meta):
    """Extract a single post's HTML from its week file."""
    hdr(f"STEP 2: Extract HTML – Post #{post['n']}")

    week_key = post["week"]
    # Integer week key (9-12): post carries its own html_file field
    if isinstance(week_key, int):
        html_name = post.get("html_file")
        if not html_name:
            err(f"Post #{post['n']} has integer week key but no html_file field")
            return None
        html_file = SCRIPT_DIR / html_name
    else:
        html_file = SCRIPT_DIR / posts_meta["weeks"][week_key]["html_file"]

    if not html_file.exists():
        err(f"Week file not found: {html_file}")
        err(f"Make sure {html_file.name} is in the same folder as pipeline.py")
        return None

    with open(html_file, encoding="utf-8") as f:
        raw = f.read()

    n = post["n"]

    # Strategy 1: <article id="post-N"> tag
    m = re.search(rf'<article[^>]*id=["\']post-{n}["\'][^>]*>(.*?)</article>',
                  raw, re.DOTALL | re.IGNORECASE)
    if m:
        ok(f"Extracted post #{n} via <article> tag")
        return f'<article id="post-{n}">{m.group(1)}</article>'

    # Strategy 2: split on <hr> boundaries, find block with "Post {n}"
    # The week files use <hr> as separator between posts
    blocks = re.split(r'<hr\s*/?>', raw, flags=re.IGNORECASE)
    for block in blocks:
        # Match "Post 113" or "Post #113" at the start of an h2
        if re.search(rf'Post\s+#?{n}\b', block, re.IGNORECASE):
            # Wrap cleanly
            content = block.strip()
            if content:
                ok(f"Extracted post #{n} via <hr> boundary ({len(content)} chars)")
                return f'<div class="blog-post" id="post-{n}">\n{content}\n</div>'

    # Strategy 3: between consecutive h2 headings
    h2_pattern = rf'(<h2[^>]*>Post\s+#?{n}\b.*?</h2>)(.*?)(?=<h2[^>]*>Post\s+#?{n+1}\b|$)'
    m = re.search(h2_pattern, raw, re.DOTALL | re.IGNORECASE)
    if m:
        content = m.group(1) + m.group(2)
        ok(f"Extracted post #{n} via h2 boundary")
        return f'<div class="blog-post" id="post-{n}">\n{content.strip()}\n</div>'

    err(f"Could not find post #{n} in {html_file.name}")
    return None

# ─── STEP 3: INJECT YOUTUBE EMBED ────────────────────────────────────────────
def inject_embed(html_content, video_id, post):
    """Replace the video placeholder with the actual YouTube iframe."""
    hdr(f"STEP 3: Inject YouTube Embed – Video {video_id}")

    embed_code = f'''<div class="video-embed" style="max-width:560px;margin:20px auto;">
  <iframe width="560" height="315"
    src="https://www.youtube.com/embed/{video_id}"
    title="{post['title']} | KJV Right Division | @ohhenry6524"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen
    style="width:100%;max-width:560px;border-radius:6px;">
  </iframe>
  <p style="text-align:center;font-size:0.8em;color:#666;margin-top:6px;">
    📺 <a href="https://www.youtube.com/@ohhenry6524" target="_blank">@ohhenry6524</a> · Subscribe for daily KJV right division studies
  </p>
</div>'''

    placeholder = f"[VIDEO EMBED – Replace with YouTube iframe: YOUR_YOUTUBE_LINK_{post['n']}]"
    if placeholder in html_content:
        result = html_content.replace(placeholder, embed_code)
        ok(f"Replaced placeholder for Post #{post['n']}")
    else:
        # Try generic placeholder
        generic = re.search(r'\[VIDEO EMBED[^\]]*\]', html_content)
        if generic:
            result = html_content.replace(generic.group(0), embed_code)
            ok("Replaced generic video placeholder")
        else:
            inf("No placeholder found — appending embed before closing tag")
            result = html_content.replace("</article>", embed_code + "\n</article>")

    return result

# ─── STEP 4: PUBLISH TO BLOGGER ──────────────────────────────────────────────
def publish_to_blogger(post, html_content, cfg):
    """Create a new Blogger post and return its URL."""
    hdr(f"STEP 4: Publish to Blogger – Post #{post['n']}")

    try:
        from googleapiclient.discovery import build
    except ImportError:
        err("google-api-python-client not installed.")
        sys.exit(1)

    SCOPES = ["https://www.googleapis.com/auth/blogger"]
    creds = get_google_credentials(cfg, SCOPES)

    blogger = build("blogger", "v3", credentials=creds)

    wk = post["week"]
    week_num = str(wk).replace("week", "")  # handles both "week8" and integer 9
    title = f"Post #{post['n']}: {post['title']} | KJV Right Division (Week {week_num})"

    labels = [
        "KJV",
        "Right Division",
        "Dispensational",
        "Bible Study",
        f"Week {week_num}",
        "2 Timothy 2:15",
        "Grace Age"
    ]

    body = {
        "title": title,
        "content": html_content,
        "labels": labels,
    }

    inf(f"Creating Blogger post: {title[:80]}...")

    result = blogger.posts().insert(
        blogId=cfg["blogger"]["blog_id"],
        body=body,
        isDraft=False
    ).execute()

    post_url = result.get("url", "")
    ok(f"Blogger post published: {post_url}")
    return post_url

# ─── STEP 5: SAVE TRACKING ───────────────────────────────────────────────────
def save_post_tracking(post_n, video_id, video_url, blogger_url, tracking):
    hdr(f"STEP 5: Save Tracking – Post #{post_n}")
    tracking[str(post_n)] = {
        "youtube_id":  video_id,
        "youtube_url": video_url,
        "blogger_url": blogger_url,
        "published_at": datetime.now().isoformat(),
        "yt_done": True,
        "blog_done": True
    }
    save_tracking(tracking)
    ok(f"Tracking saved for Post #{post_n}")

# ─── STEP 6: UPDATE GITHUB PAGES ─────────────────────────────────────────────
def update_github(post, blogger_url, cfg):
    """Update index.html with blog link and git push."""
    hdr(f"STEP 6: Update GitHub Pages – Post #{post['n']}")

    repo_path = Path(cfg["github"]["repo_path"])
    if not repo_path.exists():
        err(f"GitHub repo not found at: {repo_path}")
        inf("Set 'github.repo_path' in config.json to your local clone of the repo")
        return False

    index_file = repo_path / "index.html"
    if not index_file.exists():
        err(f"index.html not found in {repo_path}")
        return False

    # Replace placeholder link in index.html
    with open(index_file, encoding="utf-8") as f:
        content = f.read()

    placeholder = f"#post-{post['n']}-blog-placeholder"
    if placeholder in content:
        updated = content.replace(placeholder, blogger_url)
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(updated)
        ok(f"Updated index.html with blog link for Post #{post['n']}")
    else:
        inf(f"No placeholder found for Post #{post['n']} in index.html — skipping link update")

    # Git commit and push
    try:
        import git
        repo = git.Repo(repo_path)
        repo.index.add(["index.html"])
        if repo.is_dirty(index="index.html"):
            repo.index.commit(f"Post #{post['n']}: {post['title'][:60]} – link updated")
            origin = repo.remote(name="origin")
            origin.push()
            ok(f"GitHub Pages pushed: {cfg['github']['pages_url']}")
        else:
            inf("No changes to commit in index.html")
    except Exception as e:
        err(f"Git push failed: {e}")
        inf("Manual push: cd " + str(repo_path) + " && git add index.html && git commit -m 'Post update' && git push")
        return False

    return True

# ─── FIND VIDEO FILE ─────────────────────────────────────────────────────────
def find_video(post_n, cfg, explicit_path=None):
    if explicit_path:
        p = Path(explicit_path)
        if p.exists():
            return p
        err(f"Video file not found: {explicit_path}")
        return None

    video_folder = Path(cfg["videos"]["source_folder"])
    candidates = [
        video_folder / f"post-{post_n}.mp4",
        video_folder / f"post-{post_n:03d}.mp4",
        video_folder / f"{post_n}.mp4",
        video_folder / f"post_{post_n}.mp4",
    ]
    for c in candidates:
        if c.exists():
            inf(f"Found video: {c}")
            return c

    err(f"No video file found for Post #{post_n} in {video_folder}")
    inf(f"Expected filename: post-{post_n}.mp4")
    return None

# ─── MAIN PIPELINE ───────────────────────────────────────────────────────────
def run_pipeline(post_n, cfg, posts, posts_meta, tracking, video_path=None,
                 dry_run=False, blog_only=False, yt_id=None):
    """Run the full pipeline for one post. Returns True on success."""
    print(f"\n{'═'*60}")
    print(f"  POST #{post_n}: {posts[post_n]['title']}")
    print(f"  Verse: {posts[post_n]['verse']} | {posts[post_n]['week']}")
    print(f"{'═'*60}")

    post = posts[post_n]

    # Skip if already done
    if str(post_n) in tracking and tracking[str(post_n)].get("blog_done"):
        inf(f"Post #{post_n} already published. Use --force to re-publish.")
        return True

    if dry_run:
        inf(f"[DRY RUN] Would process Post #{post_n} — no actual uploads")
        return True

    try:
        video_id   = yt_id or None
        video_url  = f"https://www.youtube.com/watch?v={video_id}" if video_id else ""

        if not blog_only and not yt_id:
            # Step 1: YouTube upload
            vpath = find_video(post_n, cfg, video_path)
            if not vpath:
                return False
            video_id, video_url = upload_to_youtube(post, vpath, cfg)
        elif blog_only and not yt_id:
            inf(f"Blog-only mode: skipping YouTube upload for Post #{post_n}")

        # Step 2: Extract HTML
        html = extract_post_html(post, posts_meta)
        if not html:
            return False

        # Step 3: Inject embed (only if we have a video ID)
        if video_id:
            html = inject_embed(html, video_id, post)
        else:
            # Remove placeholder comment cleanly
            html = re.sub(r'\[VIDEO EMBED[^\]]*\]',
                          '<!-- Video coming soon – subscribe @ohhenry6524 -->',
                          html)

        # Step 4: Blogger
        blogger_url = publish_to_blogger(post, html, cfg)

        # Step 5: Tracking
        save_post_tracking(post_n, video_id or "", video_url, blogger_url, tracking)

        # Step 6: GitHub
        update_github(post, blogger_url, cfg)

        print(f"\n{'─'*60}")
        ok(f"POST #{post_n} COMPLETE")
        if video_url: ok(f"  YouTube: {video_url}")
        ok(f"  Blog:    {blogger_url}")
        print(f"{'─'*60}\n")
        return True

    except Exception as e:
        err(f"Pipeline failed for Post #{post_n}: {e}")
        import traceback
        traceback.print_exc()
        return False

# ─── STATUS REPORT ───────────────────────────────────────────────────────────
def show_status(posts, tracking):
    hdr("CONTENT STATUS")
    total = len(posts)
    done = len([k for k, v in tracking.items() if v.get("blog_done")])
    pct = int(done / total * 100) if total else 0

    print(f"  Total posts: {total}")
    print(f"  Published:   {done} ({pct}%)")
    print(f"  Remaining:   {total - done}")

    if tracking:
        print("\n  Recently published:")
        recent = sorted(tracking.items(),
                        key=lambda x: x[1].get("published_at",""),
                        reverse=True)[:5]
        for n, d in recent:
            post = posts.get(int(n), {})
            print(f"    #{n}: {post.get('title','')[:50]}")
            print(f"         {d.get('blogger_url','')}")

# ─── SETUP VERIFY ────────────────────────────────────────────────────────────
def run_setup(cfg):
    hdr("SETUP VERIFICATION")

    # Check client_secrets.json
    secrets = SCRIPT_DIR / cfg["youtube"]["client_secrets_file"]
    if secrets.exists():
        ok(f"client_secrets.json found: {secrets}")
    else:
        err(f"client_secrets.json NOT found at {secrets}")
        print("""
  To get client_secrets.json:
  1. Go to https://console.cloud.google.com
  2. Create or select a project
  3. Enable APIs: YouTube Data API v3, Blogger API v3
  4. Go to APIs & Services → Credentials
  5. Create OAuth 2.0 Client ID → Desktop App
  6. Download JSON → rename to client_secrets.json
  7. Place in the same folder as pipeline.py
""")

    # Check blogger blog ID
    blog_id = cfg["blogger"]["blog_id"]
    if blog_id == "REPLACE_WITH_YOUR_BLOGGER_BLOG_ID":
        err("Blogger blog_id not set in config.json")
        print("  Find it: blogger.com → Settings → scroll to 'Blog ID'")
    else:
        ok(f"Blogger blog ID: {blog_id}")

    # Check GitHub repo
    repo = Path(cfg["github"]["repo_path"])
    if str(repo) == "REPLACE_WITH_LOCAL_PATH_TO_REPO":
        err("github.repo_path not set in config.json")
    elif repo.exists():
        ok(f"GitHub repo found: {repo}")
    else:
        err(f"GitHub repo NOT found at: {repo}")
        print(f"  Clone it: git clone https://github.com/henrynkoh/rightlydividingkjv")

    # Check video folder
    vfolder = Path(cfg["videos"]["source_folder"])
    if str(vfolder) == "REPLACE_WITH_FOLDER_CONTAINING_MP4_FILES":
        err("videos.source_folder not set in config.json")
    elif vfolder.exists():
        mp4s = list(vfolder.glob("*.mp4"))
        ok(f"Video folder found: {vfolder} ({len(mp4s)} .mp4 files)")
    else:
        err(f"Video folder NOT found: {vfolder}")

    # Test Google auth
    if secrets.exists():
        inf("Testing Google authentication (will open browser if first time)...")
        try:
            SCOPES = [
                "https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/blogger"
            ]
            get_google_credentials(cfg, SCOPES)
            ok("Google authentication successful")
        except Exception as e:
            err(f"Google auth failed: {e}")

    ok("Setup check complete. Fix any ✗ items above, then run: python pipeline.py --post 1")

# ─── CLI ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Rightly Dividing KJV – Full Publishing Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pipeline.py --setup               # verify credentials
  python pipeline.py --status              # show what's done
  python pipeline.py --post 141            # publish Post #141
  python pipeline.py --post 141 --video /path/to/video.mp4
  python pipeline.py --posts 141 142 143   # batch publish
  python pipeline.py --week 6              # all of Week 6
  python pipeline.py --week 6 --dry-run    # preview without uploading
  python pipeline.py --all                 # everything remaining
        """
    )
    parser.add_argument("--post",    type=int, help="Single post number")
    parser.add_argument("--posts",   type=int, nargs="+", help="Multiple post numbers")
    parser.add_argument("--week",    type=int, help="All posts in a week (1–8)")
    parser.add_argument("--all",     action="store_true", help="All unpublished posts")
    parser.add_argument("--video",     type=str, help="Video file path (for --post)")
    parser.add_argument("--yt-id",    type=str, help="Existing YouTube video ID to embed (skips upload)")
    parser.add_argument("--blog-only",action="store_true", help="Publish to Blogger now, no video needed")
    parser.add_argument("--setup",    action="store_true", help="Verify setup only")
    parser.add_argument("--status",   action="store_true", help="Show completion status")
    parser.add_argument("--force",    action="store_true", help="Re-publish even if done")
    parser.add_argument("--dry-run",  action="store_true", help="Simulate without uploading")
    parser.add_argument("--delay",    type=int, default=30, help="Seconds between posts (default 30)")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    cfg = load_config()
    posts, posts_meta = load_posts()
    tracking = load_tracking()

    if args.setup:
        run_setup(cfg)
        return

    if args.status:
        show_status(posts, tracking)
        return

    # Build list of post numbers to process
    post_numbers = []

    if args.post:
        post_numbers = [args.post]
    elif args.posts:
        post_numbers = args.posts
    elif args.week:
        wk = f"week{args.week}"
        post_numbers = [n for n, p in posts.items() if p["week"] == wk]
        post_numbers.sort()
        inf(f"Week {args.week}: {len(post_numbers)} posts ({post_numbers[0]}–{post_numbers[-1]})")
    elif args.all:
        done_set = {int(k) for k, v in tracking.items() if v.get("blog_done")}
        post_numbers = sorted(n for n in posts if n not in done_set)
        inf(f"All unpublished: {len(post_numbers)} posts remaining")

    if not post_numbers:
        err("No posts selected. Use --post N, --week N, or --all")
        return

    # Process
    success, failed = 0, []
    for i, n in enumerate(post_numbers):
        if n not in posts:
            err(f"Post #{n} not found in posts_data.json")
            failed.append(n)
            continue

        if str(n) in tracking and tracking[str(n)].get("blog_done") and not args.force:
            inf(f"Post #{n} already done — skipping (use --force to override)")
            continue

        video = args.video if (args.post and args.video) else None
        result = run_pipeline(n, cfg, posts, posts_meta, tracking, video,
                              dry_run=args.dry_run,
                              blog_only=args.blog_only,
                              yt_id=args.yt_id)

        if result:
            success += 1
        else:
            failed.append(n)

        # Delay between posts to avoid API rate limits
        if i < len(post_numbers) - 1 and not args.dry_run:
            inf(f"Waiting {args.delay}s before next post...")
            time.sleep(args.delay)

    # Summary
    hdr("BATCH SUMMARY")
    ok(f"Completed: {success}/{len(post_numbers)}")
    if failed:
        err(f"Failed: {failed}")
        inf("Re-run: python pipeline.py --posts " + " ".join(map(str, failed)))

if __name__ == "__main__":
    main()
