import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def swap(name, new):
    global s
    a=s.index('function '+name+'(g,ox,oy,fr,c){'); e=s.index('\nfunction',a+10)
    s=s[:a]+new.strip()+s[e:]
# Wild Rides redrawn (Nov 15): the Monster Truck gets giant knobbly tyres, a lifted body, roll bar and exhaust stacks;
# the Mega Mech becomes a proper walker (stepping feet, shoulder armour, arms holding the scoops, cockpit dome,
# thrusters); the Snow Dragon gets spread membrane wings that flap, a horned head and snout, spines, a saddle and a
# swinging spade tail. Same footprints as before, so nothing about fit or collisions changes.
rep_ok=s.count("VDRAW[tid](g,ox,oy,fr,tid==='rotary'?Object.assign({},c,{pl:Math.min(6,pl)}):c);")==1
assert rep_ok
s=s.replace("VDRAW[tid](g,ox,oy,fr,tid==='rotary'?Object.assign({},c,{pl:Math.min(6,pl)}):c);","VDRAW[tid](g,ox,oy,fr,tid==='rotary'?Object.assign({},c,{pl:Math.min(6,pl)}):tid==='mech'?Object.assign({},c,{bw}):c);")
swap('drawMonster', r"""
function drawMonster(g,ox,oy,fr,c){
  const tyre=(tx,ty)=>{R(g,tx,ty,11,15,K);R(g,tx+1,ty+1,9,13,'#2a2a36');for(let i=0;i<5;i++){const yy=ty+1+((i*3+fr)%13);R(g,tx,yy,2,2,K);R(g,tx+9,yy,2,2,K);R(g,tx+2,yy,7,1,'#3c3f52');}
    R(g,tx+3,ty+5,5,5,K);R(g,tx+4,ty+6,3,3,'#c6d0dc');R(g,tx+5,ty+7,1,1,'#55607a');R(g,tx+1,ty+1,9,1,'#55586a');};
  R(g,ox-16,oy-10,32,3,K);R(g,ox-15,oy-9,30,1,'#8793a8');R(g,ox-16,oy+8,32,3,K);R(g,ox-15,oy+9,30,1,'#8793a8');
  tyre(ox-20,oy-17);tyre(ox+9,oy-17);tyre(ox-20,oy+2);tyre(ox+9,oy+2);
  const x=ox-8,y=oy-16;R(g,x,y,16,32,K);R(g,x+1,y+1,14,30,c.b);R(g,x+1,y+1,14,1,c.l);R(g,x+1,y+1,1,30,c.l);R(g,x+14,y+1,1,30,c.d);
  R(g,x+5,y+2,6,4,K);R(g,x+6,y+3,4,2,'#8793a8');R(g,x+7,y+3,2,1,'#2a2a36');
  R(g,x+2,y+7,12,2,K);for(let i=0;i<4;i++)R(g,x+3+i*3,y+7,2,1,fr%2===i%2?'#ffef7a':'#ffd23f');
  R(g,x+2,y+9,12,5,K);R(g,x+3,y+10,10,3,'#8fd3ff');R(g,x+3,y+10,3,1,'#ffffff');R(g,x+7,y+11,3,2,curHat().c);
  R(g,x+2,y+14,12,4,c.d);R(g,x+3,y+14,10,1,c.l);
  R(g,x+1,y+19,14,2,K);R(g,x+2,y+19,12,1,'#c6d0dc');R(g,x+2,y+18,1,3,K);R(g,x+13,y+18,1,3,K);
  R(g,x+2,y+21,12,9,K);R(g,x+3,y+22,10,7,c.d);for(let i=0;i<3;i++)R(g,x+3,y+23+i*2,10,1,'rgba(0,0,0,0.18)');R(g,x+5,y+24,6,3,'#55607a');
  for(const ex of [x-2,x+16]){R(g,ex,y+17,2,9,K);R(g,ex,y+18,1,7,'#e8eef8');}if(fr%2)for(const ex of [x-2,x+16])R(g,ex-1,y+14,4,3,'rgba(200,210,225,0.75)');
  if(c.deco==='flames'){for(const sx of [x+1,x+12]){R(g,sx,y+3,3,2,'#f07a1a');R(g,sx,y+5,3,2,'#ffc727');R(g,sx+(sx<ox?1:0),y+2,2,1,'#e03a4e');}R(g,x+1,y+22,2,6,'#f07a1a');R(g,x+13,y+22,2,6,'#f07a1a');}
  else if(c.deco==='tiger'){for(let i=0;i<5;i++)R(g,x+1,y+3+i*6,3,1,'#2a2a36'),R(g,x+12,y+4+i*6,3,1,'#2a2a36');R(g,x+2,y-2,4,3,K);R(g,x+3,y-1,2,2,c.b);R(g,x+10,y-2,4,3,K);R(g,x+11,y-1,2,2,c.b);}
  else if(c.deco==='antenna'){R(g,x+4,y+12,1,6,K);R(g,x+11,y+12,1,6,K);R(g,x+3,y+11,3,2,'#ff4fa3');R(g,x+10,y+11,3,2,'#ff4fa3');}
  else if(c.deco==='crown'){R(g,x+4,y+14,8,4,K);R(g,x+5,y+15,6,2,'#ffd23f');R(g,x+5,y+14,1,1,'#ffd23f');R(g,x+7,y+13,2,2,'#ffd23f');R(g,x+10,y+14,1,1,'#ffd23f');}}
""")
swap('drawMech', r"""
function drawMech(g,ox,oy,fr,c){const st=fr%2;
  for(const [fx,dy] of [[ox-13,st?-4:2],[ox+3,st?2:-4]]){R(g,fx,oy+5+dy,10,11,K);R(g,fx+1,oy+6+dy,8,9,'#55607a');R(g,fx+1,oy+12+dy,8,3,'#3c3f52');R(g,fx+2,oy+6+dy,6,1,'#8793a8');for(let k=0;k<3;k++)R(g,fx+1+k*3,oy+15+dy,2,2,K);}
  R(g,ox-9,oy+1,18,6,K);R(g,ox-8,oy+2,16,4,c.d);R(g,ox-1,oy+2,2,4,'#55607a');
  {const reach=Math.max(14,Math.min(30,Math.round((c.bw||60)/4)));for(const sg of [-1,1]){const x0=ox+sg*13,y0=oy-3,x1=ox+sg*reach,y1=oy-16,n=Math.max(Math.abs(x1-x0),Math.abs(y1-y0));
    for(let t=0;t<=n;t++){const x=Math.round(x0+(x1-x0)*t/n),y=Math.round(y0+(y1-y0)*t/n);R(g,x-2,y-2,5,5,K);}
    for(let t=0;t<=n;t++){const x=Math.round(x0+(x1-x0)*t/n),y=Math.round(y0+(y1-y0)*t/n);R(g,x-1,y-1,3,3,'#8793a8');R(g,x-1,y-1,1,1,'#c6d0dc');if(t%4===2)R(g,x-1,y,3,1,(t>>2)%2?'#2a2a36':'#ffc727');}
    R(g,x1-4,y1-3,9,5,K);R(g,x1-3,y1-2,7,3,c.d);R(g,x1-3,y1-2,7,1,c.l);}}
  for(const sx of [ox-18,ox+10]){R(g,sx,oy-7,8,11,K);R(g,sx+1,oy-6,6,9,c.b);R(g,sx+1,oy-6,6,1,c.l);for(let k=0;k<3;k++)R(g,sx+1+k*2,oy+1,2,2,k%2?'#2a2a36':'#ffc727');R(g,sx+3,oy-4,2,2,c.d);}
  R(g,ox-9,oy-11,18,15,K);R(g,ox-8,oy-10,16,13,c.b);R(g,ox-8,oy-10,16,1,c.l);R(g,ox-8,oy+1,16,2,c.d);
  R(g,ox-6,oy-1,12,2,K);for(let k=0;k<4;k++)R(g,ox-5+k*3,oy-1,2,1,(k+fr)%2?'#ffef7a':'#ffc727');
  g.fillStyle=K;pixCircle(g,ox,oy-6,5);g.fillStyle='#8fd3ff';pixCircle(g,ox,oy-6,4);R(g,ox-3,oy-9,2,2,'#ffffff');R(g,ox-1,oy-6,3,3,curHat().c);
  R(g,ox+6,oy-14,1,5,K);R(g,ox+5,oy-15,3,2,'#e03a4e');R(g,ox-7,oy+7,4,3,K);R(g,ox+3,oy+7,4,3,K);R(g,ox-6,oy+8,2,2,fr%2?'#ff9a3c':'#ffd23f');R(g,ox+4,oy+8,2,2,fr%2?'#ffd23f':'#ff9a3c');
  if(c.deco==='ears'){g.fillStyle=K;pixCircle(g,ox-7,oy-11,3);pixCircle(g,ox+7,oy-11,3);g.fillStyle=c.d;pixCircle(g,ox-7,oy-11,2);pixCircle(g,ox+7,oy-11,2);}
  else if(c.deco==='plume'){R(g,ox-1,oy-16,3,7,K);R(g,ox,oy-15,1,5,'#e03a4e');R(g,ox-2,oy-17,5,2,'#e03a4e');}
  else if(c.deco==='crystal'){for(const [a1,b1] of [[-16,-6],[13,-6],[-7,-10],[6,-10]]){R(g,ox+a1,oy+b1,2,3,'#ffffff');R(g,ox+a1,oy+b1+1,2,1,'#bfe6ff');}}
  else if(c.deco==='dogears'){R(g,ox-11,oy-9,4,9,K);R(g,ox-10,oy-8,2,7,c.d);R(g,ox+7,oy-9,4,9,K);R(g,ox+8,oy-8,2,7,c.d);R(g,ox-1,oy-12,3,2,'#2a2a36');}}
""")
swap('drawDragon', r"""
function drawDragon(g,ox,oy,fr,c){const up=fr%2;
  for(const s of [-1,1]){const span=up?21:18,y0=oy-9,rise=up?9:3;
    for(let i=0;i<=span;i++){const x=ox+s*(5+i),top=y0-Math.round(i*rise/span),len=Math.max(2,Math.round((span-i)*0.75)+3),sc=Math.round(2.5*Math.sin(Math.PI*((i%6)/6))),bot=top+len-sc;
      R(g,x,top,1,bot-top+1,K);if(bot-top>1)R(g,x,top+1,1,bot-top-1,i%6===0?c.b:c.d);if(bot-top>3)R(g,x,top+1,1,1,c.l);}
    const tipx=ox+s*(5+span),tipy=y0-rise;R(g,tipx-(s<0?1:0),tipy-2,2,3,'#e0c08a');R(g,tipx-(s<0?1:0),tipy-2,2,1,K);}
  for(let i=0;i<12;i++){const tx=ox+Math.round(Math.sin(i*0.45+fr*0.7)*3),ty=oy+10+i;R(g,tx-2,ty,4,1,K);R(g,tx-1,ty,2,1,i%3?c.b:c.a);}
  {const tx=ox+Math.round(Math.sin(12*0.45+fr*0.7)*3);for(const [w,dy] of [[1,0],[3,1],[5,2],[5,3],[3,4],[1,5]]){R(g,tx-(w>>1)-1,oy+21+dy,w+2,1,K);R(g,tx-(w>>1),oy+21+dy,w,1,c.a);}}
  for(const s of [-1,1]){const lx=s<0?ox-9:ox+6;R(g,lx,oy+4,4,5,K);R(g,lx+1,oy+5,2,3,c.d);R(g,lx,oy+9,4,1,'#f4f8ff');}
  for(let r=0;r<22;r++){const hw=Math.round(6.5*Math.sin(Math.PI*(r+2)/25));R(g,ox-hw-1,oy-9+r,hw*2+2,1,K);if(hw>0){R(g,ox-hw,oy-9+r,hw*2,1,c.b);R(g,ox-hw,oy-9+r,1,1,c.l);}}
  for(let r=0;r<6;r++){R(g,ox,oy-7+r*3,1,2,c.a);R(g,ox-1,oy-6+r*3,3,1,c.d);}
  R(g,ox-4,oy-4,8,6,K);R(g,ox-3,oy-3,6,4,'#8a5a34');R(g,ox-3,oy-3,6,1,'#c98d4a');R(g,ox-1,oy-4,3,3,curHat().c);
  R(g,ox-2,oy-15,4,7,K);R(g,ox-1,oy-15,2,7,c.b);
  R(g,ox-4,oy-21,8,7,K);R(g,ox-3,oy-20,6,5,c.b);R(g,ox-3,oy-20,6,1,c.l);R(g,ox-2,oy-25,4,5,K);R(g,ox-1,oy-24,2,4,c.b);R(g,ox-2,oy-25,1,1,c.d);R(g,ox+1,oy-25,1,1,c.d);
  R(g,ox-3,oy-18,1,2,'#ffef7a');R(g,ox+2,oy-18,1,2,'#ffef7a');R(g,ox-6,oy-17,3,2,K);R(g,ox+3,oy-17,3,2,K);R(g,ox-6,oy-16,2,3,'#e0c08a');R(g,ox+4,oy-16,2,3,'#e0c08a');}
""")

