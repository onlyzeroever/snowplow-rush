import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:80],s.count(a));s=s.replace(a,b_)
# A tester's phone refused to start audio ("Failed to start the audio device"); resume() returns a promise, so the
# try/catch around it never caught the rejection, and every tap logged an error. Swallow it; the next tap retries.
rep("function audioInit(){if(AC){if(AC.state==='suspended')AC.resume();return;}",
    "function audioInit(){if(AC){if(AC.state==='suspended')Promise.resolve(AC.resume()).catch(()=>{});return;}")
rep("if(AC)try{AC.suspend();}catch(e){}}else if(AC)try{AC.resume();}catch(e){}}",
    "if(AC)try{Promise.resolve(AC.suspend()).catch(()=>{});}catch(e){}}else if(AC)try{Promise.resolve(AC.resume()).catch(()=>{});}catch(e){}}")
open(f,'w',encoding='utf-8').write(s)
print('p111 audio resume errors caught')
