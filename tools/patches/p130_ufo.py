import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)

# ---------------------------------------------------------------------------------------------
# UFO rework (Alex, Nov 18). Testers: it floated over everything, so jobs took ~30 s with no bumps.
# 1. Buildings block it, everything else it floats over. One rule a kid gets instantly.
# 2. Buildings near the UFO glow, so you see what will stop you; bumping one says TOO BIG! and bounces.
# 3. A thinner beam that is not sped up to make up for it: clears ~86% of your best machine's rate.
# 4. Lighter drift (grip 3.2 -> 5): enough to feel like hovering, not enough to fight the controls.
# 5. The capstone: the UFO can't be got (test drive, parts, gems, cash, coins) until you've owned the
#    Icebreaker. Players who already have it keep it.
# ---------------------------------------------------------------------------------------------

# --- buildings: every sprite these make is marked, and obstacles made from them remember it
BLD=("houseSprite smallHouseSprite cabinSprite barnSprite churchSprite siloSprite buildingSprite bigBuilding mansionSprite "
     "storeSprite kioskSprite towerSprite chaletSprite castleSprite clockTowerSprite greenhouseSprite shedSprite hutSprite "
     "lighthouseSprite liftStationSprite museumSprite officeSprite pagodaSprite startHutSprite templeSprite warehouseSprite "
     "worksSprite windmillSprite iglooPropSprite grandstandSprite arcadeSprite boothSprite bigTopSprite marqueeSprite spireSprite").split()
for n in BLD: assert s.count('function '+n+'(')==1,n
rep("const UFO_GRIP=3.2;",
    "const UFO_GRIP=5;   // how fast the UFO's speed follows your finger (ice is 1.4; ground machines are instant)\n"
    "// buildings block the UFO; it floats over everything else\n"
    "const bldMark=fn=>function(){const c=fn.apply(this,arguments);if(c&&typeof c==='object')c.bld=1;return c;};\n"
    + "".join(f"{n}=bldMark({n});" for n in BLD) + "\n"
    "function ufoLocked(){if(save&&save.tool>=toolIdx('icebreaker'))save.ibEver=true;return !(save&&save.ibEver);}  // the UFO comes after the Icebreaker\n"
    "const UFO_BEAM=0.75;   // the UFO's beam is this much narrower than a normal ride, and not sped up to make up for it\n"
    "//")
rep("const ob=(sprC,sx,sy,fx,fy,fw,fh)=>{const fz=frostOf(sprC),o={spr:fz,src:sprC,sx,sy:sy-(fz.padTop||0),x:sx+fx,y:sy+fy,w:fw,h:fh};",
    "const ob=(sprC,sx,sy,fx,fy,fw,fh)=>{const fz=frostOf(sprC),o={spr:fz,src:sprC,sx,sy:sy-(fz.padTop||0),x:sx+fx,y:sy+fy,w:fw,h:fh,bld:!!(sprC&&sprC.bld)};")

# --- collision: only buildings (and the level edge) stop the UFO. Its body is the 22px disc you see
#     (its shadow), not the old 30px box, which never mattered while it ignored everything.
rep("ufo:{hw:15,hh:15,bt:0}}","ufo:{hw:11,hh:11,bt:0}}")
rep("  if(tool().id==='ufo')return null;\n  for(const cw of G.cows)",
    "  if(tool().id==='ufo'){for(const o of G.obstacles)if(o.bld&&overlap(r,o)&&!ignOK(r,o,o)){G.lastOb=o;return 'ob';}return null;}\n  for(const cw of G.cows)")
# bump feedback: TOO BIG! and a little bounce back
rep("if(Math.abs(P.vx)>full*0.5&&b==='ob'&&P.bumpCd<=0){P.bumpCd=0.8;hit('ob');}P.vx=0;}",
    "if(Math.abs(P.vx)>full*0.5&&b==='ob'&&P.bumpCd<=0){P.bumpCd=0.8;hit('ob');if(tid==='ufo')addFloat(clamp(P.x,34,G.pw-34),P.y-24,'TOO BIG!','#ff8fb0',0.9);}P.vx=tid==='ufo'?-P.vx*0.35:0;}")
rep("if(Math.abs(P.vy)>full*0.5&&b==='ob'&&P.bumpCd<=0){P.bumpCd=0.8;hit('ob');}P.vy=0;}",
    "if(Math.abs(P.vy)>full*0.5&&b==='ob'&&P.bumpCd<=0){P.bumpCd=0.8;hit('ob');if(tid==='ufo')addFloat(clamp(P.x,34,G.pw-34),P.y-24,'TOO BIG!','#ff8fb0',0.9);}P.vy=tid==='ufo'?-P.vy*0.35:0;}")
# the rule, said once at the start of the first few UFO runs
rep("if(!run.hoverShown){run.hoverShown=true;addFloat(P.x,P.y-22,'HOVERING: IT DRIFTS!','#7fe08a',1.4);}",
    "if(!run.hoverShown){run.hoverShown=true;if((save.ufoTips||0)<3){save.ufoTips=(save.ufoTips||0)+1;addFloat(G.pw/2,P.y-34,'FLOATS OVER SMALL THINGS','#7fe08a',2.6);addFloat(G.pw/2,P.y-25,'BUILDINGS BLOCK IT!','#ff8fb0',2.6);}}")

# --- buildings glow as the UFO gets close
rep("function outlineOf(sp){",
    "const TNC=new Map();function tintOf(sp,col){let m=TNC.get(col);if(!m){m=new WeakMap();TNC.set(col,m);}let c=m.get(sp);if(c)return c;c=document.createElement('canvas');c.width=sp.width;c.height=sp.height;const x=c.getContext('2d');x.drawImage(sp,0,0);x.globalCompositeOperation='source-in';x.fillStyle=col;x.fillRect(0,0,c.width,c.height);m.set(sp,c);return c;}\n"
    "function ufoGlowA(o){const dx=Math.max(o.x-P.x,0,P.x-(o.x+o.w)),dy=Math.max(o.y-P.y,0,P.y-(o.y+o.h));return clamp(1-(Math.hypot(dx,dy)-8)/42,0,1);}\n"
    "function outlineOf(sp){")