# UFO: a soft hover glow, shading on the saucer and a shadow under the dome
_u="g.fillStyle=K;pixCircle(g,ox,oy,15);g.fillStyle=c.d;pixCircle(g,ox,oy,14);g.fillStyle=c.b;pixCircle(g,ox,oy,13);"
assert s.count(_u)==1
s=s.replace(_u,"g.fillStyle=fr%2?'rgba(150,240,255,0.30)':'rgba(150,240,255,0.18)';pixCircle(g,ox,oy,18);g.fillStyle=K;pixCircle(g,ox,oy,15);g.fillStyle=c.d;pixCircle(g,ox,oy,14);g.fillStyle=c.b;pixCircle(g,ox-1,oy-1,12);")
_d="g.fillStyle=K;pixCircle(g,ox,oy,7);g.fillStyle='#8fd3ff';pixCircle(g,ox,oy,6);"
assert s.count(_d)==1
s=s.replace(_d,"g.fillStyle='rgba(0,0,0,0.25)';pixCircle(g,ox+1,oy+2,8);"+_d)

# Mech walk: the feet change only when a stomp lands (synced to the stomp sound), and stay planted when standing still.
_a="run.stepT=0.42;sfx('stomp',0,{vol:0.4});"
assert s.count(_a)==1
s=s.replace(_a,"run.stepT=0.42;P.step=(P.step|0)+1;sfx('stomp',0,{vol:0.4});")
_b="drawRig(b,tid,P.x,P.y,P.spin>0?(P.f+Math.floor(P.spin*14))%4:P.f,bwPx,pl,P.bob,P.fr,"
assert s.count(_b)==1
s=s.replace(_b,"drawRig(b,tid,P.x,P.y,P.spin>0?(P.f+Math.floor(P.spin*14))%4:P.f,bwPx,pl,P.bob,tid==='mech'?(P.step|0):P.fr,")
open(f,'w',encoding='utf-8').write(s)
