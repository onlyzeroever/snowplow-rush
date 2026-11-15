import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)
# Alignment pass 1 (Nov 16):
#  - Streak row: each day box now shows a gem icon above the number (they're the gems you get that day), numbers
#    are centred exactly in their boxes, and the STREAK / DAYS label is centred on the boxes.
#  - Upgrades: the five cards are evenly spaced (the extra gap before SNOW VALUE looked like a mistake).
rep("function drawStreakRow(y){","function ctext(s,x,w,y,col,o){text(b,s,x+Math.floor((w-textW(s))/2),y,col,o);}\nfunction drawStreakRow(y){")
rep("text(b,'STREAK',18,y+2,'#9fc0e8',{outline:null});text(b,sn+(sn===1?' DAY':' DAYS'),18,y+10,sn?'#ffd23f':'#6a7896',{outline:null});",
    "text(b,'STREAK',18,y+1,'#9fc0e8',{outline:null});text(b,sn+(sn===1?' DAY':' DAYS'),18,y+8,sn?'#ffd23f':'#6a7896',{outline:null});")
rep("text(b,''+STREAK_GEMS[i],x+Math.floor(w/2)+1,yy+Math.floor(w/2)-2,on?'#13306b':big?'#ffd23f':'#9fc0e8',{align:'center',outline:null});",
    "b.drawImage(SPR.gemS,x+Math.floor((w-5)/2),yy+1+(big?1:0));ctext(''+STREAK_GEMS[i],x,w,yy+7+(big?1:0),on?'#13306b':big?'#ffd23f':'#9fc0e8',{outline:null});")
rep("const y=44+i*47+(i>=3?4:0),x=4,w=172,h=44;","const y=45+i*48,x=4,w=172,h=44;")
open(f,'w',encoding='utf-8').write(s)
print('p93 align 1')
