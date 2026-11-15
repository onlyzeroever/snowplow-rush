import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:80],s.count(a));s=s.replace(a,b_)
# Effects pass (Nov 16), built on the "juice" pros use: impacts you feel (hit-stop, burst, puffs, dizzy stars),
# rewards that celebrate (confetti, spinning coins, sparkle rings), sparkles that twinkle, pop-up text that pops.
# Everything stays short (<0.5s) and small so it never hides the snow.
# --- new / better particle kinds -------------------------------------------------------------------------------
rep("case 'coin':b.drawImage(SPR.coinS,px-2,py-2);break;",
    "case 'coin':{const ph=Math.floor(p.t*12+(p.y|0))%4;if(ph===1||ph===3){R(b,px-1,py-2,2,5,K);R(b,px,py-1,1,3,ph===1?'#ffd23f':'#e8b84a');}else b.drawImage(SPR.coinS,px-2,py-2);}break;")
rep("case 'spark':if(Math.floor(p.t*20)%2===0){R(b,px,py-1,1,3,k<0.5?'#ffffff':'#ffd23f');R(b,px-1,py,3,1,k<0.5?'#ffffff':'#ffd23f');}break;",
    "case 'spark':{const c2=p.c||'#ffd23f',s2=k<0.2?1:k<0.62?2:k<0.88?1:0;R(b,px,py,1,1,'#ffffff');if(s2>=1){R(b,px-1,py,1,1,c2);R(b,px+1,py,1,1,c2);R(b,px,py-1,1,1,c2);R(b,px,py+1,1,1,c2);}if(s2>=2){R(b,px-2,py,1,1,c2);R(b,px+2,py,1,1,c2);R(b,px,py-2,1,1,c2);R(b,px,py+2,1,1,c2);R(b,px-1,py-1,1,1,'#fff8c0');R(b,px+1,py+1,1,1,'#fff8c0');}}break;\n"
    "      case 'pow':{if(k<0.85){const r=k<0.3?3+Math.round(k/0.3*5):8-Math.round((k-0.3)/0.7*4);for(let a=0;a<8;a++){const t=a/8*Math.PI*2+0.39,rr=a%2?r:r-3;for(let d=Math.max(1,rr-3);d<=rr;d++){const ex=Math.round(Math.cos(t)*d),ey=Math.round(Math.sin(t)*d*0.8);R(b,px+ex,py+ey,1,1,d===rr?(a%2?'#ffd23f':'#ffffff'):'#ffffff');}}R(b,px-2,py-1,5,3,k<0.4?'#ffffff':'#ffe27a');R(b,px-1,py-2,3,5,k<0.4?'#ffffff':'#ffe27a');}}break;\n"
    "      case 'conf':{const fl=Math.floor(p.t*10+(p.y|0))%2;R(b,px,py,fl?2:1,fl?1:2,p.c||'#ff4fa3');}break;\n"
    "      case 'ring':{const r=Math.round(2+k*(p.r||8));b.fillStyle=k<0.5?'#ffffff':'#c6d9f3';for(let a=0;a<20;a++){if(k>0.65&&a%2)continue;const t=a/20*Math.PI*2;b.fillRect(px+Math.round(Math.cos(t)*r),py+Math.round(Math.sin(t)*r*0.6),1,1);}}break;")
rep("case 'fw':R(b,px,py,1,1,p.c);if(k<0.5)R(b,px,py-1,1,1,'#ffffff');break;",
    "case 'fw':R(b,px,py,1,1,p.c);if(k<0.5)R(b,px,py-1,1,1,'#ffffff');if(k<0.8){b.globalAlpha=0.45;R(b,Math.round(px-p.vx*0.04),Math.round(py-p.vy*0.04),1,1,p.c);b.globalAlpha=1;}break;")
rep("case 'debris':R(b,px,py,2,2,(p.x|0)%2?'#7a4a2a':'#8793a8');break;",
    "case 'debris':R(b,px,py,2,2,p.c||((p.x|0)%2?'#7a4a2a':'#8793a8'));R(b,px,py,1,1,'rgba(255,255,255,0.35)');R(b,px+1,py+1,1,1,'rgba(27,31,59,0.35)');break;")
