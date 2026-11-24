#!/bin/bash
# Serves the game builds for tools/promo/capture.js at http://127.0.0.1:8765
#   app6.html   = the app build (app/game/index.html: full screen, shop v2, newest look)  <- default for promo
#   index6.html = the website build (index.html)
set -e
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
SITE=/tmp/promo_site
mkdir -p "$SITE"
cp "$REPO/app/game/index.html" "$SITE/app6.html"
cp "$REPO/index.html" "$SITE/index6.html"
ln -sfn "$REPO/audio" "$SITE/audio"
ln -sfn "$REPO/ph" "$SITE/ph"
cp "$REPO/events.json" "$SITE/" 2>/dev/null || true
if ! curl -s -o /dev/null --max-time 2 http://127.0.0.1:8765/app6.html; then
  (cd "$SITE" && setsid nohup python3 -m http.server 8765 --bind 127.0.0.1 > /tmp/promo_http.log 2>&1 < /dev/null &)
  sleep 1
fi
echo "game builds on http://127.0.0.1:8765 (from $SITE)"
