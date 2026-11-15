import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# SNOWY WORLD + SIGNS THAT FIT
#  - every obstacle and piece of scenery gets frosted: snow sitting along its top edges, lumps breaking the outline
#  - shopfronts: a lumpy snow roof, icicles off the eaves, snow on window heads and sills, on the sign and awning,
#    drifts against the walls; big buildings get fully snowed roofs; office towers a snowy roof and ledges
#  - sign text never clips: it condenses, then splits onto two lines, before it would overflow
# ---------------------------------------------------------------------------------------------
KIT=r"""
const SNW=[0xf4,0xf8,0xff],SNB=[0xc6,0xd9,0xf3],SNK=[0x1b,0x1f,0x3b];
const FROSTC=new WeakMap();
function frostSprite(src){const w=src.width,h0=src.height;if(w<4||h0<4||src.noFrost)return src;const P3=4,h=h0+P3,c=mk(w,h),g=c.getContext('2d');g.drawImage(src,0,P3);const im=g.getImageData(0,0,w,h),d=im.data;
  const A=(x,y)=>x>=0&&y>=0&&x<w&&y<h&&d[(y*w+x)*4+3]>100,E=new Uint8Array(w*h),ed=[];
  for(let y=P3;y<h;y++)for(let x=0;x<w;x++)if(A(x,y)&&!A(x,y-1)){E[y*w+x]=1;ed.push(x,y);}
  const e=(x,y)=>x>=0&&y>=0&&x<w&&y<h&&E[y*w+x]===1,set=(x,y,c3)=>{if(x<0||y<0||x>=w||y>=h)return;const o=(y*w+x)*4;d[o]=c3[0];d[o+1]=c3[1];d[o+2]=c3[2];d[o+3]=255;};
  const caps=[];for(let i=0;i<ed.length;i+=2){const x=ed[i],y=ed[i+1];if(!(e(x-1,y)||e(x+1,y)))continue;caps.push(x,y);}
  const M=new Int8Array(w*h);
  for(let i=0;i<caps.length;i+=2){const x=caps[i],y=caps[i+1];const run=(e(x-1,y)?1:0)+(e(x+1,y)?1:0);const base=w>=12?2:1;
    let m=base+((Math.sin((x+w*0.37+y)*0.6)+((hash(x+w,y)%3)*0.35))>0.75?1:0);if(run<2)m=Math.max(1,m-1);m=Math.min(m,y-1);M[y*w+x]=m;
    set(x,y,SNB);for(let k=1;k<=m;k++)set(x,y-k,SNW);set(x,y-m-1,SNK);}
  // round the ends of each cap
  for(let i=0;i<caps.length;i+=2){const x=caps[i],y=caps[i+1],m=M[y*w+x];for(const dx of [-1,1]){if(!e(x+dx,y)){for(let k=1;k<=m;k++)if(!A(x+dx,y-k))set(x+dx,y-k,SNK);}}}
  g.putImageData(im,0,0);c.padTop=P3;return c;}
function frostOf(c){if(!c||!c.getContext)return c;let f=FROSTC.get(c);if(!f){f=frostSprite(c);FROSTC.set(c,f);}return f;}
// ---- sign text that fits: normal, condensed, or two lines
function fitLayout(s,maxW){s=String(s);if(textW(s)<=maxW)return {lines:[s],cond:false};const cw=t=>{let w=0;for(const ch of t){const r=FONT[ch]||FONT[' '];w+=r[0].length;}return w;};
  if(cw(s)<=maxW)return {lines:[s],cond:true};let a,b2;const sp=s.lastIndexOf(' ',Math.ceil(s.length/2)+1);if(sp>0){a=s.slice(0,sp);b2=s.slice(sp+1);}else{const m=Math.ceil(s.length/2);a=s.slice(0,m);b2=s.slice(m);}
  return {lines:[a,b2],cond:textW(a)>maxW||textW(b2)>maxW};}
function condText(g,s,cx,y,col,ol){const cw=t=>{let w=0;for(const ch of t){const r=FONT[ch]||FONT[' '];w+=r[0].length;}return w;};let x=Math.round(cx-cw(s)/2);const xs=[];for(const ch of s){xs.push(x);x+=(FONT[ch]||FONT[' '])[0].length;}
  if(ol){let i=0;for(const ch of s){const c=glyph(ch,ol,ol);g.drawImage(c,xs[i]-1,y-1);i++;}}let i=0;for(const ch of s){const c=glyph(ch,col,null);g.drawImage(c,xs[i]-1,y-1);i++;}}
function fitText(g,s,cx,y,maxW,col,ol,L){L=L||fitLayout(s,maxW);const lh=L.lines.length>1?6:0;L.lines.forEach((t,k)=>{const yy=y+k*lh-(L.lines.length>1?3:0);if(L.cond||textW(t)>maxW)condText(g,t,cx,yy,col,ol);else text(g,t,cx,yy,col,{align:'center',outline:ol});});}
// ---- snow pieces for buildings
function snowCap(g,x0,y0,w,base,seed){for(let x=x0;x<x0+w;x++){const lump=(hash(seed+x,7)%4===0?1:0)+((Math.sin((x+seed)*0.55)>0.6)?1:0),t=y0+2-lump;R(g,x,t,1,1,K);R(g,x,t+1,1,base+lump,PAL.W);R(g,x,t+1+base+lump,1,1,'#c6d9f3');}}
function icicles(g,x0,y,w,seed,max){for(let x=x0+2;x<x0+w-2;x+=3+hash(seed,x)%4){const n=1+hash(x,seed)%(max||4);R(g,x,y,1,n,'#bfe6ff');R(g,x,y,1,1,PAL.W);}}
function ledge(g,x,y,w){R(g,x,y,w,1,PAL.W);R(g,x+1,y-1,w-2,1,PAL.W);R(g,x,y+1,w,1,'#c6d9f3');}
function drift(g,x,y,w,hh){g.fillStyle=K;for(let i=0;i<hh;i++){const e=Math.round(w*Math.sqrt(Math.max(0,1-(i/hh)**2)));g.fillRect(x+w-e-1,y-i,e*2+2,1);}g.fillStyle=PAL.W;for(let i=0;i<hh-1;i++){const e=Math.round((w-1)*Math.sqrt(Math.max(0,1-(i/(hh-1))**2)));g.fillRect(x+w-e,y-i,e*2,1);}}
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){", KIT+"\nfunction buildFromData(g,D,setT,ob,setCircle,paintText){")
# shopfronts, rebuilt with snow and fitted signs
old_b=s[s.index("function buildingSprite(w,h,wall,dark,sign,signCol,seed){"):]
old_b=old_b[:old_b.index("return c;}")+len("return c;}")]
new_b=r"""function buildingSprite(w,h,wall,dark,sign,signCol,seed){
  const c=mk(w,h),g=c.getContext('2d');R(g,0,2,w,h-2,K);R(g,1,2,w-2,h-2,wall);
  for(let y=6;y<h;y+=3)for(let x=1+((y/3)%2)*2;x<w-1;x+=5)R(g,x,y,2,1,dark);
  snowCap(g,0,0,w,4,seed);icicles(g,1,8,w-2,seed,3);
  const L=fitLayout(sign,w-8),two=L.lines.length>1,sy=h-27-(two?4:0),sh=two?14:10;
  for(let y=12;y<sy-10;y+=14){for(const wx of [3,w-11]){const lit=hash(seed+wx,y)%3!==0;R(g,wx,y,8,9,K);R(g,wx+1,y+1,6,7,lit?'#ffd77a':'#2b3150');R(g,wx+3,y+1,1,7,K);R(g,wx+1,y,6,1,PAL.W);ledge(g,wx-1,y+8,10);}}
  R(g,1,sy,w-2,sh,K);R(g,2,sy+1,w-4,sh-2,signCol);ledge(g,1,sy-1,w-2);fitText(g,sign,Math.floor(w/2),sy+(two?5:3),w-8,'#ffffff',K,L);
  const ay=h-16;for(let x=1;x<w-1;x+=4){R(g,x,ay,2,4,'#e03a4e');R(g,x+2,ay,2,4,'#ffffff');}R(g,1,ay+4,w-2,1,K);R(g,1,ay-1,w-2,2,PAL.W);icicles(g,1,ay+5,w-2,seed+3,2);
  R(g,2,h-11,Math.floor(w/2)-2,10,K);R(g,3,h-10,Math.floor(w/2)-4,9,'#ffd77a');R(g,Math.floor(w/2)+2,h-11,w-Math.floor(w/2)-4,11,K);R(g,Math.floor(w/2)+3,h-10,w-Math.floor(w/2)-6,10,'#6b3f22');
  R(g,3,h-11,Math.floor(w/2)-4,1,PAL.W);drift(g,0,h-1,5,4);drift(g,w-11,h-1,5,4);
  return c;}"""
s=s.replace(old_b,new_b)
# big buildings: the whole roof under snow, icicles along the eaves
rep("function bigBuilding(w,h,wall,roof,sign,signCol){const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,roof);R(g,1,1,w-2,4,'#f4f8ff');for(let x=4;x<w-4;x+=10)R(g,x,6,1,h*0.45,'#00000022');",
    "function bigBuilding(w,h,wall,roof,sign,signCol){const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,roof);const ry=Math.floor(h*0.6);R(g,1,1,w-2,ry-3,'#f4f8ff');for(let x=3;x<w-3;x+=9)R(g,x,4,1,ry-8,'#dfe9f8');R(g,1,ry-3,w-2,2,'#c6d9f3');R(g,w-22,3,8,8,K);R(g,w-21,4,6,7,roof);R(g,w-21,3,6,2,'#f4f8ff');for(let x=4;x<w-4;x+=10)R(g,x,6,1,0,'#00000022');icicles(g,1,ry,w-2,w+h,3);")
rep("for(let x=6;x<w-8;x+=12){R(g,x,Math.floor(h*0.68),6,5,K);R(g,x+1,Math.floor(h*0.68)+1,4,3,'#ffef7a');}",
    "for(let x=6;x<w-8;x+=12){R(g,x,Math.floor(h*0.68),6,5,K);R(g,x+1,Math.floor(h*0.68)+1,4,3,'#ffef7a');ledge(g,x-1,Math.floor(h*0.68)+5,8);}drift(g,0,h-1,6,4);drift(g,w-13,h-1,6,4);")
# office towers: snowy roof with a plant room, icicles, snow on every few ledges
rep("R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,pal[0]);R(g,1,1,2,h-2,pal[1]);R(g,w-3,1,2,h-2,pal[1]);R(g,0,0,w,4,PAL.W);R(g,2,4,w-4,1,'#c6d9f3');",
    "R(g,0,2,w,h-2,K);R(g,1,3,w-2,h-4,pal[0]);R(g,1,3,2,h-4,pal[1]);R(g,w-3,3,2,h-4,pal[1]);snowCap(g,0,0,w,4,w*3+a);icicles(g,1,8,w-2,w+a,3);")
rep("for(let y=8;y<h-14;y+=6)for(let x=5;x<w-6;x+=5){const lit=((x*7+y*13+a*5)%11)<4;R(g,x,y,3,4,lit?'#ffe9a8':'#2a3450');}",
    "for(let y=11;y<h-14;y+=6)for(let x=5;x<w-6;x+=5){const lit=((x*7+y*13+a*5)%11)<4;R(g,x,y,3,4,lit?'#ffe9a8':'#2a3450');}for(let y=29;y<h-16;y+=18)ledge(g,2,y,w-4);drift(g,0,h-1,6,4);drift(g,w-13,h-1,6,4);")
# frost every obstacle and every piece of scenery as it is placed
rep("const ob=(sprC,sx,sy,fx,fy,fw,fh)=>{const o={spr:sprC,sx,sy,x:sx+fx,y:sy+fy,w:fw,h:fh};",
    "const ob=(sprC,sx,sy,fx,fy,fw,fh)=>{const fz=frostOf(sprC),o={spr:fz,sx,sy:sy-(fz.padTop||0),x:sx+fx,y:sy+fy,w:fw,h:fh};")
rep("g.scenery.push({spr:sp,sx:p[1],sy:p[2],base:p[2]+f2[1]+f2[3]});","{const fz=frostOf(sp);g.scenery.push({spr:fz,sx:p[1],sy:p[2]-(fz.padTop||0),base:p[2]+f2[1]+f2[3]});}")
rep("const sp=wildSpr(kind,rn);if(!sp)continue;","const sp=frostOf(wildSpr(kind,rn));if(!sp)continue;")
open(f,'w',encoding='utf-8').write(s)
s=open(f,encoding='utf-8').read()
rep("window.__SR={drawToolIconTo,","window.__SR={frostOf,drawToolIconTo,")
open(f,'w',encoding='utf-8').write(s)
