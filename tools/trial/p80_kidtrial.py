import sys,re,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# TRIAL ONLY (not in the build): player kid with hat highlights, a scarf in the hat-trim colour, coat light and shade.
def edit(name,changes):
    global s
    a=s.index('const '+name+'=[');b=s.index('];',a)
    rows=re.findall(r'"([^"]*)"',s[a:b])
    for i,r in changes.items(): assert len(r)==len(rows[i]),(name,i); rows[i]=r
    s=s[:a]+'const '+name+'=['+','.join('"'+r+'"' for r in rows)+s[b:]
edit('ROWS_DOWN',{1:".....KY1K.....",3:"...KY1YYYYK...",4:"..KY1YYYYY2K..",5:".KYYYYYYYYY2K.",12:".KyyyyyyyyyyK.",13:"KR1RRyyrRRR2RK",14:"KMR1RyyrRRR2MK",15:".KKRRRrRRR2KK."})
edit('ROWS_UP',{1:".....KY1K.....",3:"...KY1YYYYK...",4:"..KY1YYYYY2K..",5:".KYYYYYYYYY2K.",10:".KyyyyyyyyyyK.",11:"KR1rrrrrrrr2RK",12:"KR1RRRRRRRR2RK",13:"KMRRRRRRRRR2MK",14:"KMRRRRRRRRR2MK"})
edit('ROWS_SIDE',{1:".....KY1K.....",3:"...KY1YYYYK...",4:"..KY1YYYYYYK..",12:"...KyyyyyyK...",13:"..KyR1RRRRMMK.",14:"..KyrR1RRRMMK."})
a="const col=(over&&over[ch])||PAL[ch];"
assert s.count(a)==1
s=s.replace(a,"const col=(over&&over[ch])||PAL[ch]||({'1':'rgba(255,255,255,0.38)','2':'rgba(20,24,60,0.22)'})[ch];")
open(f,'w',encoding='utf-8').write(s)
