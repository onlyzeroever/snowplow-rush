import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Farmyard + Ranch: the right-hand fence line sat 32px from the edge (the left one 40px), a lane the Rotary and Icebreaker
# only just fit down. It moves 8px left to mirror the left side. The same fence segments are kept (hash on the old x).
rep("for(let y=200;y<ph-100;y+=200){for(const x of [40,136]){if(hash(x,y)%5===0)continue;for(const [a,c] of cutSegs(",
    "for(let y=200;y<ph-100;y+=200){for(const [hx,x] of [[40,40],[136,128]]){if(hash(hx,y)%5===0)continue;for(const [a,c] of cutSegs(")
open(f,'w',encoding='utf-8').write(s)
print('p129 Farmyard/Ranch right fence lane 40px')
