# Builds app.html for the lab site (lab.snowplowrush.app/app): the exact app build (app/game/index.html), so Alex can
# test what goes into the apps on his own phone before TestFlight exists. Two changes only:
#   - its analytics say build 'lab', so test play never counts as live play;
#   - it keeps its own save (snowplowRush.appPreview.*), so it never mixes with the lab game's save on the same site;
#   - /app?fresh wipes that save first, to play again as a brand-new player.
# Usage: python3 tools/make_app_preview.py app/game/index.html app.html
import sys
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit(f'make_app_preview: expected {n} of {a[:60]!r}, found {c}')
    s = s.replace(a, b)
rep("build:DEV_MODE?'dev':REVIEW_MODE?'review':'live'", "build:DEV_MODE?'dev':'lab'", 2)
rep("p.register({build:'live',", "p.register({build:'lab',")
i = s.index('const SAVE_KEY='); j = s.index(';', i)
line = s[i:j]
if line.count("'snowplowRush.") < 5: sys.exit('make_app_preview: save key line changed shape')
s = s[:i] + line.replace("'snowplowRush.", "'snowplowRush.appPreview.") + s[j:]
rep('<title>', '<title>APP PREVIEW | ')
fresh = ("<script>if(/[?&]fresh\\b/.test(location.search)){try{Object.keys(localStorage).filter(k=>k.indexOf('snowplowRush.appPreview.')===0)"
         ".forEach(k=>localStorage.removeItem(k));}catch(e){}history.replaceState(null,'',location.pathname);}</script>")
i = s.index('<script'); s = s[:i] + fresh + s[i:]
open(out, 'w', encoding='utf-8').write(s)
print('built', out)
