import json,glob,random,math,sys
KEEP=0.75;MAX=20;CRACK=float(sys.argv[1]) if len(sys.argv)>1 else 3.0
runs=[]
for f in sorted(glob.glob('/tmp/cmb/*.json')):
    d=json.load(open(f))
    if d['res']['pct']<18: continue
    runs.append(d)
def replay(d,rule,rate,seed):
    rnd=random.Random(seed);combo=0;prog=0;T=0;cr=0;stun=0;tot=0;w=0;peak=0;t=0;hits=0;maxed=0;ends={'bonk':0,'decay':0}
    for e in d['log']:
        if e[0]=='H': continue  # bot's own hits replaced by synthetic ones at human rates
        dt,got,cnt,fresh=e
        t+=dt
        if rnd.random()<rate*dt and stun<=0:
            hits+=1;st=0.45;stun=st
            if combo>=2: pass
            if rule=='reset' or (rule=='two' and cr>0):
                if combo>=2: ends['bonk']+=1
                combo=0;prog=0;cr=0
            elif rule in('halve','two','halve0'):
                combo=combo//2;prog=0
                if rule!='halve0':T=max(T,KEEP+st)
                if rule=='two':cr=CRACK
        if stun>0: stun-=dt;got=0;cnt=0
        if cr>0: cr-=dt
        m=1+0.1*combo;tot+=got*m;w+=got
        if got>0 and cnt>0:
            if fresh>=2:T=KEEP
            prog+=cnt
            while prog>=d['step']:
                prog-=d['step']
                if combo<MAX:
                    combo+=1
                    if combo==MAX:maxed+=1
        T-=dt
        if T<=0 and combo>0:
            if combo>=2: ends['decay']+=1
            combo=0;prog=0
        peak=max(peak,combo)
    return tot/max(w,1),peak,maxed,hits,ends,t
for rate in (0.0,0.06,0.1,0.2):
    print('hits/s',rate,'(~%d per 80s run)'%round(rate*80))
    for rule in ('reset','halve0','halve','two'):
        M=[];P=[];X=0;H=0;E={'bonk':0,'decay':0};n=0
        for d in runs:
            for s in range(30):
                m,p,mx,h,e,t=replay(d,rule,rate,s);M.append(m);P.append(p);X+=mx>0;H+=h;n+=1
                for k in E:E[k]+=e[k]
        print('  %-7s mult %.3f  peak %.1f  reached x3.0 in %2d%% of runs  combo ends: bonk %d decay %d'%(rule,sum(M)/len(M),sum(P)/len(P),100*X/n,E['bonk'],E['decay']))
print('runs used',[(d['id'],d['res']['pct']) for d in runs])
