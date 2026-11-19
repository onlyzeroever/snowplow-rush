import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# PLOW SIZES (Alex, Nov 19: "the monster truck, snow boat, and the one before it all feel a little TOO big, especially
# on some of the smaller maps"). Lab only, with a NEW/OLD switch on the lab screen so you can feel the difference:
#  1. Wing plows: the blade's wings fold in when they would run into a building, fence or prop, and swing back out in
#     the open. The blade never cuts through scenery again, and it reads as one machine on narrow streets.
#  2. (SMALL setting only) Blade size curve: blades up to 64px are unchanged; above that each extra pixel counts 45%. Icebreaker 124 -> 91,
#     Rotary 96 -> 78, Monster 92 -> 77, Loader 104 -> 82. Size upgrades still add width (softer).
#  3. Coins per snow go up by the same ratio, so earning per minute stays the same.
#  4. Collision boxes 1-4px tighter than the art for the long machines (bumps feel fair; the art may kiss a wall).
rep("function bladeCells(t){t=t||tool();return Math.min(80,Math.round(t.width*(1+mspec(t.id).sizePer*(chal()||t.ride?0:mLv(t.id).size))));}",
"""function bladeRaw(t){t=t||tool();return Math.min(80,Math.round(t.width*(1+mspec(t.id).sizePer*(chal()||t.ride?0:mLv(t.id).size))));}
const LABQS=(()=>{try{return new URLSearchParams(location.search);}catch(e){return new Map();}})(),LABCURVE=parseFloat(LABQS.get('labcurve'))||0.45,LABTRIM=LABQS.get('labtrim')!=='0',LABFOLD=LABQS.get('labfold')!=='0';
function sizeCurve(px){return px<=64?px:64+(px-64)*LABCURVE;}
function bladeCells(t){t=t||tool();let c=bladeRaw(t);if(labSizeSmall()&&!isKidTool(t.id))c=Math.round(sizeCurve(c*2)/2);
  if(state==='play'&&G&&G.def&&G.def.mode==='snowday')c=Math.round(c*1.7);return c;}
function sizeComp(){if(!labSizeSmall())return 1;const t=tool();if(isKidTool(t.id))return 1;const r=bladeRaw(t);return r/Math.max(1,Math.round(sizeCurve(r*2)/2));}
const CSPEC={loader:{hw:11,hh:20},icebreaker:{hw:12,hh:20},super:{hw:11,hh:20},snowcat:{hw:12,hh:19},rotary:{hw:12,hh:20},monster:{hw:11,hh:14},jet:{hw:10,hh:18},mech:{hw:13,hh:12},dragon:{hw:8,hh:17}};
// wing plow: how far each wing can reach before it would hit a wall / prop (in the blade's own left/right)
let RIGWING=null;
function wingUpdate(tid,dt){if(!labSizeNew()||!LABFOLD||isKidTool(tid)||tid==='ufo'||!VSPEC[tid]||!VSPEC[tid].bt){P.wing=null;return;}const s2=VSPEC[tid],half=Math.floor(bladeCells()),f=P.f,
    fv=[[0,-1],[1,0],[0,1],[-1,0]][f],pv=[[1,0],[0,1],[-1,0],[0,-1]][f],d0=s2.hh+1,d1=s2.hh+s2.bt+1,core=s2.hw;
  const lim=sg=>{for(let d=core;d<half;d+=2)for(let a=d0;a<=d1;a+=2){const x=Math.round(P.x+fv[0]*a+pv[0]*d*sg),y=Math.round(P.y+fv[1]*a+pv[1]*d*sg);if(x<0||y<0||x>=G.pw||y>=G.ph)return d;if(G.type[(y>>1)*G.cols+(x>>1)]===T_BLOCK)return d;}return half;};
  const tp=lim(1),tn=lim(-1);if(!P.wing||P.wing.f!==f)P.wing={p:tp,n:tn,f};const st=150*dt;P.wing.p=tp<P.wing.p?tp:Math.min(tp,P.wing.p+st);P.wing.n=tn<P.wing.n?tn:Math.min(tn,P.wing.n+st);P.wing.half=half;}
function foldRect(tid,x,y,f,bw){const r=bladeRect(tid,x,y,f,bw),w=P.wing;if(!w||isKidTool(tid)||w.f!==f)return r;
  if(f===0){r.x=x-w.n;r.w=w.n+w.p;}else if(f===2){r.x=x-w.p;r.w=w.n+w.p;}else if(f===1){r.y=y-w.n;r.h=w.n+w.p;}else{r.y=y-w.p;r.h=w.n+w.p;}return r;}
function rigBodyHalf(v,hh){if(v.bh!=null)return v.bh;let m=0;try{const d=v.c.getContext('2d').getImageData(0,0,v.c.width,v.c.height).data,y0=Math.max(0,Math.round(v.oy-hh+4));
  for(let y=y0;y<v.c.height;y++)for(let x=0;x<v.c.width;x++)if(d[(y*v.c.width+x)*4+3]>20)m=Math.max(m,Math.abs(x-v.ox)+1);}catch(e){m=40;}return v.bh=m;}
const LABSZ=(()=>{try{return new URLSearchParams(location.search).get('labsize');}catch(e){return null;}})();
// three settings: NEW = folding wings + fairer collision boxes (no change to how much you clear), SMALL = NEW + narrower
// blades (the size Alex asked about; clears 10-13 points less of a small job), OLD = as live
function labSizeMode(){if(!PROTO)return 'old';const m=LABSZ||save.labSize||'new';return m==='old'||m==='small'?m:'new';}
function labSizeNew(){return labSizeMode()!=='old';}function labSizeSmall(){return labSizeMode()==='small'||(PROTO&&LABQS.has('labcurve'));}""")
rep("function footprint(tid,x,y,f){if(isKidTool(tid))return{x:x-5,y:y-5,w:10,h:6};const s=VSPEC[tid];",
    "function footprint(tid,x,y,f){if(isKidTool(tid))return{x:x-5,y:y-5,w:10,h:6};const s=(labSizeNew()&&LABTRIM&&CSPEC[tid])||VSPEC[tid];")
