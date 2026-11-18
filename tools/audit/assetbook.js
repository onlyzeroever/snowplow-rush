// Collect every asset the game draws (in jobs and outside them) into /tmp/assets/assets.json for the review page.
// node tools/audit/assetbook.js [page]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const page = process.argv[2] || 'index6.html';
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/' + page + '?test=1'); await p.waitForTimeout(1000);
  const r = await p.evaluate(() => window.__EV(`(()=>{const out=[];const seen=new Map();const H=c=>{const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let h=2166136261>>>0;for(let i=0;i<d.length;i+=4){if(d[i+3]<20)continue;h=Math.imul(h^(d[i]|d[i+1]<<8|d[i+2]<<16|(i>>2)<<3),16777619)>>>0;}return c.width+'x'+c.height+':'+h;};
  const add=(cat,name,c,where)=>{if(!c||!c.getContext||!c.width||!c.height)return;let k;try{k=H(c);}catch(e){return;}const e=seen.get(k);if(e){e.n++;if(where&&e.where.length<4&&!e.where.includes(where))e.where.push(where);return;}const o={cat,name,w:c.width,h:c.height,u:c.toDataURL(),n:1,where:where?[where]:[]};seen.set(k,o);out.push(o);};
  const cv=(w,h,f)=>{const c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d');g.imageSmoothingEnabled=false;f(g);return c;};
  const crop=c=>{const g=c.getContext('2d'),d=g.getImageData(0,0,c.width,c.height).data;let x0=c.width,y0=c.height,x1=-1,y1=-1;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(d[(y*c.width+x)*4+3]>10){if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y;}if(x1<0)return c;return cv(x1-x0+1,y1-y0+1,g2=>g2.drawImage(c,-x0,-y0));};
  // ---------- machines and skins ----------
  const saved={tool:save.tool,use:save.use};
  for(const t of TOOLS){const n=(SKIN_PAL[t.id]||[0]).length;for(let si=0;si<Math.max(1,n);si++){const nm=(SKIN_NAMES[t.id]||[])[si]||('SKIN '+si);add('Machines and skins',t.name+' · '+nm,crop(cv(140,140,g=>{try{drawToolIconTo(g,t.id,10,10,120,si);}catch(e){}})));}}
  // ---------- the kid: outfits and hats ----------
  for(const o of OUTFITS){const s=outfitSet(o.id,'yellow');for(const [f,v] of [['down',s.down],['side',s.side],['up',s.up]])add('The kid: outfits and hats',o.name+' · '+f,v);}
  for(const h of HATS){const s=outfitSet('classic',h.id);add('The kid: outfits and hats','HAT '+h.name,s.down);}
  // ---------- characters and animals ----------
  const CH='Characters and animals';
  for(const k of ['peds','thrower','throwerWind','granny','helper','dog','dogL']){const v=SPR[k];if(Array.isArray(v))v.forEach((c,i)=>add(CH,k+' '+(i+1),c));else add(CH,k,v);}
  try{add(CH,'stadium mascot',MASCOT);}catch(e){}
  for(const [nm,a] of [['ghost',GHOST_FR],['skier',SKIER_FR],['sheep',SHEEP_FR],['penguin',PENG_FR],['gull',GULL_FR],['horse',HORSE_FR]])try{a.forEach((c,i)=>add(CH,nm+' '+(i+1),c));}catch(e){}
  try{add(CH,'cow',COW);}catch(e){}
  for(const k in CHASERS){const C=CHASERS[k];(C.frames||[]).forEach((c,i)=>add('Boss chasers',(C.name||k)+' '+(i+1),c));}
  // ---------- items, pickups, icons ----------
  for(const k of ['coin','coinBig','coinS','gem','gemS','star','starOff','bigStar','bigStarOff','present','bow','frost','trophy'])add('Items and pickups',k,SPR[k]);
  try{add('Items and pickups','buried present',giftSnowSpr());add('Items and pickups','machine part',partIcon());add('Items and pickups','test-drive key',driveIcon());}catch(e){}
  for(const id in TR_ART)try{add('Treasures',id,trIco(id));}catch(e){}
  for(const a of ACH)try{add('Trophies',a.name,trophyIcon(a.id));}catch(e){}
  for(const k of ['speed','size','bumper','value','helpers'])try{add('Icons','upgrade: '+k,upIcon(k));}catch(e){}
  for(const k of ['bladeIco','boot','cal','check','gear','lock','pause','speaker','watch','helmet'])add('Icons',k,SPR[k]);
  // ---------- hazards and traffic (named) ----------
  const HZ='Hazards and traffic';
  add(HZ,'shopping trolley',CART);add(HZ,'bus',BUS);add(HZ,'baggage tug',TUG);add(HZ,'tractor + hay trailer',crossSprite());add(HZ,'sled train',sledSprite());add(HZ,'parade float',floatSprite());
  try{add(HZ,'dragon dance',dragonSprite());add(HZ,'zamboni',zamSprite());add(HZ,'plane',planeSprite());add(HZ,'tram',trainSprite(102,'#d8364b'));}catch(e){}
  for(let a=0;a<5;a++)try{add(HZ,'car (side) '+(a+1),carSideSprite(a));const cc=CAR_PAL[a];add(HZ,'car '+(a+1),carSprite(cc[0],cc[1],false,false));}catch(e){}
  add(HZ,'sledging kid',SPR.sled);try{add(HZ,'rockfall rock',ROCK_SPR);}catch(e){}
  (BUMPER_FR||[]).forEach((c,i)=>add(HZ,'bumper car '+(i+1),c));(FORK_FR||[]).forEach((c,i)=>add(HZ,'forklift '+(i+1),c));
  try{add(HZ,'snow cannon',cannonSprite(Math.PI/2));add(HZ,'ball machine',ballMachineSprite(1));add(HZ,'bridge barrier',bridgeBarSprite(60));}catch(e){}
  add(HZ,'snowball',cv(8,8,g=>{const X=3,Y=4;R(g,X-2,Y-1,5,3,K);R(g,X-1,Y-2,3,5,K);R(g,X-1,Y-1,3,3,'#f4f8ff');R(g,X-1,Y-1,1,1,'#ffffff');}));
  add(HZ,'tennis ball',cv(6,7,g=>{const sx=2,sy2=3;R(g,sx-1,sy2-3,3,1,K);R(g,sx-2,sy2-2,5,3,K);R(g,sx-1,sy2+1,3,1,K);R(g,sx-1,sy2-2,3,3,'#d7f03a');R(g,sx-1,sy2-2,1,1,'#f4ffb0');R(g,sx,sy2-1,2,1,'#ffffff');}));
  // ---------- everything placed on the 125 job maps ----------
  const NAT=new Set(['pine','bare','stree','oak','rock','iceblock','spire','reed','bush','shrub','mogul','cairn','iceberg','boulder','log','stump','xmastree','tree','birch','palm','hedge','hedgev','bough']);
  const BLD=new Set(['house','smallhouse','shop','shopv','big','cabin','chalet','hut','igloo','kennel','shed','barn','tent','greenhouse','kiosk','booth','station','hall','tower','lighthouse','windmill','silo','stage','stand','container','cottage']);
  const named=new Map();for(const k in SPR){const v=SPR[k];if(v&&v.getContext)named.set(v,k);}for(const [k,v] of Object.entries({CONE,BARREL,TIRES,HAY,CRATE,CART,BUS}))named.set(v,k.toLowerCase());
  for(let i=0;i<LEVELS.length;i++){let g;try{g=buildLevel(i);}catch(e){continue;}const L=LEVELS[i],D=L.data||{},tag=new Map();
    for(const pp of (D.props||[])){const P2=PROPS[pp[0]];if(!P2)continue;const a=pp[3]!=null?pp[3]:P2.arg;let f;try{f=P2.foot(a);}catch(e){continue;}tag.set((pp[1]+f[0])+','+(pp[2]+f[1]),pp[0]);}
    for(const o of g.obstacles){const id=tag.get(o.x+','+o.y)||named.get(o.src)||'';const big=o.spr.width>=40&&o.spr.height>=30;const cat=NAT.has(id)?'Nature':(BLD.has(id)||(!id&&big)||o.bld)?'Buildings and landmarks':'Props and street furniture';add(cat,id||L.name.toLowerCase(),o.src||o.spr,L.name);}
    for(const o of g.scenery){const cat=o.wild?'Nature':o.spr.width>=40?'Buildings and landmarks':'Props and street furniture';add(cat,o.wild?'wild':L.name.toLowerCase(),o.spr,L.name);}
    for(const o of g.over)add('Overhead: lights, banners, arches, cables',o.k||'overhead',o.spr,L.name);
    for(const o of g.decor)add('Ground decor',L.name.toLowerCase(),o.spr,L.name);
    for(const h of g.hazards)if(h.spr)add(HZ,h.kind,h.spr,L.name);}
  // ---------- the world map screen ----------
  try{ensureMapArt();const m=mapArt,n=Math.ceil(m.height/640);for(let k=0;k<n;k++){const y0=k*640,hh=Math.min(640,m.height-y0);add('World map screen','map part '+(k+1)+' of '+n,cv(m.width,hh,g=>g.drawImage(m,0,-y0)));}}catch(e){out.push({err:String(e)});}
  return JSON.stringify(out);})()`));
  const o = JSON.parse(r); fs.writeFileSync('/tmp/assets/assets.json', JSON.stringify(o));
  const c = {}; for (const x of o) c[x.cat] = (c[x.cat] || 0) + 1; console.log(o.length, c, o.filter(x => x.err).map(x => x.err), errs.slice(0, 3));
  await b.close();
})();
