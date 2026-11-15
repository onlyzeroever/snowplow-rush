import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# Economy calibration (Nov 15, after the late areas were rebuilt): the stadium road fee drops from 500,000 to 350,000.
# In the sim a player who spends on upgrades now reaches the stadium 18 runs sooner (run 74 instead of 92); a player
# who saves is barely affected (run 59 instead of 60), so it is softer without being free.
rep("from:['street','lot'],toll:500000,","from:['street','lot'],toll:350000,")
open(f,'w',encoding='utf-8').write(s)
