import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# Effects pass 1 (Nov 16): thrown snow is now chunky clumps (1-3 px) with a blue edge and a ground shadow, so the
# spray reads on white snow as well as on tarmac, instead of near-invisible white pixels.
old="default:R(b,px,py,p.z>3?2:1,p.z>3?2:1,'#ffffff');if(p.z>2)R(b,px,Math.round(p.y),1,1,'rgba(120,150,200,0.5)');"
assert s.count(old)==1
new=("default:{const sz=k>0.8?0:((Math.abs(p.vx*13+p.vy*7)|0)%3)+(p.z>3?0:-1);if(p.z>1)R(b,px,Math.round(p.y)+1,sz>1?2:1,1,'rgba(110,140,190,0.35)');"
     "if(sz>=2){R(b,px-1,py,3,1,'#c6d9f3');R(b,px,py-1,1,3,'#c6d9f3');R(b,px-1,py,2,1,'#ffffff');R(b,px,py-1,1,2,'#ffffff');R(b,px+1,py+1,1,1,'#8fb0dc');R(b,px,py+2,1,1,'#a6c2ea');}"
     "else if(sz===1){R(b,px,py,2,2,'#ffffff');R(b,px+1,py+1,1,1,'#a6c2ea');R(b,px,py+2,2,1,'rgba(143,176,220,0.6)');}"
     "else{R(b,px,py,1,1,'#ffffff');R(b,px+1,py,1,1,'#b8cff0');R(b,px,py+1,1,1,'#c6d9f3');}}")
s=s.replace(old,new)
open(f,'w',encoding='utf-8').write(s)
print('p88 fx: snow clumps')
