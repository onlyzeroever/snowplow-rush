import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# MAP STRETCH: the old map (2436 tall) is drawn exactly as before, then a new band is opened just
# above the old Suburbs (at y=1992) for the 9 new Suburbs jobs. Everything at or below the split
# moves down by SUB_EXT. Later areas can be inserted the same way.
# ---------------------------------------------------------------------------------------------
# Three inserts, in old-map coordinates: Suburbs part 2 above the old Suburbs (1992), Farmland part 2 above the old
# farm (1462), and above the old City (846): City part 2, Theme Park, Frozen Harbour, Ski Resort, Mountain Pass and
# more room for the Frozen North. SY maps old y to the final map; FY maps the Suburbs-only layout (v1) to the final map.
rep("const MAP_H=2436,","const MAP_OLD_H=2436,MAP_SPLIT=1992,SUB_EXT=560,FARM_SPLIT=1462,FARM_EXT=560,TOP_SPLIT=846,CITY_EXT=560,AREA_BAND=960,NORTH_EXT=200,TOP_EXT=CITY_EXT+AREA_BAND*4+NORTH_EXT,MAP_H=MAP_OLD_H+SUB_EXT+FARM_EXT+TOP_EXT,")
rep("const BIOMES=[","const FY=y=>y+(y>=FARM_SPLIT?FARM_EXT:0)+(y>=TOP_SPLIT?TOP_EXT:0),SY=y=>FY(y>=MAP_SPLIT?y+SUB_EXT:y);\nlet MOFF=0;\nlet BIOMES=[")
# the old map is drawn with the old biome bands; everything after uses the new ones (top to bottom)
rep("function biomeAt(y){","const BIOMES_OLD=BIOMES,BIOMES_NEW=[{id:'north',name:'THE FROZEN NORTH',y0:0,y1:TOP_SPLIT+NORTH_EXT,snow:1,ground:'#eaf0fc'},\n"
    "  {id:'pass',name:'MOUNTAIN PASS',y0:TOP_SPLIT+NORTH_EXT,y1:TOP_SPLIT+NORTH_EXT+AREA_BAND,snow:0.9,ground:'#e6ecf7'},\n"
    "  {id:'ski',name:'SKI RESORT',y0:TOP_SPLIT+NORTH_EXT+AREA_BAND,y1:TOP_SPLIT+NORTH_EXT+AREA_BAND*2,snow:0.82,ground:'#f2f6fd'},\n"
    "  {id:'harbour',name:'FROZEN HARBOUR',y0:TOP_SPLIT+NORTH_EXT+AREA_BAND*2,y1:TOP_SPLIT+NORTH_EXT+AREA_BAND*3,snow:0.72,ground:'#e9eff8'},\n"
    "  {id:'themepark',name:'THEME PARK',y0:TOP_SPLIT+NORTH_EXT+AREA_BAND*3,y1:TOP_SPLIT+TOP_EXT-CITY_EXT,snow:0.66,ground:'#f1f4fb'},\n"
    "  {id:'city',name:'THE CITY',y0:TOP_SPLIT+TOP_EXT-CITY_EXT,y1:FARM_SPLIT+TOP_EXT,snow:0.62,ground:'#e8eef7'},\n"
    "  {id:'farm',name:'FARMLAND',y0:FARM_SPLIT+TOP_EXT,y1:MAP_SPLIT+TOP_EXT+FARM_EXT,snow:0.36,ground:'#f3f7fc'},\n"
    "  {id:'suburbs',name:'SUBURBS',y0:MAP_SPLIT+TOP_EXT+FARM_EXT,y1:MAP_H,snow:0.16,ground:'#f4f8ff'}];\nBIOMES=BIOMES_NEW;\nfunction biomeAt(y){")

