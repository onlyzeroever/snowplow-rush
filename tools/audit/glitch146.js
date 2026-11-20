// Glitch audit (Alex, Nov 20: "a cow stuck in the fence"): run every job with a ghost player sweeping the map and
// look at every walking character and animal as it is DRAWN, not just its collision box:
//   behind-prop  - part of the mover is drawn under a prop it stands beside (prop's opaque pixels over the mover,
//                  mover's feet inside the prop's height band): looks stuck in the prop
//   in-prop      - mover's feet inside a prop's collision box
//   off-map      - mover drawn more than 2px past the map's left/right edge
// Only movers that stay in that state for 0.5s+ are reported (a passing overlap of a frame or two is fine).
//   node tools/audit/glitch146.js [ids|all] [out.json] [page=index6.html] [port=8765] [qs]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const want = process.argv[2] || 'all', out = process.argv[3] || '/tmp/glitch146.json', page = process.argv[4] || 'index6.html', port = process.argv[5] || 8765, qs = process.argv[6] || '';
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:' + port + '/' + page + '?test=1' + (qs ? '&' + qs : '')); await p.waitForTimeout(900);
  const all = JSON.parse(await p.evaluate(() => window.__EV('JSON.stringify(LEVELS.map(L=>L.id))')));
  const list = want === 'all' ? all : want.split(',');
  await p.evaluate(() => window.__EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=8;save.bzTips=9;window.__HOLD=1;
    window.__AM=new Map();window.__alpha=c=>{let m=window.__AM.get(c);if(m)return m;const w=c.width,h=c.height;m=new Uint8Array(w*h);try{const d=c.getContext('2d').getImageData(0,0,w,h).data;for(let i=0;i<w*h;i++)m[i]=d[i*4+3]>40?1:0;}catch(e){}window.__AM.set(c,m);return m;};return 1;})()`));
  const res = [];
  for (const id of list) {
    const r = await p.evaluate(([id, opts]) => window.__EV(`(()=>{const li=LEVELS.findIndex(L=>L.id==='${id}');if(li<0)return JSON.stringify({id:'${id}',err:'none'});
      startLevel(li${opts ? ',' + opts : ''});run.time=9999;run.moved=true;const ph=G.ph,pw=G.pw;
      // props as drawn: sprite box, base, opaque mask; bucketed by 64px bands
      const DP=(G.def.data&&G.def.data.props)||[],pname=o=>{let best=null,bd=9;for(const q of DP){const d=Math.abs(q[1]-o.sx)+Math.abs(q[2]-(o.sy+(o.spr.padTop||0)));if(d<bd){bd=d;best=q;}}return best?best[0]+'@'+best[1]+','+best[2]:'prop@'+Math.round(o.x)+','+Math.round(o.y);};
      const props=[];for(const o of G.obstacles)props.push({o,nm:pname(o),sx:o.sx,sy:o.sy,spr:o.spr,base:o.base,cb:[o.x,o.y,o.w,o.h]});
      for(const o of G.scenery)props.push({o,nm:'building',sx:o.sx,sy:o.sy,spr:o.spr,base:o.base,cb:null});
      const band=new Map();for(const q of props){const y0=Math.floor(q.sy/64),y1=Math.floor((q.sy+q.spr.height)/64);for(let k=y0;k<=y1;k++){if(!band.has(k))band.set(k,[]);band.get(k).push(q);}}
      const near=(y0,y1)=>{const s=new Set();for(let k=Math.floor(y0/64);k<=Math.floor(y1/64);k++)for(const q of (band.get(k)||[]))s.add(q);return s;};
      // movers as drawn
      const box=(m)=>{if(m.cow){const cw=m.cow,spr=cw.flip?COWL:COW;return {x:Math.round(cw.x)-8,y:Math.round(cw.y)-10,spr,base:cw.y+3,fx:cw.x,fy:cw.y};}
        const hz=m.hz,hx=Math.round(hz.x),hy=Math.round(hz.y);let spr=null,x=0,y=0;
        if(hz.kind==='dog'){spr=hz.spr||(hz.vx>=0?SPR.dog:SPR.dogL);x=hx-1;y=hy-4;}
        else if(hz.kind==='cart'){spr=hz.vx<0?CARTL:CART;x=hx-2;y=hy-3;}
        else if(hz.kind==='ped'&&!hz.ghost){spr=hz.spr;x=hx-2;y=hy-9;}
        else if(hz.kind==='sheep'&&!hz.gull){spr=hz.peng?PENG_FR[0]:hz.horse?HORSE_FR[hz.col||0]:SHEEP_FR[0];const ox=(hz.horse||hz.peng)?1:3,oy=hz.horse?6:hz.peng?3:5;x=hx-ox;y=hy-oy;}
        else if(hz.kind==='thrower'&&hz.state!=='buried'){spr=SPR.thrower;x=hz.sx-6;y=hz.sy-14;}
        else if(hz.kind==='bumper'&&!hz.fork){spr=hz.spr;x=hx-1;y=hy-4;}
        if(!spr)return null;return {x,y,spr,base:hz.y+hz.h,fx:hz.x+hz.w/2,fy:hz.y+hz.h-1};};
      const movers=[];for(const cw of G.cows)movers.push({cow:cw,k:'cow'});for(const hz of G.hazards)if(['dog','cart','ped','sheep','thrower','bumper'].includes(hz.kind)&&!hz.gull)movers.push({hz,k:hz.horse?'horse':hz.peng?'penguin':hz.kind});
      for(const m of movers)m.st={behind:0,inprop:0,off:0,maxB:0,maxI:0,maxO:0,atB:null,atI:null,atO:null};
      const N=Math.min(3600,Math.round(Math.max(30,(ph-G.start.y)/50)*30));
      for(let f=0;f<N;f++){const t=f/N;P.y=Math.min(ph-20,G.start.y+t*(ph-G.start.y));P.x=pw/2+Math.sin(f/40)*60;P.inv=99;P.stun=0;update(1/30);
        if(f%3)continue;
        for(const m of movers){const bx=box(m),S=m.st;if(!bx){S.behind=S.inprop=S.off=0;continue;}const w=bx.spr.width,h=bx.spr.height;
          // off-map
          if(bx.x<-2||bx.x+w>pw+2){S.off++;if(S.off>S.maxO){S.maxO=S.off;S.atO=[Math.round(bx.fx),Math.round(bx.fy)];}}else S.off=0;
          let hidden=0,hidNm='',inside=0,inNm='';
          for(const q of near(bx.y,bx.y+h)){const qw=q.spr.width,qh=q.spr.height,pad=q.spr.padTop||0;
            if(q.cb&&bx.fx>q.cb[0]+1&&bx.fx<q.cb[0]+q.cb[2]-1&&bx.fy>q.cb[1]+1&&bx.fy<q.cb[1]+q.cb[3]-1){inside=1;inNm=q.nm;}
            if(!(q.base>bx.base))continue;            // prop drawn under the mover: fine
            const top=q.sy+pad;if(!(bx.base>top+3))continue; // mover's feet above the prop's top: properly behind it
            const x0=Math.max(bx.x,q.sx),x1=Math.min(bx.x+w,q.sx+qw),y0=Math.max(bx.y,q.sy),y1=Math.min(bx.y+h,q.sy+qh);if(x1<=x0||y1<=y0)continue;
            const qa=window.__alpha(q.spr),ma=window.__alpha(bx.spr);let n=0;
            for(let yy=y0;yy<y1;yy++)for(let xx=x0;xx<x1;xx++)if(qa[(yy-q.sy)*qw+(xx-q.sx)]&&ma[(yy-bx.y)*w+(xx-bx.x)])n++;
            if(n>=6&&n>hidden){hidden=n;hidNm=q.nm;}}
          if(hidden){S.behind++;if(S.behind>S.maxB){S.maxB=S.behind;S.atB=[Math.round(bx.fx),Math.round(bx.fy),hidNm,hidden];}}else S.behind=0;
          if(inside){S.inprop++;if(S.inprop>S.maxI){S.maxI=S.inprop;S.atI=[Math.round(bx.fx),Math.round(bx.fy),inNm];}}else S.inprop=0;}}
      const finds=[];for(const m of movers){const S=m.st;if(S.maxB>=5)finds.push({c:'behind-prop',k:m.k,at:S.atB,s:+(S.maxB/10).toFixed(1)});if(S.maxI>=5)finds.push({c:'in-prop',k:m.k,at:S.atI,s:+(S.maxI/10).toFixed(1)});if(S.maxO>=5)finds.push({c:'off-map',k:m.k,at:S.atO,s:+(S.maxO/10).toFixed(1)});}
      return JSON.stringify({id:'${id}',movers:movers.length,finds});})()`), [id, process.env.OPTS || '']);
    const o = JSON.parse(r); res.push(o); process.stdout.write(o.id + ':' + (o.finds ? o.finds.length : o.err) + ' ');
  }
  fs.writeFileSync(out, JSON.stringify(res, null, 0)); const by = {}; for (const o of res) for (const f of (o.finds || [])) by[f.c + '/' + f.k] = (by[f.c + '/' + f.k] || 0) + 1;
  console.log('\n', by, 'errors', errs.slice(0, 5)); await b.close();
})();
