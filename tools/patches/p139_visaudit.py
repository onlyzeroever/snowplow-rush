import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Alex, Nov 19 01:17: "audit so there's no more visual bugs like this, things disconnected etc."
# Full visual audit of all 125 jobs (tools/audit/visaudit.js, motion.js, film.js + an eyeball pass of every map).
# Fixes, all in one go:
#  - string lights, banners and lantern strings get a post wherever an end hangs in the air (pixel test, not box test)
#  - gondola cable: a bullwheel station at each loose end; chairlift cable now runs into the LIFT station
#  - Moonlit Ranch: the glowing pools on the path now come from lamp posts
#  - taxis no longer drive through a parked van, cones, roadworks, a broken-down car or the village church
#  - props that were buried inside shop buildings (some poking out of roofs) removed
#  - boats no longer sit in a white box of snow on a cleared yard
#  - ghost-train rails end in a buffer stop; mill roads cross the river on a bridge; Gull Island lighthouse on rocks;
#    Skyline water steps no longer run under a tower; Igloo Village mosaic no longer split by the path

# ---------- shared helpers ----------
rep("function lampSprite(",
    "function sprAlpha(c){if(!c._al){const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data,a=new Uint8Array(c.width*c.height);for(let k=0;k<a.length;k++)a[k]=d[k*4+3]>60?1:0;c._al=a;}return c._al;}\n"
    "function solidNear(x,y,up,dn,dxr,noWild){for(const q of G.obstacles.concat(G.scenery)){if(noWild&&q.wild)continue;if(x<q.sx-dxr-1||x>q.sx+q.spr.width+dxr+1||y+dn<q.sy||y-up>q.sy+q.spr.height)continue;const a=sprAlpha(q.spr),w=q.spr.width,h=q.spr.height;\n"
    "  for(let dy=-up;dy<=dn;dy++)for(let dx=-dxr;dx<=dxr;dx++){const lx=Math.round(x+dx-q.sx),ly=Math.round(y+dy-q.sy);if(lx>=0&&ly>=0&&lx<w&&ly<h&&a[ly*w+lx])return true;}}return false;}\n"
    "function overPosts(o){const P=[],a=sprAlpha(o.spr),w=o.spr.width,h=o.spr.height;for(const lx of [0,w-1]){let ty=-1;for(let y=0;y<h;y++)if(a[y*w+lx]){ty=y;break;}if(ty<0)continue;\n"
    "  const ex=o.sx+lx,ey=o.sy+ty;if(ex<=3||ex>=G.pw-4)continue;if(solidNear(ex,ey,2,8,2))continue;P.push([ex,ey]);}return P;}\n"
    "function cableTerms(o){const a=sprAlpha(o.spr),w=o.spr.width,h=o.spr.height,T=[];let y0=-1,y1=-1;for(let y=0;y<h&&y0<0;y++)for(let x=0;x<w;x++)if(a[y*w+x]){y0=y;break;}for(let y=h-1;y>=0&&y1<0;y--)for(let x=0;x<w;x++)if(a[y*w+x]){y1=y;break;}\n"
    "  if(y0<0)return T;const cx=o.sx+(w>>1);for(const ey of [o.sy+y0,o.sy+y1]){if(ey<=6||ey>=G.ph-6)continue;if(solidNear(cx,ey,10,10,12,true))continue;T.push([cx,ey]);}return T;}\n"
    "function cableTermSpr(){if(cableTermSpr.c)return cableTermSpr.c;const c=mk(26,22),g=c.getContext('2d');R(g,1,8,24,13,K);R(g,2,9,22,11,'#8793a8');R(g,2,9,22,2,'#c6d0e0');R(g,2,18,22,2,'#5a6478');R(g,10,13,6,7,K);R(g,11,14,4,6,'#3a3f52');\n"
    "  R(g,0,7,26,2,K);R(g,1,7,24,1,PAL.W);g.fillStyle=K;pixCircle(g,13,6,6);g.fillStyle='#d8364b';pixCircle(g,13,6,5);g.fillStyle=K;pixCircle(g,13,6,2);R(g,12,5,2,2,'#c6d0e0');cableTermSpr.c=c;return c;}\n"
    "function lampSprite(")

