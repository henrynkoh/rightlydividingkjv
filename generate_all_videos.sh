#!/bin/bash
# =============================================================================
# generate_all_videos.sh – Create all slide videos for Weeks 5-12
# @ohhenry6524 | rightlydividingkjv.blogspot.com
#
# Generates post-113.mp4 through post-344.mp4 (232 videos)
# Each video is ~1:30 minutes, 1280x720, dark navy + gold style
# Estimated time: ~140 minutes total (~35 seconds/video)
#
# Usage:
#   chmod +x generate_all_videos.sh
#   ./generate_all_videos.sh           # all weeks 5-12
#   ./generate_all_videos.sh 5         # week 5 only (posts 113-140)
#   ./generate_all_videos.sh 6         # week 6 only (posts 141-168)
#   ./generate_all_videos.sh 7         # week 7 only (posts 169-196)
#   ./generate_all_videos.sh 8         # week 8 only (posts 197-232)
#   ./generate_all_videos.sh 9         # week 9 only (posts 233-260)
#   ./generate_all_videos.sh 10        # week 10 only (posts 261-288)
#   ./generate_all_videos.sh 11        # week 11 only (posts 289-312)
#   ./generate_all_videos.sh 12        # week 12 only (posts 313-344)
# =============================================================================

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()  { echo -e "${GREEN}✓${NC} $1"; }
err() { echo -e "${RED}✗${NC} $1"; }
inf() { echo -e "${YELLOW}→${NC} $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
PYTHON=python3
LOG="$SCRIPT_DIR/video_generation_$(date +%Y%m%d_%H%M%S).log"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   Rightly Dividing KJV – Video Generator               ║"
echo "║   @ohhenry6524 · 1280×720 · ~1:30/video               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Week ranges
WEEK5_START=113;  WEEK5_END=140
WEEK6_START=141;  WEEK6_END=168
WEEK7_START=169;  WEEK7_END=196
WEEK8_START=197;  WEEK8_END=232
WEEK9_START=233;  WEEK9_END=260
WEEK10_START=261; WEEK10_END=288
WEEK11_START=289; WEEK11_END=312
WEEK12_START=313; WEEK12_END=344

# Determine range based on argument
ARG="${1:-}"
case "$ARG" in
    5)  START=$WEEK5_START;  END=$WEEK5_END;  LABEL="Week 5" ;;
    6)  START=$WEEK6_START;  END=$WEEK6_END;  LABEL="Week 6" ;;
    7)  START=$WEEK7_START;  END=$WEEK7_END;  LABEL="Week 7" ;;
    8)  START=$WEEK8_START;  END=$WEEK8_END;  LABEL="Week 8" ;;
    9)  START=$WEEK9_START;  END=$WEEK9_END;  LABEL="Week 9" ;;
    10) START=$WEEK10_START; END=$WEEK10_END; LABEL="Week 10" ;;
    11) START=$WEEK11_START; END=$WEEK11_END; LABEL="Week 11" ;;
    12) START=$WEEK12_START; END=$WEEK12_END; LABEL="Week 12" ;;
    "")  START=$WEEK5_START;  END=$WEEK12_END; LABEL="Weeks 5-12" ;;
    *) echo "Usage: $0 [5|6|7|8|9|10|11|12]"; exit 1 ;;
esac

TOTAL=$((END - START + 1))
echo "  Target:  $LABEL (Posts $START–$END, $TOTAL videos)"
echo "  Estimated time: ~$((TOTAL * 40 / 60)) minutes"
echo "  Log: $LOG"
echo ""

# Check prerequisites
if ! command -v python3 &>/dev/null; then
    err "python3 not found"; exit 1
fi
if ! command -v ffmpeg &>/dev/null; then
    err "ffmpeg not found. Install: brew install ffmpeg"; exit 1
fi
python3 -c "from PIL import Image" 2>/dev/null || {
    inf "Installing Pillow..."
    pip3 install Pillow --quiet
}

mkdir -p "$SCRIPT_DIR/videos"

# Generate loop
DONE=0; FAILED=0; SKIPPED=0
START_TIME=$(date +%s)

for N in $(seq $START $END); do
    MP4="$SCRIPT_DIR/videos/post-${N}.mp4"

    # Skip valid existing files
    if [ -f "$MP4" ] && [ $(stat -f%z "$MP4" 2>/dev/null || stat -c%s "$MP4" 2>/dev/null) -gt 10000 ]; then
        echo -e "  ${GREEN}✓${NC} post-${N}.mp4 already exists – skipping"
        SKIPPED=$((SKIPPED+1))
        continue
    fi

    # Generate
    echo -ne "  → Generating post-${N}.mp4 ... "
    if $PYTHON generate_videos.py --post $N >> "$LOG" 2>&1; then
        SZ=$(stat -f%z "$MP4" 2>/dev/null || stat -c%s "$MP4" 2>/dev/null || echo 0)
        echo -e "${GREEN}✓${NC} ($(( SZ / 1024 ))KB)"
        DONE=$((DONE+1))
    else
        echo -e "${RED}✗ FAILED${NC}"
        FAILED=$((FAILED+1))
    fi
done

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
MINS=$((ELAPSED / 60)); SECS=$((ELAPSED % 60))

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo -e "║  ${GREEN}DONE${NC}  ✓ ${DONE} generated  ✗ ${FAILED} failed  → ${SKIPPED} skipped    ║"
echo "║  Time: ${MINS}m ${SECS}s                                       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "  Videos in: $SCRIPT_DIR/videos/"
echo ""

if [ $DONE -gt 0 ]; then
    echo "  Next — upload to YouTube + publish to Blogger:"
    echo "    python3 pipeline.py --week 9"
    echo "    python3 pipeline.py --week 10"
    echo "    python3 pipeline.py --week 11"
    echo "    python3 pipeline.py --week 12"
    echo "  Or let daily_publish.py handle it automatically."
fi

if [ $FAILED -gt 0 ]; then
    echo ""
    echo "  Retry failed posts:"
    echo "    ./generate_all_videos.sh"
fi
