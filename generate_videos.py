#!/usr/bin/env python3
"""
generate_videos.py – Slide-style video generator for "Rightly Dividing KJV"
Matches the visual style of @ohhenry6524 existing videos (dark navy + gold).

Generates post-NNN.mp4 for posts 113–232 (Weeks 5–8).

Usage:
  python3 generate_videos.py                   # all weeks 5-8
  python3 generate_videos.py --week 5          # week 5 only
  python3 generate_videos.py --posts 113 114   # specific posts
  python3 generate_videos.py --post 113        # single post
  python3 generate_videos.py --preview 113     # save slide PNGs only, no video

Output: videos/post-NNN.mp4  (created beside this script)
"""

import os
import sys
import json
import re
import html as htmllib
import subprocess
import textwrap
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# ── PATHS ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
POSTS_JSON  = SCRIPT_DIR / "posts_data.json"
VIDEOS_DIR  = SCRIPT_DIR / "videos"
SLIDES_DIR  = SCRIPT_DIR / "slides_tmp"

# Font paths
FONT_BOLD   = "/usr/share/fonts/truetype/lato/Lato-Bold.ttf"
FONT_BLACK  = "/usr/share/fonts/truetype/lato/Lato-Black.ttf"
FONT_REG    = "/usr/share/fonts/truetype/lato/Lato-Regular.ttf"
FONT_LIGHT  = "/usr/share/fonts/truetype/lato/Lato-Light.ttf"

# ── COLORS ────────────────────────────────────────────────────────────────────
BG_DARK     = (8, 8, 40)        # deep navy
GOLD        = (212, 175, 55)    # classic gold
GOLD_LIGHT  = (240, 210, 100)   # lighter gold for text
WHITE       = (255, 255, 255)
GRAY_LIGHT  = (200, 200, 220)
GRAY_DIM    = (140, 140, 165)
ACCENT_BLUE = (30, 80, 160)     # dark blue accent
BG_SLIDE2   = (5, 5, 30)        # slightly deeper for verse slides

# ── VIDEO SETTINGS ────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1280, 720
FPS           = 24

# Slide durations (seconds)
DUR_INTRO   = 3
DUR_TITLE   = 22
DUR_VERSE   = 25
DUR_TEACH   = 18
DUR_APP     = 14
DUR_OUTRO   = 8
# total ≈ 1:30

WEEK_NAMES = {
    "week5": "Week 5 – Practical Right Division",
    "week6": "Week 6 – Prophetic Right Division",
    "week7": "Week 7 – Doctrinal Foundations",
    "week8": "Week 8 – Advanced Application",
    9:  "Week 9 – Ministry & Missions in the Grace Age",
    10: "Week 10 – Prophecy Rightly Divided",
    11: "Week 11 – The Mysteries of Paul's Gospel",
    12: "Week 12 – Finishing Strong: A Life Rightly Divided",
}

# ─────────────────────────────────────────────────────────────────────────────
# PIL drawing helpers
# ─────────────────────────────────────────────────────────────────────────────
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Installing Pillow...")
    subprocess.run([sys.executable, "-m", "pip", "install", "Pillow",
                    "--break-system-packages", "--quiet"])
    from PIL import Image, ImageDraw, ImageFont


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def draw_gold_lines(draw, y_top=None, y_bot=None, thickness=4, margin=60):
    """Draw horizontal gold accent lines."""
    if y_top is None: y_top = 130
    if y_bot is None: y_bot = HEIGHT - 130
    for i in range(thickness):
        draw.line([(margin, y_top + i), (WIDTH - margin, y_top + i)], fill=GOLD)
        draw.line([(margin, y_bot + i), (WIDTH - margin, y_bot + i)], fill=GOLD)


def draw_corner_accents(draw, size=40, margin=60):
    """Small gold corner squares for visual style."""
    corners = [
        (margin, 130), (WIDTH - margin - size, 130),
        (margin, HEIGHT - 130 - size), (WIDTH - margin - size, HEIGHT - 130 - size)
    ]
    for cx, cy in corners:
        draw.rectangle([cx, cy, cx + size, cy + size], fill=GOLD)


