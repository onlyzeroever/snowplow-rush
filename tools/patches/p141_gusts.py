import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Alex, Nov 19 02:42 (playing the Blizzard preview): "If I'm moving up the gust doesn't really affect me, it's not
# dramatic or strong enough." Gusts were 16 px/s sideways, nothing next to driving speed. Now a gust:
#  - shoves you ~3x harder (52 px/s for small machines, ~38 for the biggest), in buffeting pulses, not a steady drift
#  - takes your grip: steering lags like on ice, and driving into it is 20% slower
#  - kicks the camera at the start and on each strong pulse, blows snow spray off the plow
#  - is unmistakable on screen: heavier white-out, sheets of snow sweeping across, more and longer wind streaks,
#    big GUST! warning with arrows down both sides
#  - comes a bit more often (calm 4.5-7 s instead of 5.5-8.5 s)

rep("else{z.wind+=(130*z.dir-z.wind)*Math.min(1,dt*4);if(z.t<=0){z.phase='calm';z.t=rnd(5.5,8.5);}\n"
    "      else{const hw=((VSPEC[tid]||{}).hw||6),ramp=Math.min(1,(2.6-z.t)/0.4,z.t/0.5+0.2),wx=z.dir*16/(1+Math.max(0,hw-6)/12)*ramp*dt;\n"
    "        if(wx&&!(P.stun>0)&&!blockedBy(footprint(tid,P.x+wx,P.y,P.f)))P.x+=wx;run.snowAcc+=G.def.snowfall*1.2*dt;}}",
    "else{const el=2.6-z.t,gs=0.72+0.22*Math.sin(el*9)+0.12*Math.sin(el*23);z.gs=gs;z.wind+=(170*z.dir*gs-z.wind)*Math.min(1,dt*5);if(z.t<=0){z.phase='calm';z.t=rnd(4.5,7);}\n"
    "      else{const hw=((VSPEC[tid]||{}).hw||6),ramp=Math.min(1,el/0.35,z.t/0.5+0.2),str=52/(1+Math.max(0,hw-6)/18)*ramp*gs,wx=z.dir*str*dt;z.str=str;\n"
    "        if(wx&&!(P.stun>0)){if(!blockedBy(footprint(tid,P.x+wx,P.y,P.f)))P.x+=wx;else if(!z.bonk){z.bonk=1;shake=Math.max(shake,0.15);addFloat(P.x,P.y-24,'WHOA!','#9fd8ff',0.8);}}\n"
    "        if(gs>0.98&&!z.kick){z.kick=1;shake=Math.max(shake,0.12);}else if(gs<0.8)z.kick=0;\n"
    "        if(Math.random()<dt*30)particles.push({x:P.x+rnd(-12,12),y:P.y+rnd(-10,6),vx:z.dir*rnd(70,130),vy:rnd(-10,10),z:rnd(2,12),vz:rnd(4,18),life:0.55,t:0,kind:'snow'});\n"
    "        run.snowAcc+=G.def.snowfall*1.2*dt;}}")
rep("else if(z.phase==='warn'){z.wind+=(40*z.dir-z.wind)*Math.min(1,dt*2);if(z.t<=0){z.phase='blow';z.t=2.6;sfx('whoosh',0,{vol:0.55,rate:0.7});shake=Math.max(shake,0.12);}}",
    "else if(z.phase==='warn'){z.wind+=(40*z.dir-z.wind)*Math.min(1,dt*2);if(z.t<=0){z.phase='blow';z.t=2.6;z.bonk=0;z.kick=0;sfx('whoosh',0,{vol:0.7,rate:0.6});shake=Math.max(shake,0.25);buzz(30);}}")

# grip: during a gust steering lags (like light ice) and driving into the wind is slower
rep("const dir=inputDir();let moving=false;const full=moveSpeed()*(run.boost?BOOST_SPEED:1);",
    "const dir=inputDir();let moving=false;const gust=!!(run.bz&&run.bz.phase==='blow'),full=moveSpeed()*(run.boost?BOOST_SPEED:1)*(gust?0.8:1);")
