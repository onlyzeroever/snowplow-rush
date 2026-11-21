# App versions: fetch the weekend-event schedule from the website, not from the copy bundled inside the app, so
# events can be scheduled without an app update (APP_HANDOFF.md section 4). The site sends events.json with
# Access-Control-Allow-Origin: * (vercel.json). On the web nothing changes. HELD: ships with the app build.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("try{fetch('/events.json?d='+",
    "try{fetch((window.SRNative&&SRNative.platform&&SRNative.platform!=='web'?'https://snowplowrush.app':'')+'/events.json?d='+")
open(f,'w',encoding='utf-8').write(s)
print('p172 app: event schedule from snowplowrush.app')
