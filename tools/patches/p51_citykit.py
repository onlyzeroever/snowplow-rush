import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# CITY KIT (City part 2): office towers, a museum front, platforms and trains, trams on a timetable,
# cross traffic at junctions (cars, and parade floats for the boss), and the city boss chaser: the parking warden.
# ---------------------------------------------------------------------------------------------
KIT=r"""
function officeSprite(w,h,a){const pal=[['#8793a8','#6a7896'],['#c6b49a','#a8967a'],['#9fb3c8','#7f93a8'],['#d8a07a','#b8805a'],['#6b7fa8','#4f5f8a']][a%5];const c=mk(w,h),g=c.getContext('2d');
  R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,pal[0]);R(g,1,1,2,h-2,pal[1]);R(g,w-3,1,2,h-2,pal[1]);R(g,0,0,w,4,PAL.W);R(g,2,4,w-4,1,'#c6d9f3');
  for(let y=8;y<h-14;y+=6)for(let x=5;x<w-6;x+=5){const lit=((x*7+y*13+a*5)%11)<4;R(g,x,y,3,4,lit?'#ffe9a8':'#2a3450');}
  R(g,Math.round(w/2)-6,h-12,12,12,K);R(g,Math.round(w/2)-5,h-11,10,11,'#8fd3ff');R(g,Math.round(w/2),h-11,1,11,K);return c;}
function museumSprite(){const c=mk(120,62),g=c.getContext('2d');for(let r=0;r<14;r++){const hw=Math.round(8+r*4);R(g,60-hw-1,r,hw*2+2,1,K);R(g,60-hw,r,hw*2,1,r<4?PAL.W:'#e8e0cc');}
  R(g,4,14,112,4,K);R(g,5,14,110,3,'#d6cdb4');text(g,'MUSEUM',60,7,'#7a4a2a',{align:'center',outline:null});
  for(let x=8;x<112;x+=13){R(g,x,18,7,36,K);R(g,x+1,18,5,35,'#f4f0e4');R(g,x+2,18,1,35,'#d6cdb4');}R(g,0,54,120,8,K);R(g,1,55,118,6,'#d6cdb4');R(g,1,55,118,1,PAL.W);R(g,52,40,16,14,K);R(g,53,41,14,13,'#3a2a20');return c;}
function trackSprite(h){const c=mk(22,h),g=c.getContext('2d');for(let y=0;y<h;y+=5){R(g,0,y,22,2,'#6b4a2c');}R(g,3,0,2,h,'#55607a');R(g,17,0,2,h,'#55607a');R(g,3,0,1,h,'#c6d0e0');R(g,17,0,1,h,'#c6d0e0');return c;}
function trainSprite(len,col){const c=mk(24,len),g=c.getContext('2d');for(let y=0;y<len;y+=34){const hh=Math.min(32,len-y);R(g,0,y,24,hh,K);R(g,1,y+1,22,hh-2,col);R(g,1,y+1,22,3,PAL.W);
    for(let yy=y+6;yy<y+hh-4;yy+=6){R(g,2,yy,3,4,'#8fd3ff');R(g,19,yy,3,4,'#8fd3ff');}R(g,8,y+5,8,hh-10,'#d6dee9');}R(g,4,0,16,3,'#ffd23f');return c;}
function flagSprite(a){const col=['#d8364b','#3f86d6','#33b24a','#ffc727'][a%4];const c=mk(12,30),g=c.getContext('2d');R(g,1,0,2,30,K);R(g,2,1,1,28,'#c6d0e0');R(g,3,2,9,7,K);R(g,3,3,8,5,col);R(g,3,3,8,1,PAL.W);R(g,0,27,4,3,K);return c;}
function foodTruckSprite(a){const col=['#ffc727','#e07a8a','#33b24a'][a%3];const c=mk(26,40),g=c.getContext('2d');R(g,0,0,26,38,K);R(g,1,1,24,36,col);R(g,1,1,24,3,PAL.W);R(g,3,6,20,8,'#8fd3ff');R(g,1,18,24,3,'#d8364b');for(let y=22;y<34;y+=4)R(g,3,y,20,2,'#f4f8ff');R(g,1,36,6,4,K);R(g,19,36,6,4,K);return c;}
function lanternSprite(w){const c=mk(w,10),g=c.getContext('2d');const sag=x=>Math.round(3*Math.sin(x/w*Math.PI));for(let x=0;x<w;x++)R(g,x,sag(x),1,1,K);for(let x=6;x<w-6;x+=12){const y=sag(x)+1;R(g,x-2,y,5,6,K);R(g,x-1,y+1,3,4,'#d8364b');R(g,x,y+1,1,4,'#ffc727');}return c;}
function floatSprite(){const c=mk(60,22),g=c.getContext('2d');R(g,0,6,60,14,K);R(g,1,7,58,12,'#9b5fd6');for(let x=1;x<59;x+=6)R(g,x,7,3,12,'#ffc727');R(g,1,7,58,2,PAL.W);
  g.fillStyle=K;pixCircle(g,16,6,6);g.fillStyle='#f4f8ff';pixCircle(g,16,6,5);R(g,14,4,1,1,K);R(g,18,4,1,1,K);R(g,15,7,3,1,'#f07a1a');R(g,30,0,4,7,K);R(g,31,1,2,5,'#d8364b');R(g,40,1,14,6,K);R(g,41,2,12,4,'#ffc727');R(g,4,19,6,3,K);R(g,50,19,6,3,K);return c;}
function carSideSprite(a){const cc=CAR_PAL[a%5];const c=mk(30,14),g=c.getContext('2d');R(g,2,3,26,8,K);R(g,3,4,24,6,cc[0]);R(g,8,1,13,4,K);R(g,9,2,11,3,'#8fd3ff');R(g,3,4,24,1,PAL.W);R(g,4,10,6,4,K);R(g,20,10,6,4,K);R(g,26,5,2,2,'#ffe9a8');return c;}
function wardenSprite(fr){const c=mk(14,18),g=c.getContext('2d');R(g,3,0,8,4,K);R(g,4,1,6,2,'#1f2f5a');R(g,3,3,8,1,'#ffc727');R(g,4,4,6,5,K);R(g,5,4,4,4,'#f2c7a5');R(g,5,5,1,1,K);R(g,8,5,1,1,K);
  R(g,2,9,10,6,K);R(g,3,9,8,5,'#d8f03a');R(g,3,11,8,1,'#c6d0e0');R(g,10,9,4,6,K);R(g,11,10,2,4,'#f4f8ff');R(g,1,15,12,3,K);R(g,2,15,10,2,'#55607a');const l=fr?1:0;R(g,1+l,16,3,2,'#2a2a36');R(g,10-l,16,3,2,'#2a2a36');return c;}
SHOPS.push(['CITY HALL','#e8e0cc','#d6cdb4','#13306b'],['STATION','#c6d0e0','#8793a8','#d8364b'],['HOSPITAL','#f4f8ff','#c6d9f3','#d8364b'],['NOODLES','#d8364b','#a82639','#ffc727'],['TEA HOUSE','#33b24a','#1f7a5c','#ffc727'],['DUMPLINGS','#ffc727','#e29a1c','#d8364b'],['HOTEL','#9b7fd6','#6b4fa8','#ffc727'],['THEATRE','#7a1f33','#55102a','#ffc727'],['ICE RINK','#9fd4f4','#6fb4e0','#13306b']);
Object.assign(PROPS,{
  tower:{arg:0,min:0,max:4,make:a=>officeSprite(50,96,a),foot:()=>[0,0,50,96]},
  towerw:{arg:0,min:0,max:4,make:a=>officeSprite(70,80,a),foot:()=>[0,0,70,80]},
  museum:{make:()=>museumSprite(),foot:()=>[0,12,120,50]},
  track:{arg:200,min:20,max:600,make:a=>trackSprite(a),foot:a=>[0,0,22,a]},
  train:{arg:102,min:34,max:300,make:a=>trainSprite(a,'#3f86d6'),foot:a=>[0,0,24,a]},
  flag:{arg:0,min:0,max:3,make:a=>flagSprite(a),foot:()=>[0,26,4,4]},
  foodtruck:{arg:0,min:0,max:2,make:a=>foodTruckSprite(a),foot:()=>[0,0,26,40]}});
CHASERS.warden={name:'THE WARDEN',frames:[wardenSprite(0),wardenSprite(1)],w:10,h:6,ox:2,oy:12,speed:1.08,lines:['TICKET!','YOU CAN\'T PARK THAT HERE!','NO PLOWING ZONE!','THAT\'S A FINE!','STOP RIGHT THERE!'],catchLine:'TICKETED!',col:'#d8f03a'};
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){",KIT+"function buildFromData(g,D,setT,ob,setCircle,paintText){")
# decor: strings of lanterns
rep("  for(const d of D.decor||[])if(d[0]==='bunting')g.decor.push({spr:buntingSprite(d[3]||60),x:d[1],y:d[2]});",
    "  for(const d of D.decor||[]){if(d[0]==='bunting')g.decor.push({spr:buntingSprite(d[3]||60),x:d[1],y:d[2]});else if(d[0]==='lanterns')g.decor.push({spr:lanternSprite(d[3]||80),x:d[1],y:d[2]});}")
# cross traffic skins: h[5] = 'car' (side-on car, quick) or 'float' (parade float, slow); taxi: a>=4 = tram (long, slow)
rep("    else if(H.cross){const d=h[3]||1;g.hazards.push({kind:'cross',lane:h[2],x:d>0?-50:g.pw+8,y:h[2],w:42,h:12,dir:d,per:h[4]||7,t:rnd(1,4),state:'idle',spr:crossSprite()});}",
    "    else if(H.cross){const d=h[3]||1,sk=h[5]||'farm',spr=sk==='car'?carSideSprite((h[1]+h[2])%5):sk==='float'?floatSprite():crossSprite();g.hazards.push({kind:'cross',lane:h[2],x:d>0?-60:g.pw+8,y:h[2],w:spr.width-2,h:12,dir:d,per:h[4]||7,t:rnd(1,4),state:'idle',spr,speed:sk==='car'?70:sk==='float'?28:46});}")
rep("      else{hz.x+=hz.dir*46*dt;","      else{hz.x+=hz.dir*(hz.speed||46)*dt;")
rep("        if((hz.dir>0&&hz.x>G.pw+4)||(hz.dir<0&&hz.x<-46)){","        if((hz.dir>0&&hz.x>G.pw+4)||(hz.dir<0&&hz.x<-hz.w-4)){")
rep("if(hz.t<=0&&near){hz.state='warn';hz.t=1.4;hz.x=hz.dir>0?-46:G.pw+4;","if(hz.t<=0&&near){hz.state='warn';hz.t=1.4;hz.x=hz.dir>0?-hz.w-4:G.pw+4;")
rep("  taxi:{make:(x,y,a)=>{const bus=(a|0)>=2,d=(a|0)%2?-1:1,cc=CAR_PAL[(x+y)%5];return {kind:'taxi',x,y,w:bus?24:22,h:bus?52:28,vy:d*(bus?28:36),dir:d,big:true,spr:bus?BUS:carSprite(cc[0],cc[1],false,false)};}},",
    "  taxi:{make:(x,y,a)=>{a=a|0;const tram=a>=4,bus=a>=2&&!tram,d=a%2?-1:1,cc=CAR_PAL[(x+y)%5];return {kind:'taxi',x,y,w:tram||bus?24:22,h:tram?102:bus?52:28,vy:d*(tram?24:bus?28:36),dir:d,big:true,spr:tram?trainSprite(102,'#d8364b'):bus?BUS:carSprite(cc[0],cc[1],false,false)};}},")
open(f,'w',encoding='utf-8').write(s);print('p51 ok')
