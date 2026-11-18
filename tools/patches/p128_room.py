import sys,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
def blob(name):
    i=s.index('const '+name+'=')+len('const '+name+'=');o,e=json.JSONDecoder().raw_decode(s,i);assert json.dumps(o,separators=(',',':'),ensure_ascii=False)==s[i:e];return o,i,e
def put(o,i,e):
    global s;s=s[:i]+json.dumps(o,separators=(',',':'),ensure_ascii=False)+s[e:]
def mv(props,idx,pid,old,new):
    p=props[idx];assert p[0]==pid and p[1:3]==old,(pid,idx,p);p[1],p[2]=new
# Big machines in early jobs (bumps data, Nov 18: the Plow Truck bumps ~3x as often as the Blower in Suburbs jobs).
# 1. Corner help scales with the machine: when you clip the corner of a prop while driving straight, the game slides you
#    round it if the way is clear. It used to allow 5px for every machine; now about 3/4 of the body's half-width
#    (Plow Truck 8, Super Plow/Loader 9, Rotary 10, Icebreaker 11; kid tools stay at 5). It never lets you through a gap
#    you don't fit: it only nudges you round corners.
rep("const slide=(ax,mv)=>{const N=5,sp=Math.abs(mv);","const slide=(ax,mv)=>{const N=Math.max(5,Math.round(((VSPEC[tid]||{}).hw||6)*0.75)),sp=Math.abs(mv);")
# 2. Allotments: the four pairs of vegetable beds had 20px between them, exactly a big machine's width side-on.
#    The lower bed of each pair moves down 16px (36px gaps: room for every machine side-on), with the barrels below them.
sub,si,se=blob('SUB_DATA')
al=sub['allotments']['props']
mv(al,1,'plot',[6,82],[6,98]);mv(al,2,'barrel',[64,102],[64,105])
mv(al,8,'plot',[6,282],[6,298]);mv(al,9,'plot',[44,282],[44,298])
mv(al,31,'plot',[110,282],[110,298]);mv(al,32,'barrel',[110,302],[110,305])
mv(al,34,'plot',[110,382],[110,398]);mv(al,35,'barrel',[110,402],[110,405])
mv(al,20,'plot',[6,582],[6,598]);mv(al,21,'barrel',[64,602],[64,605])
mv(al,41,'plot',[110,582],[110,598]);mv(al,42,'plot',[148,582],[148,598])
# and the single beds under the sheds and greenhouses (18-24px gaps) get the same room. Barrels tuck in against
# their beds, and the signpost moves down off the top edge, so no gap is only just wide enough for a big machine.
mv(al,5,'plot',[6,188],[6,206]);mv(al,29,'plot',[110,188],[110,206]);mv(al,18,'plot',[6,488],[6,506]);mv(al,38,'plot',[110,488],[110,506])
mv(al,51,'signpost',[106,8],[106,14])
put(sub,si,se)
# 3. Gardens: the hedges sat 30px from the houses and the swing, a gap the Rotary and Icebreaker only just fit.
#    Hedges down 6px, swing and hot tub down 12px and 6px, one gnome up 10px: every gap is now 35px or more, or closed.
rep("[[0,90,62,10],[118,90,62,10],[0,200,50,10]","[[0,96,62,10],[118,96,62,10],[0,200,50,10]")
rep("ob(swingSprite(),44,130,0,0,26,14);ob(SPR.gnome,64,166,1,8,7,5);ob(SPR.gnome,120,250,1,8,7,5);","ob(swingSprite(),44,142,0,0,26,14);ob(SPR.gnome,64,166,1,8,7,5);ob(SPR.gnome,120,240,1,8,7,5);")
rep("ob(tubSprite(),120,136,1,1,14,14);","ob(tubSprite(),120,142,1,1,14,14);")
open(f,'w',encoding='utf-8').write(s)
print('p128 corner help scales with the machine; Allotments and Gardens opened up')