# ---------- 1. posts under every hanging string end (lights, banners, lantern strings) ----------
rep("""  for(const o of G.over)if((o.k==='lights'||o.k==='banner')&&o.sy+30>top&&o.sy<bot){if(!o.posts){o.posts=[];for(const ex of [o.sx,o.sx+o.spr.width-1]){if(ex<=3||ex>=G.pw-4)continue;const ey=o.sy+(o.k==='banner'?2:1);
      if(G.obstacles.some(q=>ex>=q.sx-1&&ex<=q.sx+q.spr.width&&ey+6>=q.sy&&ey<=q.sy+q.spr.height))continue;o.posts.push([ex,ey]);}}""",
"""  for(const o of G.over)if((o.k==='lights'||o.k==='banner'||o.k==='lant')&&o.sy+30>top&&o.sy<bot){if(!o.posts)o.posts=overPosts(o);""")

# ---------- 2. cable stations at loose gondola / chairlift ends (drawn above the cable) ----------
rep("b.globalAlpha=un?0.4:1;b.drawImage(bright(o.spr),o.sx,o.sy);b.restore();}",
    "b.globalAlpha=un?0.4:1;b.drawImage(bright(o.spr),o.sx,o.sy);b.restore();\n"
    "    if(o.k==='gondola'||o.k==='liftline'){if(!o.terms)o.terms=cableTerms(o);for(const [tx,ty] of o.terms)if(ty>top-24&&ty<bot+24){R(b,tx-12,ty+11,26,2,'rgba(40,50,90,0.25)');b.drawImage(cableTermSpr(),tx-13,ty-11);}}}")

# ---------- 3. Moonlit Ranch: path light pools come from lamp posts ----------
rep("if(big){for(let y=40;y<ph;y+=300)g.lights.push({x:90,y,r:30,c:'#9fd8ff'});",
    "if(big){for(let y=40;y<ph;y+=300){ob(lampSprite(),101,y-3,1,22,5,6);g.lights.push({x:104,y,r:30,c:'#9fd8ff'});}")

# ---------- 4. taxis: village car no longer drives through the church green; motorway cones/broken-down cars out of the taxi lanes ----------
rep("g.hazards.push({kind:'taxi',x:80,y:-60,w:22,h:28,vy:36,dir:1,spr:carSprite('#d8364b','#9c2a45',false,false)});","")
rep("for(let y=300;y<ph-100;y+=380){const lane=[24,46,68,96,118,140][hash(y,3)%6];for(let k=0;k<3;k++)ob(CONE,lane+k*6,y+k*10,1,4,5,5);}",
    "const carLane=y=>93;for(let y=300;y<ph-100;y+=380){let lane=[68,96][hash(y,3)%2];const cy2=Math.round(y/900)*900;if(cy2>=900&&Math.abs(cy2-y)<70&&Math.abs(carLane(cy2)-lane)<10)lane=lane===68?96:68;for(let k=0;k<3;k++)ob(CONE,lane+k*6,y+k*10,1,4,5,5);}")
rep("for(let y=900;y<ph-100;y+=900)ob(carSprite(...cc[(y/900)%4]),hash(y,1)%2?22:136,y,1,2,22,28);",
    "for(let y=900;y<ph-100;y+=900)ob(carSprite(...cc[(y/900)%4]),carLane(y),y,1,2,22,28);")

# ---------- 5. map data fixes ----------
rep("  if(L.data){buildFromData(g,L.data,setT,ob,setCircle,paintText);}",
    "  if(L.data){dataFix(L);buildFromData(g,L.data,setT,ob,setCircle,paintText);}")
