import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# NEW MAP BANDS: Farmland part 2, City part 2, Theme Park, Frozen Harbour, Ski Resort, Mountain Pass and more
# Frozen North. Each band: its ground, roads and job spots reserved, the jobs' landmarks (BAND_DECOR, filled in by
# each area's patch), then filler scenery in that area's style, and a sign where you enter the area.
# ---------------------------------------------------------------------------------------------
# the old "THE FROZEN NORTH" sign sat on top of the old City; the North's sign now goes at its own edge
rep("put(848,G2=>mSign(G2,92,834,'THE FROZEN NORTH','#6b3fa8'));mMark(40,828,104,24,MK_RES);","")

KIT=r"""
const BAND_DECOR={};
function mTent(g,x,y,w,h,c1,c2){const rh=Math.round(h*0.55);for(let r=0;r<rh;r++){const hw=Math.round((r+1)/rh*w/2);R(g,x+Math.round(w/2)-hw-1,y+r,hw*2+2,1,K);for(let xx=-hw;xx<hw;xx++)R(g,x+Math.round(w/2)+xx,y+r,1,1,((xx+40)>>2)%2?c1:c2);}
  R(g,x,y+rh,w,h-rh,K);R(g,x+1,y+rh,w-2,h-rh-1,c2);R(g,x+Math.round(w/2)-2,y+rh+1,4,h-rh-2,'#3a2a20');R(g,x+Math.round(w/2),y-3,1,3,K);R(g,x+Math.round(w/2)+1,y-3,3,2,c1);
  R(g,x+Math.round(w/2)-3,y,6,2,MC.snow);}
function mFerris(g,cx,cy,r){g.fillStyle=K;for(let a=0;a<64;a++){const t=a/64*Math.PI*2;g.fillRect(Math.round(cx+Math.cos(t)*r),Math.round(cy+Math.sin(t)*r),2,2);}
  for(let k=0;k<8;k++){const t=k/8*Math.PI*2;for(let d=0;d<r;d+=2)R(g,Math.round(cx+Math.cos(t)*d),Math.round(cy+Math.sin(t)*d),1,1,'#8793a8');const px=Math.round(cx+Math.cos(t)*r),py=Math.round(cy+Math.sin(t)*r);
    R(g,px-3,py,6,5,K);R(g,px-2,py+1,4,3,['#d8364b','#ffc727','#3f86d6','#33b24a'][k%4]);R(g,px-2,py+1,4,1,MC.snow);}
  R(g,cx-1,cy,3,r+6,K);R(g,cx-r/2|0,cy+r+4,r+2,3,K);R(g,cx-2,cy-2,5,5,K);R(g,cx-1,cy-1,3,3,'#ffc727');}
function mTrack(g,pts,col){for(let i=0;i<pts.length-1;i++){const [x0,y0]=pts[i],[x1,y1]=pts[i+1],n=Math.max(Math.abs(x1-x0),Math.abs(y1-y0));for(let k=0;k<=n;k++){const x=Math.round(x0+(x1-x0)*k/n),y=Math.round(y0+(y1-y0)*k/n);R(g,x,y-1,2,3,K);R(g,x,y,2,1,col);}
    for(let k=0;k<=n;k+=6){const x=Math.round(x0+(x1-x0)*k/n),y=Math.round(y0+(y1-y0)*k/n);R(g,x,y+2,1,5,'#55607a');}}}
function mCarousel(g,cx,cy){g.fillStyle=K;pixCircle(g,cx,cy+4,11);g.fillStyle='#e8c87a';pixCircle(g,cx,cy+4,10);for(let k=0;k<6;k++){const t=k/6*Math.PI*2;R(g,Math.round(cx+Math.cos(t)*7)-1,Math.round(cy+4+Math.sin(t)*4)-3,3,4,['#d8364b','#3f86d6','#f4f8ff'][k%3]);}
  for(let r=0;r<7;r++){const hw=r+3;R(g,cx-hw-1,cy-10+r,hw*2+2,1,K);R(g,cx-hw,cy-10+r,hw*2,1,r%2?'#d8364b':'#f4f8ff');}R(g,cx-1,cy-14,2,4,K);R(g,cx-10,cy-4,20,2,MC.snow);}
function mBoat(g,x,y,w,col){R(g,x,y+4,w,6,K);R(g,x+1,y+5,w-2,4,col);R(g,x+2,y+9,w-4,2,K);R(g,x+1,y+5,w-2,1,MC.snow);R(g,x+Math.round(w*0.55),y-6,7,10,K);R(g,x+Math.round(w*0.55)+1,y-5,5,8,'#f4f8ff');R(g,x+Math.round(w*0.55)+2,y-3,3,2,'#8fd3ff');R(g,x+Math.round(w*0.55),y-6,7,2,MC.snow);}
function mContainer(g,x,y,w,col){R(g,x,y,w,9,K);R(g,x+1,y+1,w-2,7,col);for(let xx=x+3;xx<x+w-2;xx+=3)R(g,xx,y+2,1,5,'rgba(0,0,0,0.22)');R(g,x+1,y+1,w-2,2,MC.snow);}
function mChalet(g,x,y,w,h,seed){const rh=Math.round(h*0.45);for(let r=0;r<rh;r++){const hw=Math.round((r+1)/rh*(w/2+2));R(g,x+w/2-hw-1|0,y+r,hw*2+2,1,K);R(g,x+w/2-hw|0,y+r,hw*2,1,r<rh-2?MC.snow:'#7a4a2a');}
  R(g,x,y+rh,w,h-rh,K);R(g,x+1,y+rh,w-2,h-rh-1,'#a8673a');for(let yy=y+rh+2;yy<y+h-1;yy+=2)R(g,x+1,yy,w-2,1,'#8a5a2c');mWin(g,x+3,y+rh+2,true);mWin(g,x+w-7,y+rh+2,hash(seed,3)%2===0);R(g,x+w/2-2|0,y+h-6,4,6,K);}
function mPylon(g,x,y){R(g,x,y,3,22,K);R(g,x+1,y,1,21,'#8793a8');R(g,x-4,y,11,3,K);R(g,x-3,y+1,9,1,'#c6d9f3');}
function mIgloo(g,cx,cy){g.fillStyle=K;pixCircle(g,cx,cy,8);g.fillStyle='#f4f8ff';pixCircle(g,cx,cy,7);for(let r=-5;r<=5;r+=3)R(g,cx-6,cy+r,12,1,'#c6d9f3');R(g,cx-3,cy+3,6,5,K);R(g,cx-2,cy+4,4,4,'#3a4a6a');}
function mSea(g,y0,y1){for(let y=y0;y<y1;y++){R(g,0,y,W,1,(y>>2)%2?'#9fc4e8':'#a9cdee');}for(let i=0;i<Math.round((y1-y0)/4);i++){const x=hash(i,901)%W,y=y0+hash(903,i)%(y1-y0),w=8+hash(i,905)%22;R(g,x,y,w,4,K);R(g,x+1,y,w-2,3,'#eaf2fc');R(g,x+1,y,w-2,1,'#ffffff');}}
function bandRange(id){const B=BIOMES_NEW.find(B2=>B2.id===id);return [B.y0,B.y1];}
function genBand(g,og,id,y0,y1,opts){const objs=[],put=(by,fn)=>objs.push({by,fn}),res=(x,y,w,h)=>mMark(x,y,w,h,MK_RES);
  const B=BIOMES_NEW.find(B2=>B2.id===id);R(g,0,y0,W,y1-y0,B.ground);
  for(let i=0;i<Math.round((y1-y0)*1.1);i++){const x=hash(i,311+y0)%W,y=y0+hash(313+y0,i)%(y1-y0),v=hash(i,317)%10;if(v<5)R(g,x,y,2,1,MC.snowB);else if(v<8)R(g,x,y,1,1,MC.sh);else R(g,x,y,1,1,'#ffffff');}
  if(opts.ground)opts.ground(g,y0,y1,res);
  for(const e of mapEdges())for(const [x,y] of e.pts)if(y>y0-8&&y<y1+8)mMark(x-6,y-6,13,13,MK_ROAD);
  for(const L of LEVELS){const p=MAPPOS[L.id];if(p&&p[1]>=y0-16&&p[1]<y1+16)mMark(p[0]-14,p[1]-16,29,32,MK_RES);}
  if(BAND_DECOR[opts.decor||id])BAND_DECOR[opts.decor||id](g,put,res,y0,y1);
  if(opts.sign){const sy2=y1-30;put(sy2+12,G2=>mSign(G2,opts.signX||46,sy2,B.name,opts.signCol));res((opts.signX||46)-50,sy2-4,100,22);}
  const tryPut=(x,y,w,h,fx)=>{if(y<y0+4||y+h>y1-2)return false;if(!mFree(x,y,w,h,MK_ROAD|MK_RES))return false;const fy=y+Math.floor(h*0.25);if(!mFree(x,fy,w,h-Math.floor(h*0.25),MK_OBJ))return false;mMark(x,fy,w,h-Math.floor(h*0.25),MK_OBJ);put(y+h,fx);return true;};
  for(let y=y0+6;y<y1-4;y+=opts.step||5){for(let x=-6;x<W;x+=7){const hv=hash(x+731+y0,y+1291),jx=x+(hv%5),jy=y+((hv>>>4)%4),r=(hv>>>8)%100;opts.fill(tryPut,jx,jy,r,hv);}}
  objs.sort((a,b)=>a.by-b.by);for(const o of objs)o.fn(og);}
function genNewBands(g,og){
  const HC=HOUSE_COLS;
  genBand(g,og,'farm',FARM_SPLIT+TOP_EXT,FARM_SPLIT+TOP_EXT+FARM_EXT,{decor:'farm2',fill:(tp,x,y,r,hv)=>{if(r>60)return;
    if(r<8){tp(x,y-14,26,16,G2=>mField(G2,x,y-14,26,14,hv));}else if(r<12){tp(x,y-18,22,20,G2=>mBarn(G2,x,y-18,22,20));}else if(r<20)tp(x,y-10,9,10,G2=>mApple(G2,x,y-10));
    else if(r<44){const h=12+((hv>>>12)%4)*2;tp(x-5,y-h,10,h,G2=>mPine(G2,x,y,h));}else if(r<48)tp(x,y-5,10,6,G2=>mHay(G2,x,y-5));else if(r<52)tp(x,y-9,9,10,G2=>mBare(G2,x,y-9,9));}});
  genBand(g,og,'city',TOP_SPLIT+TOP_EXT-CITY_EXT,TOP_SPLIT+TOP_EXT,{decor:'city2',fill:(tp,x,y,r,hv)=>{if(r>62)return;
    if(r<22){const w=14+((hv>>>12)%3)*4,h=22+((hv>>>14)%4)*6,c=[['#8793a8','#6a7896'],['#c6b49a','#a8967a'],['#9fb3c8','#7f93a8'],['#d8a07a','#b8805a']][(hv>>>16)%4];tp(x,y-h,w,h,G2=>mTower(G2,x,y-h,w,h,c[0],c[1],hv));}
    else if(r<30)tp(x,y-14,30,14,G2=>mShop(G2,x,y-14,30,['#d8364b','#3f86d6','#5aa35a','#ffc727'][(hv>>>12)%4],hv));else if(r<36)tp(x,y-12,4,12,G2=>mLamp(G2,x,y-12,false));
    else if(r<50){const h=12+((hv>>>12)%3)*2;tp(x-5,y-h,10,h,G2=>mPine(G2,x,y,h));}}});
  {const [y0,y1]=bandRange('themepark');genBand(g,og,'themepark',y0,y1,{sign:true,signCol:'#d8364b',signX:132,fill:(tp,x,y,r,hv)=>{if(r>58)return;
    if(r<10){const c=[['#d8364b','#f4f8ff'],['#3f86d6','#f4f8ff'],['#ffc727','#d8364b'],['#9b5fd6','#ffc727']][(hv>>>12)%4];tp(x,y-18,18,18,G2=>mTent(G2,x,y-18,18,18,c[0],c[1]));}
    else if(r<16)tp(x,y-14,22,14,G2=>mStall(G2,x,y-14,['#d8364b','#3f86d6','#ffc727'][(hv>>>12)%3]));else if(r<22)tp(x,y-12,4,12,G2=>mLamp(G2,x,y-12,true));
    else if(r<44){const h=12+((hv>>>12)%3)*2;tp(x-5,y-h,10,h,G2=>mPine(G2,x,y,h));}else if(r<48)tp(x,y-5,10,6,G2=>mBush(G2,x,y-5,10,6));}});}
  {const [y0,y1]=bandRange('harbour');genBand(g,og,'harbour',y0,y1,{sign:true,signCol:'#2f6f8a',signX:132,step:6,ground:(G2,a,b2,res)=>{mSea(G2,a+40,a+230);R(G2,0,a+230,W,4,K);R(G2,0,a+234,W,6,'#8793a8');res(0,a+36,W,206);},fill:(tp,x,y,r,hv)=>{if(r>40)return;
    if(r<5){const w=18+((hv>>>12)%2)*8;tp(x,y-9,w,9,G2=>mContainer(G2,x,y-9,w,['#d8364b','#3f86d6','#33b24a','#ffc727','#f07a1a'][(hv>>>14)%5]));}
    else if(r<8){const w=18,h=20;tp(x,y-h,w,h,G2=>mTower(G2,x,y-h,w,h,'#9fb3c8','#7f93a8',hv));}else if(r<11)tp(x,y-12,12,12,G2=>mCrate(G2,x,y-12,12,12,''));
    else if(r<36){const h=12+((hv>>>12)%3)*2;tp(x-5,y-h,10,h,G2=>mPine(G2,x,y,h));}else if(r<38)tp(x,y-6,10,6,G2=>mRock(G2,x,y-6,10,6));}});}
  {const [y0,y1]=bandRange('ski');genBand(g,og,'ski',y0,y1,{sign:true,signCol:'#4fb0d8',signX:132,ground:(G2,a,b2)=>{for(let k=0;k<6;k++){const x=20+hash(k,77)%140;for(let y=a+10;y<b2-10;y+=2)R(G2,x+Math.round(Math.sin(y*0.04+k)*14),y,2,1,'#dfe8f5');}},fill:(tp,x,y,r,hv)=>{if(r>64)return;
    if(r<6){tp(x,y-18,20,18,G2=>mChalet(G2,x,y-18,20,18,hv));}
    else if(r<50){const h=12+((hv>>>12)%5)*2;tp(x-5,y-h,10,h,G2=>mPine(G2,x,y,h));}else if(r<56)tp(x,y-6,10,6,G2=>mRock(G2,x,y-6,10,6));}});}
  {const [y0,y1]=bandRange('pass');genBand(g,og,'pass',y0,y1,{sign:true,signCol:'#5a6a8a',signX:132,fill:(tp,x,y,r,hv)=>{if(r>66)return;
    if(r<10){const hw=14+(hv>>>12)%10,h=30+(hv>>>14)%26;tp(x-hw,y-h,hw*2,h,G2=>mMountain(G2,x,y,hw,h,hv));}else if(r<16){const w=8+((hv>>>12)%3)*4;tp(x,y-6,w,7,G2=>mRock(G2,x,y-6,w,7));}
    else if(r<50){const h=12+((hv>>>12)%5)*2;tp(x-5,y-h,10,h,G2=>mPine(G2,x,y,h));}}});}
  genBand(g,og,'north',TOP_SPLIT,TOP_SPLIT+NORTH_EXT,{sign:true,signCol:'#6b3fa8',signX:132,fill:(tp,x,y,r,hv)=>{if(r>56)return;
    if(r<4)tp(x-8,y-9,17,17,G2=>mIgloo(G2,x,y-8));else if(r<10){const w=8+((hv>>>12)%3)*4;tp(x,y-6,w,7,G2=>mRock(G2,x,y-6,w,7));}
    else if(r<44){const h=12+((hv>>>12)%5)*2;tp(x-5,y-h,10,h,G2=>mPine(G2,x,y,h));}}});
}
"""
rep("function mapInit(){if(mapBase)return;",KIT+"function mapInit(){if(mapBase)return;")
open(f,'w',encoding='utf-8').write(s);print('p49 ok')
