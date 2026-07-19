# Operator Manual – Rightly Dividing KJV

Complete reference for running the content system.

## 1. Architecture

```
posts_data.json          → catalog of 344 posts
weekN-posts.html         → HTML bodies per week
post-NNN.mp4             → local video (optional)
        │
        ▼
   pipeline.py
        ├── YouTube Data API  → upload + description/tags
        ├── Blogger API       → publish HTML with embed
        ├── tracking.json     → YouTube IDs + Blogger URLs
        └── git push          → GitHub Pages update
```

**Public surfaces**

| Surface | URL |
|---------|-----|
| GitHub Pages | https://henrynkoh.github.io/rightlydividingkjv/ |
| Blogger | https://rightlydividingkjv.blogspot.com |
| YouTube | https://www.youtube.com/@ohhenry6524 |

---

## 2. Repository map

| Path | Role |
|------|------|
| `index.html` | Public landing / study hub |
| `archive-index.html` | Full archive |
| `week*-posts.html` | Week post HTML |
| `posts_data.json` | Post metadata (titles, verses, weeks) |
| `pipeline.py` | Main automation entry |
| `daily_publish.py` | Daily helper publisher |
| `blog_poster.py` | Blogger-focused helper |
| `generate_voice.py` / `generate_videos.py` | Media generation helpers |
| `setup.sh` | One-time environment setup |
| `config.template.json` | Config template (safe to commit) |
| `publishing-guide.html` | Visual ops guide |
| `content-dashboard.html` | Content dashboard |
| `ads/` | Marketing copy pack |
| `docs/` | This documentation |

---

## 3. Configuration

Copy template:

```bash
cp config.template.json config.json
```

### Required fields

```json
{
  "youtube": {
    "channel_handle": "@ohhenry6524",
    "client_secrets_file": "client_secrets.json"
  },
  "blogger": {
    "blog_id": "YOUR_BLOG_ID",
    "blog_url": "https://rightlydividingkjv.blogspot.com",
    "client_secrets_file": "client_secrets.json"
  },
  "github": {
    "repo_path": "/absolute/path/to/rightlydividingkjv",
    "repo_url": "https://github.com/henrynkoh/rightlydividingkjv",
    "pages_url": "https://henrynkoh.github.io/rightlydividingkjv/",
    "branch": "main"
  },
  "videos": {
    "source_folder": "/absolute/path/to/mp4s"
  },
  "publishing": {
    "default_visibility": "public",
    "default_category": "KJV Right Division",
    "thumbnail_folder": "thumbnails"
  },
  "tracking": {
    "json_file": "tracking.json"
  }
}
```

### Finding the Blogger Blog ID

Blogger → Settings → scroll to **Blog ID**.

### Video naming

```
<source_folder>/post-1.mp4
<source_folder>/post-141.mp4
```

Optional thumbnails:

```
thumbnails/post-1.jpg
thumbnails/post-141.png
```

---

## 4. Google Cloud setup

1. Create project in [Google Cloud Console](https://console.cloud.google.com)  
2. Enable APIs:
   - YouTube Data API v3  
   - Blogger API v3  
3. OAuth consent screen → External  
4. Add scopes for YouTube upload + Blogger  
5. Add your Gmail as a test user  
6. Create OAuth Client ID (Desktop)  
7. Save as `client_secrets.json` in the repo root  

First run of `pipeline.py --setup` opens a browser and writes `token.json`.

> Korean step-by-step: [SETUP_YOUTUBE.md](../SETUP_YOUTUBE.md)

---

## 5. Pipeline commands

| Command | Description |
|---------|-------------|
| `python3 pipeline.py --setup` | Verify config + OAuth |
| `python3 pipeline.py --status` | Show published / remaining |
| `python3 pipeline.py --post N` | Full publish for post N |
| `python3 pipeline.py --post N --video path.mp4` | Custom video path |
| `python3 pipeline.py --posts A B C` | Multiple posts |
| `python3 pipeline.py --week W` | All posts in week W |
| `python3 pipeline.py --week W --blog-only` | Blogger only |
| `python3 pipeline.py --all --blog-only` | All posts to Blogger |
| `python3 pipeline.py --post N --yt-id VIDEO_ID` | Attach existing YouTube ID |

### Per-post automation steps

1. Upload video to YouTube (unless `--blog-only` or `--yt-id`)  
2. Extract post HTML from the week file  
3. Insert iframe embed for the YouTube ID  
4. Publish to Blogger  
5. Save tracking (`tracking.json`)  
6. Update GitHub Pages files and push  

---

## 6. Related scripts

| Script | Use |
|--------|-----|
| `./setup.sh` | First-time install |
| `./batch_run.sh` | Batch helper |
| `./generate_all_videos.sh` | Bulk video generation |
| `python3 daily_publish.py` | Daily publishing helper |
| `python3 blog_poster.py` | Blogger posting helper |
| `python3 generate_voice.py` | Voice generation |
| `python3 generate_videos.py` | Video generation |
| `python3 upload_video.py` | Standalone YouTube upload |

Open `publishing-guide.html` for the recommended daily/weekly rhythm.

---

## 7. Series data

- **Total posts:** 344 (`posts_data.json` → `meta.total_posts`)  
- **Weeks:** 12  
- **Anchor verse:** 2 Timothy 2:15 KJV  

Week themes (1–8 named in data; 9–12 continue through “Finishing Strong”).

---

## 8. Troubleshooting

| Problem | Fix |
|---------|-----|
| `config.json not found` | Copy from `config.template.json` |
| `client_secrets.json not found` | Download OAuth Desktop JSON from Google Cloud |
| OAuth browser fails | Add yourself as test user on consent screen; re-enable APIs |
| Token expired | Delete `token.json` and run `--setup` again |
| Video not found | Check `videos.source_folder` and `post-N.mp4` name |
| Blogger 404 / permission | Confirm `blog_id` and that the Google account owns the blog |
| Git push fails | Check `github.repo_path`, remotes, and auth (`gh auth login` or SSH) |
| Quota exceeded | YouTube daily upload quota — wait or reduce batch size |

---

## 9. Security

Never commit:

- `config.json`
- `client_secrets.json` / `client_secret.json`
- `token.json`, `token.pickle`, `token_blog.pickle`

If secrets were ever pushed publicly, **rotate** OAuth credentials in Google Cloud Console immediately.

---

## 10. Marketing assets

Platform-ready posts: [`../ads/`](../ads/)

| File | Platform |
|------|----------|
| `facebook.md` | Facebook |
| `instagram.md` | Instagram |
| `threads.md` | Threads |
| `blogger.md` | Blogger (EN + KO) |
| `naver-blog.md` | Naver Blog (EN + KO) |
| `tistory.md` | Tistory (EN + KO) |
| `wordpress.md` | WordPress |
| `newsletter.md` | Newsletter |
| `email.md` | Email |

---

## 11. Support links

- Site: https://henrynkoh.github.io/rightlydividingkjv/  
- Blog: https://rightlydividingkjv.blogspot.com  
- Channel: https://www.youtube.com/@ohhenry6524  
- Repo: https://github.com/henrynkoh/rightlydividingkjv  
