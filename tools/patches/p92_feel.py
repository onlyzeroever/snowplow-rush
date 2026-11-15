import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)
# Game feel pass (Nov 16):
#  - coin totals count up/down smoothly instead of jumping (top bar on every screen and in jobs)
#  - while you plow, coins fly from the machine up into the coin counter, which bumps as they land; big bonuses
#    (CRUNCH!, JAMMED!...) send a burst
#  - results: coins earned and the bonus lines count up after the % does; each star lands with a pixel sparkle
#    burst and a 1px panel thump; ALL CLEAR! pops in
# Buttons already squash 1px on press and bumps already shake the view; both kept.
rep("function earn(v){if(run&&run.challenge)return;save.coins+=v;run.earned+=v;}",
    "function earn(v){if(run&&run.challenge)return;save.coins+=v;run.earned+=v;if(state==='play'&&P){FLY.acc+=v;if(v>=Math.max(20,12*valueMult()))FLY.burst=Math.min(6,FLY.burst+4);}}\n"
    "const FLY={list:[],acc:0,t:0,burst:0,bump:0,disp:null};\n"
    "function flySpawn(){const sx=P.x+rnd(-4,4),sy=P.y-camY+VIEW_Y+rnd(-6,2);FLY.list.push({sx,sy,cx:sx+rnd(-30,10),cy:Math.min(sy,VIEW_Y+40)-rnd(20,40),t:0,dur:rnd(0.42,0.6)});}\n"
    "function flyUpdate(dt){FLY.t-=dt;if(FLY.burst>0&&FLY.list.length<18){flySpawn();FLY.burst--;}else if(FLY.acc>0&&FLY.t<=0&&FLY.list.length<14){flySpawn();FLY.t=0.16;FLY.acc=0;}\n"
    "  for(const c of FLY.list)c.t+=dt;const n=FLY.list.length;FLY.list=FLY.list.filter(c=>c.t<c.dur);if(FLY.list.length<n)FLY.bump=0.12;}\n"
    "function drawCoinFly(){for(const c of FLY.list){const k=Math.min(1,c.t/c.dur),e=k*k,u=1-e,tx=6,ty=8;const x=u*u*c.sx+2*u*e*c.cx+e*e*tx,y=u*u*c.sy+2*u*e*c.cy+e*e*ty;b.drawImage(k<0.85?SPR.coin:SPR.coinS,Math.round(x)-1,Math.round(y)-1);}}\n"
    "function coinsShown(){return Math.floor(FLY.disp==null?save.coins:FLY.disp);}")
rep("tNow+=dt;if(pressT>0)pressT-=dt;",
    "tNow+=dt;if(pressT>0)pressT-=dt;{if(FLY.disp==null)FLY.disp=save.coins;const d=save.coins-FLY.disp;if(Math.abs(d)<1)FLY.disp=save.coins;else FLY.disp+=d*Math.min(1,dt*7)+Math.sign(d)*Math.min(Math.abs(d),dt*3);if(FLY.bump>0)FLY.bump-=dt;if(state!=='play'){FLY.list=[];FLY.acc=0;FLY.burst=0;}}")
rep("function updateFx(dt){","function updateFx(dt){flyUpdate(dt);")
rep("drawChaserArrows();drawHUD();drawBottomBar();","drawChaserArrows();drawHUD();drawBottomBar();drawCoinFly();")
rep("b.drawImage(SPR.coin,5,7);text(b,fmt(save.coins),14,8,'#ffffff');",
    "b.drawImage(SPR.coin,5,FLY.bump>0?6:7);text(b,fmt(coinsShown()),14,8,FLY.bump>0?'#ffd23f':'#ffffff');")
rep("text(b,fmt(save.coins),x+14,y+6,'#ffffff');","text(b,fmt(coinsShown()),x+14,y+6,'#ffffff');")
rep("if(!run.challenge){save.coins+=coins;run.earned+=coins;run.pending+=coins;}","if(!run.challenge){save.coins+=coins;run.earned+=coins;run.pending+=coins;FLY.acc+=coins;}")
rep("save.coins+=c;run.earned+=c;addFloat(pr.x,pr.y-10,'GIFT +'","save.coins+=c;run.earned+=c;FLY.burst=Math.min(6,FLY.burst+4);addFloat(pr.x,pr.y-10,'GIFT +'")
# results
rep("const py=Math.max(44,Math.round(44+(1-Math.min(1,t*4))*60));",
    "let land=0;for(let s2=0;s2<r.stars;s2++){const d2=t-(0.9+s2*0.35);if(d2>=0&&d2<0.07)land=1;}const py=Math.max(44,Math.round(44+(1-Math.min(1,t*4))*60))+land;")
rep("text(b,r.allClear?'ALL CLEAR!':close?'SO CLOSE!':\"TIME'S UP!\",W/2,py+10,r.allClear?'#7fe08a':close?'#ffd23f':'#ffffff',{align:'center',scale:2});",
    "{const popT=r.allClear&&t>0.25&&t<0.37;text(b,r.allClear?'ALL CLEAR!':close?'SO CLOSE!':\"TIME'S UP!\",W/2,py+10-(popT?3:0),r.allClear?'#7fe08a':close?'#ffd23f':'#ffffff',{align:'center',scale:popT?3:2});}")
rep("b.drawImage(img,Math.round(W/2-36+s*27-sz/2+9),py+74-(sc-2)*4,sz,sz);",
    "b.drawImage(img,Math.round(W/2-36+s*27-sz/2+9),py+74-(sc-2)*4,sz,sz);if(on){const dd=t-appear;if(dd<0.38){const cx=Math.round(W/2-36+s*27+9),cy=py+83,rr=7+dd*46;for(let q=0;q<6;q++){const an=q/6*Math.PI*2+s,qx=Math.round(cx+Math.cos(an)*rr),qy=Math.round(cy+Math.sin(an)*rr*0.8),col=q%2?'#ffffff':'#ffd23f';if(dd<0.26){R(b,qx-1,qy,3,1,col);R(b,qx,qy-1,1,3,col);}else R(b,qx,qy,1,1,col);}}}")
rep("b.drawImage(SPR.coin,24,py+108);text(b,'+'+fmt(run.earned),34,py+109,'#ffd23f');",
    "b.drawImage(SPR.coin,24,py+108);text(b,'+'+fmt(Math.floor(run.earned*Math.min(1,Math.max(0,(t-0.8)/0.9)))),34,py+109,'#ffd23f');")
rep("let ly=py+122;if(r.bonus>0){text(b,'NEW STARS +'+fmt(r.bonus),W/2,ly,'#7fe08a',{align:'center'});ly+=10;}",
    "let ly=py+122;if(r.bonus>0){if(t>1.9)text(b,'NEW STARS +'+fmt(Math.floor(r.bonus*Math.min(1,(t-1.9)/0.5))),W/2,ly,'#7fe08a',{align:'center'});ly+=10;}")
rep("if(r.timeBonus>0){text(b,'TIME BONUS +'+fmt(r.timeBonus),W/2,ly,'#7fe08a',{align:'center'});ly+=10;}",
    "if(r.timeBonus>0){if(t>2.1)text(b,'TIME BONUS +'+fmt(Math.floor(r.timeBonus*Math.min(1,(t-2.1)/0.5))),W/2,ly,'#7fe08a',{align:'center'});ly+=10;}")
open(f,'w',encoding='utf-8').write(s)
print('p92 game feel')