# --- the 9 new Suburbs jobs (final designs are filled in by the jobs patch) ---
NEW = """
  // ---- Suburbs, part 2 (Nov 2026): 7 main jobs, 1 side job, 1 boss ----
  {id:'cornershop',name:'CORNER SHOP', area:'suburbs',h:600, time:70,value:1.65,stars:[35,60,85],snowfall:100,presents:5,squall:0,from:['maple'],     mx:0,my:0,data:{}},
  {id:'playground',name:'PLAYGROUND',  area:'suburbs',h:640, time:70,value:1.7, stars:[35,60,85],snowfall:105,presents:5,squall:0,from:['cornershop'],mx:0,my:0,data:{}},
  {id:'allotments',name:'ALLOTMENTS',  area:'suburbs',h:700, time:75,value:1.75,stars:[35,60,85],snowfall:110,presents:5,squall:0,from:['playground'],mx:0,my:0,data:{}},
  {id:'dogpark',   name:'DOG PARK',    area:'suburbs',h:720, time:75,value:1.8, stars:[35,60,85],snowfall:115,presents:6,squall:0,from:['allotments'],mx:0,my:0,data:{}},
  {id:'tennis',    name:'TENNIS CLUB', area:'suburbs',h:760, time:75,value:1.85,stars:[35,60,85],snowfall:120,presents:6,squall:0,from:['dogpark'],   mx:0,my:0,data:{}},
  {id:'highst',    name:'HIGH STREET', area:'suburbs',h:820, time:75,value:1.9, stars:[35,60,85],snowfall:125,presents:6,squall:0,from:['tennis'],    mx:0,my:0,data:{}},
  {id:'sledhill',  name:'SLEDGING HILL',area:'suburbs',h:700,time:70,value:1.9, stars:[35,60,85],snowfall:120,presents:7,squall:0,from:['highst'],    mx:0,my:0,data:{},bonus:true},
  {id:'fountainsq',name:'FOUNTAIN SQUARE',area:'suburbs',h:860,time:80,value:1.95,stars:[35,60,85],snowfall:130,presents:6,squall:0,from:['highst'],mx:0,my:0,data:{}},
  {id:'blockparty',name:'BLOCK PARTY', area:'suburbs',h:1000,time:85,value:2.0, stars:[35,60,85],snowfall:140,presents:8,squall:0,from:['fountainsq'],mx:0,my:0,data:{},boss:true},
];"""
rep("night:true,from:[],mx:40,my:1460},\n];","night:true,from:[],mx:40,my:1460},"+NEW)

# --- positions: keep the old ones for drawing the old map, move the live ones ---
rep("for(const L of LEVELS){const p=MAPPOS[L.id];if(p){L.mx=p[0];L.my=p[1];}}",
r"""// the old map is drawn from the old positions and links; everything else uses the stretched map
const MAPPOS_OLD=JSON.parse(JSON.stringify(MAPPOS)),EDGE_VIA_OLD=JSON.parse(JSON.stringify(EDGE_VIA));
const OLD_LINKS=[];LEVELS.forEach(L=>{if(!MAPPOS_OLD[L.id])return;for(const f2 of L.from)if(MAPPOS_OLD[f2])OLD_LINKS.push([f2,L.id,false]);});for(const k in WILD_LINK)OLD_LINKS.push([WILD_LINK[k],k,true]);
for(const k in MAPPOS)MAPPOS[k][1]=SY(MAPPOS[k][1]);for(const k in EDGE_VIA)for(const p of EDGE_VIA[k])p[1]=SY(p[1]);for(const k in LANDMARK)LANDMARK[k][1]=SY(LANDMARK[k][1]);
// new Suburbs jobs, bottom to top, in the band between the river (1984) and the old Suburbs
Object.assign(MAPPOS,{cornershop:[92,2504],playground:[36,2444],allotments:[128,2396],dogpark:[44,2334],tennis:[132,2276],highst:[88,2208],sledhill:[22,2150],fountainsq:[142,2146],blockparty:[86,2066]});
Object.assign(LANDMARK,{cornershop:[118,2480],playground:[28,2420],allotments:[140,2372],dogpark:[44,2310],tennis:[150,2256],highst:[88,2186],sledhill:[28,2122],fountainsq:[150,2122],blockparty:[86,2040]});
Object.assign(EDGE_VIA,{'maple>cornershop':[[93,2600],[93,2552]],'blockparty>lane':[[90,2030],[94,1996],[94,1980],[94,1948]]});
for(const id of ['cornershop','playground','allotments','dogpark','tennis','highst','sledhill','fountainsq','blockparty']){MAPPOS[id][1]=FY(MAPPOS[id][1]);LANDMARK[id][1]=FY(LANDMARK[id][1]);}
for(const k of ['maple>cornershop','blockparty>lane'])for(const p of EDGE_VIA[k])p[1]=FY(p[1]);
{const ln=LEVELS.find(L=>L.id==='lane');if(ln)ln.from=['blockparty'];}
for(const L of LEVELS){const p=MAPPOS[L.id];if(p){L.mx=p[0];L.my=p[1];}}
function mapEdgesOld(){const out=[];for(const [a,b2,wild] of OLD_LINKS){const A=MAPPOS_OLD[a],B=MAPPOS_OLD[b2];if(!A||!B)continue;const key=a+'>'+b2,via=EDGE_VIA_OLD[key];out.push({a,b:b2,key,wild,pts:pixPath(via?crPts([A,...via,B]):bezPts(A,B))});}return out;}""")

