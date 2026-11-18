// Motion audit: run every job with a ghost player sweeping down the map; flag movers that teleport on screen,
// pass through props, shake back and forth, or never move; and any game text drawn off the screen edge.
// node tools/audit/motion.js [ids|all] [out.json] [page]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const want=process.argv[2]||'all', out=process.argv[3]||'/tmp/va/motion.json', page=process.argv[4]||'index6.html';
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await (await b.newContext({viewport:{width:390,height:844}})).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/'+page+'?test=1');await p.waitForTimeout(900);
 const all=JSON.parse(await p.evaluate(()=>window.__EV('JSON.stringify(LEVELS.map(L=>L.id))')));
 const list=want==='all'?all.map((id,i)=>i):want.split(',').map(id=>all.indexOf(id));
 await p.evaluate(()=>window.__EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=8;save.bzTips=9;window.__HOLD=1;
   if(!window.__TXT){window.__TXT=[];const o=text;text=function(c,s,x,y,col,op){try{if(c===b&&state==='play'&&y>=VIEW_Y&&y<VIEW_Y+VIEW_H-4){const sc=(op&&op.scale)||1,w=textW(String(s),sc),al=op&&op.align,x0=al==='center'?x-w/2:al==='right'?x-w:x;
     window.__TXT.push([String(s),Math.round(x0),Math.round(y),Math.round(w),Math.round(5*sc+2)]);}}catch(e){}return o.apply(this,arguments);};}return 1;})()`));
 const res=[];
 for(const i of list){
  const r=await p.evaluate((i)=>window.__EV(`(()=>{const i=${i};startLevel(i);run.time=9999;run.moved=true;const ph=G.ph,pw=G.pw;const FLY=['gull','ufo','balloon','skier','firework','plane','bird'];
   const fp=G.obstacles.map(o=>[o.x,o.y,o.w,o.h]);const inProp=(x,y,w,h)=>fp.some(([X,Y,W2,H2])=>x+2<X+W2-2&&X+2<x+w-2&&y+2<Y+H2-2&&Y+2<y+h-2);
   const H=G.hazards.map(h=>({k:h.kind,path:0,last:[h.x,h.y],jumps:[],thru:0,thruAt:null,thruMax:0,rev:[],dxs:0,win:[]}));
   const T=[];const N=Math.min(5400,Math.round(Math.max(20,(ph-G.start.y)/55)*30));const fr=[];
   for(let f=0;f<N;f++){const t=f/N;P.y=Math.min(ph-20,G.start.y+t*(ph-G.start.y));P.x=pw/2+Math.sin(f/40)*60;P.inv=99;P.stun=0;
     window.__TXT.length=0;update(1/30);if(f%3===0){draw();const tx=window.__TXT.slice();for(const [s,x,y,w,h] of tx){if(x<0||x+w>W)T.push({c:'text-off',s,x,y,w,cam:Math.round(camY)});}
       for(let a=0;a<tx.length;a++)for(let c=a+1;c<tx.length;c++){const A=tx[a],B=tx[c];if(A[0]===B[0]&&A[1]===B[1]&&A[2]===B[2])continue;if(A[1]<B[1]+B[3]&&B[1]<A[1]+A[3]&&A[2]<B[2]+B[4]-1&&B[2]<A[2]+A[4]-1)T.push({c:'text-overlap',s:A[0]+' / '+B[0],x:A[1],y:A[2]});}}
     G.hazards.forEach((h,j)=>{const S=H[j];if(!S)return;const dx=h.x-S.last[0],dy=h.y-S.last[1],d=Math.hypot(dx,dy);S.path+=d;
       const inMap=(x,y)=>x>-4&&x<pw-(h.w||8)+4&&y>4&&y<ph-4;if(d>10&&f>2&&inMap(h.x,h.y)&&inMap(S.last[0],S.last[1])&&S.jumps.length<4)S.jumps.push([Math.round(S.last[0]),Math.round(S.last[1]),Math.round(h.x),Math.round(h.y),h.state||'']);
       if(!FLY.includes(h.kind)&&h.w&&d>0.05&&inProp(h.x,h.y,h.w,h.h)){S.thru++;S.thruMax=Math.max(S.thruMax,S.thru);if(!S.thruAt)S.thruAt=[Math.round(h.x),Math.round(h.y),h.state||''];}else S.thru=0;
       S.win.push([dx,d]);if(S.win.length>30)S.win.shift();if(S.win.length===30&&f%15===0){let pth=0,nx=0,ny=0,rv=0,ps=0;for(const [ddx,dd] of S.win){pth+=dd;nx+=ddx;const sg=Math.sign(ddx);if(sg&&ps&&sg!==ps)rv++;if(sg)ps=sg;}if(pth>20&&Math.abs(nx)<3&&rv>=6&&S.rev.length<3)S.rev.push([Math.round(h.x),Math.round(h.y),rv,h.state||'']);}
       S.last=[h.x,h.y];});}
   const finds=[];H.forEach((S,j)=>{const h=G.hazards[j];if(!h)return;if(S.jumps.length)finds.push({c:'jump',k:S.k,j:S.jumps});if(S.thruMax>=6)finds.push({c:'through-prop',k:S.k,at:S.thruAt,frames:S.thruMax});
     if(S.rev.length)finds.push({c:'jitter',k:S.k,at:S.rev});if(S.path<1&&!['barrier','pull','thrower','chaser'].includes(S.k))finds.push({c:'never-moves',k:S.k,at:[Math.round(h.x),Math.round(h.y)]});});
   const seenT=new Set();for(const t of T){const k=t.c+t.s;if(seenT.has(k))continue;seenT.add(k);finds.push(t);}
   return JSON.stringify({id:LEVELS[i].id,frames:N,hz:G.hazards.length,finds});})()`),i);
  const o=JSON.parse(r);res.push(o);process.stdout.write(o.id+':'+o.finds.length+' ');}
 fs.writeFileSync(out,JSON.stringify(res));const by={};for(const o of res)for(const f of o.finds)by[f.c]=(by[f.c]||0)+1;console.log('\n',by,'errors',errs.slice(0,5));await b.close();})();