# confetti flutters down instead of dropping like a stone
rep("for(const p of particles){p.t+=dt;","for(const p of particles){if(p.kind==='conf'){if(p.vz<-24)p.vz=-24;p.vx*=Math.pow(0.3,dt);p.x+=Math.sin(p.t*11+p.y)*0.3;}p.t+=dt;")
# --- impacts: hit-stop, burst at the contact point, puffs thrown back, dizzy stars while stunned ---------------
rep("function hit(kind,spill){\n  if(P.inv>0)return;",
    "function hitFx(){const fp=footprint(tool().id,P.x,P.y,P.f),cx=[fp.x+fp.w/2,fp.x+fp.w,fp.x+fp.w/2,fp.x][P.f],cy=[fp.y,fp.y+fp.h/2,fp.y+fp.h,fp.y+fp.h/2][P.f],dx=[0,1,0,-1][P.f],dy=[-1,0,1,0][P.f];\n"
    "  particles.push({x:cx,y:cy-2,vx:0,vy:0,z:0,vz:0,life:0.3,t:0,kind:'pow'});for(let k=0;k<5;k++)particles.push({x:cx,y:cy,vx:rnd(-26,26)-dx*30,vy:rnd(-18,18)-dy*24,z:3,vz:rnd(30,60),life:0.45,t:0,kind:'snow'});HITSTOP=0.06;}\n"
    "let HITSTOP=0;\nfunction hit(kind,spill){\n  if(P.inv>0)return;hitFx();")
rep("if(state==='play'&&!paused&&!settingsOpen)updatePlay(dt);","if(state==='play'&&!paused&&!settingsOpen){if(HITSTOP>0)HITSTOP-=dt;else updatePlay(dt);}")
rep("ents.push({base:fp.y+fp.h,draw:()=>drawRig(b,tid,P.x,P.y,P.spin>0?(P.f+Math.floor(P.spin*14))%4:P.f,bwPx,pl,P.bob,tid==='mech'?(P.step|0):P.fr,(P.stun>0||P.inv>0)&&Math.floor(tNow*20)%2===0)});",
    "ents.push({base:fp.y+fp.h,draw:()=>{drawRig(b,tid,P.x,P.y,P.spin>0?(P.f+Math.floor(P.spin*14))%4:P.f,bwPx,pl,P.bob,tid==='mech'?(P.step|0):P.fr,(P.stun>0||P.inv>0)&&Math.floor(tNow*20)%2===0);\n"
    "      if(P.stun>0){const top=Math.min(fp.y,P.y-12)-8;for(let k=0;k<3;k++){const t=tNow*7+k*2.09,sx=Math.round(P.x+Math.cos(t)*7),sy=Math.round(top+Math.sin(t)*2.5),front=Math.sin(t)>0;R(b,sx,sy-1,1,3,front?'#ffd23f':'#c98a12');R(b,sx-1,sy,3,1,front?'#ffd23f':'#c98a12');R(b,sx,sy,1,1,front?'#ffffff':'#ffe27a');}}}});")
# --- rewards ------------------------------------------------------------------------------------------------------
rep("buzz(20);for(let k=0;k<10;k++)particles.push({x:pr.x,y:pr.y,vx:rnd(-40,40),vy:rnd(-30,30),z:2,vz:rnd(40,80),life:0.7,t:0,kind:Math.random()<0.5?'coin':'snow'});",
    "buzz(20);const CF=['#ff4fa3','#ffd23f','#7ad3ff','#9cff7a','#ff7a3a','#ffffff'];for(let k=0;k<24;k++)particles.push({x:pr.x,y:pr.y,vx:rnd(-55,55),vy:rnd(-25,25),z:4,vz:rnd(25,60),life:rnd(1.0,1.4),t:0,kind:'conf',c:CF[k%6]});\n"
    "  for(let k=0;k<5;k++)particles.push({x:pr.x,y:pr.y,vx:rnd(-30,30),vy:rnd(-20,20),z:2,vz:rnd(50,80),life:0.6,t:0,kind:'coin'});particles.push({x:pr.x,y:pr.y,vx:0,vy:0,z:0,vz:0,life:0.32,t:0,kind:'ring',r:12});")
