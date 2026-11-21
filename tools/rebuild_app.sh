set -e
# app build (Nov 21): every main patch, plus the held patches listed in scripts/patches/APP (store bridge, app hooks,
# prices, lighter recording, remote event schedule). Other held patches (e.g. p145 Blizzard deep snow) and the lab
# prototypes stay out. Output: proto/app6.html, committed as app/game/index.html for Claude Code on the Mac.
cd /home/claude/proto && cp game5.html gameapp.html && python3 /home/claude/scripts/patches/p1_levels.py gameapp.html >/dev/null && python3 /home/claude/scripts/patches/p2_map.py gameapp.html >/dev/null
HOLD=$(cat /home/claude/scripts/patches/HOLD 2>/dev/null || true); APP=$(cat /home/claude/scripts/patches/APP 2>/dev/null || true)
for f in $(ls /home/claude/scripts/patches/p*_*.py | sed -E 's#.*/p([0-9]+)_.*#\1 &#' | sort -n | awk '$1>=3{print $2}'); do
  b=$(basename "$f"); if echo "$HOLD" | grep -qx "$b" && ! echo "$APP" | grep -qx "$b"; then echo "not in the app: $b"; continue; fi; python3 "$f" gameapp.html >/dev/null; done
python3 /home/claude/scripts/build.py gameapp.html /home/claude/ref/logo_crop.png app6.html
