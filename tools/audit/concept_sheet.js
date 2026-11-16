const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs = require('fs');
(async () => { const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await br.newContext({ viewport: { width: 400, height: 400 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(1000);
  const code = fs.readFileSync('/home/claude/scripts/concepts.js', 'utf8');
  await p.evaluate(src => window.__EV(`window.__C=(()=>{${src};return {drawLoader,drawTitan,drawIcebreaker,drawCruiser,bladeTitan,bladeIcebreaker,bladeCruiser,bladeLoader};})()`), code);
  const url = await p.evaluate(() => window.__EV(`(()=>{const C=window.__C;
    const NEW={loader:{d:C.drawLoader,bl:C.bladeLoader,hh:22,bt:8,bw:42,c:{b:'#f5b82e',l:'#ffe07a',d:'#c4861a',x:'#ffc727'}},
      titan:{d:C.drawTitan,bl:(g,cx,y,bw,bt,c,fr)=>C.bladeTitan(g,cx,y,bw,bt,c,fr),hh:24,bt:9,bw:50,c:{b:'#4a5068',l:'#7a8298',d:'#2e3346'}},
      icebreaker:{d:C.drawIcebreaker,bl:(g,cx,y,bw,bt,c,fr)=>C.bladeIcebreaker(g,cx,y,bw,bt,c,fr),hh:24,bt:7,bw:50,c:{b:'#d8343c',l:'#ff6a6a',d:'#9a1f2a'}},
      cruiser:{d:C.drawCruiser,bl:C.bladeCruiser,hh:24,bt:8,bw:50,c:{b:'#e8562a',l:'#ff8a5a',d:'#a8381a'}}};
    const sprite=(id,fr)=>{if(NEW[id]){const n=NEW[id],cw=72,ch=n.hh*2+n.bt+30,cv=mk(cw,ch),g=cv.getContext('2d'),ox=36,oy=n.bt+n.hh+8;n.d(g,ox,oy,fr,n.c);n.bl(g,ox,oy-n.hh-n.bt,n.bw,n.bt,n.c,fr);return cv;}
      const t=TOOLS[toolIdx(id)],v=vehicleSprite(id,t.width,2,fr,0);return v.c;};
    const W2=420,H2=840,S=mk(W2,H2),g=S.getContext('2d');g.imageSmoothingEnabled=false;
    g.fillStyle='#13306b';g.fillRect(0,0,W2,H2);
    text(g,'NEW MACHINES: CONCEPTS',W2/2,8,'#ffd23f',{align:'center',scale:2});text(g,'ACTUAL GAME PIXELS, 1X AND 3X. NOT IN THE GAME YET.',W2/2,26,'#9fc0e8',{align:'center',outline:null});
    // lineup at 1x on snow, in price order
    g.fillStyle='#f4f8ff';g.fillRect(8,40,W2-16,92);g.fillStyle='#e3ecf8';for(let x=8;x<W2-8;x+=6)g.fillRect(x+(x%4),40+(x*7)%88,3,1);
    const line=[['super','SUPER PLOW'],['loader','WHEEL LOADER*'],['snowcat','SNOWCAT'],['rotary','ROTARY'],['titan','TITAN*'],['icebreaker','ICEBREAKER*'],['cruiser','CRUISER*']];
    line.forEach(([id,nm],k)=>{const s=sprite(id,1),x0=14+k*58;g.drawImage(s,x0+29-Math.floor(s.width/2),46);text(g,nm,x0+29,122,id==='loader'||NEW[id]?'#e03a4e':'#13306b',{align:'center',outline:null});});
    text(g,'* NEW. THE LINEUP IS TO SCALE.',14,136,'#9fc0e8',{outline:null});
    // big views at 3x, two frames each so the motion reads
    const big=[['loader','WHEEL LOADER','HARBOUR, ABOUT 2.2M COINS','BUCKET ON LIFT ARMS, BENDS IN THE MIDDLE'],
      ['titan','GLACIER TITAN','FINALE IDEA A','MINING CRAWLER WITH A RED-HOT CUTTER DRUM'],
      ['icebreaker','ICEBREAKER','FINALE IDEA B','AN ICE-SHIP ON TRACKS, HELICOPTER ON BOARD'],
      ['cruiser','SNOW CRUISER','FINALE IDEA C','GIANT EXPEDITION RIG, PLANE ON THE ROOF']];
    big.forEach(([id,nm,sub,desc],k)=>{const col=k%2,row=Math.floor(k/2),x0=8+col*206,y0=148+row*344;g.fillStyle='#0b1838';g.fillRect(x0,y0,198,336);g.fillStyle='#a8d4f2';g.fillRect(x0+4,y0+4,190,276);
      g.fillStyle='#f4f8ff';g.fillRect(x0+4,y0+150,190,130);
      {const s=sprite(id,(window.__FR||0)),cw=58,sx=Math.floor(s.width/2)-29;g.drawImage(s,sx,0,cw,s.height,x0+99-87,y0+8,cw*3,s.height*3);}
      text(g,nm,x0+99,y0+288,'#ffd23f',{align:'center',scale:2});text(g,sub,x0+99,y0+306,'#7fe08a',{align:'center',outline:null});text(g,desc,x0+99,y0+318,'#ffffff',{align:'center',outline:null});});
    return S.toDataURL();})()`));
  fs.writeFileSync('/tmp/concept_sheet.png', Buffer.from(url.split(',')[1], 'base64')); console.log('errors', JSON.stringify(errs)); await br.close(); })();