rep("for(const o of G.obstacles)if(o.sy+o.spr.height>top&&o.sy<bot){ents.push({base:o.base,draw:()=>{if(lkOutline()||(LOOK==='e'&&smallOb(o)))b.drawImage(outlineOf(o.spr),o.sx-1,o.sy-1);b.drawImage(bright(o.spr),o.sx,o.sy);}});",
    "for(const o of G.obstacles)if(o.sy+o.spr.height>top&&o.sy<bot){ents.push({base:o.base,draw:()=>{const ga=tid==='ufo'&&o.bld?ufoGlowA(o)*(0.6+0.4*Math.sin(tNow*7)):0;if(ga>0){b.globalAlpha=ga;const rim=tintOf(outlineOf(o.spr),'#ff4f7e');for(const [dx,dy] of [[-2,-1],[0,-1],[-1,-2],[-1,0]])b.drawImage(rim,o.sx+dx,o.sy+dy);b.globalAlpha=1;}else if(lkOutline()||(LOOK==='e'&&smallOb(o)))b.drawImage(outlineOf(o.spr),o.sx-1,o.sy-1);b.drawImage(bright(o.spr),o.sx,o.sy);if(ga>0){b.globalAlpha=ga*0.38;b.drawImage(tintOf(o.spr,'#ff8fb0'),o.sx,o.sy);b.globalAlpha=1;}}});")

# --- a thinner beam, not sped up to make up for it
rep("function rideTool(i){const t=TOOLS[i],b=rideBase(),w=Math.max(8,Math.min(80,Math.round(b.w*Math.sqrt(RIDE_BOOST)*(RIDE_WIDE[t.id]||1))));\n  return Object.assign({},t,{width:w,speed:Math.round(RIDE_BOOST*b.w*b.sp/w*10)/10,",
    "function rideTool(i){const t=TOOLS[i],b=rideBase(),ufo=t.id==='ufo',w=Math.max(8,Math.min(80,Math.round(b.w*Math.sqrt(RIDE_BOOST)*(ufo?UFO_BEAM:(RIDE_WIDE[t.id]||1)))));\n  return Object.assign({},t,{width:w,speed:ufo?Math.round(Math.sqrt(RIDE_BOOST)*b.sp*10)/10:Math.round(RIDE_BOOST*b.w*b.sp/w*10)/10,")
rep("wild?'BEST MACHINE +15%':", "wild?(t.id==='ufo'?'COINS +15%, THIN BEAM':'BEST MACHINE +15%'):")

# --- the capstone: no way to get the UFO before the Icebreaker
rep("function rideNextIdx(){for(let i=BASE_TOOLS;i<TOOLS.length;i++)if(!owns(i))return i;return -1;}",
    "function rideNextIdx(){for(let i=BASE_TOOLS;i<TOOLS.length;i++)if(!owns(i))return TOOLS[i].id==='ufo'&&ufoLocked()?-1:i;return -1;}")
# garage card and peek screen say so
rep("else{text(b,'???',x+37,y+6,'#7d6ab8',{outline:null});text(b,'A WILD RIDE',x+37,y+15,'#5a4a90',{outline:null});}\n      const sw=textW('WINTER '+t.winter)+6;R(b,x+w-sw-5,y+9,sw+2,13,isNext?'#e03a4e':'#3a2f60');R(b,x+w-sw-4,y+10,sw,11,isNext?'#1b1530':'#14102a');text(b,'WINTER '+t.winter,x+w-sw/2-4,y+13,isNext?'#ff8a98':'#5a4a90',{align:'center',outline:null});",
    "else if(t.id==='ufo'&&ufoLocked()){text(b,'LEGENDARY RIDE',x+37,y+6,'#ffd23f',{outline:null});text(b,'AFTER ICEBREAKER',x+37,y+15,'#c4a0f5',{outline:null});}\n      else{text(b,'???',x+37,y+6,'#7d6ab8',{outline:null});text(b,'A WILD RIDE',x+37,y+15,'#5a4a90',{outline:null});}\n"
    "      const sw=textW('WINTER '+t.winter)+6;if(!(t.id==='ufo'&&ufoLocked())){R(b,x+w-sw-5,y+9,sw+2,13,isNext?'#e03a4e':'#3a2f60');R(b,x+w-sw-4,y+10,sw,11,isNext?'#1b1530':'#14102a');text(b,'WINTER '+t.winter,x+w-sw/2-4,y+13,isNext?'#ff8a98':'#5a4a90',{align:'center',outline:null});}")
rep("else{text(b,'A WILD RIDE FOR WINTER '+t.winter,W/2,184,'#ffd23f',{align:'center',outline:null});",
    "else if(tid==='ufo'&&ufoLocked()){text(b,'THE LEGENDARY RIDE',W/2,184,'#ffd23f',{align:'center',outline:null});text(b,'UNLOCKS AFTER',W/2,200,'#ffffff',{align:'center',outline:null});text(b,'THE ICEBREAKER',W/2,210,'#ffffff',{align:'center',outline:null});}\n  else{text(b,'A WILD RIDE FOR WINTER '+t.winter,W/2,184,'#ffd23f',{align:'center',outline:null});")

open(f,'w',encoding='utf-8').write(s)
print('p130 UFO: buildings block it (glow + TOO BIG!), thin beam, lighter drift, unlocks after the Icebreaker')
