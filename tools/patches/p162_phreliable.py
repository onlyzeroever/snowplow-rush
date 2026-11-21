# Audit Nov 21: analytics lost events. Two new players on Nov 20 (18:03/18:04 London) reached PostHog only as a single
# "app_hidden" each, though their session recordings arrived: a batch was taken out of the queue before it was sent,
# and a failed send was never retried. Now:
#  - a batch leaves the queue only when PostHog confirms it; a failed send goes back into the queue (after 5 failures in
#    a row, at most one try a minute);
#  - when the page hides: a keepalive post, not a beacon (a beacon can't say whether it arrived); if the page is closed
#    before the answer, the batch stays saved and goes again on the next launch; offline, everything waits;
#  - anything unconfirmed is kept in localStorage (sr.phq, last 300) and sent on the next launch; every event carries a
#    uuid so PostHog can drop a copy that arrives twice;
#  - the first send goes 3 s after launch instead of 15 s, so short visits still arrive;
#  - session ids are UUIDv7 and the recorder starts with ours, so a visit stays one session when the recorder loads;
#  - job_end also says which render scale the phone drew at (ks, from p161).
# Held until Alex OKs it (it changes how analytics sends, not what it collects, apart from ks).
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("function track(ev,props){try{if(!phOn())return;",
    "function uuid7(){let h='';try{const r=crypto.getRandomValues(new Uint8Array(10));for(const x of r)h+=x.toString(16).padStart(2,'0');}catch(e){for(let i=0;i<20;i++)h+=Math.floor(Math.random()*16).toString(16);}\n"
    "  const t=Date.now().toString(16).padStart(12,'0');return t.slice(0,8)+'-'+t.slice(8,12)+'-7'+h.slice(0,3)+'-'+(8|(parseInt(h[3],16)&3)).toString(16)+h.slice(4,7)+'-'+h.slice(7,19);}\n"
    "function phSave(){try{if(!phOn()){localStorage.removeItem('sr.phq');return;}localStorage.setItem('sr.phq',JSON.stringify(PH.q.concat(PH.fly||[]).slice(-300)));}catch(e){}}\n"
    "try{if(phOn()){const old=JSON.parse(localStorage.getItem('sr.phq')||'[]');if(Array.isArray(old)&&old.length)PH.q.push(...old.slice(-300));}else localStorage.removeItem('sr.phq');}catch(e){}\n"
    "function track(ev,props){try{if(!phOn())return;")
rep("PH.q.push({event:ev,properties:p,timestamp:new Date().toISOString()});if(PH.q.length>=25)phFlush(false);}catch(e){}}",
    "PH.q.push({event:ev,properties:p,timestamp:new Date().toISOString(),uuid:uuid7()});if(PH.q.length>300)PH.q.splice(0,PH.q.length-300);phSave();if(PH.q.length>=25)phFlush(false);}catch(e){}}")
rep("({event:e.event,timestamp:e.timestamp,properties:Object.assign({token:PH.key},e.properties)})",
    "({event:e.event,timestamp:e.timestamp,uuid:e.uuid,properties:Object.assign({token:PH.key},e.properties)})")
a=s.find("function phFlush(final){if(!PH.q.length||!phOn()){if(!phOn())PH.q.length=0;return;}");b=s.find("function trackErr(msg,where){")
assert a>0 and b>a
NEW = """function phPostForm(batch,keep){const body=phForm(batch);if(!body)return Promise.resolve(true);
  return fetch(PH.host+'/e/?compression=base64',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body,keepalive:!!keep}).then(r=>r.ok);}
// a batch leaves the queue only when PostHog confirms it; failures go back in the queue. When the page hides, a keepalive
// post (a beacon can't say whether it arrived); a batch whose answer never comes stays saved and goes again next launch
function phFlush(final){if(!phOn()){PH.q.length=0;PH.fly=[];phSave();return;}if(!PH.q.length)return;
  if(final&&navigator.onLine===false){phSave();return;}
  const batch=PH.q.splice(0,final?40:50);PH.fly=(PH.fly||[]).concat(batch);phSave();
  const done=ok=>{PH.fly=(PH.fly||[]).filter(e=>batch.indexOf(e)<0);if(ok)PH.fails=0;else{PH.q.unshift(...batch);PH.fails=(PH.fails||0)+1;PH.failT=Date.now();}phSave();};
  if(final){phPostForm(batch,true).then(done,()=>done(false));if(PH.q.length)phFlush(true);return;}
  // JSON to /batch/ first; if the browser blocks it (CORS) or it fails, the simple form post that needs no preflight, and stick with it
  const form=()=>{PH.form=true;phPostForm(batch).then(done,()=>done(false));};if(PH.form){form();return;}
  try{fetch(PH.host+'/batch/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({api_key:PH.key,batch})}).then(r=>{if(!r.ok)throw new Error('http '+r.status);done(true);}).catch(form);}catch(e){form();}}
"""
s=s[:a]+NEW+s[b:]
rep("setInterval(()=>phFlush(false),15000);",
    "setInterval(()=>{if((PH.fails||0)>=5&&Date.now()-(PH.failT||0)<60000)return;phFlush(false);},15000);setTimeout(()=>phFlush(false),3000);")
rep("if(!PH.sid||now-PH.last>30*60e3)PH.sid=now.toString(36)+Math.random().toString(36).slice(2,8);",
    "if(!PH.sid||now-PH.last>30*60e3)PH.sid=uuid7();")
rep("bootstrap:{distinctID:PH_ID}", "bootstrap:{distinctID:PH_ID,sessionID:phSession()}")
rep("'job_end',Object.assign(phJob(),{combo_halved:", "'job_end',Object.assign(phJob(),{ks:typeof KS==='number'?KS:null,combo_halved:")
open(f,'w',encoding='utf-8').write(s)
print('p162 analytics: confirmed sends, retries, unsent events kept for the next launch, first send at 3 s')
