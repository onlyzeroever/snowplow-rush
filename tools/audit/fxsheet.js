// node fxsheet.js page out.png  -- captures effect frames (bonk, gift, crunch, sparkles, coins) zoomed
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const page=process.argv[2],out=process.argv[3];
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await (await b.newContext({viewport:{width:360,height:640}})).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/'+page+'?test=1');await p.waitForTimeout(800);
 const res=await p.evaluate(async()=>{const R=window.__SR,EV=window.__EV;window.__HOLD=true;R.save.tut=true;R.save.privSeen=true;const raf=()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  const cv=document.querySelector('canvas');const rows=[];
  const grab=async(wx,wy,w,h)=>{await raf();const s=cv.width/180;const c=document.createElement('canvas');c.width=w*4;c.height=h*4;const x=c.getContext('2d');x.imageSmoothingEnabled=false;const sx=(wx-w/2),sy=(wy-h/2)-R.camY+R.VIEW_Y;x.drawImage(cv,sx*s,sy*s,w*s,h*s,0,0,w*4,h*4);return c.toDataURL();};
  const setup=()=>{R.startLevel(R.LEVELS.findIndex(l=>l.id==='maple'));window.__STEP(60,1/30,0);R.run.moved=true;const P=R.P;EV('(()=>{G.hazards=[];G.spawners=[];G.cows=[];})()');P.x=90;P.y=330;P.f=0;P.inv=0;window.__STEP(40,1/30,40);P.inv=0;P.stun=0;};
  const seq=async(name,trigger,times,wx,wy)=>{setup();const P=R.P;const t0=trigger();const fr=[];let el=0;for(const t of times){const n=Math.max(1,Math.round((t-el)*30));window.__STEP(n,1/30,n);el+=n/30;const c=(typeof wx==='function')?wx():[P.x,P.y-8];fr.push(await grab(c[0],c[1],64,44));}rows.push({name,fr,times});};
  await seq('bonk',()=>EV('hit("ob")'),[0.03,0.1,0.2,0.4,0.8]);
  await seq('gift',()=>EV('openGift({x:P.x,y:P.y-16})'),[0.05,0.15,0.3,0.5,0.8]);
  let cpos=null;await seq('crunch',()=>{EV('(()=>{const o=G.obstacles.filter(o=>o.crush).sort((a,c)=>Math.abs(a.y-330)-Math.abs(c.y-330))[0];if(!o)return null;P.x=o.x+o.w/2;P.y=o.y+o.h+16;window.__CO=[o.x+o.w/2,o.y+o.h/2];crushOb(o);return 1;})()');},[0.03,0.1,0.2,0.4,0.6],()=>window.__CO||[90,300]);
  await seq('sparkles',()=>EV('(()=>{for(let k=0;k<7;k++)particles.push({x:P.x-18+k*6,y:P.y-12+(k%3)*4,vx:0,vy:0,z:1,vz:8,life:0.5,t:-k*0.04,kind:"spark"});})()'),[0.05,0.12,0.2,0.3,0.42]);
  await seq('coins',()=>EV('(()=>{for(let k=0;k<5;k++)particles.push({x:P.x-10+k*5,y:P.y-10,vx:0,vy:0,z:0,vz:0,life:2,t:0,kind:"coin"});})()'),[0.03,0.1,0.17,0.24,0.31]);
  return rows;});
 const u=await p.evaluate(async(rows)=>{const load=u=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=u;});const FW=256,FH=176;const c=document.createElement('canvas');c.width=120+rows[0].fr.length*(FW+8);c.height=rows.length*(FH+24);const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);
  for(let r=0;r<rows.length;r++){x.fillStyle='#13306b';x.font='bold 16px sans-serif';x.fillText(rows[r].name,6,r*(FH+24)+FH/2);for(let k=0;k<rows[r].fr.length;k++){const im=await load(rows[r].fr[k]);x.drawImage(im,120+k*(FW+8),r*(FH+24)+16);x.font='11px sans-serif';x.fillStyle='#6a7896';x.fillText(rows[r].times[k]+'s',120+k*(FW+8),r*(FH+24)+12);}}return c.toDataURL();},res);
 fs.writeFileSync(out,Buffer.from(u.split(',')[1],'base64'));console.log('ok',errs.slice(0,3));await b.close();})();