rep("function sprAlpha(c){",
"""// visual audit fixes to job data (Nov 19): applied once, before a job is first built
const DATAFIX={
  junction:[['hz','taxi',20,300,{1:42}]],                  // taxi drove through a parked van and its cones
  cityhall:[['hz','taxi',34,1600,{1:54}]],                 // taxi drove through the roadworks
  lift:[['ov','liftline',138,157,{2:86,3:3677}]],          // chairlift cable now starts at the LIFT station
  igloos:[['pathend',0,480]],                              // path no longer splits the plaza mosaic
  haunted:[['add','decals',['buffer',150,596]]],           // ghost-train rails end in a buffer stop
  gullisland:[['add','circles',['stone',90,182,22]]],      // lighthouse stands on rocks, not open ice
  mill:[['add','ground',['deck',140,900,40,40]],['add','ground',['deck',140,1240,40,40]]], // bridges over the river
  skyline:[['groundw',74,360,680,56]],                     // water steps stop short of the tower
  // props buried inside shop buildings (some poked out of the roof)
  chinatown:[['del','tlight',6,1318],['del','tlight',168,1318],['del','lantpost',46,650]],
  carousel:[['del','kiosk',2,2240],['del','popcorn',160,2300],['del','kiosk',2,2380],['del','popcorn',160,2440],['del','kiosk',2,2520]],
  bumpers:[['del','kiosk',150,2200]],
  food:[['del','foodtruck',4,980],['del','foodtruck',150,1940],['del','kiosk',4,1180]],
  coaster:[['del','lamp',140,1650]],openingday:[['del','popcorn',32,2496]],drawbridge:[['del','lamp',136,720]],
  shipyard:[['del','pots',168,2314],['del','barrel',133,2683],['del','barrel',125,2312],['hz','cannon',2,1300,{1:58}]], // snow cannon fired out of a wall
  // animals that started inside a fence, an iceberg or a fountain and never moved
  stables:[['hz','sheep',136,820,{1:132,3:2}]],harvestfair:[['hz','sheep',128,1370,{1:112}]],
  penguins:[['hz','peng',90,5840,{1:60}]],gardens2:[['hz','peng',90,2560,{2:2600}]],
  // pallets hanging off the edge of the quay (only a sliver showed)
  customs:[['del','pallet',175,2810]],ferry:[['del','pallet',173,1374]]};
function dataFix(L){const D=L.data,F=DATAFIX[L.id];if(!F||D._fx)return;D._fx=1;
  for(const op of F){const [k]=op;
    if(k==='mv'){const p=(D.props||[]).find(p=>p[0]===op[1]&&p[1]===op[2]&&p[2]===op[3]);if(p){p[1]=op[4];p[2]=op[5];}}
    else if(k==='del'){const i=(D.props||[]).findIndex(p=>p[0]===op[1]&&p[1]===op[2]&&p[2]===op[3]);if(i>=0)D.props.splice(i,1);}
    else if(k==='hz'){const h=(D.hazards||[]).find(h=>h[0]===op[1]&&h[1]===op[2]&&h[2]===op[3]);if(h)for(const j in op[4])h[j]=op[4][j];}
    else if(k==='ov'){const o=(D.over||[]).find(o=>o[0]===op[1]&&o[1]===op[2]&&o[2]===op[3]);if(o)for(const j in op[4])o[j]=op[4][j];}
    else if(k==='add'){(D[op[1]]=D[op[1]]||[]).push(op[2]);}
    else if(k==='pathend'){const p=D.paths&&D.paths[op[1]];if(p){let n=p.length;while(n>4&&p[n-1]<op[2])n-=2;p.length=n;}}
    else if(k==='groundw'){for(const r of D.ground||[])if(r[1]===op[1]&&r[2]>=op[2]&&r[2]<op[3])r[3]=op[4];}}}
function sprAlpha(c){""")
rep("  rails:(a)=>{",
    "  buffer:()=>{const c=mk(16,8),g=c.getContext('2d');R(g,0,1,16,6,K);for(let x=1;x<15;x++)R(g,x,2,1,4,(x>>1)%2?'#f4f8ff':'#d8364b');R(g,1,6,3,2,K);R(g,12,6,3,2,K);return c;},\n  rails:(a)=>{")

# ---------- 6. boats: transparent corners of the hull show whatever the yard around them shows ----------
rep("  boat:{arg:0,min:0,max:3,make:a=>boatSprite(a),foot:()=>[1,0,28,64]},",
    "  boat:{arg:0,min:0,max:3,bare:1,make:a=>boatSprite(a),foot:()=>[1,0,28,64]},")