# --- the mask can be sized for the old map or the stretched one ---
rep("function mMark(x,y,w,h,bit){x=Math.floor(x);y=Math.floor(y);for(let yy=Math.max(0,y);yy<Math.min(MAP_H,y+h);yy++)",
    "let MASK_H=0;\nfunction mMark(x,y,w,h,bit){x=Math.floor(x);y=Math.floor(y)+MOFF;for(let yy=Math.max(0,y);yy<Math.min(MASK_H,y+h);yy++)")
rep("if(x<-4||x+w>W+4||y<0||y+h>MAP_H)return false;","if(x<-4||x+w>W+4||y<0||y+h>MASK_H)return false;")
rep("function mFree(x,y,w,h,bits){x=Math.floor(x);y=Math.floor(y);","function mFree(x,y,w,h,bits){x=Math.floor(x);y=Math.floor(y)+MOFF;")
rep("for(let yy=Math.max(0,y);yy<Math.min(MAP_H,y+h);yy+=2)","for(let yy=Math.max(0,y);yy<Math.min(MASK_H,y+h);yy+=2)")

# --- the old map is drawn at its old size ---
rep("mapBase=mk(W,MAP_H);mapObj=mk(W,MAP_H);mapArt=mk(W,MAP_H);","mapBase=mk(W,MAP_OLD_H);mapObj=mk(W,MAP_OLD_H);mapArt=mk(W,MAP_H);")
rep("MASK=new Uint8Array(W*MAP_H);","MASK=new Uint8Array(W*MAP_OLD_H);MASK_H=MAP_OLD_H;")
rep("y=hash(13,i)%MAP_H","y=hash(13,i)%MAP_OLD_H")
rep("for(let y=236;y<MAP_H-6;y+=5)","for(let y=236;y<MAP_OLD_H-6;y+=5)")
rep("const E=mapEdges();for(const e of E)for(const [x,y] of e.pts)mMark(x-6,y-6,13,13,MK_ROAD);","const E=mapEdgesOld();for(const e of E)for(const [x,y] of e.pts)mMark(x-6,y-6,13,13,MK_ROAD);")
rep("for(const L of LEVELS)mMark(L.mx-14,L.my-16,29,32,MK_RES);","for(const id in MAPPOS_OLD){const p=MAPPOS_OLD[id];mMark(p[0]-14,p[1]-16,29,32,MK_RES);}")