rep("  else{P.vx=tvx;P.vy=tvy;}\n  if(P.stun>0&&(!onIce||tid==='ufo')){P.vx=0;P.vy=0;}",
    "  else if(gust){const k=Math.min(1,dt*3.5);P.vx+=(tvx-P.vx)*k;P.vy+=(tvy-P.vy)*k;}\n  else{P.vx=tvx;P.vy=tvy;}\n  if(P.stun>0&&(!onIce||tid==='ufo')){P.vx=0;P.vy=0;}")

# look: heavier white-out, sweeping snow sheets, more/longer streaks, a big warning
rep("  if(blow){const a=0.12+0.08*Math.sin(tNow*7);b.fillStyle='rgba(240,246,255,'+a.toFixed(3)+')';b.fillRect(0,HUD_H,W,VIEW_H);}",
    "  if(blow){const g2=z.gs||1,a=0.12+0.14*g2+0.04*Math.sin(tNow*7);b.fillStyle='rgba(150,172,214,'+a.toFixed(3)+')';b.fillRect(0,HUD_H,W,VIEW_H);\n"
    "    for(let k=0;k<3;k++){const hh=26+k*14,yy=HUD_H+((k*97+Math.floor(tNow*0.7)*61)%(VIEW_H-hh)),span=W+160,xx=((tNow*(150+k*40)+k*90)%span)-120,sx=z.dir>0?xx:W-xx-120;\n"
    "      for(let r2=0;r2<hh;r2+=2){const fade=Math.sin(Math.PI*r2/hh);b.fillStyle='rgba(250,252,255,'+(0.38*fade*g2).toFixed(3)+')';b.fillRect(Math.round(sx+Math.sin((r2+tNow*20)/5)*6),yy+r2,120,2);}}}")
rep("for(let i=0;i<9;i++){const yy=HUD_H+20+((i*47+Math.floor(tNow*3)*13)%(VIEW_H-40)),ln=10+(i%3)*5,",
    "for(let i=0;i<(z.phase==='blow'?40:9);i++){const yy=HUD_H+12+((i*47+Math.floor(tNow*3)*13)%(VIEW_H-24)),ln=(z.phase==='blow'?16:10)+(i%3)*7,")
rep("if(Math.random()<k)R(b,sx,yy,ln,1,'rgba(120,150,200,0.55)');",
    "if(Math.random()<k){if(z.phase==='blow'){R(b,sx,yy,ln,1,'#ffffff');R(b,sx,yy+1,ln,1,'rgba(90,120,180,0.55)');}else R(b,sx,yy,ln,1,'rgba(110,140,195,0.7)');}")
rep("  if(z.phase==='warn'&&Math.floor(tNow*6)%2===0){const yy=HUD_H+VIEW_H/2-20;for(let k=0;k<3;k++){const ax=z.dir>0?6+k*8:W-12-k*8;text(b,z.dir>0?'>':'<',ax,yy,'#9fd8ff');text(b,z.dir>0?'>':'<',ax,yy+30,'#9fd8ff');}}}",
    "  if(z.phase==='warn'&&Math.floor(tNow*6)%2===0){for(let r2=0;r2<4;r2++){const yy=HUD_H+30+r2*Math.round((VIEW_H-60)/3);for(let k=0;k<3;k++){const ax=z.dir>0?4+k*9:W-12-k*9;text(b,z.dir>0?'>':'<',ax,yy,'#ffffff',{scale:2});}}\n"
    "    text(b,'GUST!',W/2,HUD_H+46,'#ffffff',{align:'center',scale:3});}}")
# the old small floating "GUST >>>" is replaced by the big banner
rep("sfx('warn');addFloat(clamp(P.x,40,G.pw-40),P.y-26,z.dir>0?'GUST >>>':'<<< GUST','#9fd8ff',1.3);",
    "sfx('warn');")

open(f,'w',encoding='utf-8').write(s)
print('p141 gusts: 3x stronger, buffeting, grip loss, bigger warning and white-out')
