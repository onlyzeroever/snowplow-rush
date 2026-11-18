// Filmstrip of one spot of a job over time: node film.js id x y w h frames every out.png [scale] [preSteps] [playerX,playerY]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const [id,X,Y,Wd,Hd,N,EV,out,S0,PRE,PP]=process.argv.slice(2);const S=+(S0||2);
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await (await b.newContext()).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/index6.html?test=1');await p.waitForTimeout(800);
 const url=await p.evaluate(a=>window.__EV(`(()=>{const [id,X,Y,Wd,Hd,N,EV,S,PRE,PP]=${JSON.stringify(a)};save.privSeen=true;save.tut=true;save.fbRuns=8;save.bzTips=9;window.__HOLD=1;
  startLevel(LEVELS.findIndex(L=>L.id===id));run.time=9999;run.moved=true;const pp=PP?PP.split(',').map(Number):[-300,-300];
  for(let i=0;i<(+PRE||0);i++){P.x=pp[0];P.y=pp[1];P.inv=99;update(1/30);}
  const n=+N,ev=+EV,cols=Math.min(n,Math.floor(1500/(Wd*S+4)));const c=document.createElement('canvas');c.width=cols*(Wd*S+4);c.height=Math.ceil(n/cols)*(Hd*S+14);const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);
  for(let k=0;k<n;k++){for(let s=0;s<ev;s++){P.x=pp[0];P.y=pp[1];P.inv=99;update(1/30);}camY=Math.max(0,Math.min(G.ph-VIEW_H,+Y-40));shake=0;draw();
    const cx=(k%cols)*(Wd*S+4),cy=Math.floor(k/cols)*(Hd*S+14);x.drawImage(b.canvas,+X,VIEW_Y+(+Y-camY),+Wd,+Hd,cx,cy+12,Wd*S,Hd*S);x.fillStyle='#000';x.font='10px sans-serif';x.fillText(String(k*ev),cx+2,cy+10);}
  return c.toDataURL();})()`),[id,X,Y,Wd,Hd,N,EV,S,PRE,PP]);
 fs.writeFileSync(out,Buffer.from(url.split(',')[1],'base64'));console.log(out,errs.slice(0,2));await b.close();})();