rep("function valueMult(){return ","function valueMult(){return sizeComp()*")
rep("  const br=bladeRect(tid,P.x,P.y,P.f,bwPx);","  wingUpdate(tid,dt);const br=foldRect(tid,P.x,P.y,P.f,bwPx);")
rep("const pdraw=()=>{drawRig(b,tid,P.x,P.y,","const pdraw=()=>{RIGWING=P.wing&&!(P.spin>0)?P.wing:null;drawRig(b,tid,P.x,P.y,")
rep("g.save();g.translate(x,y);g.rotate(f*Math.PI/2);if(flash)g.globalAlpha=0.5;g.drawImage(v.c,-v.ox,-v.oy);const vs=VSPEC[tid];",
    "g.save();g.translate(x,y);g.rotate(f*Math.PI/2);if(flash)g.globalAlpha=0.5;const vs=VSPEC[tid],wg=RIGWING;RIGWING=null;"
    "if(wg&&wg.f===f&&(wg.n<wg.half-0.5||wg.p<wg.half-0.5)){const bh=Math.max(rigBodyHalf(v,vs.hh),vs.hw+1);g.save();g.beginPath();g.rect(-bh,-300,bh*2,600);g.rect(-wg.n,-300,wg.n+wg.p,300-vs.hh+3);g.clip();g.drawImage(v.c,-v.ox,-v.oy);g.restore();"
    "for(const [sg,len] of [[-1,wg.n],[1,wg.p]])if(len<wg.half-0.5){const ex=Math.round(sg*len),y0=-vs.hh-vs.bt;R(g,sg<0?ex-1:ex-2,y0-1,3,vs.bt+2,K);R(g,sg<0?ex:ex-1,y0,1,vs.bt,'#9aa4b8');}}"
    "else g.drawImage(v.c,-v.ox,-v.oy);")
open(f,'w',encoding='utf-8').write(s)
print('p153 lab plow sizes: wing plows, blade curve, coin compensation, fairer collision boxes (NEW/OLD switch)')
