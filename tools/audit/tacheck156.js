// Time Attack fairness: shortest drivable path between checkpoint lines vs. the time each segment gives
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await (await b.newContext({viewport:{width:390,height:844}})).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://127.0.0.1:8766/lab6.html?test=1&lab&review=all');await p.waitForTimeout(900);
const r=await p.evaluate(()=>window.__EV(`(()=>{const out=[];for(const job of LAB_JOBS.timeattack)for(const m of ['shovel','truck','super','rotary']){save.privSeen=true;save.tut=true;window.__HOLD=1;{const ti=toolIdx(m);save.tool=Math.max(save.tool,ti);save.use=ti;}
  startLevel(LEVELS.findIndex(L=>L.id===job),{event:'lab-timeattack'});const S=G.lab,tid=TOOLS[useIdx()].id,R=labReachGrid(G,tid),gw=R.gw,gh=R.gh,st=R.st,v=moveSpeed();
  // BFS distance (px) from a set of start cells to the first cell that crosses line y in direction dir
  const bfs=(seeds,y,dir)=>{const d=new Float32Array(gw*gh).fill(1e9),q=[];for(const k of seeds){d[k]=0;q.push(k);}for(let i=0;i<q.length;i++){const k=q[i],x=k%gw,yy=(k/gw)|0;if(dir>0?yy*st>=y+3:yy*st<=y-3)return {len:d[k],k};
      for(const [ax,ay] of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+ax,ny=yy+ay;if(nx<0||ny<0||nx>=gw||ny>=gh)continue;const nk=ny*gw+nx;if(!R.seen[nk]||d[nk]<1e9)continue;d[nk]=d[k]+st;q.push(nk);}}return {len:1e9};};
  let seeds=[Math.round(G.start.y/st)*gw+Math.round(G.start.x/st)];if(!R.seen[seeds[0]]){for(let k=0;k<R.seen.length;k++)if(R.seen[k]&&Math.hypot((k%gw)*st-G.start.x,((k/gw)|0)*st-G.start.y)<12){seeds=[k];break;}}
  const segs=[];let tot=0,need=0;S.cps.forEach((c,k)=>{const r2=bfs(seeds,c.y,c.dir);const t=S.seg[k]+(k===0?5:0);segs.push(Math.round(r2.len/(t*v)*100));
    // next seeds: every reachable cell within 3 rows past this line
    seeds=[];for(let i=0;i<R.seen.length;i++){if(!R.seen[i])continue;const yy=((i/gw)|0)*st;if(Math.abs(yy-(c.y+c.dir*4))<=4)seeds.push(i);}});
  out.push({job,m,v:Math.round(v),t0:G.def.time,n:S.cps.length,pct:segs});}return JSON.stringify(out);})()`));
for(const o of JSON.parse(r))console.log(o.job.padEnd(11),o.m.padEnd(7),'v',o.v,'t0',o.t0,'n',o.n,'path/allowed %',o.pct.join(' '));console.log(errs);await b.close();})();
