// try prop edits on one job in-page and report unreachable % per machine. node nctry.js id 'edits-json' [renderTool out y0 hh]
// edits: [[idx,x,y],...] move ; [idx,null] delete ; ['add',pid,x,y,arg]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const [id,ej,rt,out,y0s,hhs]=process.argv.slice(2);const edits=JSON.parse(ej||'[]');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await (await b.newContext()).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/'+(process.env.PAGE||'index6.html')+'?test=1');await p.waitForTimeout(800);
 const r=await p.evaluate(({id,edits,rt,y0,hh})=>{const R=window.__SR,EV=window.__EV;window.__HOLD=true;R.save.tut=true;const TN=EV('TOOLS.length'),tids=EV('TOOLS.map(t=>t.id)');
  const li=R.LEVELS.findIndex(l=>l.id===id);const L=R.LEVELS[li];const pr=L.data?L.data.props:[];const del=[];
  for(const e of edits){if(e[0]==='key'){L.data[e[1]][e[2]][e[3]]=e[4];continue;}if(e[0]==='add')pr.push(e.slice(1));else if(e[1]===null)del.push(e[0]);else{pr[e[0]][1]=e[1];pr[e[0]][2]=e[2];}}
  del.sort((a,c)=>c-a).forEach(i=>pr.splice(i,1));
  const res={};for(let ti=0;ti<TN;ti++){if(tids[ti]==='ufo')continue;R.save.tool=TN-1;R.save.use=ti;R.startLevel(li);const G=EV('G');res[tids[ti]]=+((G.ncN||0)/(G.clearable+(G.ncN||0))*100).toFixed(2);}
  let img=null;if(rt!=null){R.save.use=+rt;R.startLevel(li);const G=EV('G');const c=document.createElement('canvas');c.width=G.pw;c.height=hh;const x=c.getContext('2d');x.drawImage(G.canvas,0,-y0);
   for(const o of G.obstacles.slice().sort((a,b2)=>a.base-b2.base))x.drawImage(o.spr,o.sx,o.sy-y0);
   x.fillStyle='rgba(255,0,60,0.75)';if(G.nc)for(let i=0;i<G.nc.length;i++)if(G.nc[i]){const cx=i%G.cols,cy=(i/G.cols)|0;x.fillRect(cx*2,cy*2-y0,2,2);}img=c.toDataURL();}
  return {res,img};},{id,edits,rt:rt==null?null:+rt,y0:+(y0s||0),hh:+(hhs||700)});
 console.log(id,Object.entries(r.res).filter(([k,v])=>v>0).map(([k,v])=>k+':'+v).join(' ')||'all 0',errs.length?'ERR '+errs[0]:'');
 if(r.img)fs.writeFileSync(out,Buffer.from(r.img.split(',')[1],'base64'));await b.close();})();
