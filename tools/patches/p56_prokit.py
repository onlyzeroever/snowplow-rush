import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# PRO KIT: the tools that let a job look designed rather than generated.
#  - 14 new ground finishes to uncover (cobbles, brick paving, station tiles, sandstone slabs, painted courts,
#    gravel, groomed piste corduroy, mountain stone, mosaic, boardwalk deck, sand...)
#  - decals painted into the ground: manholes, drains, road arrows, box junctions, zebras, tram rails, tree grates,
#    compass-rose mosaics, cracks, parking bays, hatching, a city crest...
#  - wild areas: forest/rock/ice/park masses that block and fill themselves with scenery, with winding corridors
#    carved through them (pistes, trails, lanes). Grid-tested collision, so hundreds of trees cost nothing.
#  - scenery: decorative sprites that block by grid (not in the obstacle list), and an overhead layer
#    (gate arches, footbridges, banners, fairy lights, gantries, overhanging boughs) that fades when you drive under.
#  - new street furniture: bare street trees, traffic lights, bike racks, newsstands, roadworks, vans, shelters,
#    signposts, sculptures, billboards, lantern posts, gate pillars, wheelie bins, meters, planters, skips, clocks.
# ---------------------------------------------------------------------------------------------
KIT=r"""
const T_COBB=10,T_PAVE=11,T_TILE=12,T_SLAB=13,T_BLUE=14,T_GRN=15,T_GRAV=16,T_PISTE=17,T_STONE=18,T_ORNG=19,T_PURP=20,T_MOSA=21,T_DECK=22,T_SAND=23;
Object.assign(GROUND_T,{cobble:T_COBB,pave:T_PAVE,tile:T_TILE,slab:T_SLAB,blue:T_BLUE,green:T_GRN,gravel:T_GRAV,piste:T_PISTE,stone:T_STONE,orange:T_ORNG,purple:T_PURP,mosaic:T_MOSA,deck:T_DECK,sand:T_SAND});
function groundCol2(t,x,y,n){switch(t){
  case T_COBB:{const row=y>>2,sx=x+(row%2)*3,si=(sx/6)|0;if((y&3)===3||sx%6===5)return [0x5c,0x5a,0x6a];const B=[[0x9c,0x96,0xa2],[0x8c,0x88,0x96],[0xa8,0x9e,0xa2],[0x94,0x8c,0x8c]][hash(si,row)&3];return (y&3)===0?[B[0]+16,B[1]+16,B[2]+16]:B;}
  case T_PAVE:{const row=y>>2,sx=x+(row%2)*4;if((y&3)===3||(sx&7)===7)return [0xc4,0xa8,0x96];return [[0xb0,0x52,0x46],[0xa2,0x4a,0x40],[0xbc,0x62,0x52]][hash(sx>>3,row)%3];}
  case T_TILE:{if((x&7)===7||(y&7)===7)return [0x86,0x8c,0x9e];return ((x>>3)+(y>>3))&1?[0xd8,0xdc,0xe4]:[0xa4,0xac,0xbe];}
  case T_SLAB:{const row=(y/12)|0,sx=x+(row%2)*8;if(y%12===11||(sx&15)===15)return [0x9a,0x8a,0x6c];const B=[[0xd8,0xc8,0xa4],[0xcc,0xba,0x96],[0xe2,0xd4,0xb2]][hash(sx>>4,row)%3];return n<2?[B[0]-12,B[1]-12,B[2]-12]:B;}
  case T_BLUE:return n<3?[0x37,0x7a,0xc4]:[0x3f,0x86,0xd6];
  case T_GRN:return n<3?[0x34,0x8c,0x52]:[0x3a,0x9a,0x5a];
  case T_GRAV:return n<4?[0x9a,0x92,0x84]:n<8?[0xb4,0xac,0x9c]:n<11?[0x84,0x7c,0x70]:[0xc4,0xbc,0xac];
  case T_PISTE:return x%3===0?[0xa6,0xbc,0xdc]:n<3?[0xc0,0xd2,0xea]:[0xcc,0xdc,0xf0];
  case T_STONE:{if(hash(x>>3,y>>3)%7===0&&(x+y)%5===0)return [0x48,0x4c,0x5e];return n<3?[0x5a,0x5e,0x72]:n<6?[0x76,0x7a,0x8e]:[0x68,0x6c,0x80];}
  case T_ORNG:return n<3?[0xc8,0x5e,0x32]:[0xd8,0x6a,0x3a];
  case T_PURP:return n<3?[0x6e,0x48,0xaa]:[0x7a,0x52,0xb8];
  case T_MOSA:{if((x&3)===3||(y&3)===3)return [0x8a,0x90,0xa2];return [[0x3f,0x86,0xd6],[0x2f,0xb8,0xb0],[0xff,0xc7,0x27],[0xec,0xef,0xf4],[0xd8,0x36,0x4b],[0x9b,0x5f,0xd6]][hash(x>>2,y>>2)%6];}
  case T_DECK:{const row=(y/5)|0,k=x+row*17;if(y%5===4)return [0x4a,0x4e,0x5e];if(k%34===0)return [0x5a,0x5e,0x6c];return [[0x9a,0x9e,0xa8],[0x8a,0x8e,0x9a],[0xa6,0xaa,0xb2]][hash((k/34)|0,row)%3];}
  case T_SAND:return n<3?[0xcc,0xb6,0x7e]:[0xd8,0xc4,0x8a];}
  return [0x9a,0xa1,0xb5];}
// ---- tiny text into a sprite (signs, billboards, plaques)
function sprText(g,s,x,y,col,sc){sc=sc||1;g.fillStyle=col;for(const ch of s){const r=FONT[ch];if(!r){x+=3*sc;continue;}for(let yy=0;yy<5;yy++)for(let xx=0;xx<r[0].length;xx++)if(r[yy][xx]==='#')g.fillRect(x+xx*sc,y+yy*sc,sc,sc);x+=(r[0].length+1)*sc;}}
function sprTextW(s,sc){sc=sc||1;let w=0;for(const ch of s){const r=FONT[ch];w+=((r?r[0].length:2)+1)*sc;}return w-sc;}
function srng(seed){let a=(seed|0)+0x9e3779b9;return()=>{a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
// ---- DECALS: painted into the ground, revealed as you clear
const DECAL_IM=new Map();
function wornPaint(g,w,h,seed,every){const im=g.getImageData(0,0,w,h);for(let y=0;y<h;y++)for(let x=0;x<w;x++)if(hash(x+seed*7,y*3+seed)%(every||8)===0)im.data[(y*w+x)*4+3]=0;g.putImageData(im,0,0);}
const DWH='#e6eaf0',DYE='#efcb40';
const DECALS={
  manhole:()=>{const c=mk(11,11),g=c.getContext('2d');g.fillStyle='#2a2e40';pixCircle(g,5,5,5);g.fillStyle='#4a5064';pixCircle(g,5,5,4);for(let y=2;y<10;y+=2)R(g,2,y,7,1,'#383d50');R(g,3,1,5,1,'#5e6680');return c;},
  drain:()=>{const c=mk(10,5),g=c.getContext('2d');R(g,0,0,10,5,'#2a2e40');for(let x=1;x<9;x+=2)R(g,x,1,1,3,'#12151f');return c;},
  arrow:(a)=>{const c=mk(7,20),g=c.getContext('2d');for(let r=0;r<7;r++){const k=Math.min(3,r>>1);R(g,3-k,r,2*k+1,1,DWH);}R(g,2,7,3,13,DWH);wornPaint(g,7,20,a+3);if(a===1){const d=mk(7,20),x=d.getContext('2d');x.translate(0,20);x.scale(1,-1);x.drawImage(c,0,0);return d;}return c;},
  arrowt:(a)=>{const c=mk(12,20),g=c.getContext('2d');R(g,7,6,3,14,DWH);R(g,4,4,6,3,DWH);for(let i=0;i<5;i++)R(g,i,5-i,1,1+i*2,DWH);wornPaint(g,12,20,a+9);if(a===1){const d=mk(12,20),x=d.getContext('2d');x.translate(12,0);x.scale(-1,1);x.drawImage(c,0,0);return d;}return c;},
  boxj:(a,b)=>{const c=mk(a,b),g=c.getContext('2d');g.fillStyle=DYE;g.fillRect(0,0,a,2);g.fillRect(0,b-2,a,2);g.fillRect(0,0,2,b);g.fillRect(a-2,0,2,b);for(let y=0;y<b;y++)for(let x=0;x<a;x++)if((x+y)%14<2||(x-y+1400)%14<2)g.fillRect(x,y,1,1);wornPaint(g,a,b,a+b,7);return c;},
  zebra:(a,b)=>{const c=mk(a,b),g=c.getContext('2d');for(let x=2;x+4<=a;x+=8)R(g,x,0,4,b,DWH);wornPaint(g,a,b,a*3+b);return c;},
  zebrah:(a,b)=>{const c=mk(a,b),g=c.getContext('2d');for(let y=2;y+4<=b;y+=8)R(g,0,y,a,4,DWH);wornPaint(g,a,b,a+b*5);return c;},
  stop:(a)=>{const c=mk(a,3),g=c.getContext('2d');R(g,0,0,a,3,DWH);wornPaint(g,a,3,a);return c;},
  stopv:(a)=>{const c=mk(3,a),g=c.getContext('2d');R(g,0,0,3,a,DWH);wornPaint(g,3,a,a+1);return c;},
  dashv:(a)=>{const c=mk(2,a),g=c.getContext('2d');for(let y=0;y<a;y+=16)R(g,0,y,2,8,DWH);wornPaint(g,2,a,a+2);return c;},
  dashh:(a)=>{const c=mk(a,2),g=c.getContext('2d');for(let x=0;x<a;x+=16)R(g,x,0,8,2,DWH);wornPaint(g,a,2,a+3);return c;},
  dyl:(a)=>{const c=mk(4,a),g=c.getContext('2d');R(g,0,0,1,a,DYE);R(g,3,0,1,a,DYE);wornPaint(g,4,a,a+4,10);return c;},
  dylh:(a)=>{const c=mk(a,4),g=c.getContext('2d');R(g,0,0,a,1,DYE);R(g,0,3,a,1,DYE);wornPaint(g,a,4,a+5,10);return c;},
  edge:(a)=>{const c=mk(2,a),g=c.getContext('2d');R(g,0,0,2,a,DWH);wornPaint(g,2,a,a+6,10);return c;},
  edgeh:(a)=>{const c=mk(a,2),g=c.getContext('2d');R(g,0,0,a,2,DWH);wornPaint(g,a,2,a+7,10);return c;},
  kerb:(a)=>{const c=mk(2,a),g=c.getContext('2d');for(let y=0;y<a;y+=8){R(g,0,y,2,8,'#c8ceda');R(g,0,y+7,2,1,'#6a7088');}R(g,1,0,1,a,'#9aa2b6');return c;},
  kerbh:(a)=>{const c=mk(a,2),g=c.getContext('2d');for(let x=0;x<a;x+=8){R(g,x,0,8,2,'#c8ceda');R(g,x+7,0,1,2,'#6a7088');}R(g,0,1,a,1,'#9aa2b6');return c;},
  tactile:()=>{const c=mk(12,8),g=c.getContext('2d');R(g,0,0,12,8,'#e8b830');for(let y=1;y<8;y+=2)for(let x=1;x<12;x+=2)R(g,x,y,1,1,'#b88a18');return c;},
  grate:()=>{const c=mk(16,16),g=c.getContext('2d');R(g,0,0,16,16,'#2a2e40');R(g,1,1,14,14,'#3a3f52');for(let i=2;i<14;i+=2){R(g,i,1,1,4,'#22263a');R(g,i,11,1,4,'#22263a');R(g,1,i,4,1,'#22263a');R(g,11,i,4,1,'#22263a');}R(g,5,5,6,6,'#3a2a1e');R(g,6,6,4,4,'#4a3626');return c;},
  compass:(a)=>{const s=a*2+1,c=mk(s,s),g=c.getContext('2d');for(let y=0;y<s;y++)for(let x=0;x<s;x++){const dx=x-a,dy=y-a,r=Math.hypot(dx,dy);if(r>a)continue;const th=Math.atan2(dy,dx);let col=r>a-2?'#8a6a3c':r>a-4?'#e2d4b2':(hash(x>>1,y>>1)%3?'#d4c49e':'#cbb990');
      const m=a*0.92*Math.pow(Math.abs(Math.cos(2*th)),5),d2=a*0.6*Math.pow(Math.abs(Math.sin(2*th)),5);
      if(r<m)col=(Math.sin(2*th+0.0001)*Math.cos(2*th)>0)?'#c8524e':'#9a3a36';else if(r<d2)col=(Math.cos(2*th)*Math.sin(2*th)<0)?'#3f6fae':'#2a5088';if(r<3)col='#ffc727';if(r<1.2)col='#c98a12';g.fillStyle=col;g.fillRect(x,y,1,1);}return c;},
  crest:(a)=>{const s=a*2+1,c=mk(s,s),g=c.getContext('2d');g.fillStyle='#1f4a8a';pixCircle(g,a,a,a);g.fillStyle='#2f5fae';pixCircle(g,a,a,a-2);g.fillStyle='#e6eaf0';for(let k=0;k<6;k++){const an=k*Math.PI/3;for(let r=0;r<a-3;r++){const x=Math.round(a+Math.cos(an)*r),y=Math.round(a+Math.sin(an)*r);g.fillRect(x,y,1,1);if(r===((a-3)*0.6|0)){for(const sg of [-1,1]){const an2=an+sg*0.7;for(let q=1;q<4;q++)g.fillRect(Math.round(x+Math.cos(an2)*q),Math.round(y+Math.sin(an2)*q),1,1);}}}}g.fillStyle='#ffc727';pixCircle(g,a,a,2);return c;},
  rails:(a)=>{const c=mk(16,a),g=c.getContext('2d');for(const x of [1,13]){R(g,x-1,0,1,a,'#2e3244');R(g,x,0,1,a,'#c8d0dc');R(g,x+1,0,1,a,'#6a7088');}return c;},
  railsh:(a)=>{const c=mk(a,16),g=c.getContext('2d');for(const y of [1,13]){R(g,0,y-1,a,1,'#2e3244');R(g,0,y,a,1,'#c8d0dc');R(g,0,y+1,a,1,'#6a7088');}return c;},
  track:(a)=>{const c=mk(20,a),g=c.getContext('2d');for(let y=0;y<a;y+=6)R(g,1,y,18,3,'#6b4a2c');for(const x of [4,15]){R(g,x,0,1,a,'#c8d0dc');R(g,x+1,0,1,a,'#5a6078');}return c;},
  crack:(a,b)=>{const c=mk(a,a),g=c.getContext('2d'),rn=srng(b||a);g.fillStyle='#2a2e40';const walk=(x,y,an,n)=>{for(let i=0;i<n;i++){x+=Math.cos(an);y+=Math.sin(an);an+=(rn()-0.5)*0.9;g.fillRect(Math.round(x),Math.round(y),1,1);if(rn()<0.06&&n>6)walk(x,y,an+(rn()<0.5?1:-1),n*0.4|0);}};walk(a/2,a/2,rn()*6.28,a*0.55|0);walk(a/2,a/2,rn()*6.28,a*0.45|0);return c;},
  bay:(a,b)=>{const c=mk(a,b),g=c.getContext('2d');R(g,0,0,2,b,DWH);R(g,a-2,0,2,b,DWH);wornPaint(g,a,b,a*b);return c;},
  bayh:(a,b)=>{const c=mk(a,b),g=c.getContext('2d');R(g,0,0,a,2,DWH);R(g,0,b-2,a,2,DWH);wornPaint(g,a,b,a*b+1);return c;},
  hatch:(a,b)=>{const c=mk(a,b),g=c.getContext('2d');g.fillStyle=DWH;g.fillRect(0,0,a,2);g.fillRect(0,b-2,a,2);g.fillRect(0,0,2,b);g.fillRect(a-2,0,2,b);for(let y=0;y<b;y++)for(let x=0;x<a;x++)if((x+y)%10<2)g.fillRect(x,y,1,1);wornPaint(g,a,b,a+b*3,7);return c;},
  bike:()=>{const c=mk(15,9),g=c.getContext('2d');g.fillStyle=DWH;for(const cx of [3,11]){for(let k=0;k<12;k++){const an=k*Math.PI/6;g.fillRect(Math.round(cx+Math.cos(an)*3),Math.round(5+Math.sin(an)*3),1,1);}}R(g,3,5,5,1,DWH);R(g,7,1,1,5,DWH);R(g,7,2,4,1,DWH);R(g,10,2,1,3,DWH);R(g,6,0,3,1,DWH);return c;},
  oil:(a,b)=>{const s=a*2,c=mk(s,s),g=c.getContext('2d'),rn=srng(b||a);for(let k=0;k<4;k++){const x=a+(rn()-0.5)*a,y=a+(rn()-0.5)*a,r=a*0.3+rn()*a*0.4;for(let yy=-r;yy<=r;yy++)for(let xx=-r;xx<=r;xx++)if(xx*xx+yy*yy<=r*r&&((xx+yy)&1)===0&&x+xx>=0&&y+yy>=0)R(g,Math.round(x+xx),Math.round(y+yy),1,1,'#2e3244');}return c;},
  puddle:(a,b)=>{const c=mk(a*2+1,a+1),g=c.getContext('2d');g.fillStyle='#9fd4f4';for(let y=0;y<=a;y++){const hw=Math.round(a*Math.sqrt(Math.max(0,1-((y-a/2)/(a/2))**2)));g.fillRect(a-hw,y,hw*2,1);}g.fillStyle='#e8f6ff';R(g,a-a/2|0,2,3,1,'#e8f6ff');R(g,a+2,a/2|0,4,1,'#bfe6ff');return c;},
  starm:(a)=>{const s=a*2+1,c=mk(s,s),g=c.getContext('2d');for(let y=0;y<s;y++)for(let x=0;x<s;x++){const dx=x-a,dy=y-a,r=Math.hypot(dx,dy),th=Math.atan2(dy,dx)+Math.PI/2,st=a*(0.55+0.45*Math.pow(Math.abs(Math.cos(2.5*th)),2));if(r<=st){g.fillStyle=r>st-2?'#c8302e':(hash(x,y)%4?'#ffc727':'#ffe36a');g.fillRect(x,y,1,1);}}return c;},
  hop:()=>{const c=mk(22,52),g=c.getContext('2d');g.fillStyle=DWH;const box=(x,y)=>{g.fillRect(x,y,10,1);g.fillRect(x,y+9,10,1);g.fillRect(x,y,1,10);g.fillRect(x+9,y,1,10);};box(6,42);box(6,33);box(1,24);box(11,24);box(6,15);box(1,6);box(11,6);sprText(g,'1',10,45,DWH);sprText(g,'2',10,36,DWH);sprText(g,'5',10,18,DWH);wornPaint(g,22,52,5);return c;},
  heli:(a)=>{const s=a*2+1,c=mk(s,s),g=c.getContext('2d');g.fillStyle=DYE;pixCircle(g,a,a,a);g.fillStyle='rgba(0,0,0,0)';g.clearRect(0,0,0,0);const im=g.getImageData(0,0,s,s);for(let y=0;y<s;y++)for(let x=0;x<s;x++){const r=Math.hypot(x-a,y-a);if(r<a-2)im.data[(y*s+x)*4+3]=0;}g.putImageData(im,0,0);sprText(g,'H',a-5,a-7,DWH,3);return c;},
  lane:(a)=>{const c=mk(2,a),g=c.getContext('2d');for(let y=0;y<a;y+=12)R(g,0,y,2,6,DWH);wornPaint(g,2,a,a+8);return c;},
  piste:(a)=>{const c=mk(16,22),g=c.getContext('2d');const col=['#33b24a','#2f5fae','#e03a4e','#1b1f3b'][a|0];g.fillStyle=col;if((a|0)===3){for(let r=0;r<8;r++)g.fillRect(8-r,3+r,r*2+1,1),g.fillRect(8-r,18-r,r*2+1,1);}else pixCircle(g,8,11,7);return c;}};
function decalIm(k,a,b){const key=k+'|'+a+'|'+b;let m=DECAL_IM.get(key);if(m!==undefined)return m;const f=DECALS[k],cv=f?f(a,b):null;m=cv?{w:cv.width,h:cv.height,d:cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data}:null;DECAL_IM.set(key,m);return m;}
function paintDecals(g){for(const dc of g.decals){const m=decalIm(dc[0],dc[3],dc[4]);if(!m)continue;const x0=dc[1]|0,y0=dc[2]|0;
  for(let y=0;y<m.h;y++){const py=y0+y;if(py<0||py>=g.ph)continue;for(let x=0;x<m.w;x++){const px=x0+x;if(px<0||px>=g.pw)continue;const s4=(y*m.w+x)*4;if(m.d[s4+3]<128)continue;const o=(py*g.pw+px)*3;g.ground[o]=m.d[s4];g.ground[o+1]=m.d[s4+1];g.ground[o+2]=m.d[s4+2];}}}}
// ---- street furniture and set dressing
function bareTreeSprite(h,seed){const w=(Math.round(h*0.9)|1),c=mk(w,h),g=c.getContext('2d'),rn=srng(seed||h*13),cx=w>>1;
  const px=(x,y,col)=>{x=Math.round(x);y=Math.round(y);if(x>=0&&y>=0&&x<w&&y<h){g.fillStyle=col;g.fillRect(x,y,1,1);}};
  const seg=(x0,y0,x1,y1,th)=>{const n=Math.max(1,Math.ceil(Math.max(Math.abs(x1-x0),Math.abs(y1-y0))));for(let i=0;i<=n;i++){const x=x0+(x1-x0)*i/n,y=y0+(y1-y0)*i/n;px(x,y,'#4a3020');if(th>1)px(x+1,y,'#6a4a30');if(Math.abs(y1-y0)<Math.abs(x1-x0)*1.4)px(x,y-1,'#f4f8ff');}};
  const br=(x,y,an,len,d)=>{const x1=x+Math.sin(an)*len,y1=y-Math.cos(an)*len;seg(x,y,x1,y1,d>2?2:1);if(d<=0){px(x1,y1-1,'#f4f8ff');return;}const sp=0.35+rn()*0.3;br(x1,y1,an-sp,len*(0.62+rn()*0.12),d-1);br(x1,y1,an+sp,len*(0.62+rn()*0.12),d-1);if(rn()<0.4)br(x1,y1,an+(rn()-0.5)*0.3,len*0.5,d-2);};
  const tt=Math.round(h*0.42);seg(cx,h-1,cx,h-tt,2);br(cx,h-tt,-0.2+rn()*0.1,h*0.3,3);br(cx,h-tt,0.25+rn()*0.1,h*0.28,3);R(g,cx-1,h-2,4,2,'#3a2418');return c;}
const SCN_CACHE=new Map();function scnSpr(key,f){let s2=SCN_CACHE.get(key);if(!s2){s2=f();SCN_CACHE.set(key,s2);}return s2;}
function tlightSprite(){const c=mk(8,28),g=c.getContext('2d');R(g,3,10,2,18,K);R(g,3,11,1,16,'#55607a');R(g,1,0,6,13,K);R(g,2,1,4,11,'#2a2a36');R(g,3,2,2,2,'#e03a4e');R(g,3,5,2,2,'#7a5a1c');R(g,3,8,2,2,'#33b24a');R(g,1,0,6,1,PAL.W);R(g,2,26,4,2,K);return c;}
function bikeRackSprite(){const c=mk(26,14),g=c.getContext('2d');R(g,0,6,26,3,K);R(g,1,7,24,1,'#9aa6ba');const cols=['#e03a4e','#3f86d6','#33b24a','#ffc727'];for(let k=0;k<4;k++){const x=1+k*6;R(g,x,0,4,5,K);R(g,x+1,1,2,3,'#55607a');R(g,x,9,4,5,K);R(g,x+1,10,2,3,'#55607a');R(g,x+1,4,2,6,cols[k]);R(g,x,5,4,1,K);}return c;}
function newsSprite(){const c=mk(20,22),g=c.getContext('2d');R(g,0,6,20,16,K);R(g,1,7,18,14,'#2f8a5a');R(g,0,1,20,7,K);R(g,1,2,18,5,'#1f6a44');R(g,1,1,18,2,PAL.W);R(g,3,12,14,7,'#ffe9a8');for(let x=4;x<16;x+=3)R(g,x,13,2,5,['#e03a4e','#3f86d6','#f4f8ff','#ffc727'][(x/3|0)%4]);R(g,4,8,12,3,'#ffc727');sprText(g,'NEWS',4,8,'#1b1f3b',0.6);return c;}
function worksSprite(w){const c=mk(w,10),g=c.getContext('2d');R(g,1,5,2,5,K);R(g,w-3,5,2,5,K);R(g,0,1,w,6,K);for(let x=1;x<w-1;x+=6){R(g,x,2,3,4,'#e03a4e');R(g,x+3,2,Math.min(3,w-1-x-3),4,'#f4f8ff');}R(g,0,0,4,3,K);R(g,1,0,2,2,'#ffc727');R(g,w-4,0,4,3,K);R(g,w-3,0,2,2,'#ffc727');return c;}
function vanSprite(a){const c=mk(24,42),g=c.getContext('2d'),st=['#e03a4e','#3f86d6','#33b24a','#f07a1a','#9b5fd6'][a%5];R(g,1,0,22,42,K);R(g,2,1,20,40,'#e8ecf2');R(g,2,1,1,40,'#b8c0cc');R(g,21,1,1,40,'#b8c0cc');R(g,4,4,16,5,K);R(g,5,5,14,3,'#8fd3ff');R(g,3,12,18,26,PAL.W);R(g,3,12,18,1,'#c6d9f3');R(g,2,24,20,3,st);R(g,0,6,1,6,K);R(g,23,6,1,6,K);R(g,0,30,1,7,K);R(g,23,30,1,7,K);return c;}
function shelterSprite(){const c=mk(34,20),g=c.getContext('2d');R(g,0,0,34,9,K);R(g,1,1,32,7,'#3a3f52');R(g,1,0,32,3,PAL.W);R(g,0,9,34,9,K);R(g,1,10,32,7,'#9fd4f4');for(let x=8;x<32;x+=8)R(g,x,10,1,7,'#5a7a9a');R(g,25,10,8,7,'#ffc727');R(g,26,11,6,2,'#e03a4e');R(g,3,14,20,2,'#c98d4a');R(g,1,18,2,2,K);R(g,31,18,2,2,K);return c;}
function signpostSprite(a){const c=mk(16,26),g=c.getContext('2d');R(g,7,6,2,20,K);R(g,7,7,1,18,'#8a5a2c');R(g,0,1,13,5,K);R(g,1,2,11,3,'#2f8a5a');R(g,12,2,2,3,K);R(g,4,8,12,5,K);R(g,5,9,10,3,'#2f8a5a');R(g,3,9,2,3,K);R(g,0,1,13,1,PAL.W);return c;}
function sculptSprite(){const c=mk(22,28),g=c.getContext('2d');R(g,3,21,16,7,K);R(g,4,22,14,5,'#c6d0dc');R(g,4,22,14,1,PAL.W);g.fillStyle=K;for(let k=0;k<64;k++){const an=k/64*Math.PI*2,x=11+Math.cos(an)*8,y=11+Math.sin(an)*9*Math.cos(an*0.5);R(g,Math.round(x)-2,Math.round(y)-2,5,5,K);}for(let k=0;k<64;k++){const an=k/64*Math.PI*2,x=11+Math.cos(an)*8,y=11+Math.sin(an)*9*Math.cos(an*0.5);R(g,Math.round(x)-1,Math.round(y)-1,3,3,k<32?'#e03a4e':'#a82639');}R(g,9,17,4,5,K);R(g,10,17,2,5,'#a82639');return c;}
function billboardSprite(a){const c=mk(46,32),g=c.getContext('2d');R(g,8,18,3,14,K);R(g,35,18,3,14,K);R(g,0,0,46,21,K);const bg=['#2f5fae','#e03a4e','#2f8a5a','#9b5fd6','#f07a1a'][a%5];R(g,1,1,44,19,bg);R(g,1,0,44,2,PAL.W);
  const words=[['HOT','COCOA'],['SKI','NOW'],['VISIT','PARK'],['WINTER','FEST'],['GO','PLOW']][a%5];sprText(g,words[0],Math.round(23-sprTextW(words[0])/2),5,'#ffffff');sprText(g,words[1],Math.round(23-sprTextW(words[1])/2),12,'#ffd23f');return c;}
function lantPostSprite(){const c=mk(10,30),g=c.getContext('2d');R(g,3,4,3,26,K);R(g,4,5,1,24,'#c8302e');R(g,3,3,7,2,K);R(g,5,5,5,9,K);R(g,6,6,3,7,'#e03a4e');R(g,6,6,3,1,'#ffc727');R(g,6,12,3,1,'#ffc727');R(g,7,13,1,2,'#ffc727');R(g,2,28,5,2,K);return c;}
function gatePillarSprite(){const c=mk(12,40),g=c.getContext('2d');R(g,2,4,8,30,K);R(g,3,5,6,28,'#c8302e');R(g,3,5,2,28,'#e04a40');R(g,1,1,10,5,K);R(g,2,2,8,3,'#ffc727');R(g,0,32,12,8,K);R(g,1,33,10,6,'#c6c0b0');R(g,1,33,10,2,PAL.W);return c;}
function binsSprite(){const c=mk(18,14),g=c.getContext('2d');for(const [x,col,dk] of [[0,'#2f8a5a','#1f6a44'],[10,'#3f86d6','#2a5fa8']]){R(g,x,3,8,11,K);R(g,x+1,4,6,9,col);R(g,x+1,4,1,9,dk);R(g,x,0,8,4,K);R(g,x+1,1,6,2,dk);R(g,x+1,0,6,2,PAL.W);}return c;}
function meterSprite(){const c=mk(6,16),g=c.getContext('2d');R(g,2,6,2,10,K);R(g,0,0,6,7,K);R(g,1,1,4,5,'#8793a8');R(g,2,2,2,2,'#7ad3ff');R(g,1,0,4,1,PAL.W);return c;}
function planterLSprite(w){const c=mk(w,16),g=c.getContext('2d');R(g,0,6,w,10,K);R(g,1,7,w-2,8,'#8a6a4a');R(g,1,7,w-2,2,'#a8886a');for(let x=1;x+8<=w;x+=8){R(g,x+1,1,7,7,K);R(g,x+2,2,5,5,'#2f8a4a');R(g,x+3,3,2,2,'#3fa85a');R(g,x+2,1,5,2,PAL.W);}return c;}
function skipSprite(){const c=mk(26,16),g=c.getContext('2d');R(g,0,4,26,12,K);R(g,1,5,24,10,'#ffc727');R(g,1,5,24,2,'#c98a12');R(g,3,7,20,6,'#6a5a4a');for(let x=4;x<22;x+=4)R(g,x,7+(x%3),3,2,['#8793a8','#c98d4a','#9aa6ba'][x%3]);R(g,3,6,20,2,PAL.W);return c;}
function clockSprite(){const c=mk(12,34),g=c.getContext('2d');R(g,5,10,2,24,K);R(g,5,11,1,22,'#2f5f4a');g.fillStyle=K;pixCircle(g,6,5,5);g.fillStyle='#f4f8ff';pixCircle(g,6,5,4);R(g,6,2,1,4,K);R(g,6,5,3,1,K);R(g,3,32,6,2,K);return c;}
function parasolSprite(a){const c=mk(18,20),g=c.getContext('2d'),col=['#e03a4e','#3f86d6','#33b24a','#f07a1a'][a%4];R(g,8,8,2,10,K);g.fillStyle=K;pixCircle(g,9,6,8);for(let y=-7;y<=7;y++)for(let x=-7;x<=7;x++)if(x*x+y*y<=49)R(g,9+x,6+y,1,1,(Math.atan2(y,x)*4/Math.PI+8|0)%2?col:'#f4f8ff');R(g,8,5,3,3,K);R(g,3,16,12,3,K);R(g,4,16,10,2,'#c98d4a');return c;}
function iceBlockSprite(w,h){const c=mk(w,h),g=c.getContext('2d');R(g,0,2,w,h-2,K);R(g,1,3,w-2,h-4,'#9fd4f4');R(g,1,3,w-2,2,'#e8f6ff');R(g,2,0,w-4,3,K);R(g,3,1,w-6,2,PAL.W);R(g,2,h-3,w-4,1,'#6aa8d8');return c;}
// overhead pieces (drawn above everything, faded while you drive underneath)
function gateArchSprite(w){const c=mk(w,30),g=c.getContext('2d');R(g,0,4,w,8,K);for(let x=1;x<w-1;x+=3)R(g,x,5,2,6,(x/3|0)%2?'#2f8a6a':'#247a5a');R(g,1,4,w-2,2,PAL.W);R(g,0,2,4,4,K);R(g,w-4,2,4,4,K);R(g,1,1,2,3,'#2f8a6a');R(g,w-3,1,2,3,'#2f8a6a');R(g,4,12,w-8,5,K);R(g,5,13,w-10,3,'#c8302e');
  const pw2=Math.min(44,w-30),px2=(w-pw2)>>1;R(g,px2,15,pw2,12,K);R(g,px2+1,16,pw2-2,10,'#ffc727');R(g,px2+3,18,pw2-6,6,'#c8302e');R(g,px2+4,19,pw2-8,4,'#ffc727');R(g,8,24,w-16,4,K);R(g,9,25,w-18,2,'#c8302e');return c;}
function footBridgeSprite(w){const c=mk(w,24),g=c.getContext('2d');R(g,0,2,w,20,K);R(g,1,3,w-2,18,'#8793a8');R(g,1,3,w-2,4,PAL.W);R(g,1,7,w-2,1,'#c6d9f3');for(let x=2;x<w-2;x+=10)R(g,x,8,1,12,'#6a7896');R(g,0,0,w,3,K);R(g,0,21,w,3,K);for(let x=1;x<w;x+=4){R(g,x,0,1,3,'#55607a');R(g,x,21,1,3,'#55607a');}return c;}
function bannerOverSprite(w,a){const c=mk(w,22),g=c.getContext('2d');for(let x=0;x<w;x++){const y=Math.round(2+4*Math.sin(Math.PI*x/w));R(g,x,y,1,1,K);}const cols=[['#e03a4e','#ffc727'],['#2f5fae','#f4f8ff'],['#2f8a5a','#ffc727'],['#9b5fd6','#ffc727']][a%4];const bw=Math.min(40,w-20),bx=(w-bw)>>1;R(g,bx,6,bw,14,K);R(g,bx+1,7,bw-2,12,cols[0]);R(g,bx+1,7,bw-2,2,PAL.W);const s2=['WELCOME','WINTER','PARADE','FESTIVAL'][a%4];sprText(g,s2,Math.round(w/2-sprTextW(s2)/2),11,cols[1]);for(let x=bx+2;x<bx+bw-2;x+=4)R(g,x,19,2,2,cols[0]);return c;}
function lightsOverSprite(w,a){const c=mk(w,12),g=c.getContext('2d'),cols=['#ffd23f','#ff7a7a','#7ad3ff','#9cff7a','#ffb84a'];for(let x=0;x<w;x++){const y=Math.round(1+7*Math.sin(Math.PI*((x*2)%w)/w));R(g,x,y,1,1,'#2a2a36');if(x%6===3){R(g,x-1,y+1,3,3,cols[((x/6|0)+a)%5]);R(g,x,y+1,1,1,'#ffffff');}}return c;}
function boughSprite(a,seed){const s2=a*2+4,c=mk(s2,s2),g=c.getContext('2d'),rn=srng(seed||a);for(let k=0;k<7;k++){const x=4+rn()*(s2-8),y=4+rn()*(s2-8),r=a*0.35+rn()*a*0.3;g.fillStyle=K;pixCircle(g,x|0,y|0,(r+1)|0);}for(let k=0;k<7;k++){const x=4+rn()*(s2-8),y=4+rn()*(s2-8),r=a*0.3+rn()*a*0.3;g.fillStyle='#1f6a44';pixCircle(g,x|0,y|0,r|0);g.fillStyle='#2f8a5a';pixCircle(g,(x-1)|0,(y-1)|0,(r*0.6)|0);g.fillStyle=PAL.W;R(g,(x-r*0.5)|0,(y-r*0.7)|0,(r)|0,2,PAL.W);}return c;}
function gantryOverSprite(w,a){const c=mk(w,22),g=c.getContext('2d');R(g,0,8,w,4,K);R(g,0,9,w,2,'#8793a8');const bw=Math.min(52,(w-12)>>1);for(const bx of [6,w-6-bw]){R(g,bx,0,bw,18,K);R(g,bx+1,1,bw-2,16,'#2f7a4a');R(g,bx+1,0,bw-2,2,PAL.W);}const t1=['CITY','SKI','HARBOUR','NORTH','AIRPORT','STATION','FARMS','RESORT'][a%8],t2=['DOCKS','PASS','PARK','POLE','CENTRE','STADIUM','HARBOUR','SUMMIT'][a%8];sprText(g,t1,Math.round(6+bw/2-sprTextW(t1)/2),6,'#ffffff');sprText(g,t2,Math.round(w-6-bw/2-sprTextW(t2)/2),6,'#ffffff');R(g,Math.round(6+bw/2)-1,12,3,4,'#ffffff');R(g,Math.round(w-6-bw/2)-1,12,3,4,'#ffffff');return c;}
const OVERS={lant:a=>lanternOverSprite(a||180),rbridge:a=>redBridgeSprite(a||60),garch:a=>gateArchSprite(a||120),fbridge:a=>footBridgeSprite(a||180),banner:(a,b)=>bannerOverSprite(a||120,b||0),lights:(a,b)=>lightsOverSprite(a||120,b||0),bough:(a,b)=>boughSprite(a||14,b),gantry:(a,b)=>gantryOverSprite(a||180,b||0)};
SHOPS.push(['COFFEE','#7a4a2a','#55321d','#ffc727'],['CINEMA','#2a2a36','#1b1f3b','#ff4fa3'],['POST OFFICE','#d8364b','#a82639','#ffc727'],['LIBRARY','#c6b08a','#a08a64','#13306b'],['DINER','#e8eef7','#c6d0e0','#d8364b'],['RECORDS','#9b5fd6','#6b4fa8','#ffc727'],['GALLERY','#f4f8ff','#c6d9f3','#1b1f3b'],['TAILOR','#2f5fae','#244a87','#ffd23f'],['LAUNDRY','#7ad3ff','#3f86d6','#13306b'],['JEWELLER','#1b1f3b','#0b1838','#ffd23f'],['MARKET HALL','#e8c87a','#c98d4a','#7a1f33'],['TRAM DEPOT','#55607a','#3a3f52','#ffc727'],['CAR PARK','#8793a8','#6a7896','#3f86d6'],['OPERA','#c6b08a','#a08a64','#a82639'],['COURT','#e8e0cc','#d6cdb4','#13306b'],['FLORIST','#ffb6d0','#e07a8a','#2f8a5a'],['HERBALIST','#2f8a5a','#1f6a44','#ffc727'],['BAO BAR','#f4f0e0','#d6cdb4','#c8302e'],['MAHJONG','#1f6a44','#145146','#ffc727'],['LUCKY CAT','#ffc727','#e29a1c','#c8302e'],['HOT POT','#c8302e','#8a1f1f','#ffc727'],['KITES','#3f86d6','#2a5fa8','#ffc727']);
Object.assign(PROPS,{
  stree:{arg:26,min:16,max:40,make:a=>scnSpr('bt'+a,()=>bareTreeSprite(a,a*7)),foot:a=>[(Math.round(a*0.9)>>1)-2,a-4,5,4]},
  bare:{arg:30,min:14,max:50,make:a=>scnSpr('bt'+a,()=>bareTreeSprite(a,a*7)),foot:a=>[(Math.round(a*0.9)>>1)-3,a-5,7,5]},
  tlight:{make:()=>scnSpr('tl',tlightSprite),foot:()=>[2,24,4,4]},
  bikerack:{make:()=>scnSpr('br',bikeRackSprite),foot:()=>[0,3,26,9]},
  news:{make:()=>scnSpr('nw',newsSprite),foot:()=>[0,10,20,12]},
  works:{arg:40,min:16,max:120,make:a=>worksSprite(a),foot:a=>[0,4,a,6]},
  van:{arg:0,min:0,max:4,make:a=>vanSprite(a),foot:()=>[1,1,22,40]},
  shelter:{make:()=>scnSpr('sh',shelterSprite),foot:()=>[0,10,34,10]},
  signpost:{make:()=>scnSpr('sp',signpostSprite),foot:()=>[5,22,6,4]},
  sculpt:{make:()=>scnSpr('sc',sculptSprite),foot:()=>[3,18,16,10]},
  billboard:{arg:0,min:0,max:4,make:a=>billboardSprite(a),foot:()=>[6,26,34,6]},
  lantpost:{make:()=>scnSpr('lp',lantPostSprite),foot:()=>[2,26,5,4]},
  gpill:{make:()=>scnSpr('gp',gatePillarSprite),foot:()=>[0,32,12,8]},
  bins:{junk:true,make:()=>scnSpr('bn',binsSprite),foot:()=>[0,3,18,11]},
  meter:{junk:true,make:()=>scnSpr('mt',meterSprite),foot:()=>[0,11,6,5]},
  planterl:{arg:40,min:16,max:160,make:a=>planterLSprite(a),foot:a=>[0,6,a,10]},
  skip:{make:()=>scnSpr('sk',skipSprite),foot:()=>[0,4,26,12]},
  clock:{make:()=>scnSpr('ck',clockSprite),foot:()=>[3,30,6,4]},
  parasol:{arg:0,min:0,max:3,make:a=>parasolSprite(a),foot:()=>[3,14,12,6]},
  pagoda:{make:()=>scnSpr('pg',pagodaSprite),foot:()=>[6,64,52,18]},
  temple:{make:()=>scnSpr('tp',templeSprite),foot:()=>[0,26,124,48]},
  lion:{arg:0,min:0,max:1,make:a=>scnSpr('ln'+a,()=>lionSprite(a)),foot:()=>[0,11,14,7]},
  stonelamp:{make:()=>scnSpr('sl',stoneLampSprite),foot:()=>[1,13,8,5]},
  urn:{make:()=>scnSpr('ur',urnSprite),foot:()=>[1,8,14,10]},
  pillar:{make:()=>scnSpr('pl',pillarSprite),foot:()=>[0,4,10,12]},
  iceblock:{arg:14,min:8,max:30,make:a=>iceBlockSprite(a,Math.round(a*0.75)),foot:a=>[0,2,a,Math.round(a*0.75)-2]}});

// ---- Chinatown set pieces
function pagodaSprite(){const c=mk(64,82),g=c.getContext('2d');R(g,4,70,56,12,K);R(g,5,71,54,10,'#c6c0b0');R(g,5,71,54,2,PAL.W);R(g,5,76,54,1,'#9a9488');
  for(let i=0;i<3;i++){const rw=64-i*16,x0=(64-rw)/2,ry=52-i*19;R(g,x0+8,ry+6,rw-16,14,K);R(g,x0+9,ry+7,rw-18,12,'#c8302e');R(g,x0+9,ry+7,2,12,'#e04a40');R(g,29,ry+10,6,8,K);R(g,30,ry+11,4,7,'#ffc727');
    R(g,x0,ry,rw,8,K);R(g,x0+1,ry+1,rw-2,6,'#2f8a6a');for(let x=x0+2;x<x0+rw-2;x+=3)R(g,x,ry+3,1,4,'#247a5a');R(g,x0+1,ry,rw-2,2,PAL.W);R(g,x0-2,ry-3,4,4,K);R(g,x0-1,ry-2,2,2,'#2f8a6a');R(g,x0+rw-2,ry-3,4,4,K);R(g,x0+rw-1,ry-2,2,2,'#2f8a6a');}
  R(g,30,0,4,16,K);R(g,31,1,2,14,'#ffc727');R(g,29,4,6,2,K);return c;}
function templeSprite(){const c=mk(124,74),g=c.getContext('2d');R(g,0,58,124,16,K);R(g,1,59,122,14,'#c6c0b0');R(g,1,59,122,2,PAL.W);for(let y=63;y<73;y+=3)R(g,30,y,64,1,'#9a9488');
  R(g,8,28,108,32,K);R(g,9,29,106,30,'#c8302e');for(let x=14;x<112;x+=14){R(g,x,29,4,30,'#a82628');R(g,x,29,1,30,'#e04a40');}R(g,48,38,28,21,K);R(g,49,39,26,20,'#5a1a1a');R(g,61,39,1,20,'#ffc727');
  R(g,0,10,124,20,K);R(g,1,11,122,18,'#2f8a6a');for(let x=2;x<122;x+=3)R(g,x,14,1,15,'#247a5a');R(g,1,10,122,4,PAL.W);R(g,0,26,124,3,'#ffc727');R(g,-1,4,6,8,K);R(g,0,5,4,6,'#2f8a6a');R(g,119,4,6,8,K);R(g,120,5,4,6,'#2f8a6a');
  R(g,20,0,84,12,K);R(g,21,1,82,10,'#2f8a6a');R(g,21,0,82,3,PAL.W);R(g,44,30,36,10,K);R(g,45,31,34,8,'#ffc727');sprText(g,'TEMPLE',48,32,'#a82628');R(g,58,0,8,4,'#ffc727');return c;}
function lionSprite(f){const c=mk(14,18),g=c.getContext('2d');R(g,0,12,14,6,K);R(g,1,13,12,4,'#c6c0b0');R(g,1,13,12,1,PAL.W);R(g,2,2,10,11,K);R(g,3,3,8,9,'#9aa2b0');R(g,3,3,8,4,'#b8bec8');R(g,f?3:7,5,4,3,K);R(g,f?4:8,6,2,1,'#e03a4e');R(g,3,2,8,2,PAL.W);for(let x=3;x<11;x+=2)R(g,x,7,1,1,'#6a7088');return c;}
function stoneLampSprite(){const c=mk(10,18),g=c.getContext('2d');R(g,0,0,10,4,K);R(g,1,1,8,2,'#9aa2b0');R(g,1,0,8,1,PAL.W);R(g,1,4,8,6,K);R(g,2,5,6,4,'#ffc727');R(g,4,5,2,4,'#ffe36a');R(g,3,10,4,5,K);R(g,4,10,2,5,'#9aa2b0');R(g,1,15,8,3,K);R(g,2,15,6,2,'#9aa2b0');return c;}
function urnSprite(){const c=mk(16,18),g=c.getContext('2d');R(g,2,8,12,8,K);R(g,3,9,10,6,'#a8673a');R(g,3,9,10,1,'#ffc727');R(g,1,7,14,3,K);R(g,2,7,12,1,'#c98d4a');R(g,3,16,3,2,K);R(g,10,16,3,2,K);for(const [x,y] of [[6,5],[7,3],[6,1],[9,4],[10,2]])R(g,x,y,1,1,'#c6d0dc');return c;}
function dragonSprite(){const c=mk(96,22),g=c.getContext('2d');for(let k=0;k<11;k++){const x=k*7,y=6+Math.round(Math.sin(k*0.9)*3);R(g,x,y,9,9,K);R(g,x+1,y+1,7,7,k%2?'#ffc727':'#e03a4e');R(g,x+2,y,4,2,'#ffc727');R(g,x+3,y+8,2,6,K);R(g,x+3,y+9,1,5,'#2a2a36');}
  R(g,76,2,18,14,K);R(g,77,3,16,12,'#e03a4e');R(g,85,4,4,4,PAL.W);R(g,86,5,2,2,K);R(g,90,8,5,5,'#ffc727');R(g,78,1,4,3,'#ffc727');R(g,82,0,3,3,'#ffc727');R(g,77,13,10,2,'#ffc727');R(g,80,16,2,6,K);R(g,86,16,2,6,K);return c;}
function lanternOverSprite(w){const c=mk(w,20),g=c.getContext('2d');for(let x=0;x<w;x++){const y=Math.round(1+5*Math.sin(Math.PI*x/w));R(g,x,y,1,1,'#2a2a36');if(x%16===8){R(g,x-3,y+1,7,9,K);R(g,x-2,y+2,5,7,'#e03a4e');R(g,x-2,y+2,5,1,'#ffc727');R(g,x-2,y+8,5,1,'#ffc727');R(g,x-1,y+3,1,4,'#ff7a6a');R(g,x,y+10,1,3,'#ffc727');}}return c;}
function redBridgeSprite(w){const c=mk(w,30),g=c.getContext('2d');for(let x=0;x<w;x++){const lift=Math.round(6*Math.sin(Math.PI*x/w));R(g,x,8-lift,1,16,K);R(g,x,9-lift,1,14,(x>>2)%2?'#a8673a':'#c98d4a');R(g,x,9-lift,1,2,PAL.W);R(g,x,24-lift,1,3,K);R(g,x,25-lift,1,1,'#c8302e');R(g,x,4-lift,1,4,x%6===0?K:'rgba(0,0,0,0)');}
  for(let x=0;x<w;x+=6){const lift=Math.round(6*Math.sin(Math.PI*x/w));R(g,x,3-lift,2,6,K);R(g,x,4-lift,1,4,'#c8302e');R(g,x,23-lift,2,6,K);R(g,x,24-lift,1,4,'#c8302e');}for(let x=0;x<w;x++){const lift=Math.round(6*Math.sin(Math.PI*x/w));R(g,x,3-lift,1,1,'#c8302e');R(g,x,22-lift,1,1,'#c8302e');}return c;}
function pillarSprite(){const c=mk(10,16),g=c.getContext('2d');R(g,0,0,10,16,K);R(g,1,1,8,14,'#a8aeba');R(g,1,1,3,14,'#c6ccd6');R(g,1,12,8,3,'#ffc727');R(g,1,13,8,1,K);return c;}
// ---- a car circling a roundabout
function orbitHz(x,y,a,b2){const cc=CAR_PAL[(x+y+(a|0))%5];return {kind:'orbit',cx:x,cy:y,r:a||60,ang:(b2||0)*0.7,spd:(b2&1?-1:1)*(58/(a||60)),x:x-9,y:y-9,w:18,h:18,big:true,spr:carSprite(cc[0],cc[1],false,false)};}
HAZ.orbit={make:(x,y,a)=>orbitHz(x,y,a,0)};

// ---- wild areas: mass scenery with carved corridors
function wildSpr(kind,rn){const r=rn();
  if(kind==='forest'){if(r<0.8){const a=18+((rn()*20)|0);return scnSpr('pn'+a,()=>pineSprite(a));}if(r<0.93){const a=18+((rn()*14)|0);return scnSpr('bt'+a,()=>bareTreeSprite(a,a*7));}const w=10+((rn()*8)|0);return scnSpr('rk'+w,()=>rockSprite(w,8+(w>>2)));}
  if(kind==='rocks'){if(r<0.72){const w=12+((rn()*16)|0);return scnSpr('rk'+w,()=>rockSprite(w,9+(w>>1)));}const a=16+((rn()*12)|0);return scnSpr('pn'+a,()=>pineSprite(a));}
  if(kind==='ice'){if(r<0.45)return scnSpr('sp',()=>spireSprite());const w=10+((rn()*14)|0);return scnSpr('ib'+w,()=>iceBlockSprite(w,Math.round(w*0.75)));}
  if(kind==='park'){if(r<0.45){const a=20+((rn()*16)|0);return scnSpr('bt'+a,()=>bareTreeSprite(a,a*7));}if(r<0.8)return scnSpr('oak',()=>oakSprite());const a=18+((rn()*12)|0);return scnSpr('pn'+a,()=>pineSprite(a));}
  if(kind==='bush'){const w=10+((rn()*8)|0);return scnSpr('bu'+w,()=>{const c=mk(w,w),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,w>>1,w>>1,(w>>1));g.fillStyle='#1f6a44';pixCircle(g,w>>1,w>>1,(w>>1)-1);R(g,2,1,w-4,2,PAL.W);return c;});}
  return null;}
function inCarveF(cv){return (px,py,m)=>{for(const c of cv){const r=c[0]/2+(m||0),r2=r*r;for(let i=1;i+3<c.length;i+=2){const ax=c[i],ay=c[i+1],bx=c[i+2],by=c[i+3];if(py<Math.min(ay,by)-r||py>Math.max(ay,by)+r)continue;const dx=bx-ax,dy=by-ay,L=dx*dx+dy*dy;let t=L?((px-ax)*dx+(py-ay)*dy)/L:0;t=t<0?0:t>1?1:t;const qx=ax+dx*t-px,qy=ay+dy*t-py;if(qx*qx+qy*qy<=r2)return true;}}return false;};}
function buildWilds(g,D,setT,setCircle){const cols=g.cols,rows=g.rows;
  for(const p of D.paths||[]){const t=GROUND_T[p[0]]!=null?GROUND_T[p[0]]:T_GRASS,r=p[1]/2;for(let i=2;i+3<p.length;i+=2){const ax=p[i],ay=p[i+1],bx=p[i+2],by=p[i+3],n=Math.max(1,Math.ceil(Math.hypot(bx-ax,by-ay)/2));for(let k=0;k<=n;k++)setCircle(t,ax+(bx-ax)*k/n,ay+(by-ay)*k/n,r);}}
  if(!D.wilds&&!D.scen&&!D.over)return;
  g.wild=new Uint8Array(cols*rows);const blk=(cx,cy)=>{if(cx<0||cy<0||cx>=cols||cy>=rows)return;const i=cy*cols+cx;g.wild[i]=1;g.type[i]=T_BLOCK;};
  const inC=inCarveF(D.carves||[]);
  for(const wd of D.wilds||[]){const [kind,x,y,w,h,seed,dens]=wd;const cx0=Math.max(0,x>>1),cy0=Math.max(0,y>>1),cx1=Math.min(cols,(x+w+1)>>1),cy1=Math.min(rows,(y+h+1)>>1);
    for(let cy=cy0;cy<cy1;cy++)for(let cx=cx0;cx<cx1;cx++)if(!inC(cx*2+1,cy*2+1))blk(cx,cy);
    const rn=srng(seed||(x*31+y*7)),st=wd[7]||9;
    for(let py=y+4;py<y+h;py+=st)for(let px=x+2;px<x+w;px+=st){const qx=Math.round(px+(rn()-0.5)*st*0.9),qy=Math.round(py+(rn()-0.5)*st*0.9);if(rn()>(dens==null?0.75:dens))continue;
      if(qx<0||qy<0||qx>=g.pw||qy>=g.ph)continue;if(!g.wild[(qy>>1)*cols+(qx>>1)]||inC(qx,qy,3))continue;const sp=wildSpr(kind,rn);if(!sp)continue;g.scenery.push({spr:sp,sx:Math.round(qx-sp.width/2),sy:qy-sp.height+2,base:qy+2});}}
  for(const p of D.scen||[]){const P2=PROPS[p[0]];if(!P2)continue;const a=p[3]!=null?p[3]:P2.arg,sp=P2.make(a),f2=P2.foot(a);g.scenery.push({spr:sp,sx:p[1],sy:p[2],base:p[2]+f2[1]+f2[3]});if(!p[4])for(let cy=(p[2]+f2[1])>>1;cy<Math.ceil((p[2]+f2[1]+f2[3])/2);cy++)for(let cx=(p[1]+f2[0])>>1;cx<Math.ceil((p[1]+f2[0]+f2[2])/2);cx++)blk(cx,cy);}
  for(const p of D.over||[]){const f=OVERS[p[0]];if(f)g.over.push({spr:f(p[3],p[4]),sx:p[1],sy:p[2]});}
  const W1=cols+1,S=new Int32Array(W1*(rows+1));for(let y=0;y<rows;y++){let rs=0;for(let x=0;x<cols;x++){rs+=g.wild[y*cols+x];S[(y+1)*W1+x+1]=S[y*W1+x+1]+rs;}}g.wsat=S;}
function hzVis(hz){if(hz.r0==null)return hz;const y0=Math.max(hz.y,hz.r0),y1=Math.min(hz.y+hz.h,hz.r1);return y1>y0?{x:hz.x,y:y0,w:hz.w,h:y1-y0}:{x:-999,y:-999,w:0,h:0};}
function wildHit(r){const g=G;if(!g||!g.wsat)return false;const cols=g.cols,x0=Math.max(0,Math.floor(r.x/2)),y0=Math.max(0,Math.floor(r.y/2)),x1=Math.min(cols,Math.ceil((r.x+r.w)/2)),y1=Math.min(g.rows,Math.ceil((r.y+r.h)/2));if(x1<=x0||y1<=y0)return false;const S=g.wsat,W1=cols+1;return S[y1*W1+x1]-S[y0*W1+x1]-S[y1*W1+x0]+S[y0*W1+x0]>0;}
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){", KIT+"\nfunction buildFromData(g,D,setT,ob,setCircle,paintText){")
# ground finishes
rep("case T_ICE:return n<3?[0xe8,0xf6,0xff]:n<6?[0x9f,0xd4,0xf4]:[0xbf,0xe6,0xff];default:return [0x9a,0xa1,0xb5];}};",
    "case T_ICE:return n<3?[0xe8,0xf6,0xff]:n<6?[0x9f,0xd4,0xf4]:[0xbf,0xe6,0xff];default:return groundCol2(t,x,y,n);}};")
# level fields
rep("obstacles:[],decor:[],hazards:[],spawners:[],lights:[],presents:[],neighbours:[],pullBlocks:[],start:{x:90,y:60},clearable:0,cleared:0};",
    "obstacles:[],scenery:[],over:[],decor:[],hazards:[],spawners:[],lights:[],presents:[],neighbours:[],pullBlocks:[],start:{x:90,y:60},clearable:0,cleared:0};")
# data: wilds/paths/scenery/overhead after the props, decals stored for after the ground fill
rep("  g.start=D.start?{x:D.start[0],y:D.start[1]}:{x:90,y:40};}",
    "  buildWilds(g,D,setT,setCircle);if(D.decals)g.decals=D.decals;\n  g.start=D.start?{x:D.start[0],y:D.start[1]}:{x:90,y:40};}")
rep("for(let y=0;y<ph;y++)for(let x=0;x<pw;x++){const c=col(g.type[(y>>1)*cols+(x>>1)],x,y);const o=(y*pw+x)*3;g.ground[o]=c[0];g.ground[o+1]=c[1];g.ground[o+2]=c[2];}",
    "for(let y=0;y<ph;y++)for(let x=0;x<pw;x++){const c=col(g.type[(y>>1)*cols+(x>>1)],x,y);const o=(y*pw+x)*3;g.ground[o]=c[0];g.ground[o+1]=c[1];g.ground[o+2]=c[2];}if(g.decals)paintDecals(g);")
# forest snow reads as off-limits: a touch shaded
rep("if(blocked||d>BAYER[sy*2+sx]){c=snowCol(px,py,g.mark[i]&&sy===1,SNOW,SNOW2,g);",
    "if(blocked||d>BAYER[sy*2+sx]){c=snowCol(px,py,g.mark[i]&&sy===1,SNOW,SNOW2,g);if(g.wild&&g.wild[i])c=[c[0]-16,c[1]-11,c[2]-4];")
# collision: wild areas block the plow, chasers and roaming hazards; pushed things stop at them
rep("  for(const o of G.obstacles)if(overlap(r,o)&&!ignOK(r,o,o)){G.lastOb=o;return 'ob';}",
    "  for(const o of G.obstacles)if(overlap(r,o)&&!ignOK(r,o,o)){G.lastOb=o;return 'ob';}\n  if(wildHit(r)){G.lastOb=null;return 'ob';}")
rep("function chaserFree(hz,x,y){if(x<1||y<1||x+hz.w>G.pw-1||y+hz.h>G.ph-1)return false;",
    "function chaserFree(hz,x,y){if(x<1||y<1||x+hz.w>G.pw-1||y+hz.h>G.ph-1)return false;if(wildHit({x,y,w:hz.w,h:hz.h}))return false;")
rep("for(const o of G.obstacles)if(overlap(r,o)){bad=true;break;}","if(wildHit(r))bad=true;else for(const o of G.obstacles)if(overlap(r,o)){bad=true;break;}",3)
rep("function shoveOb(o,dx,dy,depth){depth=depth||0;const r2={x:o.x+dx,y:o.y+dy,w:o.w,h:o.h};if(r2.x<0||r2.y<0||r2.x+r2.w>G.pw||r2.y+r2.h>G.ph)return false;",
    "function shoveOb(o,dx,dy,depth){depth=depth||0;const r2={x:o.x+dx,y:o.y+dy,w:o.w,h:o.h};if(r2.x<0||r2.y<0||r2.x+r2.w>G.pw||r2.y+r2.h>G.ph)return false;if(wildHit(r2))return false;")
# drawing: scenery shadows + y-sorted with everything else; the overhead layer last
rep("    for(const o of G.obstacles)if(o.sy+o.spr.height>top-4&&o.sy<bot+4)b.drawImage(shadowOf(o.spr),o.sx+sp[0],o.sy+sp[1]);",
    "    for(const o of G.obstacles)if(o.sy+o.spr.height>top-4&&o.sy<bot+4)b.drawImage(shadowOf(o.spr),o.sx+sp[0],o.sy+sp[1]);\n    for(const o of G.scenery)if(o.sy+o.spr.height>top-4&&o.sy<bot+4)b.drawImage(shadowOf(o.spr),o.sx+sp[0],o.sy+sp[1]);")
rep("  for(const o of G.obstacles)if(o.sy+o.spr.height>top&&o.sy<bot)ents.push({base:o.base,draw:()=>{if(lkOutline()||(LOOK==='e'&&smallOb(o)))b.drawImage(outlineOf(o.spr),o.sx-1,o.sy-1);b.drawImage(bright(o.spr),o.sx,o.sy);}});",
    "  for(const o of G.obstacles)if(o.sy+o.spr.height>top&&o.sy<bot)ents.push({base:o.base,draw:()=>{if(lkOutline()||(LOOK==='e'&&smallOb(o)))b.drawImage(outlineOf(o.spr),o.sx-1,o.sy-1);b.drawImage(bright(o.spr),o.sx,o.sy);}});\n  for(const o of G.scenery)if(o.sy+o.spr.height>top&&o.sy<bot)ents.push({base:o.base,draw:()=>{if(lkOutline())b.drawImage(outlineOf(o.spr),o.sx-1,o.sy-1);b.drawImage(bright(o.spr),o.sx,o.sy);}});")
rep("  ents.sort((a,c)=>a.base-c.base);for(const e of ents)e.draw();",
    "  ents.sort((a,c)=>a.base-c.base);for(const e of ents)e.draw();\n  for(const o of G.over)if(o.sy+o.spr.height>top&&o.sy<bot){const un=P&&P.x>o.sx-6&&P.x<o.sx+o.spr.width+6&&P.y>o.sy-4&&P.y<o.sy+o.spr.height+14;b.save();b.globalAlpha=0.18;b.drawImage(shadowOf(o.spr),o.sx+4,o.sy+10);b.globalAlpha=un?0.4:1;b.drawImage(bright(o.spr),o.sx,o.sy);b.restore();}")

# bounded traffic: a taxi/bus/tram with a y range enters from a cross street and leaves at the next one
rep("    else g.hazards.push(H.make(h[1],h[2],h[3]));}",
    "    else{const hz=H.make(h[1],h[2],h[3]);if(h[0]==='taxi'&&h[4]!=null){hz.r0=h[4];hz.r1=h[5];hz.y=Math.max(hz.r0,Math.min(hz.r1-hz.h,hz.y));}if(h[0]==='orbit'&&h[4]!=null)hz.ang=h[4];g.hazards.push(hz);}}")
rep("if(hz.dir>0&&hz.y>G.ph+30)hz.y=-70;if(hz.dir<0&&hz.y<-70)hz.y=G.ph+30;",
    "{const r0=hz.r0!=null?hz.r0-hz.h-4:-70,r1=hz.r1!=null?hz.r1+4:G.ph+30;if(hz.dir>0&&hz.y>r1)hz.y=r0;if(hz.dir<0&&hz.y<r0)hz.y=r1;}")
rep("&&overlap(pr,hz)){const big=hz.kind==='taxi'||hz.big;",
    "&&overlap(pr,hzVis(hz))){const big=hz.kind==='taxi'||hz.big;")
rep("    else ents.push({base:hz.y+hz.h,draw:()=>{b.save();b.translate(hx+11,hy+Math.round(hz.h/2));",
    "    else ents.push({base:hz.y+hz.h,draw:()=>{b.save();if(hz.r0!=null){b.beginPath();b.rect(-20,hz.r0,W+40,hz.r1-hz.r0);b.clip();}b.translate(hx+11,hy+Math.round(hz.h/2));")

# stage boards say what the stage is for
rep("function stageSprite(){const c=mk(80,34),g=c.getContext('2d');","function stageSprite(a){a=a|0;const c=mk(80,34),g=c.getContext('2d');")
rep("  text(g,'BLOCK PARTY',40,6,'#ffffff',{align:'center',outline:null});","  text(g,['BLOCK PARTY','CITY HALL','WINTER FEST','LIVE MUSIC','FIREWORKS','HARBOUR FEST','APRES SKI','NORTH POLE'][a]||'BLOCK PARTY',40,6,'#ffffff',{align:'center',outline:null});")
rep("stage:{make:()=>stageSprite(),","stage:{arg:0,min:0,max:7,make:a=>stageSprite(a),")
# the roundabout car
rep("    else if(hz.kind==='taxi'){hz.y+=hz.vy*dt;","    else if(hz.kind==='orbit'){hz.ang+=hz.spd*dt;hz.x=hz.cx+Math.cos(hz.ang)*hz.r-hz.w/2;hz.y=hz.cy+Math.sin(hz.ang)*hz.r-hz.h/2;}\n    else if(hz.kind==='taxi'){hz.y+=hz.vy*dt;")
rep("    else ents.push({base:hz.y+hz.h,draw:()=>{b.save();if(hz.r0!=null)","    else if(hz.kind==='orbit')ents.push({base:hz.y+hz.h,draw:()=>{b.save();b.translate(Math.round(hz.x+hz.w/2),Math.round(hz.y+hz.h/2));b.rotate(hz.ang+(hz.spd>0?Math.PI:0));b.drawImage(hz.spr,-12,-16);b.restore();}});\n    else ents.push({base:hz.y+hz.h,draw:()=>{b.save();if(hz.r0!=null)")
# a dragon dance crosses the street (cross skin 'dragon')
rep("spr=sk==='sled'?sledSprite():","spr=sk==='dragon'?scnSpr('dragon',dragonSprite):sk==='sled'?sledSprite():")
rep("speed:sk==='sled'?64:sk==='car'?70:","speed:sk==='dragon'?30:sk==='sled'?64:sk==='car'?70:")

open(f,'w',encoding='utf-8').write(s)
