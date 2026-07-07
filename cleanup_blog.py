"""
Delete all non-KJV posts from rightlydividingtruth.blogspot.com
Run: python3 cleanup_blog.py
"""
import pickle, json
from pathlib import Path
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

BLOG_URL         = "rightlydividingtruth.blogspot.com"
BLOG_TOKEN_PICKLE = "token_blog.pickle"
SCOPES           = ["https://www.googleapis.com/auth/blogger"]

# Load credentials
with open(BLOG_TOKEN_PICKLE, "rb") as f:
    creds = pickle.load(f)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

service = build("blogger", "v3", credentials=creds)
blog    = service.blogs().getByUrl(url=f"https://{BLOG_URL}").execute()
blog_id = blog["id"]
print(f"Blog ID: {blog_id}\n")

# Load our posted tracking to know which posts are OURS
posted_log = Path("output/posted_blog.json")
our_urls   = set()
if posted_log.exists():
    data = json.loads(posted_log.read_text())
    our_urls = {v["url"] for v in data.values()}

# List all posts
token = None
to_delete = []
while True:
    resp = service.posts().list(
        blogId=blog_id, maxResults=50,
        pageToken=token, status="live"
    ).execute()
    for post in resp.get("items", []):
        url = post.get("url", "")
        if url not in our_urls:
            to_delete.append((post["id"], post.get("title", "")[:60]))
    token = resp.get("nextPageToken")
    if not token:
        break

print(f"Found {len(to_delete)} post(s) to delete:\n")
for pid, title in to_delete:
    print(f"  • {title}")

if not to_delete:
    print("Nothing to delete. Blog is clean! ✅")
else:
    confirm = input("\nDelete these? (yes/no): ").strip().lower()
    if confirm == "yes":
        for pid, title in to_delete:
            service.posts().delete(blogId=blog_id, postId=pid).execute()
            print(f"  ✓ Deleted: {title}")
        print("\n✅ Done! Old posts removed.")
    else:
        print("Aborted.")
