# Lighter session recording in the apps (agreed Nov 21): 1 in 4 new players, first visit only, up to 10 minutes,
# 1 frame a second, only on Wi-Fi, and never when the app says the player hasn't agreed (UK/EU consent card).
# The web version is unchanged (first 2 visits, 20 min, 2 fps). HELD: ships with the app versions.
# Native contract additions (APP_HANDOFF.md): SRNative.network = 'wifi' | 'cellular' | 'none' (a value or a function
# returning one, kept current by the app), SRNative.recordOK() = false when the player said no to analytics.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("function phRecStart(){try{if(!phOn()||DEV_MODE||REVIEW_MODE||PH.rec||window.posthog)return;const n=save.phRec||0;if(n>=2)return;",
    "function recApp(){const N=window.SRNative;return !!(N&&N.platform&&N.platform!=='web');}\n"
    "function recAppOK(){if(!recApp())return true;const N=window.SRNative;if(save.recDraw==null){save.recDraw=Math.random()<0.25;persist();}\n"
    "  if(!save.recDraw||(save.phRec||0)>=1)return false;let net;try{net=typeof N.network==='function'?N.network():N.network;}catch(e){}if(net!=='wifi')return false;\n"
    "  try{if(typeof N.recordOK==='function'&&N.recordOK()===false)return false;}catch(e){}return true;}\n"
    "function phRecStart(){try{if(!phOn()||DEV_MODE||REVIEW_MODE||PH.rec||window.posthog)return;if(!recAppOK())return;const APP=recApp(),n=save.phRec||0;if(n>=2)return;")
rep("captureCanvas:{recordCanvas:true,canvasFps:2,canvasQuality:'0.4'}","captureCanvas:{recordCanvas:true,canvasFps:APP?1:2,canvasQuality:'0.4'}")
rep("setTimeout(()=>{try{p.stopSessionRecording();}catch(e){}},20*60e3);","setTimeout(()=>{try{p.stopSessionRecording();}catch(e){}},(APP?10:20)*60e3);")
open(f,'w',encoding='utf-8').write(s)
print('p171 app recordings: 1 in 4 new players, first visit, 10 min, 1 fps, Wi-Fi only, consent (held)')
