# Alex, Nov 21 00:34: "it spawned me at the bottom facing down to the bottom wall" -> a machine starts facing into
# the map (up when its start is in the lower half), the same forward direction start146.js already checks.
# "the audio isn't working for me at all, even when I have it turned on": iPhone Safari can leave the audio
# 'interrupted' after you switch apps; the next tap now resumes it whatever state it is in (was: only 'suspended').
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("P={x:G.start.x,y:G.start.y,f:2,","P={x:G.start.x,y:G.start.y,f:G.start.y>G.ph*0.5?0:2,")
rep("function audioInit(){if(AC){if(AC.state==='suspended')Promise.resolve(AC.resume()).catch(()=>{});return;}",
    "function audioInit(){if(AC){if(AC.state!=='running')Promise.resolve(AC.resume()).catch(()=>{});return;}")
open(f,'w',encoding='utf-8').write(s)
print('p149 start facing into the map, audio resumes from any state')
