# Rightly Dividing the Word of Truth – KJV

**Study to shew thyself approved unto God… rightly dividing the word of truth.**  
— *2 Timothy 2:15 (KJV)*

A 12-week, **344-post** King James Bible study series on right division (dispensational truth), with automation for YouTube, Blogger, and GitHub Pages.

| Resource | Link |
|----------|------|
| **Study site** | https://henrynkoh.github.io/rightlydividingkjv/ |
| **Blog** | https://rightlydividingkjv.blogspot.com |
| **YouTube** | https://www.youtube.com/@ohhenry6524 |
| **Archive** | https://henrynkoh.github.io/rightlydividingkjv/archive-index.html |

---

## What this repo is

- **Content:** KJV Bible studies from foundations of right division through advanced application (12 weeks).
- **Publishing system:** Python pipeline that uploads video → embeds on Blogger → tracks IDs → updates GitHub Pages.
- **Operator tools:** HTML dashboards, publishing guide, weekly post pages, Threads copy.

This is both a **public study library** and a **content automation toolkit** for the channel `@ohhenry6524`.

---

## Documentation

| Doc | Purpose |
|-----|---------|
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | Get set up and publish your first post in ~15 minutes |
| [docs/TUTORIAL.md](docs/TUTORIAL.md) | Step-by-step walkthrough (video → blog → week) |
| [docs/MANUAL.md](docs/MANUAL.md) | Full operator manual (config, commands, troubleshooting) |
| [publishing-guide.html](publishing-guide.html) | Visual publishing workflow (open in browser) |
| [SETUP_YOUTUBE.md](SETUP_YOUTUBE.md) | YouTube OAuth setup (Korean) |

### Marketing / ads pack

Ready-to-post copy lives in [`ads/`](ads/):

- Facebook, Instagram, Threads  
- Blogger (English + Korean)  
- Naver Blog & Tistory (English + Korean)  
- WordPress, Newsletter, Email  

---

## Quick start

```bash
git clone https://github.com/henrynkoh/rightlydividingkjv.git
cd rightlydividingkjv
chmod +x setup.sh && ./setup.sh
```

Then:

```bash
cp config.template.json config.json   # if setup did not already
# Edit config.json (blog_id, repo_path, videos folder)
# Place client_secrets.json from Google Cloud Console

python3 pipeline.py --setup           # verify credentials
python3 pipeline.py --post 1          # publish post #1
```

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for the full path.

---

## Series overview (12 weeks)

| Week | Theme |
|------|--------|
| 1 | Foundations of Right Division |
| 2 | The Grace Age Defined |
| 3 | Israel, Law, and the Kingdom |
| 4 | Paul's Epistles – Our Instruction |
| 5 | Practical Right Division |
| 6 | Advanced Dispensational Truths |
| 7 | Common Doctrinal Pitfalls |
| 8 | Advanced Application & Maturity |
| 9–12 | Continued studies through “Finishing Strong” |

---

## Main commands

```bash
python3 pipeline.py --setup                 # verify Google / config
python3 pipeline.py --status                # completion status
python3 pipeline.py --post 141              # one post (needs post-141.mp4)
python3 pipeline.py --week 6                # full week
python3 pipeline.py --week 6 --blog-only    # Blogger only (no video)
python3 pipeline.py --all --blog-only       # all posts to Blogger
```

---

## Security note

Do **not** commit real credentials:

- `config.json`
- `client_secrets.json` / `client_secret.json`
- `token.json`, `token.pickle`, `token_blog.pickle`

Use `config.template.json` as the template. A `.gitignore` is included for these files.

---

## License / use

Scripture quotations are from the King James Version (public domain).  
Study content and tooling are provided for edification and free sharing of the Word. Please keep attribution when republishing.