rep("if(P2.junk)o.junk=true;","if(P2.junk)o.junk=true;if(P2.bare)o.bare=true;")
rep("for(const o of g.obstacles){if(o.junk||[SPR.gnome,SPR.mailbox,SPR.hydrant,SPR.trash,SPR.snowman,CONE,BARREL,TIRES,HAY].includes(o.src))o.crush=true;setT(T_BLOCK,o.x,o.y,o.w,o.h);}",
    "for(const o of g.obstacles){if(o.junk||[SPR.gnome,SPR.mailbox,SPR.hydrant,SPR.trash,SPR.snowman,CONE,BARREL,TIRES,HAY].includes(o.src))o.crush=true;setT(T_BLOCK,o.x,o.y,o.w,o.h);}\n"
    "  for(const o of g.obstacles)if(o.bare){if(!g.bare){g.bare=new Uint8Array(cols*rows);g.bareSrc=new Int32Array(cols*rows);g.bareDep=new Map();}const a=sprAlpha(o.spr),sw=o.spr.width,sh=o.spr.height;\n"
    "    for(let cy=Math.max(0,o.y>>1);cy<Math.min(rows,Math.ceil((o.y+o.h)/2));cy++)for(let cx=Math.max(0,o.x>>1);cx<Math.min(cols,Math.ceil((o.x+o.w)/2));cx++){let op=0;\n"
    "      for(let dy=0;dy<2;dy++)for(let dx=0;dx<2;dx++){const lx=cx*2+dx-o.sx,ly=cy*2+dy-o.sy;if(lx>=0&&ly>=0&&lx<sw&&ly<sh&&a[ly*sw+lx])op=1;}if(op)continue;\n"
    "      let best=-1,bd=1e9;for(let r=1;r<10&&best<0;r++)for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){const X=cx+dx,Y=cy+dy;if(X<0||Y<0||X>=cols||Y>=rows)continue;const j=Y*cols+X;if(g.type[j]===T_BLOCK)continue;const dd=dx*dx+dy*dy;if(dd<bd){bd=dd;best=j;}}\n"
    "      if(best<0)continue;const i=cy*cols+cx;g.bare[i]=1;g.bareSrc[i]=best;let L2=g.bareDep.get(best);if(!L2)g.bareDep.set(best,L2=[]);L2.push(i);}}")
rep("  const i=cy*g.cols+cx,d=g.depth[i],blocked=g.type[i]===T_BLOCK;",
    "  const i=cy*g.cols+cx;let d=g.depth[i],blocked=g.type[i]===T_BLOCK;if(blocked&&g.bare&&g.bare[i]){blocked=false;d=g.depth[g.bareSrc[i]];}")
rep("const cx=i%g.cols;paintCell(g,cx,cy);paintCell(g,cx,cy-1);paintCell(g,cx,cy+1);}",
    "const cx=i%g.cols;paintCell(g,cx,cy);paintCell(g,cx,cy-1);paintCell(g,cx,cy+1);if(g.bareDep){const L2=g.bareDep.get(i);if(L2)for(const j of L2)paintCell(g,j%g.cols,(j/g.cols)|0);}}")

# ---------- 7. a trophy/treasure pop-up no longer sits on top of the combo label: the label drops below it ----------
_i=s.find("if(run.combo>=2&&!run.ended){const m=");_j=s.find("'CAREFUL!'",_i);_k=s.find("}",_j)+3
_blk=s[_i:_k];assert _blk.count("VIEW_Y+")==5,_blk.count("VIEW_Y+")
_nb=_blk.replace("if(run.combo>=2&&!run.ended){const m=","if(run.combo>=2&&!run.ended){const CYO=achQueue.length?28:0,m=",1)
for _a in ["VIEW_Y+10","VIEW_Y+24","VIEW_Y+25","VIEW_Y+31"]:_nb=_nb.replace(_a,_a+"+CYO")
s=s[:_i]+_nb+s[_k:]

open(f,'w',encoding='utf-8').write(s)
print('p139 visual audit: posts for hanging strings, cable stations, ranch lamps, taxi lanes, buried props, boats, rails/bridge/lighthouse/mosaic')
