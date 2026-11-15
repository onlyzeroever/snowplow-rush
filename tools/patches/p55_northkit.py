import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# MOUNTAIN PASS + FROZEN NORTH KIT: tunnels, warning signs, snow poles, avalanche fences, cairns, a radio mast;
# igloos, ice spires, the ice palace walls, a research station. Hazards: falling rocks (warned like skiers),
# penguin huddles that scatter, dog sleds crossing. Boss chasers: the yeti and the polar bear.
# ---------------------------------------------------------------------------------------------
KIT=r"""
function tunnelSprite(){const c=mk(90,56),g=c.getContext('2d');R(g,0,10,90,46,K);R(g,1,11,88,44,'#8793a8');for(let y=14;y<54;y+=6)for(let x=2+((y/6|0)%2)*6;x<88;x+=12)R(g,x,y,10,4,'#9aa6ba');
  g.fillStyle=K;for(let y=0;y<34;y++){const hw=Math.round(26*Math.sqrt(Math.max(0,1-((34-y)/34)**2)));g.fillRect(45-hw,22+y,hw*2,1);}g.fillStyle='#1b1f3b';for(let y=1;y<34;y++){const hw=Math.round(24*Math.sqrt(Math.max(0,1-((34-y)/33)**2)));g.fillRect(45-hw,22+y,hw*2,1);}
  R(g,0,8,90,6,PAL.W);R(g,0,14,90,1,'#c6d9f3');return c;}
function warnSignSprite(){const c=mk(14,20),g=c.getContext('2d');R(g,6,8,2,12,K);for(let r=0;r<10;r++){R(g,7-r/1.2|0,r,(r/1.2|0)*2+1,1,K);}for(let r=2;r<9;r++){R(g,7-(r-1)/1.5|0,r,((r-1)/1.5|0)*2+1,1,'#ffc727');}R(g,6,4,2,3,K);R(g,6,8,2,1,K);return c;}
function snowPoleSprite(){const c=mk(4,18),g=c.getContext('2d');R(g,0,0,4,18,K);for(let y=1;y<17;y+=4){R(g,1,y,2,2,'#f07a1a');R(g,1,y+2,2,2,'#2a2a36');}return c;}
function cairnSprite(){const c=mk(14,16),g=c.getContext('2d');for(const [x,y,w] of [[4,0,6],[2,4,10],[1,8,12],[0,12,14]]){R(g,x,y,w,4,K);R(g,x+1,y+1,w-2,2,'#9aa6ba');R(g,x+1,y+1,w-2,1,PAL.W);}return c;}
function mastSprite(){const c=mk(18,70),g=c.getContext('2d');for(let y=0;y<64;y++){const hw=1+Math.round(y*0.11);R(g,9-hw,y,1,1,K);R(g,9+hw,y,1,1,K);if(y%6===0)R(g,9-hw,y,hw*2+1,1,K);}R(g,7,0,4,4,'#d8364b');R(g,0,64,18,6,K);R(g,1,65,16,4,'#8793a8');return c;}
function iglooPropSprite(){const c=mk(30,22),g=c.getContext('2d');g.fillStyle=K;for(let y=0;y<22;y++){const hw=Math.round(15*Math.sqrt(Math.max(0,1-((22-y)/22)**2)));g.fillRect(15-hw,y,hw*2,1);}g.fillStyle=PAL.W;for(let y=1;y<21;y++){const hw=Math.round(14*Math.sqrt(Math.max(0,1-((22-y)/21)**2)));g.fillRect(15-hw,y,hw*2,1);}
  for(let y=5;y<21;y+=4)R(g,2,y,26,1,'#c6d9f3');R(g,10,13,10,9,K);R(g,11,14,8,8,'#2a3450');return c;}
function spireSprite(){const c=mk(16,34),g=c.getContext('2d');for(let y=0;y<34;y++){const hw=Math.round(y*0.24)+1;R(g,8-hw-1,y,hw*2+2,1,K);R(g,8-hw,y,hw,1,'#bfe6ff');R(g,8,y,hw,1,'#8fc8f0');}R(g,7,2,1,10,PAL.W);return c;}
function iceWallSprite(w,h){const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,'#9fd4f4');for(let y=2;y<h-2;y+=5)for(let x=2+((y/5|0)%2)*4;x<w-2;x+=8)R(g,x,y,6,4,'#bfe6ff');R(g,1,1,w-2,2,PAL.W);if(w>=h)for(let x=0;x<w;x+=8){R(g,x,0,4,3,K);R(g,x+1,0,2,2,'#bfe6ff');}return c;}
function sledSprite(){const c=mk(70,16),g=c.getContext('2d');for(let k=0;k<4;k++){const x=k*12;R(g,x,4,10,8,K);R(g,x+1,5,8,6,k%2?'#8793a8':'#c6c0d0');R(g,x+7,3,3,3,K);R(g,x+1,5,8,1,PAL.W);}R(g,48,2,22,12,K);R(g,49,3,20,10,'#d8364b');R(g,52,0,8,6,K);R(g,53,1,6,4,'#3f86d6');R(g,48,14,22,2,K);R(g,47,5,2,4,K);return c;}
function penguinSprite(fr){const c=mk(9,11),g=c.getContext('2d');R(g,1,0,7,10,K);R(g,2,1,5,8,'#2a2a36');R(g,3,3,3,6,'#f4f8ff');R(g,3,2,1,1,PAL.W);R(g,5,2,1,1,PAL.W);R(g,4,3,1,1,'#f07a1a');R(g,0,4+(fr?1:0),1,4,K);R(g,8,4+(fr?0:1),1,4,K);R(g,2,10,2,1,'#f07a1a');R(g,5,10,2,1,'#f07a1a');return c;}
function yetiSprite(fr){const c=mk(22,26),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,11,8,8);g.fillStyle='#f4f8ff';pixCircle(g,11,8,7);R(g,6,6,10,7,'#9fc0e8');R(g,7,7,2,2,K);R(g,13,7,2,2,K);R(g,8,11,6,2,K);R(g,9,11,1,1,PAL.W);R(g,12,11,1,1,PAL.W);
  R(g,3,14,16,10,K);R(g,4,14,14,9,'#f4f8ff');R(g,0,13,4,9,K);R(g,18,13,4,9,K);R(g,1,14,2,7,'#f4f8ff');R(g,19,14,2,7,'#f4f8ff');const l=fr?1:0;R(g,4+l,23,6,3,K);R(g,12-l,23,6,3,K);R(g,5+l,23,4,2,'#9fc0e8');R(g,13-l,23,4,2,'#9fc0e8');return c;}
function bearSprite(fr){const c=mk(26,18),g=c.getContext('2d');R(g,2,4,18,10,K);R(g,3,5,16,8,'#f4f8ff');R(g,18,2,8,9,K);R(g,19,3,6,7,'#f4f8ff');R(g,19,2,2,2,K);R(g,23,2,2,2,K);R(g,24,6,2,2,K);R(g,21,5,1,1,K);R(g,3,5,16,1,'#ffffff');R(g,3,11,16,2,'#d6dee9');
  const l=fr?1:0;for(const x of [3+l,8-l,13+l,17-l])R(g,x,13,3,5,K);return c;}
SHOPS.push(['MOUNTAIN HUT','#a8673a','#7a4a2a','#f4f8ff'],['WEATHER STN','#f4f8ff','#c6d9f3','#d8364b'],['RESEARCH BASE','#d8364b','#a82639','#f4f8ff'],['ICE PALACE','#bfe6ff','#8fc8f0','#6b3fa8'],['NORTH POLE POST','#3f86d6','#2a5fa8','#ffc727']);
Object.assign(PROPS,{
  tunnel:{make:()=>tunnelSprite(),foot:()=>[0,10,90,46]},
  warnsign:{make:()=>warnSignSprite(),foot:()=>[5,15,4,5]},
  snowpole:{make:()=>snowPoleSprite(),foot:()=>[0,13,4,5]},
  cairn:{make:()=>cairnSprite(),foot:()=>[0,8,14,8]},
  mast:{make:()=>mastSprite(),foot:()=>[0,60,18,10]},
  igloo:{make:()=>iglooPropSprite(),foot:()=>[0,6,30,16]},
  spire:{make:()=>spireSprite(),foot:()=>[2,24,12,10]},
  icewall:{arg:60,min:10,max:180,make:a=>iceWallSprite(a,10),foot:a=>[0,0,a,10]},
  icewallv:{arg:60,min:10,max:400,make:a=>iceWallSprite(10,a),foot:a=>[0,0,10,a]}});
Object.assign(CHASERS,{
  yeti:{name:'THE YETI',frames:[yetiSprite(0),yetiSprite(1)],w:16,h:8,ox:3,oy:18,speed:1.06,lines:['RAAAWR!','GRRRR!','*STOMP STOMP*','ROAAAR!'],catchLine:'RAWR!!',col:'#9fd8ff'},
  bear:{name:'THE POLAR BEAR',frames:[bearSprite(0),bearSprite(1)],w:20,h:8,ox:3,oy:10,speed:1.08,lines:['GRRROWL!','*SNIFF SNIFF*','HUFF!','ROOOAR!'],catchLine:'CHOMP!',col:'#ffffff'}});
const PENG_FR=[penguinSprite(0),penguinSprite(1)];
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){",KIT+"function buildFromData(g,D,setT,ob,setCircle,paintText){")
# penguins are a flock skin; rocks are skiers that are rocks; dog sleds are crossing traffic
rep("    else if(H.gull){","    else if(H.peng){const n=h[3]||6;for(let k=0;k<n;k++)g.hazards.push({kind:'sheep',peng:true,flock:h[1]*1000+h[2],x:h[1]+(k%3)*11,y:h[2]+((k/3)|0)*10,w:7,h:5,hx:h[1],hy:h[2],vx:0,vy:0,t:rnd(0,3),anim:rnd(0,2)});}\n    else if(H.gull){")
rep("Object.assign(HAZ,{skier:{skier:1}});","Object.assign(HAZ,{skier:{skier:1},rockfall:{skier:1,rock:1},peng:{peng:1}});")
rep("    else if(H.skier){g.hazards.push({kind:'skier',lane:h[1],","    else if(H.skier){g.hazards.push({kind:'skier',rock:!!H.rock,lane:h[1],")
rep("else{hz.wob+=dt;hz.y+=120*dt;hz.x=hz.lane+Math.sin(hz.wob*3)*14;if(tid!=='ufo'&&overlap(pr,hz)){hit('hz',SPILL_HAZARD*0.6);addFloat(P.x,P.y-22,'WHOOPS!','#9fd8ff',0.8);}",
    "else{hz.wob+=dt;hz.y+=(hz.rock?95:120)*dt;hz.x=hz.lane+(hz.rock?0:Math.sin(hz.wob*3)*14);if(tid!=='ufo'&&overlap(pr,{x:hz.x-(hz.rock?4:0),y:hz.y,w:hz.w+(hz.rock?8:0),h:hz.h+(hz.rock?4:0)})){hit('hz',SPILL_HAZARD*(hz.rock?1:0.6));addFloat(P.x,P.y-22,hz.rock?'ROCKFALL!':'WHOOPS!','#9fd8ff',0.8);}")
rep("        if(hz.state==='go'){R(b,hx-1,hy+5,10,2,'rgba(27,31,59,0.2)');b.drawImage(SKIER_FR[hz.a],hx-1,hy-10);}}});",
    "        if(hz.state==='go'){R(b,hx-1,hy+5,10,2,'rgba(27,31,59,0.2)');if(hz.rock){b.save();b.translate(hx+4,hy+2);b.rotate(hz.wob*6);b.drawImage(ROCK_SPR,-8,-6);b.restore();}else b.drawImage(SKIER_FR[hz.a],hx-1,hy-10);}}});")
rep("const PENG_FR=[penguinSprite(0),penguinSprite(1)];","const PENG_FR=[penguinSprite(0),penguinSprite(1)],ROCK_SPR=rockSprite(16,12);")
rep("const d=h[3]||1,sk=h[5]||'farm',spr=sk==='car'?carSideSprite((h[1]+h[2])%5):","const d=h[3]||1,sk=h[5]||'farm',spr=sk==='sled'?sledSprite():sk==='car'?carSideSprite((h[1]+h[2])%5):")
rep("speed:sk==='car'?70:","speed:sk==='sled'?64:sk==='car'?70:")
rep("fr=hz.gull?GULL_FR[Math.floor(hz.anim*10)%2]:","fr=hz.peng?PENG_FR[mv]:hz.gull?GULL_FR[Math.floor(hz.anim*10)%2]:")
rep("if(Math.random()<0.4)addFloat(hz.x+4,hz.y-8,hz.gull?'SQUAWK!':","if(Math.random()<0.4)addFloat(hz.x+4,hz.y-8,hz.peng?'SQUEAK!':hz.gull?'SQUAWK!':")
open(f,'w',encoding='utf-8').write(s);print('p55 ok')
