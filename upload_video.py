#!/usr/bin/env python3
"""
upload_video.py – One-shot YouTube uploader for @ohhenry6524
Uses existing OAuth credentials (client_secrets.json + token.json)

Usage:
  python3 upload_video.py --file "path/to/video.mp4" --title "My Title"
  python3 upload_video.py  # uses defaults below
"""

import os, sys, json, argparse
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCRIPT_DIR   = Path(__file__).parent
SECRETS_FILE = SCRIPT_DIR / "client_secrets.json"
TOKEN_FILE   = SCRIPT_DIR / "token.json"
SCOPES       = ["https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube"]

# ── defaults ────────────────────────────────────────────────────────────────
DEFAULT_FILE  = str(Path.home() / "Downloads" / "How_Right_Division_Clarifies_The_Bible.mp4")
DEFAULT_TITLE = "How Right Division Clarifies The Bible | KJV Study @ohhenry6524"
DEFAULT_DESC  = """How does rightly dividing the Word of Truth (2 Timothy 2:15) clarify every part of the Bible?

This KJV study explains the dispensational key that unlocks Scripture — separating what God said to Israel from what He reveals to the Body of Christ through the Apostle Paul.

📖 Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth. — 2 Timothy 2:15 KJV

🔗 Full study series: https://rightlydividingkjv.blogspot.com
📌 GitHub Pages: https://henrynkoh.github.io/rightlydividingkjv/

#KJV #RightlyDividing #BibleStudy #Dispensational #PaulsPistles #GraceAge #BodyOfChrist"""
DEFAULT_TAGS  = ["KJV","Right Division","Bible Study","Dispensational","Paul","Grace Age",
                 "Body of Christ","2 Timothy 2:15","rightly dividing","ohhenry6524"]
DEFAULT_VIS   = "public"   # public / private / unlisted
# ─────────────────────────────────────────────────────────────────────────────

def authenticate():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not SECRETS_FILE.exists():
                print(f"❌  client_secrets.json not found at {SECRETS_FILE}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def upload(yt, file_path, title, description, tags, visibility):
    body = {
        "snippet": {
            "title":       title[:100],
            "description": description,
            "tags":        tags,
            "categoryId":  "27",   # Education
        },
        "status": {
            "privacyStatus":           visibility,
            "selfDeclaredMadeForKids": False,
        }
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/*")
    req   = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    print(f"\n  Uploading: {Path(file_path).name}")
    print(f"  Title:     {title}")
    print(f"  Visibility:{visibility}\n")

    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            print(f"\r  [{bar}] {pct}%", end="", flush=True)

    vid_id = response["id"]
    print(f"\n\n  ✓ Upload complete!")
    print(f"  Video ID:  {vid_id}")
    print(f"  URL:       https://www.youtube.com/watch?v={vid_id}")
    print(f"  Channel:   https://www.youtube.com/@ohhenry6524\n")
    return vid_id


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file",       default=DEFAULT_FILE,  help="Path to video file")
    ap.add_argument("--title",      default=DEFAULT_TITLE, help="Video title")
    ap.add_argument("--desc",       default=DEFAULT_DESC,  help="Video description")
    ap.add_argument("--visibility", default=DEFAULT_VIS,   choices=["public","private","unlisted"])
    args = ap.parse_args()

    if not Path(args.file).exists():
        # Try uploads folder (Cowork uploaded file)
        alt = Path(SCRIPT_DIR).parent / "uploads"
        candidates = list(alt.glob("*How_Right_Division*.mp4")) if alt.exists() else []
        if candidates:
            args.file = str(candidates[0])
            print(f"  Found uploaded file: {candidates[0].name}")
        else:
            print(f"❌  File not found: {args.file}")
            print(f"    Place your video at {DEFAULT_FILE} or pass --file <path>")
            sys.exit(1)

    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║  KJV Right Division – YouTube Uploader @ohhenry6524    ║")
    print("╚══════════════════════════════════════════════════════════╝\n")

    yt = authenticate()
    upload(yt, args.file, args.title, args.desc, DEFAULT_TAGS, args.visibility)


if __name__ == "__main__":
    main()
