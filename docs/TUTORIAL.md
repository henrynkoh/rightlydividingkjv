# Tutorial – Publish Your First Rightly Dividing Study

A guided walkthrough from empty folder to a live post.

Estimated time: **30–45 minutes** the first time (including Google Cloud setup).

---

## Lesson 0 – What you will build

By the end you will have:

1. A working local clone  
2. Google OAuth connected to YouTube + Blogger  
3. At least one post published (blog-only or full with video)  
4. Understanding of the weekly publish rhythm  

Anchor verse for the series:

> *Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth.*  
> — **2 Timothy 2:15 (KJV)**

---

## Lesson 1 – Install the project

```bash
git clone https://github.com/henrynkoh/rightlydividingkjv.git
cd rightlydividingkjv
chmod +x setup.sh
./setup.sh
```

When prompted, create/edit `config.json`.

**Checkpoint:** `requirements.txt` packages install without errors.

---

## Lesson 2 – Connect Google

1. Create a Google Cloud project  
2. Enable **YouTube Data API v3** and **Blogger API v3**  
3. Configure OAuth consent (add your email as test user)  
4. Create Desktop OAuth client → download JSON  
5. Save as `client_secrets.json` in the project root  

Then:

```bash
python3 pipeline.py --setup
```

Sign in with the Google account that owns the YouTube channel and Blogger blog.

**Checkpoint:** Script prints success and creates `token.json`.

Korean detail: [SETUP_YOUTUBE.md](../SETUP_YOUTUBE.md)

---

## Lesson 3 – Publish your first blog post (no video)

Fastest win — no recording required:

```bash
python3 pipeline.py --post 1 --blog-only
```

Open:

- https://rightlydividingkjv.blogspot.com  
- Or the URL printed by the script / stored in `tracking.json`

**Checkpoint:** Post #1 appears on Blogger with title related to 2 Timothy 2:15.

---

## Lesson 4 – Full publish with a video

1. Record or export a short teaching video.  
2. Save it as:

```text
<your videos.source_folder>/post-1.mp4
```

3. Optional thumbnail:

```text
thumbnails/post-1.jpg
```

4. Run:

```bash
python3 pipeline.py --post 1
```

What happens:

1. Upload to YouTube  
2. Build HTML with embed  
3. Publish to Blogger  
4. Update tracking + GitHub Pages  

**Checkpoint:** Video appears on `@ohhenry6524` and the blog post embeds it.

---

## Lesson 5 – Attach an existing YouTube video

If the video is already on YouTube:

```bash
python3 pipeline.py --post 1 --yt-id YOUR_VIDEO_ID
```

Useful when you uploaded manually or reused a prior upload.

---

## Lesson 6 – Publish a whole week

```bash
# Full week with videos present
python3 pipeline.py --week 1

# Blog posts only for the week
python3 pipeline.py --week 1 --blog-only
```

Check status anytime:

```bash
python3 pipeline.py --status
```

---

## Lesson 7 – Browse the study library locally

Open in a browser:

| File | Purpose |
|------|---------|
| `index.html` | Home / hub |
| `archive-index.html` | All posts |
| `content-dashboard.html` | Ops dashboard |
| `publishing-guide.html` | Daily workflow |
| `week5-posts.html` … | Week HTML bodies |

Live site: https://henrynkoh.github.io/rightlydividingkjv/

---

## Lesson 8 – Share the series

Use ready-made copy in [`../ads/`](../ads/):

1. Pick a platform file (e.g. `instagram.md`)  
2. Copy a variant  
3. Paste link to the site or latest YouTube/blog post  
4. For Korean audiences, use the Korean sections in:
   - `ads/blogger.md`  
   - `ads/naver-blog.md`  
   - `ads/tistory.md`  

---

## Suggested weekly rhythm

| Day | Focus |
|-----|--------|
| Mon | Record / prepare 3–4 posts |
| Tue | `pipeline.py --posts …` or `--week` |
| Wed | Share on Threads / Instagram |
| Thu | Blog cross-post (Naver / Tistory / WordPress) |
| Fri | Newsletter or email update |
| Sat | Rest / review `pipeline.py --status` |
| Sun | Longer teaching upload + site highlight |

Details: open `publishing-guide.html`.

---

## Common first-week mistakes

1. Forgetting to set `blogger.blog_id`  
2. Saving OAuth JSON under the wrong filename  
3. Naming videos `1.mp4` instead of `post-1.mp4`  
4. Committing `token.json` / secrets to Git  
5. Using a Google account that does not own the blog/channel  

---

## 튜토리얼 요약 (한국어)

1. 저장소 클론 → `./setup.sh`  
2. Google Cloud에서 YouTube + Blogger API 활성화 → `client_secrets.json`  
3. `python3 pipeline.py --setup`  
4. 첫 글: `python3 pipeline.py --post 1 --blog-only`  
5. 영상 포함: `post-1.mp4` 준비 후 `python3 pipeline.py --post 1`  
6. 홍보: `ads/` 폴더의 한국어 원고 사용 (Blogger / 네이버 / 티스토리)  

더 자세한 명령어는 [MANUAL.md](MANUAL.md), 最短 경로는 [QUICKSTART.md](QUICKSTART.md) 를 보세요.
