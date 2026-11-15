// usage: node propview.js "id[:arg],id2" out.png [scale] [pages: before_props.html,index6.html]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const ids=process.argv[2].split(','), out=process.argv[3], S=+(process.argv[4]||5), pages=(process.argv[5]||'before_props.html,index6.html').split(',');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const grab=async(pg)=>{const p=await (await b.newContext()).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/'+pg+'?test=1');await p.waitForTimeout(700);
  const r=await p.evaluate((ids)=>{const R=window.__SR,P=R.PROPS;return ids.map(t=>{const [id,av]=t.split(':');const d=P[id];if(!d)return {id:t,u:null};let a=av!=null?+av:d.arg;let s=d.make(a);s=R.frostOf(s)||s;return {id:t,u:s.toDataURL()};});},ids);
  if(errs.length)console.log(pg,errs);return r;};
 const sets=[];for(const pg of pages)sets.push(await grab(pg));
 const p=await (await b.newContext()).newPage();
 const url=await p.evaluate(async({sets,S,pages})=>{const load=u=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=u;});
  const ims=[];for(const set of sets){const row=[];for(const e of set)row.push(e.u?await load(e.u):null);ims.push(row);}
  const n=sets[0].length;let W=10,colX=[];for(let k=0;k<n;k++){colX.push(W);const w=Math.max(...ims.map(r=>r[k]?r[k].width:10))*S;W+=Math.max(w,90)+20;}
  const rowH=ims.map(r=>Math.max(...r.map(i=>i?i.height:10))*S+30);const H=rowH.reduce((a,b)=>a+b,0)+10;
  const c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle='#eef4fb';x.fillRect(0,0,W,H);
  let y=5;for(let r=0;r<ims.length;r++){for(let k=0;k<n;k++){x.fillStyle='#13306b';x.font='bold 13px sans-serif';x.fillText(sets[r][k].id+(sets.length>1?'  '+(r==0?'before':'after'):''),colX[k],y+14);const im=ims[r][k];if(im)x.drawImage(im,colX[k],y+22,im.width*S,im.height*S);}y+=rowH[r];x.fillStyle='#c6d9f3';x.fillRect(0,y-3,W,1);}
  return c.toDataURL();},{sets,S,pages});
 fs.writeFileSync(out,Buffer.from(url.split(',')[1],'base64'));console.log('ok',out);await b.close();})();
