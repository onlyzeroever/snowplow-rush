# Lab only: the review=all lab save owns every machine and Wild Ride (to try the big three on small jobs);
# the plow size setting is NEW only now (the lab screen's SIZES button became a MACHINE switch in p150).
import sys
f=sys.argv[1];s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n==cnt,(a[:80],n)
    s=s.replace(a,b)
rep("loadSave();save.sess=(save.sess||0)+1;",
"""loadSave();save.sess=(save.sess||0)+1;
if(PROTO){delete save.labSize;if(SAVE_KEY==='snowplowRush.reviewAll'&&!save.labAll){save.tool=Math.max(save.tool|0,BASE_TOOLS-1);save.rides=Object.assign({},save.rides||{});for(let i=BASE_TOOLS;i<TOOLS.length;i++)save.rides[TOOLS[i].id]=true;save.labAll=1;persist();}}""")
open(f,'w').write(s)
