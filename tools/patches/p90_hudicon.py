import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# UI pass 2: the in-job SPEED button shows a mini speedometer (matching the new Upgrades icon) instead of a boot.
rows=["...KKKKK...",".KKQQYRRKK.",".KQWWWWWRK.","KQWWWWWKWRK","KQWWWWKWWRK","KWWWWKKWWWK","KKKKKKKKKKK"]
for r in rows: assert len(r)==11
old='SPR.boot=spr(["...KKKK...","...KTTK...","...KTTK...","..KKTTKKK.",".KTTTTTTTK","KTTTTTTTTK","KKKKKKKKKK"]);'
assert s.count(old)==1
s=s.replace(old,'SPR.boot=spr('+repr(rows).replace("'",'"')+",{Q:'#33b24a',Y:'#ffc727',R:'#e03a4e',W:'#f4f8ff'});")
open(f,'w',encoding='utf-8').write(s)
print('p90 hud speed icon')