# --- objects standing at or below the split move down whole (none get cut in two) ---
rep("objs.sort((a,b)=>a.by-b.by);for(const o of objs)o.fn(og);",
r"""objs.sort((a,b)=>a.by-b.by);const SEGS=[0,TOP_SPLIT,FARM_SPLIT,MAP_SPLIT,MAP_OLD_H],SHIFT=[0,TOP_EXT,TOP_EXT+FARM_EXT,TOP_EXT+FARM_EXT+SUB_EXT];
  const segOf=y=>y>=MAP_SPLIT?3:y>=FARM_SPLIT?2:y>=TOP_SPLIT?1:0,layers=[null,mk(W,MAP_OLD_H),mk(W,MAP_OLD_H),mk(W,MAP_OLD_H)];
  for(const o of objs){const k=segOf(o.by);o.fn(k?layers[k].getContext('2d'):og);}
  // ======== stretch: each old area moves down whole (objects are never cut), the new bands go in between ========
  {const nb=mk(W,MAP_H),no=mk(W,MAP_H),nbg=nb.getContext('2d'),nog=no.getContext('2d');BIOMES=BIOMES_NEW;
   for(let k=0;k<4;k++){const a=SEGS[k],h2=SEGS[k+1]-a;nbg.drawImage(mapBase,0,a,W,h2,0,a+SHIFT[k],W,h2);nog.drawImage(mapObj,0,a,W,h2,0,a+SHIFT[k],W,h2);if(layers[k])nog.drawImage(layers[k],0,SHIFT[k]);}
   mapBase=nb;mapObj=no;
   for(const k in MAPDYN){const v=MAPDYN[k];if(!Array.isArray(v))continue;for(const o of v){if(!o)continue;
     const mid=o.h!=null&&o.y!=null?o.y+o.h/2:o.y!=null?o.y:o.cy;if(mid==null)continue;const d=SHIFT[segOf(mid)];if(!d)continue;for(const kk of ['y','cy','y0','y1'])if(typeof o[kk]==='number')o[kk]+=d;}}
   MASK=new Uint8Array(W*MAP_H);MASK_H=MAP_H;
   // the Suburbs band was laid out before the other inserts existed: draw it in its own coordinates, shifted
   {const D=TOP_EXT+FARM_EXT,before={};for(const k in MAPDYN)if(Array.isArray(MAPDYN[k]))before[k]=MAPDYN[k].length;
    nbg.save();nog.save();nbg.translate(0,D);nog.translate(0,D);MOFF=D;genSuburbsBand(nbg,nog);MOFF=0;nbg.restore();nog.restore();
    for(const k in before)for(let i=before[k];i<MAPDYN[k].length;i++){const o=MAPDYN[k][i];if(o)for(const kk of ['y','cy','y0','y1'])if(typeof o[kk]==='number')o[kk]+=D;}}
   if(typeof genNewBands==='function')genNewBands(nbg,nog);}""")
rep("function mapInit(){if(mapBase)return;","function mapInit(){if(mapBase)return;BIOMES=BIOMES_OLD;")

