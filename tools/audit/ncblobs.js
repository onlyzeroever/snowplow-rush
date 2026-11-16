// components of snow unreachable for machine B but reachable for the shovel. node ncblobs.js id toolIdx [minCells]
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const [id,ti,minc]=process.argv.slice(2);
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await (await b.newContext()).newPage();
 await p.goto('http://127.0.0.1:8765/'+(process.env.PAGE||'index6.html')+'?test=1');await p.waitForTimeout(800);
 const r=await p.evaluate(({id,ti,minc})=>{const R=window.__SR,EV=window.__EV;window.__HOLD=true;R.save.tut=true;R.save.tool=12;const li=R.LEVELS.findIndex(l=>l.id===id);
  R.save.use=0;R.startLevel(li);let G=EV('G');const a=G.nc?G.nc.slice():new Uint8Array(G.cols*G.rows);R.save.use=ti;R.startLevel(li);G=EV('G');const c=G.nc,W=G.cols,H=G.rows;
  const seen=new Uint8Array(W*H),out=[];for(let i=0;i<W*H;i++){if(!c[i]||a[i]||seen[i])continue;const st=[i];seen[i]=1;let n=0,x0=1e9,x1=-1,y0=1e9,y1=-1;
   while(st.length){const k=st.pop();n++;const x=k%W,y=(k/W)|0;x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);for(const q of [x>0?k-1:-1,x<W-1?k+1:-1,y>0?k-W:-1,y<H-1?k+W:-1])if(q>=0&&c[q]&&!a[q]&&!seen[q]){seen[q]=1;st.push(q);}}
   if(n>=minc){const bx=[x0*2,y0*2,(x1+1)*2,(y1+1)*2];const near=(L=>{const pr=(R.LEVELS[li].data&&R.LEVELS[li].data.props)||[];return pr.map((q,qi)=>[qi,q,Math.hypot(Math.max(bx[0]-q[1],0,q[1]-bx[2]),Math.max(bx[1]-q[2],0,q[2]-bx[3]))]).sort((u,v)=>u[2]-v[2]).slice(0,3).map(z=>z[0]+':'+JSON.stringify(z[1])).join(' ');})();out.push([n,bx,near]);}}
  out.sort((u,v)=>v[0]-u[0]);return {tot:out.reduce((s,o)=>s+o[0],0),out:out.slice(0,25)};},{id,ti:+ti,minc:+(minc||8)});
 console.log(id,'machine',ti,'disparity cells',r.tot);for(const o of r.out)console.log(String(o[0]).padStart(5),JSON.stringify(o[1]),o[2]);await b.close();})();
