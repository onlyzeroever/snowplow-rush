// propose minimal moves for data-driven props whose sprites clip each other
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const page=process.argv[2]||'index6.html', out=process.argv[3]||'/tmp/decl';fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await (await b.newContext()).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/'+page+'?test=1');await p.waitForTimeout(800);
 const res=await p.evaluate(()=>{const R=window.__SR,L=R.LEVELS;const res=[];const cache=new Map();
  const STRUCT=new Set(['wall','wallv','icewall','icewallv','stonewall','stonewallv','rail','railv','fence','hedge','hedgev','icecol','track','rocknet','snowfence','snowfencev','shop','shopv','house','smallhouse','chalet','container','containerv','cabin','barn','stand','tower','towerw','warehouse','temple','castle','church','museum','greenhouse','kiosk','bigtop','marquee','groomer','pylon','train','wagon','loco','boat','hull','tug','ferris','carousel']);
  const OKPAIR=(a,b,n)=>{const s=[a,b].sort().join('|');return s==='rail|railv'||s==='gatepole|stonewall'||(s==='icewall|lantpost'&&n<=10)||(s==='flag|snowfencev'&&n<=8)||a==='track'||b==='track';};
  const alpha=(c)=>{if(cache.has(c))return cache.get(c);const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;const a=new Uint8Array(c.width*c.height);for(let i=0;i<a.length;i++)a[i]=d[i*4+3]>40?1:0;cache.set(c,a);return a;};
  const ovl=(A,B,dil)=>{const x0=Math.max(A.sx,B.sx-dil),x1=Math.min(A.sx+A.spr.width,B.sx+B.spr.width+dil),y0=Math.max(A.sy,B.sy-dil),y1=Math.min(A.sy+A.spr.height,B.sy+B.spr.height+dil);if(x1<=x0||y1<=y0)return 0;
    const aa=alpha(A.spr),bb=alpha(B.spr);let n=0;for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){if(y-A.sy<=(A.spr.padTop||0))continue;if(!aa[(y-A.sy)*A.spr.width+(x-A.sx)])continue;
      // dilated B test
      let hitB=false;for(let dy=-dil;dy<=dil&&!hitB;dy++)for(let dx=-dil;dx<=dil&&!hitB;dx++){const bx=x+dx-B.sx,by=y+dy-B.sy;if(bx<0||by<0||bx>=B.spr.width||by>=B.spr.height)continue;if(by<=(B.spr.padTop||0)+1)continue;if(bb[by*B.spr.width+bx])hitB=true;}if(hitB)n++;}return n;};
  const fo=(a,b)=>a.x<b.x+b.w&&b.x<a.x+a.w&&a.y<b.y+b.h&&b.y<a.y+a.h;
  for(let li=0;li<L.length;li++){const D=L[li].data;if(!D||!D.props||!D.props.length)continue;let G;try{G=R.buildLevel(li);}catch(e){continue;}
   const tag=new Map();D.props.forEach((p,pi)=>{const P2=R.PROPS[p[0]];if(!P2)return;const a=p[3]!=null?p[3]:P2.arg,f=P2.foot(a);tag.set(p[1]+','+(p[2]+f[1])+','+(p[1]+f[0]),pi);});
   const items=G.obstacles.filter(o=>o.spr&&o.spr.width).map(o=>{const pi=tag.get(o.sx+','+o.y+','+o.x);return {o,spr:o.spr,sx:Math.round(o.sx),sy:Math.round(o.sy),fx:o.x-o.sx,fy:o.y-o.sy,fw:o.w,fh:o.h,pi,id:pi!=null?D.props[pi][0]:'?'};});
   for(const h of G.hazards)if(h.kind==='pull'&&h.spr)items.push({spr:h.spr,sx:Math.round(h.x)-1,sy:Math.round(h.y)-2,fx:1,fy:2,fw:22,fh:28,id:'PULL',pull:1});
   const W=G.pw,H=G.ph,st=G.start;const edits=[],manual=[];
   for(let pass=0;pass<3;pass++){let changed=false;
    for(let a=0;a<items.length;a++)for(let c=a+1;c<items.length;c++){const A=items[a],B=items[c];const n=ovl(A,B,0);if(n<8)continue;if(OKPAIR(A.id,B.id,n))continue;
     let mv=null;const sA=STRUCT.has(A.id)||A.pull,sB=STRUCT.has(B.id)||B.pull;
     if(sA&&!sB)mv=B;else if(sB&&!sA)mv=A;else if(!sA&&!sB)mv=(A.spr.width*A.spr.height<=B.spr.width*B.spr.height)?A:B;
     if(!mv||mv.pi==null){if(!manual.some(m=>m.a===A.id+'@'+A.sx+','+A.sy&&m.b===B.id+'@'+B.sx+','+B.sy))manual.push({a:A.id+'@'+A.sx+','+A.sy,b:B.id+'@'+B.sx+','+B.sy,n});continue;}
     const cands=[];for(let dy=-28;dy<=28;dy++)for(let dx=-24;dx<=24;dx++){if(!dx&&!dy)continue;const cx=mv.sx+mv.fx+mv.fw/2;const toward=(Math.abs(cx+dx-W/2)<Math.abs(cx-W/2))?Math.abs(dx)*0.6:0;cands.push([Math.abs(dx)+Math.abs(dy)*1.1+toward,dx,dy]);}
     cands.sort((p,q)=>p[0]-q[0]);let best=null;
     for(const [cost,dx,dy] of cands){const T={...mv,sx:mv.sx+dx,sy:mv.sy+dy};const inX=mv.sx>=0&&mv.sx+mv.spr.width<=W;if(inX&&(T.sx<0||T.sx+T.spr.width>W))continue;if(T.sy<0||T.sy+T.spr.height>H)continue;
       const F={x:T.sx+T.fx,y:T.sy+T.fy,w:T.fw,h:T.fh};if(st&&F.x<st.x+14&&st.x-14<F.x+F.w&&F.y<st.y+18&&st.y-18<F.y+F.h)continue;
       let bad=false;for(const O of items){if(O===mv)continue;const OF={x:O.sx+O.fx,y:O.sy+O.fy,w:O.fw,h:O.fh};if(fo({x:F.x-2,y:F.y-2,w:F.w+4,h:F.h+4},OF)){bad=true;break;}if(ovl(T,O,1)>0){bad=true;break;}}
       if(!bad){best=[dx,dy];break;}}
     if(best){const from=[D.props[mv.pi][1],D.props[mv.pi][2]];mv.sx+=best[0];mv.sy+=best[1];edits.push({pi:mv.pi,id:mv.id,from,to:[from[0]+best[0],from[1]+best[1]],why:(mv===A?B:A).id});changed=true;}
     else manual.push({a:A.id+'@'+A.sx+','+A.sy,b:B.id+'@'+B.sx+','+B.sy,n,nofit:mv.id});}
    if(!changed)break;}
   if(edits.length||manual.length){// composites of each edit: before & after
    const shots=[];for(const e of edits){const it=items.find(t=>t.pi===e.pi);const dx=e.to[0]-e.from[0],dy=e.to[1]-e.from[1];
      const ux=Math.max(0,Math.min(it.sx,it.sx-dx)-26),uy=Math.min(it.sy,it.sy-dy)-26,ux1=Math.min(W,Math.max(it.sx,it.sx-dx)+it.spr.width+26),uy1=Math.max(it.sy,it.sy-dy)+it.spr.height+26;
      const draw=(moved)=>{const cv=document.createElement('canvas');cv.width=ux1-ux;cv.height=uy1-uy;const x=cv.getContext('2d');x.fillStyle='#e9f0f9';x.fillRect(0,0,cv.width,cv.height);
        const list=items.map(t=>({t,sx:t===it&&!moved?t.sx-dx:t.sx,sy:t===it&&!moved?t.sy-dy:t.sy})).filter(q=>q.sx<ux1&&q.sx+q.t.spr.width>ux&&q.sy<uy1&&q.sy+q.t.spr.height>uy).sort((p,q)=>(p.sy+p.t.fy+p.t.fh)-(q.sy+q.t.fy+q.t.fh));
        for(const q of list)x.drawImage(q.t.spr,q.sx-ux,q.sy-uy);return cv.toDataURL();};
      shots.push({e,b:draw(false),a:draw(true)});}
    res.push({lv:L[li].id,edits,manual,shots});}}
  return res;});
 if(errs.length)console.log('ERR',errs.slice(0,3));
 fs.writeFileSync(out+'/edits.json',JSON.stringify(res.map(r=>({lv:r.lv,edits:r.edits,manual:r.manual})),null,1));
 let k=0;for(const r of res){console.log(r.lv,'edits',r.edits.length,'manual',JSON.stringify(r.manual));for(const e of r.edits)console.log('   ',e.id,'#'+e.pi,e.from.join(','),'->',e.to.join(','),'(was clipping',e.why+')');}
 const flat=[];for(const r of res)for(const s of r.shots)flat.push({lv:r.lv,...s});
 const per=12;for(let pg=0;pg*per<flat.length;pg++){const chunk=flat.slice(pg*per,pg*per+per);
  const url=await p.evaluate(async(chunk)=>{const load=u=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=u;});const S=3,CW=600,CH=300,cols=3;const c=document.createElement('canvas');c.width=cols*CW;c.height=Math.ceil(chunk.length/cols)*CH;const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);
   for(let k=0;k<chunk.length;k++){const cx=(k%cols)*CW,cy=Math.floor(k/cols)*CH;const A=await load(chunk[k].b),B=await load(chunk[k].a);const sc=Math.max(1,Math.min(S,Math.floor(Math.min((CW/2-14)/A.width,(CH-30)/A.height))));x.drawImage(A,cx+5,cy+22,A.width*sc,A.height*sc);x.drawImage(B,cx+CW/2+5,cy+22,B.width*sc,B.height*sc);
    x.fillStyle='#13306b';x.font='bold 12px sans-serif';x.fillText(chunk[k].lv+': '+chunk[k].e.id+' '+chunk[k].e.from+' -> '+chunk[k].e.to+'  (before | after)',cx+5,cy+14);x.strokeStyle='#c6d9f3';x.strokeRect(cx+.5,cy+.5,CW-1,CH-1);}
   return c.toDataURL();},chunk);
  fs.writeFileSync(`${out}/decl_${pg}.png`,Buffer.from(url.split(',')[1],'base64'));}
 await b.close();})();
