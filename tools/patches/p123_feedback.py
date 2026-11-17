import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Analytics and feedback (Alex, Nov 17; plan doc decision 8).
# 1. first_tap: sent on the first touch, click or key of each page load. Link previews and screenshot bots load the game
#    but never touch it, so the dashboard counts players from their first tap.
rep("cv.addEventListener('pointerdown',e=>{e.preventDefault();audioInit();",
    "cv.addEventListener('pointerdown',e=>{e.preventDefault();audioInit();phTap('touch');")
rep("window.addEventListener('keydown',e=>{keys[e.key]=true;",
    "window.addEventListener('keydown',e=>{if(e.target&&/^(TEXTAREA|INPUT)$/.test(e.target.tagName))return;phTap('key');keys[e.key]=true;")
rep("function phOn(){",
    "let phTapped=false;function phTap(how){if(phTapped)return;phTapped=true;track('first_tap',{how,screen:state,secs:Math.round(performance.now()/1000)});}\n"
    "function phOn(){")
# 2. Feedback: a text box (Settings > FEEDBACK, and a one-time ask after the 8th and 30th finished job). It sends a
#    'feedback' event with the text and where the player is in the game. It is an explicit send, so it goes even if
#    play-data sharing is off; test runs and bots never send.
rep("function phOn(){",
    "function phFeedback(text,from){if(TEST_MODE||PH_BOT||typeof fetch!=='function')return false;try{const t=TOOLS[useIdx()];\n"
    "  const ev={event:'feedback',timestamp:new Date().toISOString(),properties:{distinct_id:PH_ID,$session_id:phSession(),$lib:'snowplow-rush',$geoip_disable:true,build:DEV_MODE?'dev':REVIEW_MODE?'review':'live',v:'0.8.0',\n"
    "    text:String(text).slice(0,600),from,screen:state,machine:t?t.id:null,stars_total:totalStars(),winter:winterNo(),runs:save.fbRuns||0}};phSendForm([ev],true);return true;}catch(e){return false;}}\n"
    "function openFeedback(from){if(document.getElementById('fbx'))return;const d=document.createElement('div');d.id='fbx';\n"
    "  d.style.cssText='position:fixed;inset:0;background:rgba(11,24,56,0.85);display:flex;align-items:center;justify-content:center;z-index:50;padding:16px;box-sizing:border-box';\n"
    "  const bt='border:0;border-radius:5px;padding:10px 16px;font:700 15px system-ui,sans-serif;cursor:pointer';\n"
    "  d.innerHTML='<div style=\"background:#13306b;border:3px solid #ffd23f;border-radius:8px;padding:16px;width:min(100%,380px);font:15px/1.4 system-ui,sans-serif;color:#fff;box-sizing:border-box\">'+\n"
    "    '<div style=\"font-weight:800;font-size:18px;margin-bottom:4px\">'+(from==='settings'?'Send feedback':'Got a minute?')+'</div>'+\n"
    "    '<div style=\"color:#bcd4f2;margin-bottom:10px\">What do you love? What annoys you? Anything broken? Every note gets read.</div>'+\n"
    "    '<textarea id=\"fbt\" maxlength=\"600\" rows=\"5\" style=\"width:100%;box-sizing:border-box;border:0;border-radius:5px;padding:10px;font:16px system-ui,sans-serif;resize:none\" placeholder=\"Type here\"></textarea>'+\n"
    "    '<div style=\"color:#9fc0e8;font-size:12px;margin:8px 0 12px\">Sent anonymously with how far you have got. Please leave out your name and contact details.</div>'+\n"
    "    '<div style=\"display:flex;gap:10px;justify-content:flex-end\"><button id=\"fbc\" style=\"'+bt+';background:#2a4a8a;color:#fff\">'+(from==='settings'?'Cancel':'Not now')+'</button>'+\n"
    "    '<button id=\"fbs\" style=\"'+bt+';background:#ffb020;color:#13306b\">Send</button></div></div>';\n"
    "  document.body.appendChild(d);const ta=d.querySelector('#fbt'),close=()=>{d.remove();};setTimeout(()=>{try{ta.focus();}catch(e){}},50);\n"
    "  d.querySelector('#fbc').onclick=()=>{close();sfx('click');};\n"
    "  d.querySelector('#fbs').onclick=()=>{const t=ta.value.trim();if(!t){ta.focus();return;}const ok=phFeedback(t,from);close();sfx('buy');showToast(ok?'THANKS! SENT':'COULD NOT SEND','#ffd23f');};}\n"
    "function phOn(){")
rep("  if(!(confirmReset>0)){R(b,24,203,132,1,'#2a4a8a');}",
    "  if(!(confirmReset>0)){R(b,24,203,132,1,'#2a4a8a');}button('fbk',24,226,64,18,'blue','FEEDBACK',()=>{sfx('click');openFeedback('settings');});")
rep("  button('close',54,234,72,18,'orange','DONE',()=>{settingsOpen=false;sfx('click');});}",
    "  button('close',92,226,64,18,'orange','DONE',()=>{settingsOpen=false;sfx('click');});}")
# count finished jobs and ask once after the 8th and once after the 30th, when back on the map with nothing else open
rep("function endRound(allClear){\n","function endRound(allClear){\n  if(!run.challenge)save.fbRuns=(save.fbRuns||0)+1;\n")
rep("function goMap(){ensureDaily();state='map';",
    "function goMap(){if(!TEST_MODE){const n=save.fbRuns||0,k=n>=30&&!save.fbAsk2?2:n>=8&&!save.fbAsk1?1:0;if(k){save['fbAsk'+k]=true;if(k===2)save.fbAsk1=true;persist();setTimeout(()=>{if(state==='map'&&!overlayOpen())openFeedback('ask'+(k===1?8:30));},900);}}\n"
    "  ensureDaily();state='map';")
open(f,'w',encoding='utf-8').write(s)
print('p123 first_tap event, feedback box (Settings + asks after 8 and 30 jobs)')