# --- the new band: ground, roads reserved, a landmark for each new job, then filler ---
rep("function mapInit(){",r"""function genSuburbsBand(g,og){const y0=MAP_SPLIT,y1=MAP_SPLIT+SUB_EXT,objs=[],put=(by,fn)=>objs.push({by,fn});
  R(g,0,y0,W,SUB_EXT,BIOMES.find(B=>B.id==='suburbs').ground);
  for(let i=0;i<620;i++){const x=hash(i,311)%W,y=y0+hash(313,i)%SUB_EXT,v=hash(i,317)%10;if(v<5)R(g,x,y,2,1,MC.snowB);else if(v<8)R(g,x,y,1,1,MC.sh);else R(g,x,y,1,1,'#ffffff');}
  for(const e of mapEdges())for(const [x,y0r] of e.pts){const y=y0r-MOFF;if(y>y0-8&&y<y1+8)mMark(x-6,y-6,13,13,MK_ROAD);}
  for(const id of ['cornershop','playground','allotments','dogpark','tennis','highst','sledhill','fountainsq','blockparty']){const p=MAPPOS[id];mMark(p[0]-14,p[1]-16-MOFF,29,32,MK_RES);}
  const res=(x,y,w,h)=>mMark(x,y,w,h,MK_RES);
  // corner shop: a little shop, a stall and a parked car
  put(2486,G=>{mShop(G,104,2462,30,'#d8364b',7);});res(102,2456,36,32);
  put(2500,G=>{mStall(G,140,2488,'#3f86d6');});res(138,2482,22,20);
  put(2520,G=>{mCarTop(G,64,2506,'#f2c94c','#c49a2a',true);});res(62,2504,12,18);
  // playground: swings, slide, a snowman
  put(2426,G=>{mSwing(G,8,2410);});put(2432,G=>{mSlide(G,52,2418);});res(4,2404,70,30);
  MAPDYN.snowmen.push({x:62,y:2470,wob:0});res(56,2456,14,16);
  // allotments: small hedged plots with gnomes
  for(const [x,y] of [[96,2356],[150,2356],[150,2410]]){put(y+18,G=>{mBush(G,x,y,22,4);mBush(G,x,y+14,22,4);mBush(G,x,y,4,18);mBush(G,x+18,y,4,18);mGnome(G,x+9,y+7);});res(x-2,y-2,26,24);}
  // dog park: fenced field with a kennel
  put(2312,G=>{mFenceH(G,4,2296,40,MC.woodD);mFenceH(G,4,2318,40,MC.woodD);mFenceV(G,4,2296,22,MC.woodD);});res(2,2290,44,32);
  put(2316,G=>{mHouse(G,16,2302,12,12,'#a8673a','#7a4a2a','#3a2a20',0,3);});
  // tennis club: two courts painted on the ground, a clubhouse
  for(const cx of [98,140]){R(g,cx,2232,30,40,K);R(g,cx+1,2233,28,38,'#4f8f5a');R(g,cx+2,2234,26,36,'#5aa36a');R(g,cx+2,2251,26,1,'#ffffff');R(g,cx+14,2234,1,36,'#ffffff');R(g,cx+2,2234,26,1,'#ffffff');R(g,cx+2,2269,26,1,'#ffffff');}res(96,2230,76,44);
  put(2300,G=>{mHouse(G,150,2284,22,16,'#e8eef8','#c6d0e0','#3f86d6',0,11);});res(148,2278,26,24);
  // high street: shops both sides of the road, lamps
  put(2196,G=>{mShop(G,108,2174,30,'#3f86d6',3);});put(2198,G=>{mShop(G,140,2176,30,'#e07a8a',5);});res(106,2168,74,32);
  put(2232,G=>{mShop(G,40,2210,30,'#5aa35a',9);});res(38,2204,34,30);
  for(const [x,y] of [[76,2222],[104,2214]]){put(y,G=>mLamp(G,x,y,false));}
  // sledging hill: a white mound with sled tracks
  {const cx=30,cy=2118;for(let dy=-14;dy<=14;dy++){const hw=Math.round(Math.sqrt(1-(dy/14)**2)*26);R(g,cx-hw,cy+dy,hw*2,1,dy<-8?'#ffffff':dy<4?MC.snowB:MC.sh);}
   for(let i=0;i<10;i++){R(g,cx-6+i*2,cy-10+i*3,1,2,MC.sh2);R(g,cx+4+i,cy-12+i*3,1,2,MC.sh2);}res(2,2100,58,34);}
  // fountain square: paved square, fountain, benches
  R(g,124,2096,52,36,K);R(g,125,2097,50,34,MC.stone);for(let x=125;x<175;x+=6)R(g,x,2097,1,34,'#b6c0d2');res(122,2094,56,40);
  put(2118,G=>{mFountain(G,150,2112);});
  // block party: bunting between houses, a stall
  put(2050,G=>{mHouse(G,32,2032,22,18,'#e07a8a','#b04a5a','#6b3f22',1,21);});put(2050,G=>{mHouse(G,126,2032,22,18,'#8fbf5a','#5e8a3a','#a8673a',1,23);});res(30,2026,26,26);res(124,2026,26,26);
  put(2054,G=>{for(let x=54;x<126;x++){const y=2036+Math.round(Math.sin((x-54)/72*Math.PI)*6);R(G,x,y,1,1,K);if(x%6===0){const c=['#d8364b','#ffd23f','#3f86d6','#5aa35a'][(x/6)%4|0];R(G,x,y+1,3,1,c);R(G,x+1,y+2,1,1,c);}}});
  put(2060,G=>{mStall(G,110,2046,'#ffc727');});res(108,2040,22,22);
  // filler: houses, pines and bushes, like the old Suburbs
  const tryPut=(x,y,w,h,fx)=>{if(y<y0+20||y+h>y1-2)return false;if(!mFree(x,y,w,h,MK_ROAD|MK_RES))return false;const fy=y+Math.floor(h*0.25);if(!mFree(x,fy,w,h-Math.floor(h*0.25),MK_OBJ))return false;mMark(x,fy,w,h-Math.floor(h*0.25),MK_OBJ);put(y+h,fx);return true;};
  for(let y=y0+22;y<y1-4;y+=5){for(let x=-6;x<W;x+=7){const hv=hash(x+731,y+1291),jx=x+(hv%5),jy=y+((hv>>>4)%4),r=(hv>>>8)%100;if(r>58)continue;
    if(r<12){const w=16+((hv>>>12)%3)*2,h=16+((hv>>>14)%2)*2,c=HOUSE_COLS[(hv>>>16)%6];tryPut(jx,jy-h,w,h+2,G2=>{const cp=mHouse(G2,jx,jy-h,w,h,c[0],c[1],c[2],(hv>>>18)%3?1:0,hv);if(cp)MAPDYN.smoke.push(cp);});}
    else if(r<44){const h=12+((hv>>>12)%4)*2;tryPut(jx-5,jy-h,10,h,G2=>mPine(G2,jx,jy,h));}else if(r<48)tryPut(jx,jy-5,10,6,G2=>mBush(G2,jx,jy-5,10,6));}}
  objs.sort((a,b)=>a.by-b.by);for(const o of objs)o.fn(og);}
function mapInit(){""")

