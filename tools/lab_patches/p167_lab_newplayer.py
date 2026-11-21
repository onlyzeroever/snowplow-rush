# Test links for Alex (Nov 21): play the start of the game exactly as a brand-new player would, as often as needed.
#   lab.snowplowrush.app/?newplayer           the first-job pack (p164)
#   lab.snowplowrush.app/?newplayer&oldftue   the same start as the live game, to compare
# Its own save slot, wiped every time the link is opened (kept on a reload, so a refresh mid-job loses nothing), and no
# weekend event, so Blizzard Weekend doesn't change the first jobs while they are being judged.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("const SAVE_KEY=DEV_MODE?'snowplowRush.dev':",
    "const NEWP=/[?&]newplayer/.test(location.search);\n"
    "if(NEWP){try{const nav=performance.getEntriesByType('navigation')[0];if(!nav||nav.type!=='reload'){localStorage.removeItem('snowplowRush.newplayer');localStorage.removeItem('snowplowRush.newplayer.bak');}}catch(e){}}\n"
    "const SAVE_KEY=NEWP?'snowplowRush.newplayer':DEV_MODE?'snowplowRush.dev':")
rep("(function evLoad(){const q=new URLSearchParams(location.search).get('event');",
    "(function evLoad(){if(NEWP)return;const q=new URLSearchParams(location.search).get('event');")
open(f,'w',encoding='utf-8').write(s)
print('p167 lab: ?newplayer test links (fresh save each open, no event; &oldftue for the live start)')
