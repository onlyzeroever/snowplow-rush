const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
(async () => { const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await br.newContext({ viewport: { width: 400, height: 400 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(1000);
  for (const fr of [0, 1]) {
  const url = await p.evaluate(fr => window.__EV(`(()=>{const FR=${fr};
    const W2=420,H2=900,S=mk(W2,H2),g=S.getContext('2d');g.imageSmoothingEnabled=false;g.fillStyle='#13306b';g.fillRect(0,0,W2,H2);
    text(g,'FRONT LOADER + ICEBREAKER',W2/2,8,'#ffd23f',{align:'center',scale:2});text(g,'GAME PIXELS FROM THE BUILD. FOR YOUR OK.',W2/2,26,'#9fc0e8',{align:'center',outline:null});
    const spr=(id,w,si,fr)=>vehicleSprite(id,w,id==='icebreaker'?0:2,fr,si).c;
    // the ladder at 1x, to scale, each at its base width
    g.fillStyle='#f4f8ff';g.fillRect(8,40,W2-16,100);
    const line=['super','loader','snowcat','rotary','icebreaker'],nm={super:'SUPER PLOW',loader:'FRONT LOADER',snowcat:'SNOWCAT',rotary:'ROTARY',icebreaker:'ICEBREAKER'};
    line.forEach((id,k)=>{const t=TOOLS[toolIdx(id)],s=spr(id,t.width,0,FR),x0=14+k*80;g.drawImage(s,x0+40-Math.floor(s.width/2),46);text(g,nm[id],x0+40,124,id==='loader'||id==='icebreaker'?'#e03a4e':'#13306b',{align:'center',outline:null});});
    text(g,'NEW IN RED. TO SCALE, EACH AT ITS STARTING WIDTH.',14,144,'#9fc0e8',{outline:null});
    // big 3x views
    const big=[['loader','FRONT LOADER','2.5M COINS, AROUND THE THEME PARK','BUCKET ON LIFT ARMS, BENDS IN THE MIDDLE','WIDTH 52  SPEED 80  x7.5 COINS'],['icebreaker','ICEBREAKER','180M, THE NORTH FINALE','ICE-SHIP ON TRACKS: NO SLIDING ON ICE','WIDTH 62  SPEED 132  x18 COINS']];
    big.forEach(([id,n1,n2,n3,n4],k)=>{const x0=8+k*206,y0=156;g.fillStyle='#0b1838';g.fillRect(x0,y0,198,330);g.fillStyle='#a8d4f2';g.fillRect(x0+4,y0+4,190,250);g.fillStyle='#f4f8ff';g.fillRect(x0+4,y0+130,190,124);
      const t=TOOLS[toolIdx(id)],s=spr(id,t.width,0,FR),cw=Math.min(s.width,62),sx=Math.floor(s.width/2)-Math.floor(cw/2);g.drawImage(s,sx,0,cw,s.height,x0+99-Math.floor(cw*3/2),y0+10,cw*3,s.height*3);
      text(g,n1,x0+99,y0+262,'#ffd23f',{align:'center',scale:2});text(g,n2,x0+99,y0+282,'#7fe08a',{align:'center',outline:null});text(g,n3,x0+99,y0+296,'#ffffff',{align:'center',outline:null});text(g,n4,x0+99,y0+310,'#9fc0e8',{align:'center',outline:null});});
    // skins at 2x
    [['loader',0],['icebreaker',1]].forEach(([id,k])=>{const y0=500+k*196;g.fillStyle='#0b1838';g.fillRect(8,y0,W2-16,188);text(g,nm[id]+' SKINS',W2/2,y0+6,'#ffd23f',{align:'center'});
      const t=TOOLS[toolIdx(id)];for(let si=0;si<6;si++){const s=spr(id,t.width,si,FR),x0=12+si*67,cw=Math.min(s.width,30),sx=Math.floor(s.width/2)-Math.floor(cw/2);g.fillStyle='#f4f8ff';g.fillRect(x0,y0+20,63,148);
        g.drawImage(s,sx,0,cw,s.height,x0+31-cw,y0+26,cw*2,s.height*2);const nmz=(SKIN_NAMES[id][si]||'');text(g,nmz,x0+31,y0+172,'#ffffff',{align:'center',outline:null,scale:textW(nmz)>62?1:1});}});
    text(g,'5 SKINS EACH, PLUS GOLD PAINT LIKE EVERY MACHINE.',W2/2,H2-14,'#9fc0e8',{align:'center',outline:null});
    return S.toDataURL();})()`, fr), fr);
  fs.writeFileSync('/tmp/nmsheet_' + fr + '.png', Buffer.from(url.split(',')[1], 'base64')); }
  console.log('errors', JSON.stringify(errs)); await br.close(); })();
