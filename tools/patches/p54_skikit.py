import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# SKI RESORT KIT: chalets, lift pylons, slalom gates, moguls, jump ramps; skiers racing down the slope after a
# warning arrow; the boss chaser: a runaway snowball.
# ---------------------------------------------------------------------------------------------
KIT=r"""
function chaletSprite(a){const c=mk(44,40),g=c.getContext('2d');for(let r=0;r<18;r++){const hw=Math.round(4+r*1.15);R(g,22-hw-1,r,hw*2+2,1,K);R(g,22-hw,r,hw*2,1,r<10?PAL.W:'#7a4a2a');}
  R(g,2,18,40,22,K);R(g,3,18,38,21,'#a8673a');for(let y=20;y<39;y+=3)R(g,3,y,38,1,'#8a5a2c');R(g,6,22,8,7,K);R(g,7,23,6,5,'#ffe9a8');R(g,30,22,8,7,K);R(g,31,23,6,5,'#ffe9a8');R(g,18,26,8,14,K);R(g,19,27,6,13,'#55321d');
  R(g,10,6,6,1,['#d8364b','#3f86d6','#33b24a'][a%3]);return c;}
function pylonSprite(){const c=mk(14,46),g=c.getContext('2d');R(g,5,6,4,40,K);R(g,6,6,2,39,'#8793a8');R(g,0,0,14,6,K);R(g,1,1,12,4,'#c6d0e0');R(g,0,0,14,1,PAL.W);R(g,2,40,10,6,K);return c;}
function gatePoleSprite(a){const col=a%2?'#3f86d6':'#d8364b';const c=mk(5,16),g=c.getContext('2d');R(g,1,0,3,16,K);R(g,2,1,1,15,col);R(g,0,2,5,6,K);R(g,1,3,3,4,col);R(g,1,3,3,1,PAL.W);return c;}
function mogulSprite(){const c=mk(16,9),g=c.getContext('2d');g.fillStyle=K;for(let y=0;y<9;y++){const hw=Math.round(8*Math.sqrt(Math.max(0,1-((y-5)/5)**2)));g.fillRect(8-hw,y,hw*2,1);}g.fillStyle=PAL.W;for(let y=1;y<8;y++){const hw=Math.round(7*Math.sqrt(Math.max(0,1-((y-5)/4.4)**2)));g.fillRect(8-hw,y,hw*2,1);}R(g,3,6,10,2,'#c6d9f3');return c;}
function rampSprite(){const c=mk(40,24),g=c.getContext('2d');for(let y=0;y<24;y++){R(g,0,y,40,1,K);}for(let y=1;y<23;y++)R(g,1,y,38,1,y<6?PAL.W:y%4?'#c6d9f3':'#9fc0e8');R(g,0,0,40,2,'#d8364b');return c;}
function skierSprite(a){const col=['#d8364b','#3f86d6','#33b24a','#9b5fd6','#ffc727'][a%5];const c=mk(10,16),g=c.getContext('2d');R(g,3,0,4,4,K);R(g,4,1,2,2,'#f2c7a5');R(g,2,4,6,6,K);R(g,3,5,4,4,col);R(g,1,9,8,3,K);R(g,2,9,6,2,'#2a2a36');R(g,0,12,3,4,K);R(g,7,12,3,4,K);R(g,0,15,10,1,K);return c;}
function snowballSprite(fr){const c=mk(20,20),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,10,10,9);g.fillStyle=PAL.W;pixCircle(g,10,10,8);g.fillStyle='#c6d9f3';pixCircle(g,12,13,4);
  for(const [x,y] of (fr?[[5,6],[13,5],[8,13]]:[[6,11],[12,8],[14,14]]))R(g,x,y,2,2,'#9fc0e8');return c;}
SHOPS.push(['SKI SCHOOL','#ffc727','#e29a1c','#d8364b'],['LIFT','#d8364b','#a82639','#f4f8ff'],['SKI HIRE','#3f86d6','#2a5fa8','#ffc727'],['APRES','#7a4a2a','#55321d','#ffc727'],['GONDOLA','#c6d0e0','#8793a8','#d8364b']);
Object.assign(PROPS,{
  chalet:{arg:0,min:0,max:2,make:a=>chaletSprite(a),foot:()=>[2,18,40,22]},
  pylon:{make:()=>pylonSprite(),foot:()=>[2,38,10,8]},
  gatepole:{arg:0,min:0,max:1,make:a=>gatePoleSprite(a),foot:()=>[0,10,5,6]},
  mogul:{make:()=>mogulSprite(),foot:()=>[1,3,14,6]},
  ramp:{make:()=>rampSprite(),foot:()=>[0,0,40,24]}});
CHASERS.snowball={name:'THE SNOWBALL',frames:[snowballSprite(0),snowballSprite(1)],w:16,h:10,ox:2,oy:8,speed:1.06,lines:['*RUMBLE*','*ROLL ROLL*','*GROWING*','*CRUNCH*'],catchLine:'SPLAT!',col:'#ffffff'};
const SKIER_FR=[0,1,2,3,4].map(k=>skierSprite(k));
Object.assign(HAZ,{skier:{skier:1}});
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){",KIT+"function buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("    else if(H.balls){",
    "    else if(H.skier){g.hazards.push({kind:'skier',lane:h[1],x:h[1],y:-40,w:8,h:6,per:h[3]||6,t:rnd(1,h[3]||6),state:'idle',a:(h[1]>>3)%5,wob:rnd(0,6)});}\n"
    "    else if(H.balls){")
# skiers: warn with an arrow at the top of the view, then race down past you
rep("    else if(hz.kind==='barrier'){",
r"""    else if(hz.kind==='skier'){if(hz.state==='idle'){hz.t-=dt;if(hz.t<=0){hz.state='warn';hz.t=1.0;sfx('whoosh',0,{vol:0.4,rate:1.4});}}
      else if(hz.state==='warn'){hz.t-=dt;if(hz.t<=0){hz.state='go';hz.y=camY-24;hz.x=hz.lane;}}
      else{hz.wob+=dt;hz.y+=120*dt;hz.x=hz.lane+Math.sin(hz.wob*3)*14;if(tid!=='ufo'&&overlap(pr,hz)){hit('hz',SPILL_HAZARD*0.6);addFloat(P.x,P.y-22,'WHOOPS!','#9fd8ff',0.8);}
        if(hz.y>camY+VIEW_H+40||hz.y>G.ph){hz.state='idle';hz.t=hz.per+rnd(-1,1);}}continue;}
    else if(hz.kind==='barrier'){""")
rep("    else if(hz.kind==='barrier')ents.push({base:hz.y+hz.h,draw:()=>{",
    "    else if(hz.kind==='skier')ents.push({base:hz.y+hz.h,draw:()=>{if(hz.state==='warn'&&Math.floor(tNow*8)%2===0){const ax=Math.round(hz.lane),ay=Math.round(camY)+4;for(let i=0;i<5;i++)R(b,ax-i,ay+4-i,i*2+1,1,'#ff4a4a');R(b,ax-1,ay-4,3,4,'#ff4a4a');}\n"
    "        if(hz.state==='go'){R(b,hx-1,hy+5,10,2,'rgba(27,31,59,0.2)');b.drawImage(SKIER_FR[hz.a],hx-1,hy-10);}}});\n"
    "    else if(hz.kind==='barrier')ents.push({base:hz.y+hz.h,draw:()=>{")
# the hazard draw loop skips things far off screen; skiers live off screen until they go
rep("for(const hz of G.hazards){if(hz.y+40<top||hz.y-40>bot)continue;","for(const hz of G.hazards){if(hz.kind!=='skier'&&(hz.y+40<top||hz.y-40>bot))continue;")
open(f,'w',encoding='utf-8').write(s);print('p54 ok')