def draw_channel_tag(draw, alpha=200):
    """Bottom channel identifier."""
    font = load_font(FONT_REG, 32)
    text = "@ohhenry6524  |  Rightly Dividing KJV"
    draw.text((WIDTH // 2, HEIGHT - 80), text, font=font,
              fill=GRAY_DIM, anchor="mm")


def wrap_text(text, max_chars):
    """Wrap text to max_chars per line."""
    return textwrap.fill(text, max_chars)


def text_block(draw, lines, font, color, x, start_y, line_spacing=1.35):
    """Draw multi-line text centered."""
    _, _, _, h = draw.textbbox((0, 0), "Ag", font=font)
    step = int(h * line_spacing)
    for i, line in enumerate(lines):
        draw.text((x, start_y + i * step), line, font=font, fill=color, anchor="mm")
    return start_y + len(lines) * step


# ─────────────────────────────────────────────────────────────────────────────
# SLIDE CREATORS
# ─────────────────────────────────────────────────────────────────────────────

def make_slide_intro(post, week_name):
    """Slide 1: Series intro card."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    draw_gold_lines(draw)
    draw_corner_accents(draw)

    # Series name
    f_series = load_font(FONT_LIGHT, 44)
    draw.text((WIDTH // 2, 300), "Rightly Dividing the Word of Truth",
              font=f_series, fill=GOLD_LIGHT, anchor="mm")

    # "2 Timothy 2:15 KJV"
    f_ref = load_font(FONT_REG, 34)
    draw.text((WIDTH // 2, 360), "2 Timothy 2:15  ·  KJV",
              font=f_ref, fill=GRAY_DIM, anchor="mm")

    # Divider dot
    draw.ellipse([(WIDTH//2-6, 400), (WIDTH//2+6, 412)], fill=GOLD)

    # Week name
    f_week = load_font(FONT_BOLD, 52)
    draw.text((WIDTH // 2, 480), week_name,
              font=f_week, fill=WHITE, anchor="mm")

    # Post number badge
    f_num = load_font(FONT_BLACK, 38)
    badge_text = f"Post #{post['n']}"
    draw.text((WIDTH // 2, 590), badge_text, font=f_num, fill=GOLD, anchor="mm")

    draw_channel_tag(draw)
    return img


def make_slide_title(post, week_name):
    """Slide 2: Post title + verse reference (main card)."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Subtle gradient-like top
    for i in range(200):
        alpha = int(30 * (1 - i / 200))
        draw.line([(0, i), (WIDTH, i)], fill=(alpha, alpha, alpha + 20))

    draw_gold_lines(draw, y_top=140, y_bot=HEIGHT - 140, thickness=5)
    draw_corner_accents(draw, size=45, margin=65)

    # Week label (small, top center)
    f_week = load_font(FONT_LIGHT, 36)
    draw.text((WIDTH // 2, 80), week_name, font=f_week, fill=GRAY_DIM, anchor="mm")

    # Post number (top right area)
    f_postnum = load_font(FONT_BOLD, 36)
    draw.text((WIDTH - 80, 80), f"#{post['n']}", font=f_postnum, fill=GOLD, anchor="rm")

    # Main title — break into lines
    title_clean = re.sub(r'^Post\s+\d+\s*[·•]\s*Day\s*[\d-]+\s*[:\-]?\s*', '', post['title'])
    title_wrapped = textwrap.wrap(title_clean, 44)

    f_title_big = load_font(FONT_BLACK, 72 if len(title_wrapped) <= 2 else 62)
    _, _, _, th = draw.textbbox((0,0), "Ag", font=f_title_big)
    total_h = len(title_wrapped) * int(th * 1.25)
    start_y = (HEIGHT - total_h) // 2 - 60

    for i, line in enumerate(title_wrapped):
        y = start_y + i * int(th * 1.25)
        # Shadow
        draw.text((WIDTH // 2 + 2, y + 2), line, font=f_title_big,
                  fill=(0, 0, 15), anchor="mm")
        draw.text((WIDTH // 2, y), line, font=f_title_big,
                  fill=WHITE, anchor="mm")

    # Gold divider
    div_y = start_y + total_h + 30
    draw.line([(WIDTH // 2 - 120, div_y), (WIDTH // 2 + 120, div_y)], fill=GOLD, width=3)

    # Verse reference
    f_verse_ref = load_font(FONT_BOLD, 48)
    draw.text((WIDTH // 2, div_y + 55), post.get('verse', ''),
              font=f_verse_ref, fill=GOLD_LIGHT, anchor="mm")

    # KJV label
    f_kjv = load_font(FONT_LIGHT, 34)
    draw.text((WIDTH // 2, div_y + 115), "King James Version",
              font=f_kjv, fill=GRAY_DIM, anchor="mm")

    draw_channel_tag(draw)
    return img


def make_slide_verse(post, verse_text):
    """Slide 3: KJV verse text."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_SLIDE2)
    draw = ImageDraw.Draw(img)

    draw_gold_lines(draw, y_top=110, y_bot=HEIGHT - 110, thickness=3)

    # "KJV" label top
    f_kjv = load_font(FONT_BOLD, 38)
    draw.text((WIDTH // 2, 70), "KJV SCRIPTURE", font=f_kjv, fill=GOLD, anchor="mm")

    # Verse text — italic style with quotation marks
    if verse_text:
        # Clean up the verse
        v = verse_text.strip()
        if not v.startswith('"') and not v.startswith('“'):
            v = '“' + v + '”'

        # Split out reference (after em-dash or last —)
        v_clean = v
        ref_part = ""
        if " — " in v:
            parts = v.rsplit(" — ", 1)
            v_clean = parts[0]
            ref_part = "— " + parts[1]
        elif " – " in v:
            parts = v.rsplit(" – ", 1)
            v_clean = parts[0]
            ref_part = "– " + parts[1]

        # Wrap verse text
        verse_lines = textwrap.wrap(v_clean, 58)
        f_verse = load_font(FONT_REG, 46)
        _, _, _, lh = draw.textbbox((0, 0), "Ag", font=f_verse)
        step = int(lh * 1.4)
        total = len(verse_lines) * step
        y0 = (HEIGHT - total) // 2 - 40

        for i, line in enumerate(verse_lines):
            draw.text((WIDTH // 2, y0 + i * step), line,
                      font=f_verse, fill=(230, 225, 255), anchor="mm")

        # Reference
        if ref_part:
            f_ref = load_font(FONT_BOLD, 42)
            draw.text((WIDTH // 2, y0 + total + 30), ref_part,
                      font=f_ref, fill=GOLD_LIGHT, anchor="mm")
    else:
        f_ref = load_font(FONT_BOLD, 48)
        draw.text((WIDTH // 2, HEIGHT // 2), post.get('verse', ''),
                  font=f_ref, fill=GOLD_LIGHT, anchor="mm")

    draw_channel_tag(draw)
    return img


def make_slide_teaching(post, teaching_text, week_name):
    """Slide 4: Right Division teaching point."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    draw_gold_lines(draw, y_top=120, y_bot=HEIGHT - 120, thickness=3)

    # Section label
    f_label = load_font(FONT_BOLD, 36)
    draw.text((WIDTH // 2, 75), "RIGHT DIVISION", font=f_label, fill=GOLD, anchor="mm")

    # Teaching text
    if teaching_text:
        t = re.sub(r'Right Division:\s*', '', teaching_text).strip()
        lines = textwrap.wrap(t, 68)[:8]  # max 8 lines
        f_teach = load_font(FONT_REG, 38)
        _, _, _, lh = draw.textbbox((0, 0), "Ag", font=f_teach)
        step = int(lh * 1.5)
        total = len(lines) * step
        y0 = (HEIGHT - total) // 2

        for i, line in enumerate(lines):
            draw.text((WIDTH // 2, y0 + i * step), line,
                      font=f_teach, fill=GRAY_LIGHT, anchor="mm")
    else:
        f_teach = load_font(FONT_BOLD, 52)
        draw.text((WIDTH // 2, HEIGHT // 2), "Rightly Dividing the Word",
                  font=f_teach, fill=WHITE, anchor="mm")

    draw_channel_tag(draw)
    return img


def make_slide_application(post, app_text):
    """Slide 5: Application + outro."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (5, 12, 35))
    draw = ImageDraw.Draw(img)

    draw_gold_lines(draw, y_top=115, y_bot=HEIGHT - 115, thickness=3)
    draw_corner_accents(draw, size=35, margin=70)

    # Section label
    f_label = load_font(FONT_BLACK, 42)
    draw.text((WIDTH // 2, 72), "APPLICATION", font=f_label, fill=GOLD, anchor="mm")

    # Application text
    if app_text:
        t = re.sub(r'Application:\s*', '', app_text).strip()
        lines = textwrap.wrap(t, 62)[:7]
        f_app = load_font(FONT_REG, 40)
        _, _, _, lh = draw.textbbox((0, 0), "Ag", font=f_app)
        step = int(lh * 1.5)
        total = len(lines) * step
        y0 = (HEIGHT - total) // 2 - 20

        for i, line in enumerate(lines):
            draw.text((WIDTH // 2, y0 + i * step), line,
                      font=f_app, fill=WHITE, anchor="mm")
    else:
        f_app = load_font(FONT_BOLD, 48)
        draw.text((WIDTH // 2, HEIGHT // 2),
                  "Study to shew thyself approved — 2 Tim 2:15",
                  font=f_app, fill=GRAY_LIGHT, anchor="mm")

    draw_channel_tag(draw)
    return img


def make_slide_outro(post):
    """Slide 6: Subscribe / outro."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)

    draw_gold_lines(draw, y_top=130, y_bot=HEIGHT - 130, thickness=5)
    draw_corner_accents(draw, size=50, margin=60)

    f_big = load_font(FONT_BLACK, 68)
    draw.text((WIDTH // 2, HEIGHT // 2 - 110), "@ohhenry6524",
              font=f_big, fill=GOLD_LIGHT, anchor="mm")

    f_sub = load_font(FONT_BOLD, 46)
    draw.text((WIDTH // 2, HEIGHT // 2 - 20), "Rightly Dividing the Word of Truth",
              font=f_sub, fill=WHITE, anchor="mm")

    f_light = load_font(FONT_LIGHT, 38)
    draw.text((WIDTH // 2, HEIGHT // 2 + 55),
              "Like · Subscribe · Share  |  KJV Right Division",
              font=f_light, fill=GRAY_DIM, anchor="mm")

    # Blog link
    f_blog = load_font(FONT_REG, 32)
    draw.text((WIDTH // 2, HEIGHT // 2 + 130),
              "rightlydividingkjv.blogspot.com",
              font=f_blog, fill=GRAY_DIM, anchor="mm")

    draw_channel_tag(draw)
    return img


# ─────────────────────────────────────────────────────────────────────────────
# HTML content extraction
# ─────────────────────────────────────────────────────────────────────────────

_html_cache = {}

def get_week_html(week_key):
    # Support integer week keys (9-12) by converting to filename
    if isinstance(week_key, int):
        week_key = f"week{week_key}"
    if week_key not in _html_cache:
        fname = SCRIPT_DIR / f"{week_key}-posts.html"
        if fname.exists():
            _html_cache[week_key] = fname.read_text(encoding="utf-8")
        else:
            _html_cache[week_key] = ""
    return _html_cache[week_key]


def strip_html(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = htmllib.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def extract_content(post):
    """Extract verse, teaching, application from week HTML file."""
    n = post['n']
    week_key = post['week']
    raw = get_week_html(week_key)

    if not raw:
        return None, None, None

    blocks = re.split(r'<hr\s*/?>', raw, flags=re.IGNORECASE)
    target = None
    for blk in blocks:
        if re.search(rf'\bPost\s+{n}\b', blk, re.IGNORECASE):
            target = blk
            break

    if not target:
        return None, None, None

    verse_m   = re.search(r'<blockquote[^>]*>(.*?)</blockquote>', target, re.DOTALL)
    app_m     = re.search(r'class="application"[^>]*>(.*?)</div>', target, re.DOTALL)
    # Look for Right Division paragraph
    teach_m   = re.search(
        r'(?:Right Division|right division)[:\s]+(.*?)(?:<div|<p class|$)',
        target, re.DOTALL | re.IGNORECASE)

    verse   = strip_html(verse_m.group(1))   if verse_m   else None
    app     = strip_html(app_m.group(1))     if app_m     else None
    teach   = strip_html(teach_m.group(1))[:400] if teach_m else None

    return verse, teach, app


# ─────────────────────────────────────────────────────────────────────────────
# VIDEO ASSEMBLY
# ─────────────────────────────────────────────────────────────────────────────

def make_video(post, preview=False, force=False):
    """Generate all slides and combine into MP4."""
    n       = post['n']
    wk = post['week']
    week_name = WEEK_NAMES.get(wk) or (post.get('week_name') or f"Week {wk}").title()
    out_mp4 = VIDEOS_DIR / f"post-{n}.mp4"

    if out_mp4.exists() and not preview and not force:
        sz = out_mp4.stat().st_size
        if sz > 10000:   # valid file (>10KB)
            print(f"  ✓ post-{n}.mp4 already exists — skipping")
            return True
        # else: corrupt/empty, overwrite

    print(f"  → Post #{n}: {post['title'][:55]}...")

    verse, teach, app = extract_content(post)

    slides = [
        (make_slide_intro(post, week_name),    DUR_INTRO),
        (make_slide_title(post, week_name),    DUR_TITLE),
        (make_slide_verse(post, verse),        DUR_VERSE),
        (make_slide_teaching(post, teach, week_name), DUR_TEACH),
        (make_slide_application(post, app),    DUR_APP),
        (make_slide_outro(post),               DUR_OUTRO),
    ]

    slide_paths = []
    SLIDES_DIR.mkdir(exist_ok=True)

    for i, (img, dur) in enumerate(slides):
        path = SLIDES_DIR / f"post{n}_slide{i}.png"
        img.save(str(path))
        slide_paths.append((path, dur))
        if preview:
            print(f"    Saved slide {i}: {path}")

    if preview:
        print(f"  Preview saved to {SLIDES_DIR}/")
        return True

    # Build ffmpeg concat list
    concat_file = SLIDES_DIR / f"post{n}_concat.txt"
    with open(concat_file, 'w') as f:
        for path, dur in slide_paths:
            f.write(f"file '{path.absolute()}'\n")
            f.write(f"duration {dur}\n")
        # ffmpeg needs last entry without duration
        f.write(f"file '{slide_paths[-1][0].absolute()}'\n")

    # Run ffmpeg
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-vf", f"scale={WIDTH}:{HEIGHT},fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "25",
        "-movflags", "+faststart",
        "-an",  # no audio
        str(out_mp4)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Cleanup slide PNGs
    for path, _ in slide_paths:
        try: path.unlink()
        except: pass
    try: concat_file.unlink()
    except: pass

    if result.returncode == 0:
        size_mb = out_mp4.stat().st_size / (1024 * 1024)
        print(f"  ✓ post-{n}.mp4  ({size_mb:.1f} MB)")
        return True
    else:
        print(f"  ✗ FAILED post-{n}: {result.stderr[-200:]}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate KJV slide videos for weeks 5-12")
    parser.add_argument("--week",    type=int, help="Generate all posts in this week (5-12)")
    parser.add_argument("--post",    type=int, help="Generate single post")
    parser.add_argument("--posts",   type=int, nargs="+", help="Generate specific post numbers")
    parser.add_argument("--all",     action="store_true", help="Generate all weeks 5-12")
    parser.add_argument("--preview", type=int, metavar="N", help="Preview: save slides for post N without making video")
    parser.add_argument("--force",   action="store_true", help="Overwrite existing videos")
    args = parser.parse_args()

    # Load posts
    with open(POSTS_JSON) as f:
        data = json.load(f)
    all_posts = {p['n']: p for p in data['posts']}
    # Posts with videos: weeks 5-12 (post 113+)
    video_weeks = ('week5','week6','week7','week8', 9, 10, 11, 12)
    w58_posts = [p for p in data['posts'] if p['week'] in video_weeks]

    VIDEOS_DIR.mkdir(exist_ok=True)
    SLIDES_DIR.mkdir(exist_ok=True)

    print(f"""
╔══════════════════════════════════════════════════════════╗
║   Rightly Dividing KJV – Video Generator                ║
║   @ohhenry6524  ·  Slide-style MP4  ·  1280×720        ║
╚══════════════════════════════════════════════════════════╝
""")

    # Determine which posts to generate
    if args.preview:
        posts = [all_posts[args.preview]] if args.preview in all_posts else []
        make_video(posts[0], preview=True)
        return

    if args.post:
        posts = [all_posts[args.post]] if args.post in all_posts else []
    elif args.posts:
        posts = [all_posts[n] for n in args.posts if n in all_posts]
    elif args.week:
        # Support both old string keys (5-8) and new int keys (9-12)
        wk_int = args.week
        wk_str = f"week{args.week}"
        posts = [p for p in w58_posts if p['week'] in (wk_str, wk_int)]
    else:
        posts = w58_posts  # default: all weeks 5-12

    if not posts:
        print("No matching posts found.")
        return

    # (--force means overwrite; ffmpeg already uses -y so no unlink needed)

    print(f"Generating {len(posts)} video(s)...\n")
    ok_count = 0
    fail_count = 0
    start = datetime.now()

    for post in posts:
        success = make_video(post, force=args.force)
        if success:
            ok_count += 1
        else:
            fail_count += 1

    elapsed = (datetime.now() - start).seconds
    mins, secs = elapsed // 60, elapsed % 60

    print(f"""
╔══════════════════════════════════════════════════════════╗
║   DONE  ✓ {ok_count:3d} generated   ✗ {fail_count:3d} failed       ║
║   Time: {mins}m {secs:02d}s                                    ║
╚══════════════════════════════════════════════════════════╝

Videos saved to: {VIDEOS_DIR}

Next steps:
  Upload to YouTube:
    python3 pipeline.py --week 5
  Or attach existing YouTube IDs:
    python3 pipeline.py --week 5 --blog-only
""")

    # Cleanup slides dir if empty
    try:
        if not any(SLIDES_DIR.iterdir()):
            SLIDES_DIR.rmdir()
    except:
        pass


if __name__ == "__main__":
    main()
