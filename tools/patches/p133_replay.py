import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# First-session recordings and the fun question (Alex, Nov 18: "I'm good with the analytics").
# 1. A new player's first two sessions are recorded with PostHog session replay (the game canvas at 2 fps, quality 0.4),
#    using PostHog's own library, self-hosted at /ph/ and loaded 1.5 s after start, only for those two sessions.
#    The canvas is drawn at 3x (not up to 8x) while recording, to keep frames small; CSS keeps it crisp.
#    Our own events use the recording's session id, so events and replays line up. Recording stops after 20 minutes,
#    and turning SHARE PLAY DATA off stops it. Dev, review and bot sessions are never recorded.
# 2. A one-tap question: "How fun is it so far? 1-5" after the 5th finished job, and once on a later day.
# 3. The privacy card says first plays may be recorded, anonymously.
rep("rideVia:null};","rideVia:null,rec:null};")
rep("KS=Math.max(1,Math.min(8,Math.ceil(cs*dpr)));","KS=Math.max(1,Math.min(window.SR_KS||8,Math.ceil(cs*dpr)));")
rep("function phSession(){const now=Date.now();",
    "function phSession(){try{if(PH.rec&&PH.rec.get_session_id){const s=PH.rec.get_session_id();if(s){PH.last=Date.now();return s;}}}catch(e){}const now=Date.now();")
rep("track('session_start',{returning:!!save.tut,",
    "function phRecStart(){try{if(!phOn()||DEV_MODE||REVIEW_MODE||PH.rec||window.posthog)return;const n=save.phRec||0;if(n>=2)return;save.phRec=n+1;persist();\n"
    "  window.SR_KS=3;resize();const sc=document.createElement('script');sc.src='/ph/posthog-1.450.1.js';sc.async=true;\n"
    "  sc.onload=()=>{try{window.posthog.init(PH.key,{api_host:PH.host,ui_host:'https://us.posthog.com',autocapture:false,capture_pageview:false,capture_pageleave:false,capture_dead_clicks:false,rageclick:false,\n"
    "    disable_surveys:true,enable_heatmaps:false,capture_performance:false,capture_exceptions:false,person_profiles:'identified_only',persistence:'localStorage',bootstrap:{distinctID:PH_ID},\n"
    "    disable_session_recording:false,session_recording:{maskAllInputs:true,captureCanvas:{recordCanvas:true,canvasFps:2,canvasQuality:'0.4'}},\n"
    "    loaded:p=>{PH.rec=p;try{p.register({build:'live',v:'0.8.0',rec_n:n+1});}catch(e){}setTimeout(()=>{try{p.stopSessionRecording();}catch(e){}},20*60e3);}});}catch(e){}};\n"
    "  sc.onerror=()=>{window.SR_KS=0;resize();};document.head.appendChild(sc);}catch(e){}}\n"
    "setTimeout(phRecStart,1500);\n"
    "track('session_start',{returning:!!save.tut,rec:(save.phRec||0)<2&&!DEV_MODE&&!REVIEW_MODE,")
rep("else{track('analytics_off');phFlush(true);save.noTrack=true;}",
    "else{track('analytics_off');phFlush(true);save.noTrack=true;try{if(PH.rec)PH.rec.stopSessionRecording();}catch(e){}}")
# privacy card wording
rep("text(b,'IT HELPS US MAKE THE GAME BETTER,',W/2,y+26,'#9fc0e8',{align:'center',outline:null});text(b,'AND WE NEVER SELL IT.',W/2,y+34,'#9fc0e8',{align:'center',outline:null});",
    "text(b,'WE MAY RECORD YOUR FIRST PLAYS,',W/2,y+26,'#9fc0e8',{align:'center',outline:null});text(b,'ANONYMOUSLY. WE NEVER SELL IT.',W/2,y+34,'#9fc0e8',{align:'center',outline:null});")
# the fun question
rep("function openShop(){shopOpen=true;sfx('click');}",
    "function funAskDue(){if(TEST_MODE&&!save.funTest)return false;if(!save.privSeen)return false;const today=new Date().toDateString();if(!save.day0){save.day0=today;persist();}\n"
    "  if(!save.funAsk1&&(save.fbRuns||0)>=5)return 'job5';if(save.funAsk1&&!save.funAsk2&&save.day0!==today)return 'day2';return false;}\n"
    "let funT=0;function drawFunCard(dt,ask){funT=Math.min(1,funT+(dt||0.016)*3.5);const e=1-Math.pow(1-funT,3),x=6,w=W-12,h=60,y=Math.round(NAV_Y-h-6+(1-e)*70);\n"
    "  btn('funbg',x,y,w,h,()=>{});panel(x,y,w,h,'#13306b','#ffd23f');b.drawImage(SPR.frost,x+6,y+5);text(b,'QUICK QUESTION',x+18,y+6,'#ffd23f',{outline:null});\n"
    "  text(b,ask==='day2'?'HOW FUN IS IT, NOW YOU\\'RE BACK?':'HOW FUN IS SNOWPLOW RUSH SO FAR?',W/2,y+17,'#ffffff',{align:'center',outline:null});\n"
    "  const done=(score)=>{save[ask==='day2'?'funAsk2':'funAsk1']=true;if(ask==='day2')save.funAsk1=true;funT=0;track('fun_rating',{score,ask,runs:save.fbRuns||0});persist();sfx(score?'buy':'click');if(score)showToast('THANKS!','#ffd23f');};\n"
    "  for(let k=1;k<=5;k++)button('fun'+k,x+12+(k-1)*28,y+29,24,14,k>=4?'green':k===3?'blue':'navy',String(k),()=>done(k));\n"
    "  text(b,'NOT FUN',x+12,y+46,'#9fc0e8',{outline:null});text(b,'LOVE IT',x+w-12,y+46,'#9fc0e8',{align:'right',outline:null});button('fun0',x+w/2-18,y+46,36,10,'navy','SKIP',()=>done(0));}\n"
    "function openShop(){shopOpen=true;sfx('click');}")
rep("if(state==='map'&&!overlayOpen()&&!save.privSeen)drawPrivacyCard(dtD);",
    "if(state==='map'&&!overlayOpen()&&!save.privSeen)drawPrivacyCard(dtD);\n  else if(state==='map'&&!overlayOpen()){const fa=funAskDue();if(fa)drawFunCard(dtD,fa);}")
open(f,'w',encoding='utf-8').write(s)
print('p133 first-session recordings (PostHog replay, canvas 2 fps), fun question after job 5 and on day 2, privacy wording')