# --- roads: a road counts as cleared if you've already played the job at its far end ---
rep("function edgeOpen(e){return e.wild?levelOpen(lvIdx(e.b)):save.stars[lvIdx(e.a)]>0;}",
    "function edgeOpen(e){return e.wild?levelOpen(lvIdx(e.b)):save.stars[lvIdx(e.a)]>0||save.stars[lvIdx(e.b)]>0;}")
# players who already reached a job keep it, even though new jobs now sit in front of it
rep("if(!L.from.length)return true;return L.from.some(id=>save.stars[lvIdx(id)]>0);}",
    "if(!L.from.length)return true;const i2=LEVELS.indexOf(L);if(save.stars[i2]>0||save.best[i2]>0)return true;return L.from.some(id=>save.stars[lvIdx(id)]>0);}")
rep("e=E.find(e=>e.key==='maple>lane')","e=E.find(e=>e.key==='blockparty>lane')")
# helpers live by your house, which moved down with the old Suburbs
rep("const YARD_SPOTS=[[70,84,2377],[104,116,2365],[66,88,2388],[64,73,2349],[100,116,2383],[78,94,2396]],HOME_Y=2366;",
    "const YARD_SPOTS=[[70,84,SY(2377)],[104,116,SY(2365)],[66,88,SY(2388)],[64,73,SY(2349)],[100,116,SY(2383)],[78,94,SY(2396)]],HOME_Y=SY(2366);")
rep("const x=100,s=sy(2378);","const x=100,s=sy(SY(2378));")
rep("const AREAS={suburbs:{name:'SUBURBS'},farm:{name:'FARMLAND'},city:{name:'THE CITY'},north:{name:'THE FROZEN NORTH'},",
    "const AREAS={suburbs:{name:'SUBURBS'},farm:{name:'FARMLAND'},city:{name:'THE CITY'},themepark:{name:'THEME PARK'},harbour:{name:'FROZEN HARBOUR'},ski:{name:'SKI RESORT'},pass:{name:'MOUNTAIN PASS'},north:{name:'THE FROZEN NORTH'},")
rep("R(b,x,a,3,c-a,B.id==='north'?'#6b3fa8':B.id==='city'?'#3f5fae':B.id==='farm'?'#4f9a3a':'#3f86d6');",
    "R(b,x,a,3,c-a,{north:'#6b3fa8',pass:'#5a6a8a',ski:'#4fb0d8',harbour:'#2f6f8a',themepark:'#d8364b',city:'#3f5fae',farm:'#4f9a3a'}[B.id]||'#3f86d6');")
rep("__SR={pineSprite,","__SR={pineSprite,get mapArt2(){return mapArt;},MAP_H,MAPPOS,")
open(f,'w',encoding='utf-8').write(s);print('p43 ok')
