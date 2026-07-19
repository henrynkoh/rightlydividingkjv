# Quickstart – Rightly Dividing KJV

Get from zero to your first published post in about **15 minutes**.

## Before you start

You need:

- Python 3.10+
- Git
- A Google account with access to:
  - YouTube channel `@ohhenry6524` (or your own test channel)
  - Blogger blog (e.g. https://rightlydividingkjv.blogspot.com)
- Optional: local `.mp4` videos named `post-NNN.mp4` (e.g. `post-1.mp4`)

---

## 1. Clone the repo

```bash
git clone https://github.com/henrynkoh/rightlydividingkjv.git
cd rightlydividingkjv
```

---

## 2. Run setup

```bash
chmod +x setup.sh
./setup.sh
```

This will:

1. Check Python  
2. Install packages from `requirements.txt`  
3. Create `config.json` from the template  
4. Guide you through Google credentials  
5. Optionally clone / sync GitHub paths  

Or install packages manually:

```bash
python3 -m pip install -r requirements.txt
cp config.template.json config.json
```

---

## 3. Fill `config.json`

Edit at least:

| Field | Example |
|-------|---------|
| `blogger.blog_id` | From Blogger → Settings → Blog ID |
| `github.repo_path` | Absolute path to this clone |
| `videos.source_folder` | Folder with `post-NNN.mp4` files |

Keep `blogger.blog_url` and `github.pages_url` unless you fork the project.

---

## 4. Add Google API credentials (once)

1. Open [Google Cloud Console](https://console.cloud.google.com)  
2. Create a project (e.g. `RightlyDividingKJV`)  
3. Enable **YouTube Data API v3** and **Blogger API v3**  
4. Configure OAuth consent screen (External + your Gmail as test user)  
5. Create **OAuth 2.0 Client ID** → Desktop app  
6. Download JSON → rename to `client_secrets.json` → place in the repo root  

More detail (Korean): [SETUP_YOUTUBE.md](../SETUP_YOUTUBE.md)

---

## 5. Verify

```bash
python3 pipeline.py --setup
```

A browser window opens the first time for Google login. Approve YouTube + Blogger access.

---

## 6. Publish something

### Blog only (no video needed)

```bash
python3 pipeline.py --post 1 --blog-only
```

### Full pipeline (video → YouTube → Blogger → GitHub)

```bash
# Put file here:  <videos.source_folder>/post-1.mp4
python3 pipeline.py --post 1
```

### Check progress

```bash
python3 pipeline.py --status
```

---

## 7. Open the study site

- Local: open `index.html` in a browser  
- Live: https://henrynkoh.github.io/rightlydividingkjv/  
- Blog: https://rightlydividingkjv.blogspot.com  

---

## Next steps

- Full walkthrough → [TUTORIAL.md](TUTORIAL.md)  
- All commands & troubleshooting → [MANUAL.md](MANUAL.md)  
- Visual workflow → [publishing-guide.html](../publishing-guide.html)  
- Share the series → [`../ads/`](../ads/)  

---

## 빠른 시작 (한국어 요약)

```bash
git clone https://github.com/henrynkoh/rightlydividingkjv.git
cd rightlydividingkjv
./setup.sh
# config.json 작성 + client_secrets.json 배치
python3 pipeline.py --setup
python3 pipeline.py --post 1 --blog-only   # 영상 없이 블로그만
```

자세한 한글 광고/소개 글은 `ads/blogger.md`, `ads/naver-blog.md`, `ads/tistory.md` 를 참고하세요.
