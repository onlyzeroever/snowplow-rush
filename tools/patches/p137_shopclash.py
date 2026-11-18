import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Alex, Nov 19: the new SHOP button sat under the helpers' "+9.1/S" badge (same row, right side).
# The badge moves up one row, just above the button row, still right-aligned and still tappable (goes home).
rep("bx=W-fw-6;panel(bx,by+3,fw,13,'#13306b','#4f8fdc');const hx=bx+4,hy=by+6;",
    "bx=W-fw-6;panel(bx,by-17,fw,13,'#13306b','#4f8fdc');const hx=bx+4,hy=by-14;")
rep("text(b,ft,bx+11+(fw-11)/2,by+7,'#9fd8ff',{align:'center',outline:null});btn('gohome',bx,by+1,fw,17,()=>{sfx('click');goHome();});}}",
    "text(b,ft,bx+11+(fw-11)/2,by-13,'#9fd8ff',{align:'center',outline:null});btn('gohome',bx,by-19,fw,17,()=>{sfx('click');goHome();});}}")
open(f,'w',encoding='utf-8').write(s)
print('p137 helpers badge moved above the button row so the SHOP button shows')