# crunch: chunks in the crushed prop's own colours, plus a burst and a ring
rep("for(let k=0;k<12;k++)particles.push({x:o.x+o.w/2,y:o.y+o.h/2,vx:rnd(-50,50),vy:rnd(-40,40),z:2,vz:rnd(40,80),life:0.7,t:0,kind:k%3?'debris':'coin'});",
    "const cs=[];try{const sp=o.spr,d=sp.getContext('2d').getImageData(0,0,sp.width,sp.height).data;for(let k=0;k<60&&cs.length<6;k++){const qx=(Math.random()*sp.width)|0,qy=(Math.random()*sp.height)|0,ii=(qy*sp.width+qx)*4;if(d[ii+3]>200&&!(d[ii]<40&&d[ii+1]<40&&d[ii+2]<70))cs.push('rgb('+d[ii]+','+d[ii+1]+','+d[ii+2]+')');}}catch(e){}\n"
    "  const ccx=o.x+o.w/2,ccy=o.y+o.h/2;particles.push({x:ccx,y:ccy-2,vx:0,vy:0,z:0,vz:0,life:0.3,t:0,kind:'pow'},{x:ccx,y:ccy,vx:0,vy:0,z:0,vz:0,life:0.3,t:0,kind:'ring',r:10});\n"
    "  for(let k=0;k<14;k++)particles.push({x:ccx,y:ccy,vx:rnd(-50,50),vy:rnd(-40,40),z:2,vz:rnd(40,85),life:0.7,t:0,kind:k%4===3?'coin':'debris',c:cs.length?cs[k%cs.length]:null});")
# snowball splat + squall dump get a soft impact ring
rep("sfx('splat',0,{vol:0.8});addSnowCircle(G,b.x1,b.y1,5,0.8);","sfx('splat',0,{vol:0.8});addSnowCircle(G,b.x1,b.y1,5,0.8);particles.push({x:b.x1,y:b.y1,vx:0,vy:0,z:0,vz:0,life:0.3,t:0,kind:'ring',r:8});")
rep("s.dumped=true;addSnowCircle(G,s.x,s.y,s.r,0.75);sfx('flump');","s.dumped=true;addSnowCircle(G,s.x,s.y,s.r,0.75);sfx('flump');particles.push({x:s.x,y:s.y,vx:0,vy:0,z:0,vz:0,life:0.4,t:0,kind:'ring',r:s.r});")
# pop-up text: a quick bounce and a white flash when it appears
rep("for(const f of floats){if(f.t>f.life*0.7&&Math.floor(f.t*16)%2)continue;text(b,f.s,f.x,f.y,f.c,{align:'center'});}",
    "for(const f of floats){if(f.t>f.life*0.7&&Math.floor(f.t*16)%2)continue;const pop=f.t<0.16?Math.round(Math.sin(f.t/0.16*Math.PI)*3):0;text(b,f.s,f.x,f.y-pop,f.t<0.05?'#ffffff':f.c,{align:'center'});}")
rep("if(kind==='ob'){addFloat(P.x,P.y-20,bmp?'BUMPER!':'BONK!',","if(kind==='ob'){addFloat(P.x,P.y-27,bmp?'BUMPER!':'BONK!',")
# Bug found while testing (Nov 16): props are stored as their frosted copy, so "is this a gnome/mailbox/cone...?" checks
# compared against the unfrosted sprite and never matched. The Monster Truck could only crush junkyard wrecks, and the
# gnome trophy could never be earned. Obstacles now remember their source sprite.
rep("const ob=(sprC,sx,sy,fx,fy,fw,fh)=>{const fz=frostOf(sprC),o={spr:fz,sx,","const ob=(sprC,sx,sy,fx,fy,fw,fh)=>{const fz=frostOf(sprC),o={spr:fz,src:sprC,sx,")
rep("[SPR.gnome,SPR.mailbox,SPR.hydrant,SPR.trash,SPR.snowman,CONE,BARREL,TIRES,HAY].includes(o.spr)","[SPR.gnome,SPR.mailbox,SPR.hydrant,SPR.trash,SPR.snowman,CONE,BARREL,TIRES,HAY].includes(o.src)")
rep("G.lastOb.spr===SPR.gnome","G.lastOb.src===SPR.gnome")
open(f,'w',encoding='utf-8').write(s)
print('p105 effects pass')
