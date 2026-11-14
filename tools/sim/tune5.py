import econ5 as e, itertools, copy
def go(costs, vg=1.62, cf=0.06, cg=1.45, show=False, **kw):
    cfg=copy.deepcopy(e.CFG);cfg.update(effFirst=0.45,effGain=0.03,effMax=0.62,costFrac=cf,costGrowth=cg,costs=costs);cfg['value']['growth']=vg;cfg.update(kw)
    res=e.run(cfg)
    ev={x[1]:x[0] for x in res['events'] if x[1].startswith('MACHINE') or x[1].startswith('TOLL')}
    f=res['first']
    def done(a): return max(f[j['id']].get('firstStar',9999) for j in e.JOBS if j['area']==a and j['id'] in f)
    # upgrade level of each machine when the next one was bought
    lvl={};prev=None
    for l in res['log']:
        if prev and l['m']!=prev['m']: lvl[prev['m']]=(prev['lv']['speed'],prev['lv']['size'])
        prev=l
    out=dict(p=ev.get('MACHINE pusher'),b=ev.get('MACHINE blower'),t=ev.get('MACHINE tractor'),tr=ev.get('MACHINE truck'),s=ev.get('MACHINE super'),
             ret=ev.get('TOLL retreat'),sta=ev.get('TOLL stadium'),sub=done('suburbs'),farm=done('farm'),city=done('city'),runs=len(res['log']),lvl=lvl)
    if show: e.report(res,cfg)
    return out,res
if __name__=='__main__':
    base={'pusher':610,'blower':3000,'tractor':18000,'truck':82000,'super':680000}
    for vg in (1.62,1.72,1.8):
      for bl,tr in ((3000,18000),(6000,30000),(8000,45000),(10000,60000)):
        c=dict(base,blower=bl,tractor=tr)
        o,_=go(c,vg=vg);print(vg,bl,tr,o)
