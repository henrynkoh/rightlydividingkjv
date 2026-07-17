#!/bin/bash
# =============================================================================
# batch_run.sh – Batch Publisher for Rightly Dividing KJV
# @ohhenry6524 | rightlydividingkjv.blogspot.com
#
# Publishes multiple posts in one session using pipeline.py
# Organizes your recording session into a full publish run
#
# Usage:
#   chmod +x batch_run.sh
#   ./batch_run.sh                        # interactive mode (asks what to run)
#   ./batch_run.sh --week 6              # all of week 6
#   ./batch_run.sh --posts 141 142 143   # specific posts
#   ./batch_run.sh --status              # show progress
#   ./batch_run.sh --dry-run --week 6    # preview week 6 without uploading
# =============================================================================

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()  { echo -e "${GREEN}✓${NC} $1"; }
err() { echo -e "${RED}✗${NC} $1"; }
inf() { echo -e "${YELLOW}→${NC} $1"; }
hdr() { echo -e "\n${CYAN}══ $1 ══${NC}"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
PYTHON=${PYTHON:-python3}
LOG_FILE="$SCRIPT_DIR/batch_$(date +%Y%m%d_%H%M%S).log"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   Rightly Dividing KJV – Batch Publisher                ║"
echo "║   @ohhenry6524 · $(date '+%Y-%m-%d %H:%M')                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ─── PARSE ARGS ───────────────────────────────────────────────────────────────
WEEK=""
POSTS_LIST=""
DRY_RUN=""
STATUS_ONLY=false
DELAY=15   # seconds between posts

while [[ $# -gt 0 ]]; do
    case "$1" in
        --week)    WEEK="$2"; shift 2 ;;
        --posts)   shift; POSTS_LIST="$@"; break ;;
        --dry-run) DRY_RUN="--dry-run"; shift ;;
        --status)  STATUS_ONLY=true; shift ;;
        --delay)   DELAY="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# ─── STATUS ───────────────────────────────────────────────────────────────────
if $STATUS_ONLY; then
    $PYTHON pipeline.py --status
    exit 0
fi

# ─── INTERACTIVE MODE ─────────────────────────────────────────────────────────
if [ -z "$WEEK" ] && [ -z "$POSTS_LIST" ]; then
    echo "  What would you like to publish?"
    echo ""
    echo "  [1] A single week (e.g., Week 6)"
    echo "  [2] Specific post numbers"
    echo "  [3] All unpublished posts"
    echo "  [4] Show status only"
    echo "  [5] Dry run (preview without uploading)"
    echo ""
    read -p "  Choice [1-5]: " CHOICE

    case "$CHOICE" in
        1)
            read -p "  Week number (1-8): " WEEK
            inf "Will publish all posts in Week $WEEK"
            ;;
        2)
            read -p "  Post numbers (space-separated, e.g. 141 142 143): " POSTS_LIST
            inf "Will publish posts: $POSTS_LIST"
            ;;
        3)
            ALL=true
            inf "Will publish all unpublished posts"
            ;;
        4)
            $PYTHON pipeline.py --status
            exit 0
            ;;
        5)
            DRY_RUN="--dry-run"
            read -p "  Week to preview (1-8): " WEEK
            ;;
        *)
            err "Invalid choice"
            exit 1
            ;;
    esac
fi

# ─── CONFIRM ──────────────────────────────────────────────────────────────────
echo ""
if [ -n "$DRY_RUN" ]; then
    echo -e "  Mode:   ${YELLOW}DRY RUN${NC} (no uploads)"
else
    echo -e "  Mode:   ${GREEN}LIVE${NC} (will upload to YouTube + Blogger + GitHub)"
fi
if [ -n "$WEEK" ]; then
    echo "  Target: Week $WEEK"
elif [ -n "$POSTS_LIST" ]; then
    echo "  Target: Posts $POSTS_LIST"
elif [ "$ALL" = true ]; then
    echo "  Target: All unpublished"
fi
echo "  Delay:  ${DELAY}s between posts"
echo "  Log:    $LOG_FILE"
echo ""

if [ -z "$DRY_RUN" ]; then
    read -p "  Start publishing? [y/N]: " CONFIRM
    if [[ ! "$CONFIRM" =~ ^[Yy] ]]; then
        inf "Cancelled."
        exit 0
    fi
fi

# ─── RUN ──────────────────────────────────────────────────────────────────────
START_TIME=$(date +%s)

run_cmd() {
    echo "$ $@" | tee -a "$LOG_FILE"
    "$@" 2>&1 | tee -a "$LOG_FILE"
    return ${PIPESTATUS[0]}
}

if [ -n "$WEEK" ]; then
    run_cmd $PYTHON pipeline.py --week "$WEEK" --delay "$DELAY" $DRY_RUN
elif [ -n "$POSTS_LIST" ]; then
    run_cmd $PYTHON pipeline.py --posts $POSTS_LIST --delay "$DELAY" $DRY_RUN
elif [ "$ALL" = true ]; then
    run_cmd $PYTHON pipeline.py --all --delay "$DELAY" $DRY_RUN
fi

STATUS=$?
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
MINS=$((ELAPSED / 60))
SECS=$((ELAPSED % 60))

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
if [ $STATUS -eq 0 ]; then
    echo -e "║   ${GREEN}BATCH COMPLETE${NC}                                          ║"
else
    echo -e "║   ${RED}BATCH FINISHED WITH ERRORS${NC}                              ║"
fi
echo "║   Time elapsed: ${MINS}m ${SECS}s                                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "  Log saved to: $LOG_FILE"
echo ""
echo "  Check status: ./batch_run.sh --status"
echo ""

# Show final status
$PYTHON pipeline.py --status

exit $STATUS
