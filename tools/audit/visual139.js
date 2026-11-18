// Regression checks for the Nov 19 visual audit (p139). Fast: builds every job once, no full-map renders.
//   node tools/audit/visual139.js [page]
// For the full picture use visaudit.js (renders + geometry) and motion.js (movers over time).
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const page = process.argv[2] || 'index6.html';
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/' + page + '?test=1'); await p.waitForTimeout(900);
  const r = JSON.parse(await p.evaluate(() => window.__EV(`(()=>{save.privSeen=true;save.tut=true;window.__HOLD=1;
    const out={taxi:[],animal:[],buried:[],cable:[],string:[],boat:[],n:0};
    for(let li=0;li<LEVELS.length;li++){startLevel(li);const id=LEVELS[li].id;out.n++;
      const fp=G.obstacles;const hitFp=(x,y,w,h)=>fp.find(o=>x+2<o.x+o.w-2&&o.x+2<x+w-2&&y+2<o.y+o.h-2&&o.y+2<y+h-2);
      // taxis: nothing parked in their lane
      for(const h of G.hazards)if(h.kind==='taxi'){const y0=h.r0!=null?h.r0:0,y1=h.r1!=null?h.r1:G.ph;const o=hitFp(h.x,y0,h.w,y1-y0);if(o)out.taxi.push([id,Math.round(h.x),o.x,o.y,o.w,o.h]);}
      // animals: none start inside a prop or off the map
      for(const h of G.hazards)if(h.kind==='sheep'){if(hitFp(h.x,h.y,h.w,h.h)||h.x+h.w>G.pw||h.x<0)out.animal.push([id,Math.round(h.x),Math.round(h.y)]);}
      // props buried inside shop buildings
      for(const o of fp){if(o.spr.width>=50)continue;const fx=Math.round(o.sx+o.spr.width/2),fy=Math.round(o.base-1);
        for(const s of G.scenery){if(s.spr.width<40||s.base<=o.base+1)continue;const a=sprAlpha(s.spr),lx=fx-s.sx,ly=fy-Math.round(s.sy);if(!(lx>=0&&ly>=0&&lx<s.spr.width&&ly<s.spr.height&&a[ly*s.spr.width+lx]))continue;
          const oa=sprAlpha(o.spr);let tot=0,cov=0;for(let y=0;y<o.spr.height;y++)for(let x=0;x<o.spr.width;x++){if(!oa[y*o.spr.width+x])continue;tot++;const X=Math.round(o.sx+x-s.sx),Y=Math.round(o.sy+y-s.sy);if(X>=0&&Y>=0&&X<s.spr.width&&Y<s.spr.height&&a[Y*s.spr.width+X])cov++;}
          if(cov>=tot*0.8){out.buried.push([id,o.sx,o.sy,o.spr.width+'x'+o.spr.height,+(cov/tot).toFixed(2)]);break;}}}
      // hazards hidden inside a shop building (e.g. a snow cannon firing out of a wall)
      for(const h of G.hazards)if(h.kind==='cannon'||h.kind==='balls'||h.kind==='thrower'){const fx=Math.round(h.x+h.w/2),fy=Math.round(h.y+h.h/2);for(const s of G.scenery){if(s.spr.width<40)continue;const a=sprAlpha(s.spr),lx=fx-s.sx,ly=fy-Math.round(s.sy);if(lx>=0&&ly>=0&&lx<s.spr.width&&ly<s.spr.height&&a[ly*s.spr.width+lx]){out.buried.push([id,h.kind,Math.round(h.x),Math.round(h.y)]);break;}}}
      // cables: every end runs into a building/prop or has a station
      for(const o of G.over)if(o.k==='gondola'||o.k==='liftline'){o.terms=cableTerms(o);const a=sprAlpha(o.spr),w=o.spr.width,h=o.spr.height;let y0=-1,y1=-1;for(let y=0;y<h&&y0<0;y++)for(let x=0;x<w;x++)if(a[y*w+x]){y0=y;break;}for(let y=h-1;y>=0&&y1<0;y--)for(let x=0;x<w;x++)if(a[y*w+x]){y1=y;break;}
        const cx=o.sx+(w>>1);for(const ey of [o.sy+y0,o.sy+y1]){if(ey<=6||ey>=G.ph-6)continue;if(o.terms.some(t=>Math.abs(t[1]-ey)<2))continue;if(!solidNear(cx,ey,10,10,12,true))out.cable.push([id,cx,ey]);}}
      // strings of lights / banners / lanterns: each end on a wall, prop, map edge or post
      for(const o of G.over)if(o.k==='lights'||o.k==='banner'||o.k==='lant'){o.posts=overPosts(o);const a=sprAlpha(o.spr),w=o.spr.width,h=o.spr.height;
        for(const lx of [0,w-1]){let ty=-1;for(let y=0;y<h;y++)if(a[y*w+lx]){ty=y;break;}if(ty<0)continue;const ex=o.sx+lx,ey=o.sy+ty;if(ex<=3||ex>=G.pw-4)continue;
          if(o.posts.some(q=>q[0]===ex))continue;if(!solidNear(ex,ey,2,8,2))out.string.push([id,ex,ey]);}}
      // boats: their see-through corners follow the yard, not a white box
      if(G.obstacles.some(o=>o.bare)&&!(G.bare&&G.bare.some(v=>v)))out.boat.push(id);}
    // a boat corner shows bare ground once the yard next to it is cleared
    let boatOK=null;{const li=LEVELS.findIndex(L=>L.id==='boatyard');startLevel(li);const i=G.bare.findIndex(v=>v);if(i>=0){const j=G.bareSrc[i];setDepth(G,j,0);flushLevel(G);
      const cx=i%G.cols,cy=(i/G.cols)|0,px=G.img.data[((cy*2)*G.pw+cx*2)*4];boatOK=px<200;}}
    out.boatOK=boatOK;return JSON.stringify(out);})()`)));
  let fails = 0; const ok = (c, m, d) => { console.log((c ? 'ok   ' : 'FAIL ') + m + (d !== undefined ? ' ' + JSON.stringify(d) : '')); if (!c) fails++; };
  ok(r.n === 125, 'built every job', r.n);
  ok(!r.taxi.length, 'no taxi lane runs through a parked prop', r.taxi.slice(0, 5));
  ok(!r.animal.length, 'no animal starts inside a prop or off the map', r.animal.slice(0, 5));
  ok(!r.buried.length, 'no prop buried inside a shop building', r.buried.slice(0, 5));
  ok(!r.cable.length, 'every gondola/chairlift cable end reaches a station', r.cable);
  ok(!r.string.length, 'every string of lights, banner and lantern string is held up at both ends', r.string.slice(0, 5));
  ok(!r.boat.length && r.boatOK === true, 'boat corners show the cleared yard, not a white box', { boat: r.boat, boatOK: r.boatOK });
  ok(!errs.length, 'no errors', errs.slice(0, 3));
  console.log(fails ? 'FAILS ' + fails : 'ALL OK'); await b.close(); process.exit(fails ? 1 : 0);
})();
