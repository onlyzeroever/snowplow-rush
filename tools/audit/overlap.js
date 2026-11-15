// scan every job for obstacle sprites whose opaque pixels overlap; writes report + contact sheets
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const page=process.argv[2]||'index6.html', outDir=process.argv[3]||'/tmp/ovl', MIN=+(process.argv[4]||8);
fs.mkdirSync(outDir,{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await (await b.newContext()).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/'+page+'?test=1');await p.waitForTimeout(800);
 const res=await p.evaluate(({MIN})=>{const R=window.__SR,L=R.LEVELS;const out=[];const cache=new Map();
  const alpha=(c)=>{if(cache.has(c))return cache.get(c);const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;const a=new Uint8Array(c.width*c.height);for(let i=0;i<a.length;i++)a[i]=d[i*4+3]>40?1:0;cache.set(c,a);return a;};
  for(let i=0;i<L.length;i++){let G;try{G=R.buildLevel(i);}catch(e){out.push({lv:L[i].id,err:e.message});continue;}
   const D=L[i].data||{};const tag=new Map();for(const p of (D.props||[])){const P2=R.PROPS[p[0]];if(!P2)continue;const a=p[3]!=null?p[3]:P2.arg,f=P2.foot(a);tag.set(p[1]+','+(p[2]+f[1])+','+(p[1]+f[0]),p[0]+(p[3]!=null?':'+p[3]:''));}
   const items=G.obstacles.filter(o=>o.spr&&o.spr.width).map(o=>({spr:o.spr,sx:Math.round(o.sx),sy:Math.round(o.sy),base:o.base,fw:o.w,fh:o.h,id:tag.get(o.sx+','+o.y+','+o.x)||('?'+o.spr.width+'x'+o.spr.height)}));
   for(const h of G.hazards)if(h.kind==='pull'&&h.spr)items.push({spr:h.spr,sx:Math.round(h.x)-1,sy:Math.round(h.y)-2,base:h.y+h.h,pull:1});
   for(const it of items)it.flat=false;G.obstacles.forEach((o,k)=>{});items.sort((a,b)=>a.sy-b.sy);const pairs=[];
   for(let a=0;a<items.length;a++){const A=items[a];const aa=alpha(A.spr);for(let c=a+1;c<items.length;c++){const B=items[c];if(B.sy>=A.sy+A.spr.height)break;
     const x0=Math.max(A.sx,B.sx),x1=Math.min(A.sx+A.spr.width,B.sx+B.spr.width),y0=Math.max(A.sy,B.sy),y1=Math.min(A.sy+A.spr.height,B.sy+B.spr.height);if(x1<=x0||y1<=y0)continue;
     const bb=alpha(B.spr);let n=0;for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){if(y-A.sy<=(A.spr.padTop||0)||y-B.sy<=(B.spr.padTop||0)+1)continue;if(aa[(y-A.sy)*A.spr.width+(x-A.sx)]&&bb[(y-B.sy)*B.spr.width+(x-B.sx)])n++;}
     if(n>=MIN&&!(A.base<A.sy||B.base<B.sy))pairs.push({a,b:c,n});}}
   if(pairs.length){const shots=[];for(const pr of pairs.slice(0,40)){const A=items[pr.a],B=items[pr.b];const ux=Math.min(A.sx,B.sx)-6,uy=Math.min(A.sy,B.sy)-6,ux1=Math.max(A.sx+A.spr.width,B.sx+B.spr.width)+6,uy1=Math.max(A.sy+A.spr.height,B.sy+B.spr.height)+6;
      const cv=document.createElement('canvas');cv.width=ux1-ux;cv.height=uy1-uy;const x=cv.getContext('2d');x.fillStyle='#e9f0f9';x.fillRect(0,0,cv.width,cv.height);
      for(const it of [A,B].sort((p,q)=>p.base-q.base))x.drawImage(it.spr,it.sx-ux,it.sy-uy);
      shots.push({ida:A.id,idb:B.id,data:!!(D.props&&D.props.length),n:pr.n,a:[A.sx,A.sy,A.spr.width,A.spr.height],b:[B.sx,B.sy,B.spr.width,B.spr.height],u:cv.toDataURL()});}
    out.push({lv:L[i].id,name:L[i].name,count:pairs.length,shots});}}
  return out;},{MIN});
 if(errs.length)console.log('ERR',errs.slice(0,3));
 const rep=[];let tot=0;for(const r of res){if(r.err){rep.push(r.lv+' ERROR '+r.err);continue;}tot+=r.count;rep.push(`${r.lv} (${r.name}): ${r.count}`+'\n'+r.shots.map(s=>`   ${s.n}px ${s.data?'D':'H'} ${s.ida}@${s.a} | ${s.idb}@${s.b}`).join('\n'));}
 fs.writeFileSync(outDir+'/report.txt',rep.join('\n'));console.log('levels with overlaps',res.filter(r=>r.count).length,'pairs',tot);
 // contact sheets
 const flat=[];for(const r of res)if(r.shots)for(const s of r.shots)flat.push({lv:r.lv,...s});
 fs.writeFileSync(outDir+'/flat.json',JSON.stringify(flat.map(f=>({lv:f.lv,n:f.n,a:f.a,b:f.b}))));
 const per=24;for(let pg=0;pg*per<flat.length;pg++){const chunk=flat.slice(pg*per,pg*per+per);
  const url=await p.evaluate(async(chunk)=>{const load=u=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=u;});const S=3,CW=300,CH=240,cols=6;const c=document.createElement('canvas');c.width=cols*CW;c.height=Math.ceil(chunk.length/cols)*CH;const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);
   for(let k=0;k<chunk.length;k++){const cx=(k%cols)*CW,cy=Math.floor(k/cols)*CH;const im=await load(chunk[k].u);const sc=Math.max(1,Math.min(S,Math.floor(Math.min((CW-10)/im.width,(CH-30)/im.height))));x.drawImage(im,cx+5,cy+22,im.width*sc,im.height*sc);x.fillStyle='#13306b';x.font='bold 12px sans-serif';x.fillText((k)+' '+chunk[k].lv+' '+chunk[k].n+'px @'+chunk[k].a[0]+','+chunk[k].a[1],cx+5,cy+14);x.strokeStyle='#c6d9f3';x.strokeRect(cx+.5,cy+.5,CW-1,CH-1);}
   return c.toDataURL();},chunk);
  fs.writeFileSync(`${outDir}/sheet_${String(pg).padStart(2,'0')}.png`,Buffer.from(url.split(',')[1],'base64'));}
 console.log('sheets',Math.ceil(flat.length/per));await b.close();})();
