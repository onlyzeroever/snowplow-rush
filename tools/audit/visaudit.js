// Visual audit of every job map: full-map renders (fresh + plowed) and geometry checks for
// loose string ends, sprites clipping each other, sprites cut by the map edge, cars/people placed inside props.
// node tools/audit/visaudit.js [ids|all] [outDir] [page]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const want=process.argv[2]||'all', out=process.argv[3]||'/tmp/va', page=process.argv[4]||'index6.html';
fs.mkdirSync(out+'/maps',{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await (await b.newContext({viewport:{width:390,height:844}})).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/'+page+'?test=1');await p.waitForTimeout(900);
 const ids=await p.evaluate(()=>window.__EV('JSON.stringify(LEVELS.map(L=>L.id))'));const all=JSON.parse(ids);
 const list=want==='all'?all.map((id,i)=>i):want.split(',').map(id=>all.indexOf(id));
 await p.evaluate(()=>window.__EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=8;save.bzTips=9;window.__HOLD=1;return 1;})()`));
 const report=[];
 for(const i of list){
  const r=await p.evaluate((i)=>window.__EV(`(()=>{const i=${i};startLevel(i);run.time=999;run.moved=true;shake=0;P.x=-400;P.y=-400;
   const ph=G.ph,pw=G.pw;const shots={};
   const grab=(tag)=>{const c=document.createElement('canvas');c.width=pw;c.height=ph;const x=c.getContext('2d');
     for(let y=0;;y+=VIEW_H){camY=Math.min(y,ph-VIEW_H);draw();x.drawImage(b.canvas,0,VIEW_Y,W,VIEW_H,0,camY,W,VIEW_H);if(camY>=ph-VIEW_H)break;}shots[tag]=c.toDataURL();};
   grab('fresh');
   // ---- geometry ----
   const solid=new Uint8Array(pw*ph),A=new Map();
   const alpha=c=>{if(A.has(c))return A.get(c);const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data,a=new Uint8Array(c.width*c.height);for(let k=0;k<a.length;k++)a[k]=d[k*4+3]>60?1:0;A.set(c,a);return a;};
   const stamp=(spr,sx,sy)=>{const a=alpha(spr);sx=Math.round(sx);sy=Math.round(sy);for(let y=0;y<spr.height;y++){const Y=sy+y;if(Y<0||Y>=ph)continue;for(let x=0;x<spr.width;x++){const X=sx+x;if(X<0||X>=pw)continue;if(a[y*spr.width+x])solid[Y*pw+X]=1;}}};
   const items=[];for(const o of G.obstacles)if(o.spr&&o.spr.width)items.push({t:'ob',o,spr:o.spr,sx:o.sx,sy:o.sy,base:o.base});
   for(const o of G.scenery)if(o.spr&&o.spr.width)items.push({t:'sc',o,spr:o.spr,sx:o.sx,sy:o.sy,base:o.base});
   for(const it of items)stamp(it.spr,it.sx,it.sy);
   const finds=[];
   // 1) loose ends on spanning overhead things
   const H=['lights','banner','lant'],V=['gondola','liftline'];
   for(const o of G.over){if(!o.spr||!o.spr.width)continue;const a=alpha(o.spr),w=o.spr.width,h=o.spr.height,sx=Math.round(o.sx),sy=Math.round(o.sy);
     const near=(X,Y,r)=>{if(X<=2||X>=pw-3||Y<=2||Y>=ph-3)return 'edge';for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){const xx=X+dx,yy=Y+dy;if(xx>=0&&xx<pw&&yy>=0&&yy<ph&&solid[yy*pw+xx])return 'prop';}
       if(o.posts&&o.posts.some(([px,py])=>Math.abs(px-X)<=2&&Math.abs(py-Y)<=4))return 'post';if(o.terms&&o.terms.some(([px,py])=>Math.abs(px-X)<=14&&Math.abs(py-Y)<=4))return 'station';for(const q of G.over)if(q!==o&&q.spr){const qa=alpha(q.spr),qx=Math.round(q.sx),qy=Math.round(q.sy);for(let dy=-r;dy<=r;dy++)for(let dx=-r;dx<=r;dx++){const lx=X+dx-qx,ly=Y+dy-qy;if(lx>=0&&ly>=0&&lx<q.spr.width&&ly<q.spr.height&&qa[ly*q.spr.width+lx])return 'over';}}return null;};
     let ends=[];
     if(H.includes(o.k)){let x0=-1,x1=-1;for(let x=0;x<w&&x0<0;x++)for(let y=0;y<h;y++)if(a[y*w+x]){x0=x;break;}for(let x=w-1;x>=0&&x1<0;x--)for(let y=0;y<h;y++)if(a[y*w+x]){x1=x;break;}
       const topY=x=>{for(let y=0;y<h;y++)if(a[y*w+x])return y;return 0;};if(x0>=0)ends.push([sx+x0,sy+topY(x0)],[sx+x1,sy+topY(x1)]);}
     else if(V.includes(o.k)){let y0=-1,y1=-1;for(let y=0;y<h&&y0<0;y++)for(let x=0;x<w;x++)if(a[y*w+x]){y0=y;break;}for(let y=h-1;y>=0&&y1<0;y--)for(let x=0;x<w;x++)if(a[y*w+x]){y1=y;break;}if(y0>=0)ends.push([sx+Math.floor(w/2),sy+y0],[sx+Math.floor(w/2),sy+y1]);}
     for(const [X,Y] of ends){const hit=near(X,Y,3);if(!hit)finds.push({c:'loose-end',k:o.k,x:X,y:Y,box:[sx,sy,w,h]});}}
   // 2) props whose pixels clip each other (beyond the top padding row), incl. scenery
   items.sort((p,q)=>p.sy-q.sy);
   for(let a1=0;a1<items.length;a1++){const P1=items[a1],aa=alpha(P1.spr);for(let c=a1+1;c<items.length;c++){const Q=items[c];if(Q.sy>=P1.sy+P1.spr.height)break;if(P1.t==='ob'&&Q.t==='ob')continue;
     const x0=Math.max(P1.sx,Q.sx),x1=Math.min(P1.sx+P1.spr.width,Q.sx+Q.spr.width),y0=Math.max(P1.sy,Q.sy),y1=Math.min(P1.sy+P1.spr.height,Q.sy+Q.spr.height);if(x1<=x0||y1<=y0)continue;
     const qa=alpha(Q.spr);let n=0;for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){if(aa[(y-P1.sy)*P1.spr.width+(x-P1.sx)]&&qa[(y-Q.sy)*Q.spr.width+(x-Q.sx)])n++;}
     let inside=false;if(n>=10){const [S1,B1]=(P1.spr.width*P1.spr.height<=Q.spr.width*Q.spr.height)?[P1,Q]:[Q,P1];const ba=alpha(B1.spr);let fx=Math.round(S1.sx+S1.spr.width/2-B1.sx),fy=Math.round(S1.base-B1.sy)-1;
       if(S1.base<B1.base-1)for(let dx=-1;dx<=1&&!inside;dx++){const xx=fx+dx;if(xx>=0&&xx<B1.spr.width&&fy>=0&&fy<B1.spr.height-1&&ba[fy*B1.spr.width+xx])inside=true;}}
     if(n>=10&&!inside)finds.push({c:'occlude',n,x:x0,y:y0,box:[Math.min(P1.sx,Q.sx),Math.min(P1.sy,Q.sy),1,1]});
     if(n>=10&&inside)finds.push({c:(P1.t==='sc'&&Q.t==='sc'&&P1.spr.width===Q.spr.width&&Math.abs(P1.sx-Q.sx)<3)?'row':'clip',n,x:x0,y:y0,box:[Math.min(P1.sx,Q.sx),Math.min(P1.sy,Q.sy),Math.max(P1.sx+P1.spr.width,Q.sx+Q.spr.width)-Math.min(P1.sx,Q.sx),Math.max(P1.sy+P1.spr.height,Q.sy+Q.spr.height)-Math.min(P1.sy,Q.sy)],what:P1.t+'+'+Q.t,sz:[P1.spr.width+'x'+P1.spr.height,Q.spr.width+'x'+Q.spr.height]});}}
   // 3) sprites cut by the left/right map edge (partly visible)
   for(const it of items){const w=it.spr.width;if(w>=150)continue;const a=alpha(it.spr);let tot=0,cut=0;for(let y=0;y<it.spr.height;y++)for(let x=0;x<w;x++)if(a[y*w+x]){tot++;const X=Math.round(it.sx)+x;if(X<0||X>=pw)cut++;}
     if(tot&&cut/tot>0.08&&cut/tot<0.92)finds.push({c:'edge-cut',f:+(cut/tot).toFixed(2),x:Math.max(0,Math.round(it.sx)),y:Math.round(it.sy),box:[Math.round(it.sx),Math.round(it.sy),w,it.spr.height],sz:w+'x'+it.spr.height});}
   // 4) movers and people that start inside a prop
   const fp=G.obstacles.map(o=>[o.x,o.y,o.w,o.h]);const inside=(x,y,w,h)=>fp.some(([X,Y,W2,H2])=>x<X+W2-1&&X<x+w-1&&y<Y+H2-1&&Y<y+h-1);
   for(const hz of G.hazards){if(hz.kind==='pull')continue;if(hz.w&&inside(hz.x,hz.y,hz.w,hz.h))finds.push({c:'mover-in-prop',k:hz.kind,x:Math.round(hz.x),y:Math.round(hz.y),box:[Math.round(hz.x)-4,Math.round(hz.y)-8,(hz.w||8)+8,(hz.h||8)+12]});}
   // plowed render
   for(let k=0;k<G.depth.length;k++)if(G.type[k]!==T_BLOCK)G.depth[k]=0;repaintSnow();grab('plowed');
   return JSON.stringify({id:LEVELS[i].id,name:LEVELS[i].name,area:LEVELS[i].area,ph,finds,shots});})()`),i);
  const o=JSON.parse(r);for(const t of ['fresh','plowed'])fs.writeFileSync(`${out}/maps/${o.id}_${t}.png`,Buffer.from(o.shots[t].split(',')[1],'base64'));
  delete o.shots;report.push(o);process.stdout.write(o.id+':'+o.finds.length+' ');}
 fs.writeFileSync(out+'/visaudit.json',JSON.stringify(report));
 const by={};for(const o of report)for(const f of o.finds)by[f.c]=(by[f.c]||0)+1;console.log('\n',by,'errors',errs.slice(0,3));await b.close();})();
