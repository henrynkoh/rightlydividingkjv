#!/bin/bash
# =============================================================================
# setup.sh – One-Time Setup for "Rightly Dividing KJV" Automation Pipeline
# @ohhenry6524 | rightlydividingkjv.blogspot.com
# =============================================================================
# Run this ONCE before using pipeline.py:
#   chmod +x setup.sh && ./setup.sh
# =============================================================================

set -e

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()  { echo -e "${GREEN}✓${NC} $1"; }
err() { echo -e "${RED}✗${NC} $1"; }
inf() { echo -e "${YELLOW}→${NC} $1"; }
hdr() { echo -e "\n${CYAN}══ $1 ══${NC}"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   Rightly Dividing KJV – Automation Setup               ║"
echo "║   @ohhenry6524 · 232 Posts · 4 Platforms                ║"
echo "╚══════════════════════════════════════════════════════════╝"

# ─── 1. CHECK PYTHON ──────────────────────────────────────────────────────────
hdr "1/7 Python Version"
if command -v python3 &>/dev/null; then
    PYVER=$(python3 --version 2>&1)
    ok "$PYVER"
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYVER=$(python --version 2>&1)
    ok "$PYVER"
    PYTHON=python
else
    err "Python not found. Install from https://python.org"
    exit 1
fi

# ─── 2. INSTALL PYTHON PACKAGES ───────────────────────────────────────────────
hdr "2/7 Install Python Packages"
if [ -f "requirements.txt" ]; then
    inf "Installing from requirements.txt..."
    $PYTHON -m pip install -r requirements.txt --break-system-packages --quiet 2>/dev/null || \
    $PYTHON -m pip install -r requirements.txt --quiet
    ok "Python packages installed"
else
    err "requirements.txt not found in $SCRIPT_DIR"
    exit 1
fi

# ─── 3. CHECK / CREATE config.json ────────────────────────────────────────────
hdr "3/7 Configuration"
if [ ! -f "config.json" ]; then
    if [ -f "config.template.json" ]; then
        cp config.template.json config.json
        inf "Created config.json from template"
        echo ""
        echo -e "${YELLOW}  ┌─────────────────────────────────────────────────────┐${NC}"
        echo -e "${YELLOW}  │  ACTION NEEDED: Edit config.json and fill in:       │${NC}"
        echo -e "${YELLOW}  │    • blogger.blog_id  (from blogger.com > Settings) │${NC}"
        echo -e "${YELLOW}  │    • github.repo_path (local clone of the repo)     │${NC}"
        echo -e "${YELLOW}  │    • videos.source_folder (where your .mp4s live)   │${NC}"
        echo -e "${YELLOW}  └─────────────────────────────────────────────────────┘${NC}"
        echo ""
        read -p "  Open config.json in editor now? [y/N]: " EDIT_CONFIG
        if [[ "$EDIT_CONFIG" =~ ^[Yy] ]]; then
            ${EDITOR:-nano} config.json
        fi
    else
        err "config.template.json not found"
        exit 1
    fi
else
    ok "config.json already exists"
fi

# ─── 4. GOOGLE CLOUD CONSOLE GUIDE ────────────────────────────────────────────
hdr "4/7 Google API Credentials"
if [ ! -f "client_secrets.json" ]; then
    echo ""
    echo "  You need a client_secrets.json from Google Cloud Console."
    echo "  This is a ONE-TIME step that takes ~5 minutes."
    echo ""
    echo "  Steps:"
    echo "  ① Go to: https://console.cloud.google.com"
    echo "  ② Create a new project (e.g., 'RightlyDividingKJV')"
    echo "  ③ Go to: APIs & Services → Library"
    echo "     Enable: 'YouTube Data API v3'"
    echo "     Enable: 'Blogger API v3'"
    echo "  ④ Go to: APIs & Services → OAuth consent screen"
    echo "     → External → Fill in app name, your email → Save"
    echo "     → Add scopes: .../auth/youtube.upload, .../auth/blogger"
    echo "     → Add test user: your Gmail address"
    echo "  ⑤ Go to: APIs & Services → Credentials"
    echo "     → Create Credentials → OAuth 2.0 Client ID → Desktop App"
    echo "     → Download JSON → RENAME to: client_secrets.json"
    echo "     → Copy to this folder: $SCRIPT_DIR"
    echo ""
    echo "  Press Enter when client_secrets.json is in place, or Ctrl+C to do it later."
    read -p "  " _
    if [ ! -f "client_secrets.json" ]; then
        inf "client_secrets.json still missing — you can add it later, then re-run setup."
    else
        ok "client_secrets.json found"
    fi
else
    ok "client_secrets.json found"
fi

# ─── 5. CLONE / VERIFY GITHUB REPO ────────────────────────────────────────────
hdr "5/7 GitHub Repository"
REPO_URL="https://github.com/henrynkoh/rightlydividingkjv"

if ! command -v git &>/dev/null; then
    err "Git not installed. Install from https://git-scm.com"
else
    ok "Git found: $(git --version)"
    echo ""
    echo "  If you have NOT cloned the repo yet, run:"
    echo -e "    ${CYAN}git clone $REPO_URL ~/rightlydividingkjv${NC}"
    echo ""
    echo "  Then set 'github.repo_path' in config.json to that path."
    read -p "  Clone it now? [y/N]: " DO_CLONE
    if [[ "$DO_CLONE" =~ ^[Yy] ]]; then
        CLONE_DIR="$HOME/rightlydividingkjv"
        if [ -d "$CLONE_DIR" ]; then
            inf "Already cloned at $CLONE_DIR"
        else
            git clone "$REPO_URL" "$CLONE_DIR"
            ok "Cloned to $CLONE_DIR"
        fi
        # Auto-update config.json with repo path
        if command -v python3 &>/dev/null; then
            python3 -c "
import json, sys
with open('config.json') as f: cfg = json.load(f)
cfg['github']['repo_path'] = '$CLONE_DIR'
with open('config.json', 'w') as f: json.dump(cfg, f, indent=2)
print('Updated config.json with repo_path: $CLONE_DIR')
"
        fi
    fi
fi

# ─── 6. COPY HTML FILES TO REPO ───────────────────────────────────────────────
hdr "6/7 Copy HTML Files to GitHub Repo"
REPO_PATH=$(python3 -c "import json; cfg=json.load(open('config.json')); print(cfg['github']['repo_path'])" 2>/dev/null || echo "")

if [ -n "$REPO_PATH" ] && [ -d "$REPO_PATH" ] && [ "$REPO_PATH" != "REPLACE_WITH_LOCAL_PATH_TO_REPO" ]; then
    HTML_FILES=(
        "index.html"
        "archive-index.html"
        "week5-posts.html"
        "week6-posts.html"
        "week7-posts.html"
        "week8-posts.html"
        "content-dashboard.html"
        "youtube-embed-map.html"
        "publishing-guide.html"
        "posts_data.json"
        "pipeline.py"
        "requirements.txt"
    )
    COPIED=0
    for f in "${HTML_FILES[@]}"; do
        if [ -f "$SCRIPT_DIR/$f" ]; then
            cp "$SCRIPT_DIR/$f" "$REPO_PATH/$f"
            ok "Copied $f → $REPO_PATH/"
            COPIED=$((COPIED+1))
        fi
    done
    if [ $COPIED -gt 0 ]; then
        echo ""
        inf "Pushing $COPIED files to GitHub Pages..."
        cd "$REPO_PATH"
        git add .
        git commit -m "Add Rightly Dividing KJV content system files" 2>/dev/null || inf "Nothing new to commit"
        git push origin main 2>/dev/null || git push origin master 2>/dev/null || err "Git push failed — check your remote"
        ok "GitHub Pages updated: https://henrynkoh.github.io/rightlydividingkjv/"
        cd "$SCRIPT_DIR"
    fi
else
    inf "Repo path not set or not found — skipping file copy"
    inf "Set 'github.repo_path' in config.json and re-run setup.sh"
fi

# ─── 7. VERIFY ────────────────────────────────────────────────────────────────
hdr "7/7 Final Verification"
cd "$SCRIPT_DIR"
if [ -f "client_secrets.json" ]; then
    $PYTHON pipeline.py --setup
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   SETUP COMPLETE – Ready to publish!                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "  Next steps:"
echo ""
echo -e "  1. Record a video → save as ${CYAN}post-141.mp4${NC} in your videos folder"
echo -e "  2. Run: ${CYAN}python3 pipeline.py --post 141${NC}"
echo -e "     → Uploads to YouTube, publishes to Blogger, updates GitHub"
echo ""
echo -e "  Or publish a whole week at once:"
echo -e "    ${CYAN}python3 pipeline.py --week 6${NC}"
echo ""
echo -e "  Or publish everything remaining:"
echo -e "    ${CYAN}python3 pipeline.py --all${NC}"
echo ""
echo "  See publishing-guide.html for the full workflow reference."
echo ""
