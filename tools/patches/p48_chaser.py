import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# BOSS CHASERS (Alex, Nov 15): every area boss has someone hunting you for the whole job.
#  - waits a few seconds, then follows you round obstacles (a distance map to you, rebuilt 3x a second)
#  - wades slowly through deep snow, runs on cleared ground: the more you clear, the faster she gets to you
#  - near you she winds up ("!") and lunges; a catch spins you out (no control ~1s, coins spill, bumper helps)
#  - after a catch she gloats for a moment, which is your chance to get away; she speeds up as time runs out
#  - an arrow at the screen edge shows where she is when she's off screen
# Skins are added per area; Suburbs: Mrs. Grimshaw, the street's busybody.
# ---------------------------------------------------------------------------------------------
KIT=r"""
function grimshawSprite(fr){const c=mk(14,19),g=c.getContext('2d');
  // curlers and hair
  R(g,3,0,8,6,K);R(g,4,1,6,4,'#c6c0d0');for(const x of [4,7,10])R(g,x-1,0,3,2,'#ff7ab0');R(g,3,1,1,1,'#ff7ab0');
  // face, specs, cross mouth
  R(g,3,4,8,6,K);R(g,4,5,6,4,'#f2c7a5');R(g,4,6,2,1,K);R(g,8,6,2,1,K);R(g,6,6,2,1,'#55607a');R(g,5,8,4,1,'#b04a5a');
  // dressing gown with a belt, clipboard under one arm
  R(g,2,10,10,7,K);R(g,3,10,8,6,'#e07a8a');R(g,3,10,8,1,'#f4a8b8');R(g,3,13,8,1,'#b04a5a');R(g,6,10,1,6,'#c25a6e');
  R(g,10,11,4,6,K);R(g,11,12,2,4,'#f4f8ff');R(g,11,12,2,1,'#a8673a');R(g,0,11,3,4,K);R(g,1,12,1,2,'#f2c7a5');
  // fluffy slippers, legs swap each frame
  const l=fr?1:0;R(g,3+l,16,4,3,K);R(g,4+l,17,2,1,'#f4f8ff');R(g,7-l,16,4,3,K);R(g,8-l,17,2,1,'#f4f8ff');return c;}
const CHASERS={grimshaw:{name:'MRS. GRIMSHAW',frames:[grimshawSprite(0),grimshawSprite(1)],w:10,h:6,ox:2,oy:13,speed:1,
  lines:["THAT'S MY PARKING SPACE!","I'M CALLING THE COUNCIL!","YOU MISSED A BIT!","OFF MY DRIVEWAY!","I'LL SEE YOUR MANAGER!","NOT ON MY WATCH!"],
  catchLine:'GOTCHA!',col:'#ff7ab0'}};
function chaserMap(hz){const G2=G,cs=6,cols=Math.ceil(G2.pw/cs),rows=Math.ceil(G2.ph/cs);
  if(!hz.pass){hz.pass=new Uint8Array(cols*rows);for(let r=0;r<rows;r++)for(let c2=0;c2<cols;c2++){const x=c2*cs+cs/2-hz.w/2,y=r*cs+cs/2-hz.h/2;let ok=x>=1&&y>=1&&x+hz.w<=G2.pw-1&&y+hz.h<=G2.ph-1;
      if(ok)for(const o of G2.obstacles)if(x<o.x+o.w&&x+hz.w>o.x&&y<o.y+o.h&&y+hz.h>o.y){ok=false;break;}hz.pass[r*cols+c2]=ok?1:0;}hz.cols=cols;hz.rows=rows;hz.dist=new Int32Array(cols*rows);}
  const D=hz.dist;D.fill(-1);let pc=Math.floor(P.x/cs),pr2=Math.floor(P.y/cs);pc=Math.max(0,Math.min(cols-1,pc));pr2=Math.max(0,Math.min(rows-1,pr2));
  const q=[];const seed=(c2,r)=>{const k=r*cols+c2;if(c2<0||r<0||c2>=cols||r>=rows||D[k]>=0||!hz.pass[k])return;D[k]=0;q.push(k);};
  for(let rr=-2;rr<=2;rr++)for(let cc=-2;cc<=2;cc++)if(Math.abs(rr)+Math.abs(cc)<=2)seed(pc+cc,pr2+rr);
  for(let qi=0;qi<q.length;qi++){const k=q[qi],c2=k%cols,r=(k/cols)|0,d=D[k]+1;
    for(const [dc,dr] of [[1,0],[-1,0],[0,1],[0,-1]]){const nc=c2+dc,nr=r+dr;if(nc<0||nr<0||nc>=cols||nr>=rows)continue;const nk=nr*cols+nc;if(D[nk]>=0||!hz.pass[nk])continue;D[nk]=d;q.push(nk);}}}
function chaserStep(hz){const cs=6,cols=hz.cols,D=hz.dist,cx=hz.x+hz.w/2,cy=hz.y+hz.h/2,c2=Math.floor(cx/cs),r=Math.floor(cy/cs),k=r*cols+c2;
  let best=null,bd=D[k]>=0?D[k]:1e9;for(const [dc,dr] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]){const nc=c2+dc,nr=r+dr;if(nc<0||nr<0||nc>=cols||nr>=hz.rows)continue;const d=D[nr*cols+nc];
    if(d<0)continue;if(dc&&dr&&(D[r*cols+nc]<0||D[nr*cols+c2]<0))continue;const dd=d+(dc&&dr?0.4:0);if(dd<bd){bd=dd;best=[nc*cs+cs/2,nr*cs+cs/2];}}
  return best||[P.x,P.y];}
function chaserFree(hz,x,y){if(x<1||y<1||x+hz.w>G.pw-1||y+hz.h>G.ph-1)return false;for(const o of G.obstacles)if(x<o.x+o.w&&x+hz.w>o.x&&y<o.y+o.h&&y+hz.h>o.y)return false;return true;}
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){",KIT+"function buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("  balls:{balls:1},cannon:{cannon:1}});","  balls:{balls:1},cannon:{cannon:1},chaser:{chaser:1}});")
rep("    else if(H.balls){",
    "    else if(H.chaser){const C=CHASERS[h[3]]||CHASERS.grimshaw;g.hazards.push({kind:'chaser',skin:h[3]||'grimshaw',C,x:h[1],y:h[2],w:C.w,h:C.h,state:'wait',t:h[4]||5,map:0,say:3,anim:0,vx:0,vy:0,lunge:null,dir:[0,1]});}\n"
    "    else if(H.balls){")

# --- update ---
rep("    else if(hz.kind==='balls'){hz.t-=dt;",
r"""    else if(hz.kind==='chaser'){const C=hz.C;hz.t-=dt;hz.say-=dt;hz.anim+=dt;
      if(hz.state==='wait'){if(hz.t<=0){hz.state='chase';chaserMap(hz);hz.map=0.33;addFloat(hz.x+5,hz.y-18,'OI!','#ff4a4a',1.1);sfx('warn',0,{vol:0.5,rate:0.7});}continue;}
      if(hz.state==='gloat'){if(hz.t<=0)hz.state='chase';continue;}
      const late=1-Math.max(0,run.time)/G.def.time,base=moveSpeed()*(0.98+0.22*late)*C.speed*(isKidTool(tid)?1:0.85);
      const ci=Math.floor((hz.y+hz.h/2)/2)*G.cols+Math.floor((hz.x+hz.w/2)/2),deep=G.depth[ci]>0.4&&G.type[ci]!==T_BLOCK;
      if(hz.slow>0)hz.slow-=dt;const sp=base*(deep?0.55:1)*(hz.slow>0?0.7:1);
      const dx=P.x-(hz.x+hz.w/2),dy=P.y-(hz.y+hz.h/2),dist=Math.hypot(dx,dy);
      if(hz.say<=0&&dist<150){hz.say=rnd(4.5,7);hz.line=C.lines[(Math.random()*C.lines.length)|0];hz.lineT=1.6;}
      if(hz.lineT>0)hz.lineT-=dt;
      if(hz.state==='wind'){if(hz.t<=0){hz.state='lunge';hz.t=0.42;const n=Math.max(1,Math.hypot(hz.dir[0],hz.dir[1]));hz.vx=hz.dir[0]/n*base*2.4;hz.vy=hz.dir[1]/n*base*2.4;sfx('whoosh',0,{vol:0.5,rate:1.2});}continue;}
      if(hz.state==='lunge'){const nx=hz.x+hz.vx*dt,ny=hz.y+hz.vy*dt;if(chaserFree(hz,nx,ny)){hz.x=nx;hz.y=ny;}else hz.t=0;
        if(tid!=='ufo'&&P.inv<=0&&overlap(pr,{x:hz.x-1,y:hz.y-2,w:hz.w+2,h:hz.h+4})){hit('hz',SPILL_HAZARD*1.2);const red=bumperRed();P.spin=0.95*red+0.15;P.stun=Math.max(P.stun,P.spin);
          addFloat(hz.x+5,hz.y-20,C.catchLine,C.col,1.2);addFloat(P.x,P.y-30,'SPUN OUT!','#ff9aa8',1.1);sfx('stomp',0,{vol:0.6});hz.state='gloat';hz.t=3.4;hz.slow=3;hz.cool=4;run.caught=(run.caught||0)+1;continue;}
        if(hz.t<=0){hz.state='chase';hz.cool=1.5;}continue;}
      hz.map-=dt;if(hz.map<=0){chaserMap(hz);hz.map=0.33;}
      if(hz.cool>0)hz.cool-=dt;
      if(dist<36&&!(hz.cool>0)&&P.inv<=0){hz.state='wind';hz.t=0.5;hz.dir=[dx,dy];addFloat(hz.x+5,hz.y-14,'!','#ff4a4a',0.5);sfx('tick',0,{vol:0.6,rate:0.8});continue;}
      const tg=dist<14?[P.x,P.y]:chaserStep(hz),mx=tg[0]-(hz.x+hz.w/2),my=tg[1]-(hz.y+hz.h/2),ml=Math.hypot(mx,my)||1,stp=Math.min(ml,sp*dt);
      const ux=mx/ml*stp,uy=my/ml*stp;if(chaserFree(hz,hz.x+ux,hz.y+uy)){hz.x+=ux;hz.y+=uy;}else if(chaserFree(hz,hz.x+ux,hz.y)){hz.x+=ux;}else if(chaserFree(hz,hz.x,hz.y+uy)){hz.y+=uy;}
      hz.moving=stp>0.01;if(deep&&Math.random()<dt*10)particles.push({x:hz.x+hz.w/2,y:hz.y+hz.h,vx:rnd(-12,12),vy:rnd(-6,4),z:1,vz:rnd(10,25),life:0.4,t:0,kind:'snow'});
      continue;}
    else if(hz.kind==='balls'){hz.t-=dt;""")

# --- draw ---
rep("    else if(hz.kind==='balls')ents.push({base:hz.y+hz.h+1,draw:()=>{",
r"""    else if(hz.kind==='chaser')ents.push({base:hz.y+hz.h,draw:()=>{const C=hz.C,fr=C.frames[(hz.moving&&hz.state==='chase')||hz.state==='lunge'?Math.floor(hz.anim*8)%2:0];
        let sx=hx-C.ox,sy2=hy-C.oy;if(hz.state==='wind')sx+=Math.round(Math.sin(tNow*60));if(hz.state==='wait'&&Math.floor(tNow*3)%2)sy2-=1;
        R(b,hx-1,hy+hz.h-2,hz.w+2,2,'rgba(27,31,59,0.25)');b.drawImage(fr,sx,sy2);
        if(hz.state==='wind'&&Math.floor(tNow*12)%2===0)text(b,'!',hx+hz.w/2,sy2-9,'#ff4a4a',{align:'center'});
        if(hz.state==='gloat')text(b,'HMPH',hx+hz.w/2,sy2-8,'#ffffff',{align:'center'});
        if(hz.lineT>0&&hz.line){const tw=textW(hz.line)+6,lx=clamp(hx+hz.w/2-tw/2,1,G.pw-tw-1);R(b,lx,sy2-17,tw,9,K);R(b,lx+1,sy2-16,tw-2,7,'#ffffff');text(b,hz.line,lx+3,sy2-15,'#13306b',{outline:null});}}});
    else if(hz.kind==='balls')ents.push({base:hz.y+hz.h+1,draw:()=>{""")

# the hunted feeling: an arrow at the screen edge when she's off screen
rep("function drawWorld(dt){",
r"""function drawChaserArrows(){if(!G||!G.hazards)return;const top=camY,bot=camY+VIEW_H;for(const hz of G.hazards){if(hz.kind!=='chaser'||hz.state==='wait')continue;const cy=hz.y+hz.h/2;if(cy>top&&cy<bot)continue;
    const up=cy<=top,ax=clamp(Math.round(hz.x+hz.w/2),6,W-7),ay=up?VIEW_Y+3:VIEW_Y+VIEW_H-14,pulse=Math.floor(tNow*6)%2;
    for(let i=0;i<4;i++)R(b,ax-i,up?ay+i:ay+3-i,i*2+1,1,pulse?'#ff4a4a':'#ffd23f');const dd=Math.round(Math.abs(cy-(up?top:bot))/10);text(b,dd+'M',ax,up?ay+6:ay-8,'#ffffff',{align:'center'});}}
function drawWorld(dt){""")
rep("  drawHUD();drawBottomBar();","  drawChaserArrows();drawHUD();drawBottomBar();")
rep("drawRig(b,tid,P.x,P.y,P.f,","drawRig(b,tid,P.x,P.y,P.spin>0?(P.f+Math.floor(P.spin*14))%4:P.f,")
rep("P.bumpCd-=dt;if(P.stun>0)P.stun-=dt;","P.bumpCd-=dt;if(P.stun>0)P.stun-=dt;if(P.spin>0)P.spin-=dt;")
open(f,'w',encoding='utf-8').write(s);print('p48 ok')
