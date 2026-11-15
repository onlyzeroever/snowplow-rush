// reachability audit: which clearable snow can the current machine's blade never touch?  node reach.js [ids|all] [toolIdx]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const want=(process.argv[2]||'all'),TI=+(process.argv[3]||0),page=process.argv[4]||'index6.html';
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await (await b.newContext()).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/'+page+'?test=1');await p.waitForTimeout(800);
 const res=await p.evaluate(({want,TI})=>{const R=window.__SR,EV=window.__EV;window.__HOLD=true;R.save.tut=true;R.save.tool=Math.max(R.save.tool,TI);R.save.use=TI;
  const ids=want==='all'?R.LEVELS.map(l=>l.id):want.split(',');const out=[];
  for(const id of ids){const idx=R.LEVELS.findIndex(l=>l.id===id);if(idx<0)continue;const L=R.LEVELS[idx];if(L.tool||L.area==='secret')continue;
   const t0=performance.now();R.startLevel(idx);const r=EV(`(()=>{const T=tool(),tid=T.id,bw=bladeCells()*2,G2=G;const S=2,nx=Math.floor(G2.pw/S)+1,ny=Math.floor(G2.ph/S)+1;
     const seen=new Uint8Array(nx*ny),okF=new Uint8Array(nx*ny);const q=new Int32Array(nx*ny);let qh=0,qt=0;
     const free=(x,y)=>{let m=0;for(let f=0;f<4;f++){if(!blockedBy(footprint(tid,x,y,f)))m|=1<<f;}return m;};
     const sx=Math.round(G2.start.x/S),sy=Math.round(G2.start.y/S);const s0=sy*nx+sx;const m0=free(sx*S,sy*S);if(!m0)return {err:'start blocked'};seen[s0]=1;okF[s0]=m0;q[qt++]=s0;
     while(qh<qt){const c=q[qh++],cx=c%nx,cy=(c/nx)|0;for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const x=cx+dx,y=cy+dy;if(x<0||y<0||x>=nx||y>=ny)continue;const k=y*nx+x;if(seen[k])continue;seen[k]=1;const m=free(x*S,y*S);if(!m)continue;okF[k]=m;q[qt++]=k;}}
     const cov=new Uint8Array(G2.cols*G2.rows);
     for(let k=0;k<nx*ny;k++){const m=okF[k];if(!m)continue;const x=(k%nx)*S,y=((k/nx)|0)*S;for(let f=0;f<4;f++){if(!(m&(1<<f)))continue;const r=bladeRect(tid,x,y,f,bw);const c0=Math.max(0,Math.floor(r.x/2)),c1=Math.min(G2.cols-1,Math.floor((r.x+r.w-1)/2)),r0=Math.max(0,Math.floor(r.y/2)),r1=Math.min(G2.rows-1,Math.floor((r.y+r.h-1)/2));for(let yy=r0;yy<=r1;yy++)for(let xx=c0;xx<=c1;xx++)cov[yy*G2.cols+xx]=1;
       // the footprint itself also rolls over snow
       const fp=footprint(tid,x,y,f);const a0=Math.max(0,Math.floor(fp.x/2)),a1=Math.min(G2.cols-1,Math.floor((fp.x+fp.w-1)/2)),b0=Math.max(0,Math.floor(fp.y/2)),b1=Math.min(G2.rows-1,Math.floor((fp.y+fp.h-1)/2));for(let yy=b0;yy<=b1;yy++)for(let xx=a0;xx<=a1;xx++)cov[yy*G2.cols+xx]=1;}}
     let tot=0,miss=0,missSnow=0;const pts=[];for(let i=0;i<G2.cols*G2.rows;i++){if(G2.type[i]===T_BLOCK)continue;tot++;if(!cov[i]){miss++;if(G2.depth[i]>=CLEAR_T){missSnow++;if(pts.length<4000)pts.push(i);}}}
     return {tid,bw,tot,clearable:G2.clearable,miss,missSnow,pct:missSnow/G2.clearable*100,cols:G2.cols,pts};})()`);
   r.id=id;r.ms=Math.round(performance.now()-t0);out.push(r);}
  return out;},{want,TI});
 if(errs.length)console.log('ERR',errs.slice(0,3));
 fs.writeFileSync('/tmp/reach_'+TI+'.json',JSON.stringify(res));
 res.sort((a,b)=>(b.pct||0)-(a.pct||0));for(const r of res)console.log(r.id.padEnd(14),r.err||'',r.tid,'bw',r.bw,'unreachable snow',r.missSnow,'cells =',(r.pct||0).toFixed(2)+'%',r.ms+'ms');
 await b.close();})();
