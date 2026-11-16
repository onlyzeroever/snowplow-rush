// compare rendered frames of two builds with seeded randomness. node pixcmp.js pageA pageB id:tool,...
const { chromium } = require('/opt/npm-tools/node_modules/playwright');const fs=require('fs');
const [A,B,list]=process.argv.slice(2);
async function frames(b,pg,id,ti){const p=await (await b.newContext({viewport:{width:360,height:640}})).newPage();
 await p.addInitScript(()=>{let a=12345;Math.random=()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};let pn=0;performance.now=()=>(pn+=16.67);});
 await p.goto('http://127.0.0.1:8765/'+pg+'?test=1');await p.waitForTimeout(600);
 const out=await p.evaluate(([id,ti])=>{const R=window.__SR;window.__HOLD=true;R.save.tut=true;R.save.tool=12;R.save.use=ti;R.startLevel(R.LEVELS.findIndex(l=>l.id===id));window.__STEP(40,1/30,1);if(R.run)R.run.moved=true;
  const P=R.P,G=R.G,res=[];for(let k=0;k<10;k++){const y=Math.max(30,G.ph*(1-k/10)-60);for(let j=0;j<6;j++){P.y=y-j*6;P.x=20+((k*37+j*23)%140);P.f=(k+j)%4;window.__STEP(1,1/30,0);}
   const c=document.createElement('canvas');c.width=180;c.height=320;const x=c.getContext('2d');x.drawImage(window.__SR.bufCanvas||document.querySelector('canvas'),0,0,180,320);window.__EV('particles=[];floats=[];');window.__STEP(0,1/30,1);res.push(window.__EV('b.canvas.toDataURL()'));}
  return res;},[id,ti]);await p.close();return out;}
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const u=await (await b.newContext()).newPage();
 for(const it of list.split(',')){const [id,ti]=it.split(':');const fa=await frames(b,A,id,+ti),fb=await frames(b,B,id,+ti);
  const r=await u.evaluate(async([fa,fb])=>{const load=s=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=s;});const out=[];for(let k=0;k<fa.length;k++){const ia=await load(fa[k]),ib=await load(fb[k]);const c=document.createElement('canvas');c.width=ia.width;c.height=ia.height;const x=c.getContext('2d');x.drawImage(ia,0,0);const da=x.getImageData(0,0,c.width,c.height).data;x.clearRect(0,0,c.width,c.height);x.drawImage(ib,0,0);const db=x.getImageData(0,0,c.width,c.height).data;let n=0;for(let i=0;i<da.length;i+=4)if(Math.abs(da[i]-db[i])+Math.abs(da[i+1]-db[i+1])+Math.abs(da[i+2]-db[i+2])>6)n++;out.push(n);}return out;},[fa,fb]);
  console.log(id,ti,'diff px per frame:',r.join(' '));if(r.some(n=>n>0)){const k=r.findIndex(n=>n>0);fs.writeFileSync('/tmp/audit/pc_'+id+'_a.png',Buffer.from(fa[k].split(',')[1],'base64'));fs.writeFileSync('/tmp/audit/pc_'+id+'_b.png',Buffer.from(fb[k].split(',')[1],'base64'));}}
 await b.close();})();
