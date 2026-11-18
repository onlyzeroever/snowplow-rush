// props whose foot sits inside a scenery building (or other big sprite); propose a sideways move
const { chromium } = require('/opt/npm-tools/node_modules/playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await (await b.newContext()).newPage();await p.goto('http://127.0.0.1:8765/index6.html?test=1');await p.waitForTimeout(800);
const r=await p.evaluate(()=>window.__EV(`(()=>{const out=[];const A=new Map();const alpha=c=>{if(A.has(c))return A.get(c);const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data,a=new Uint8Array(c.width*c.height);for(let k=0;k<a.length;k++)a[k]=d[k*4+3]>60?1:0;A.set(c,a);return a;};
 for(let li=0;li<LEVELS.length;li++){const L=LEVELS[li],D=L.data;if(!D||!D.props)continue;const g=buildLevel(li);
  const solidAt=(spr,sx,sy,x,y)=>{x=Math.round(x-sx);y=Math.round(y-sy);return x>=0&&y>=0&&x<spr.width&&y<spr.height&&alpha(spr)[y*spr.width+x];};
  D.props.forEach((pp,i)=>{const P2=PROPS[pp[0]];if(!P2)return;const a=pp[3]!=null?pp[3]:P2.arg,f=P2.foot(a);const o=g.obstacles.find(o=>o.x===pp[1]+f[0]&&o.y===pp[2]+f[1]);if(!o||o.spr.width>=50)return;
   const fx=o.sx+o.spr.width/2,fy=o.base-1;
   for(const s of g.scenery){if(s.base<=o.base+1)continue;let hit=false;for(let dx=-1;dx<=1;dx++)if(solidAt(s.spr,s.sx,s.sy,fx+dx,fy))hit=true;if(!hit)continue;
    const left=s.sx<=6,right=s.sx+s.spr.width>=174;let nx=null;if(left)nx=s.sx+s.spr.width+1;else if(right)nx=s.sx-o.spr.width-1;
    out.push({lv:L.id,i,p:pp,spr:[o.sx,o.sy,o.spr.width,o.spr.height],bld:[s.sx,s.sy,s.spr.width,s.spr.height],nx,dx:nx==null?null:nx-o.sx});break;}});}
 return JSON.stringify(out);})()`));
const o=JSON.parse(r);fs.writeFileSync('/tmp/va/inside.json',JSON.stringify(o));for(const x of o)console.log(x.lv,x.i,JSON.stringify(x.p),'spr',x.spr.join(','),'in',x.bld.join(','),'dx',x.dx);await b.close();})();
