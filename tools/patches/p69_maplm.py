import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# World map: a little hand-drawn landmark for every job of the seven newer areas (Farmland 2, City 2, Theme Park,
# Harbour, Ski Resort, Mountain Pass, Frozen North), drawn at its LANDMARK spot (which is also what the list view and
# the job card show). Space is reserved so the random band scenery keeps clear of it. The ski band's faint wavy lines
# become proper groomed runs with a chairlift, so they read as pistes rather than roads.
JS=r"""
function lmArt(g,id,x,y){
  const B=(x0,y0,w,h,c)=>{R(g,x0,y0,w,h,K);R(g,x0+1,y0+1,w-2,h-2,c);R(g,x0+1,y0+1,w-2,1,MC.snow);};
  const roof=(cx,y0,w,h,c)=>{for(let r=0;r<h;r++){const hw=Math.round((r+1)/h*w/2);R(g,cx-hw-1,y0+r,hw*2+2,1,K);R(g,cx-hw,y0+r,hw*2,1,r<2?MC.snow:c);}};
  const C=(cx,cy,r,c)=>{g.fillStyle=K;pixCircle(g,cx,cy,r+1);g.fillStyle=c;pixCircle(g,cx,cy,r);};
  const pole=(x0,y0,h,c)=>{R(g,x0,y0,1,h,K);R(g,x0+1,y0,5,3,c||'#e03a4e');};
  const ice=(x0,y0,w,h)=>{R(g,x0,y0,w,h,'#9fd4f4');R(g,x0+1,y0+1,w-2,1,'#e8f6ff');R(g,x0,y0+h-1,w,1,'#7ab0dc');};
  const shadow=(w)=>{R(g,x-w/2|0,y+10,w,2,MC.sh);};
  const pine=(px,py,h)=>mPine(g,px,py,h);
  const tree3=()=>{pine(x-10,y+10,12);pine(x+10,y+10,10);};
  switch(id){
  // ---------------- Farmland, part 2
  case 'milkshed':shadow(30);mBarn(g,x-14,y-8,20,18);mSilo(g,x+8,y-10,7,20);break;
  case 'treefarm':for(let k=0;k<6;k++)pine(x-12+(k%3)*12,y+(k<3?2:11),9+(k%2)*2);break;
  case 'sheepfields':mFenceH(g,x-15,y+6,30);for(const [a,b2] of [[-8,-2],[2,0],[8,-5],[-2,-7]]){R(g,x+a-1,y+b2-1,6,4,K);R(g,x+a,y+b2,4,2,'#f4f8ff');R(g,x+a+4,y+b2,1,2,'#2a2a36');}break;
  case 'stables':shadow(30);B(x-14,y-4,28,13,'#a8673a');for(let k=0;k<4;k++)R(g,x-11+k*6,y+2,4,6,'#55321d');roof(x,y-10,30,7,'#7a4a2a');break;
  case 'farmcafe':shadow(28);B(x-12,y-4,24,13,'#f4e3c4');roof(x,y-11,28,8,'#2f8a5a');mStall(g,x+6,y+3,'#d8364b');break;
  case 'windmill':{R(g,x-4,y-8,9,18,K);R(g,x-3,y-7,7,17,'#dfe5ef');roof(x,y-13,12,6,'#a8673a');for(let k=0;k<4;k++){const a=k*Math.PI/2+0.4;for(let d=2;d<13;d++)R(g,Math.round(x+Math.cos(a)*d),Math.round(y-9+Math.sin(a)*d),2,2,d>4?'#f4f8ff':K);}break;}
  case 'maze':R(g,x-14,y-9,28,20,K);R(g,x-13,y-8,26,18,'#2f8a5a');for(let k=0;k<4;k++){R(g,x-11+k*6,y-6+(k%2)*4,2,10,'#c9b48a');R(g,x-11,y-6+k*4,22,1,k%2?'#c9b48a':'#2f8a5a');}break;
  case 'mill':shadow(28);B(x-13,y-8,18,18,'#c6b49a');roof(x-4,y-14,22,7,'#7a4a2a');C(x+9,y+3,6,'#8a5a34');R(g,x+8,y-3,2,12,'#55321d');ice(x+4,y+9,12,3);break;
  case 'harvestfair':mTent(g,x-14,y-10,18,18,'#d8364b','#f4f8ff');mTent(g,x+2,y-6,14,14,'#ffc727','#f4f8ff');for(let k=0;k<8;k++)R(g,x-14+k*4,y-12+(k%2),2,2,['#d8364b','#3f86d6','#ffc727','#4fd36a'][k%4]);break;
  // ---------------- City, part 2
  case 'cityhall':shadow(30);B(x-14,y-4,28,14,'#e8dcc4');for(let k=0;k<5;k++)R(g,x-11+k*5,y-1,2,10,'#c6b49a');roof(x,y-10,30,6,'#8793a8');R(g,x-2,y-16,4,6,K);R(g,x-1,y-15,2,4,'#ffd23f');break;
  case 'chinatown':{shadow(30);R(g,x-14,y-6,2,16,K);R(g,x+12,y-6,2,16,K);R(g,x-16,y-9,32,4,K);R(g,x-15,y-8,30,2,'#d8364b');roof(x,y-14,26,5,'#2f8a5a');for(const lx of [-8,0,8]){C(x+lx,y,2,'#e03a4e');}break;}
  case 'junction':R(g,x-15,y-2,30,8,'#4a5068');R(g,x-3,y-12,8,24,'#4a5068');for(let k=0;k<5;k++)R(g,x-14+k*6,y+1,3,2,'#f4f8ff');R(g,x+8,y-10,3,9,K);R(g,x+9,y-9,1,2,'#e03a4e');R(g,x+9,y-6,1,2,'#33b24a');break;
  case 'station':shadow(32);B(x-15,y-2,30,10,'#c6b49a');R(g,x-16,y-6,32,4,K);R(g,x-15,y-5,30,2,'#2f5fae');R(g,x-14,y+8,28,4,K);R(g,x-13,y+9,26,2,'#d8364b');for(let k=0;k<4;k++)R(g,x-11+k*7,y+9,4,1,'#bfe6ff');break;
  case 'hospital':shadow(28);B(x-13,y-8,26,18,'#f4f8ff');R(g,x-3,y-5,6,2,'#e03a4e');R(g,x-1,y-7,2,6,'#e03a4e');for(let k=0;k<4;k++)R(g,x-10+k*6,y+2,3,3,'#7fbaf2');break;
  case 'museum':shadow(30);B(x-14,y-2,28,12,'#e8e0d0');for(let k=0;k<5;k++)R(g,x-11+k*5,y,2,9,'#c6c0b0');roof(x,y-9,30,7,'#e8e0d0');pine(x+15,y+10,9);break;
  case 'icerink':{for(let dy=-7;dy<=7;dy++){const hw=Math.round(14*Math.sqrt(1-(dy*dy)/49));R(g,x-hw-1,y+dy,hw*2+2,1,K);R(g,x-hw,y+dy,hw*2,1,dy<-5?'#e8f6ff':'#9fd4f4');}R(g,x-4,y-2,2,4,'#e03a4e');R(g,x+4,y,2,4,'#2f5fae');break;}
  case 'skyline':mTower(g,x-14,y-14,9,24,'#8793a8','#6a7896',3);mTower(g,x-4,y-18,10,28,'#9fb3c8','#7f93a8',5);mTower(g,x+7,y-10,8,20,'#c6b49a','#a8967a',7);break;
  case 'parade':for(const [a,b2,c] of [[-10,-6,'#d8364b'],[0,-10,'#ffc727'],[10,-5,'#3f86d6']]){C(x+a,y+b2,4,c);R(g,x+a,y+b2+5,1,10,K);}R(g,x-15,y+8,30,3,'#2f5fae');break;
  // ---------------- Theme Park
  case 'gates':R(g,x-14,y-8,5,18,K);R(g,x+9,y-8,5,18,K);R(g,x-13,y-7,3,17,'#9b5fd6');R(g,x+10,y-7,3,17,'#9b5fd6');R(g,x-15,y-12,30,5,K);R(g,x-14,y-11,28,3,'#ffc727');for(let k=0;k<6;k++)R(g,x-12+k*5,y-11,2,1,'#e03a4e');break;
  case 'mainst':mShop(g,x-15,y-6,14,'#d8364b',1);mShop(g,x+1,y-6,14,'#3f86d6',2);R(g,x-15,y-10,30,1,'#ffc727');break;
  case 'carousel':mCarousel(g,x,y-4);break;
  case 'games':mStall(g,x-14,y-2,'#d8364b');mStall(g,x+2,y-2,'#2f8a5a');C(x-8,y-8,3,'#ffc727');C(x+8,y-8,3,'#ff4fa3');break;
  case 'bumpers':R(g,x-15,y-8,30,18,K);R(g,x-14,y-7,28,16,'#55607a');for(const [a,b2,c] of [[-9,-3,'#e03a4e'],[2,0,'#ffc727'],[-3,4,'#3f86d6'],[8,-4,'#33b24a']]){R(g,x+a-1,y+b2-1,7,6,K);R(g,x+a,y+b2,5,4,c);}break;
  case 'food':mStall(g,x-14,y-4,'#ffc727');mStall(g,x+2,y-4,'#d8364b');C(x,y+8,3,'#f4f8ff');break;
  case 'ferris':mFerris(g,x,y-3,11);R(g,x-6,y+8,12,3,K);break;
  case 'helter':for(let r=0;r<20;r++){const hw=Math.round(2+r*0.25);R(g,x-hw,y-12+r,hw*2,1,(r>>1)%2?'#d8364b':'#f4f8ff');}R(g,x-1,y-15,2,3,'#ffc727');break;
  case 'haunted':shadow(26);B(x-11,y-6,22,16,'#55607a');roof(x,y-14,24,8,'#2a2a36');R(g,x-6,y-1,3,3,'#ffd23f');R(g,x+3,y-1,3,3,'#ffd23f');R(g,x+12,y-12,1,6,'#f4f8ff');break;
  case 'coaster':{for(let k=0;k<30;k++){const xx=x-15+k,yy=Math.round(y-2-9*Math.sin(k*0.21));R(g,xx,yy,1,2,'#e03a4e');if(k%4===0)R(g,xx,yy+2,1,y+10-yy-2,'#8793a8');}break;}
  case 'flume':R(g,x-15,y-4,30,6,K);R(g,x-14,y-3,28,4,'#7fbaf2');R(g,x+6,y-12,6,10,K);R(g,x+7,y-11,4,8,'#7fbaf2');R(g,x-9,y-6,6,3,'#8a5a34');break;
  case 'drop':R(g,x-2,y-16,5,26,K);R(g,x-1,y-15,3,25,'#c6d0dc');R(g,x-5,y-8,11,4,K);R(g,x-4,y-7,9,2,'#e03a4e');R(g,x-1,y-18,3,3,'#ffd23f');break;
  case 'minigolf':R(g,x-14,y-6,28,14,'#2f8a5a');R(g,x-14,y-6,28,1,MC.snow);C(x+6,y,1,'#2a2a36');pole(x+6,y-10,10);C(x-6,y+3,1,'#f4f8ff');break;
  case 'lake':mPond(g,x,y+1,14,7);mBoat(g,x-6,y-6,12,'#f4f8ff');break;
  case 'openingday':mFerris(g,x-6,y-4,9);R(g,x+4,y-12,3,20,K);R(g,x+5,y-11,1,18,'#c6d0dc');for(let k=0;k<5;k++)R(g,x-15+k*7,y+9,4,2,['#ff4fa3','#ffd23f','#7ad3ff','#9cff7a','#ff7a3a'][k]);break;
  // ---------------- Frozen Harbour
  case 'fishmarket':shadow(30);B(x-14,y-6,28,14,'#dfe5ef');R(g,x-15,y-8,30,3,K);for(let k=0;k<7;k++)R(g,x-14+k*4,y-7,2,1,k%2?'#2f5fae':'#f4f8ff');R(g,x-8,y+1,4,2,'#9aa6ba');R(g,x+2,y+1,4,2,'#e07a8a');break;
  case 'quay':ice(x-15,y+2,30,9);R(g,x-15,y-2,30,4,'#8793a8');for(let k=0;k<4;k++)R(g,x-12+k*8,y-4,3,3,K);mBoat(g,x-10,y-1,14,'#d8364b');break;
  case 'lighthouse':R(g,x-4,y-12,9,22,K);for(let yy=y-11;yy<y+10;yy++)R(g,x-3,yy,7,1,((yy>>2)%2)?'#e03a4e':'#f4f8ff');R(g,x-5,y-17,11,6,K);R(g,x-4,y-16,9,4,'#ffd23f');R(g,x-3,y-19,7,3,K);break;
  case 'containers':for(let k=0;k<4;k++)mContainer(g,x-15+(k%2)*15,y-6+((k>>1)*9),14,['#d8364b','#2f5fae','#33b24a','#ffc727'][k]);break;
  case 'boatyard':R(g,x-12,y+6,2,4,K);R(g,x+10,y+6,2,4,K);mBoat(g,x-14,y-2,28,'#3f86d6');break;
  case 'ferry':ice(x-15,y+5,30,6);R(g,x-15,y-2,30,8,K);R(g,x-14,y-1,28,6,'#f4f8ff');R(g,x-14,y+3,28,2,'#2f5fae');R(g,x-6,y-8,12,6,K);R(g,x-5,y-7,10,4,'#f4f8ff');R(g,x-3,y-11,3,3,'#e03a4e');break;
  case 'drawbridge':ice(x-15,y+3,30,8);R(g,x-15,y-1,12,4,K);R(g,x-14,y,10,2,'#a8673a');for(let k=0;k<9;k++)R(g,x+3+k,y-1-k,2,2,'#a8673a');R(g,x+2,y-12,2,14,K);break;
  case 'icefish':ice(x-15,y-4,30,15);for(const a of [-9,5]){R(g,x+a-1,y-7,10,8,K);R(g,x+a,y-6,8,6,'#a8673a');R(g,x+a,y-6,8,1,MC.snow);}C(x-1,y+6,2,'#2a4a7a');break;
  case 'pier':ice(x-15,y-2,30,13);R(g,x-4,y-12,8,22,K);R(g,x-3,y-11,6,20,'#a8673a');for(let yy=y-10;yy<y+9;yy+=3)R(g,x-3,yy,6,1,'#7a4a2a');break;
  case 'customs':shadow(26);B(x-12,y-6,12,14,'#f4f8ff');R(g,x+2,y+2,14,2,K);for(let k=0;k<4;k++)R(g,x+3+k*3,y+2,2,1,k%2?'#e03a4e':'#f4f8ff');pole(x-12,y-12,6,'#2f5fae');break;
  case 'locks':ice(x-15,y-6,30,16);R(g,x-15,y-1,30,3,K);R(g,x-14,y,28,1,'#8a5a34');R(g,x-15,y+5,30,3,K);R(g,x-14,y+6,28,1,'#8a5a34');break;
  case 'gullisland':ice(x-15,y+2,30,9);mRock(g,x-10,y-4,20,10);for(const [a,b2] of [[-6,-10],[4,-12],[10,-8]]){R(g,x+a,y+b2,3,1,'#f4f8ff');R(g,x+a+1,y+b2+1,1,1,K);}break;
  case 'shipyard':mCrane(g,x+8,y-12);R(g,x-14,y+4,24,6,K);R(g,x-13,y+5,22,4,'#d8364b');break;
  case 'icebreaker':ice(x-15,y+5,30,6);R(g,x-15,y-2,30,8,K);R(g,x-14,y-1,28,6,'#d8364b');R(g,x+10,y-1,4,6,'#f4f8ff');R(g,x-6,y-9,10,7,K);R(g,x-5,y-8,8,5,'#f4f8ff');R(g,x-2,y-12,3,3,K);break;
  case 'festival':mTent(g,x-14,y-8,14,16,'#2f5fae','#f4f8ff');mTent(g,x,y-8,14,16,'#d8364b','#f4f8ff');for(let k=0;k<8;k++)R(g,x-14+k*4,y-11,2,2,['#ffd23f','#ff4fa3','#7ad3ff'][k%3]);break;
  // ---------------- Ski Resort
  case 'skischool':shadow(30);mChalet(g,x-13,y-8,20,18,1);for(let k=0;k<4;k++)R(g,x+9+k*2,y-2,1,10,['#e03a4e','#3f86d6','#ffc727','#33b24a'][k]);break;
  case 'chalets':mChalet(g,x-15,y-6,14,15,2);mChalet(g,x+1,y-9,14,17,3);break;
  case 'lift':R(g,x-15,y+1,30,1,'#2a2a36');R(g,x-15,y-6,30,1,'#2a2a36');R(g,x-1,y-8,3,18,K);R(g,x-5,y-9,11,2,K);for(const a of [-10,8]){R(g,x+a,y+1,1,3,K);R(g,x+a-2,y+4,5,3,'#e03a4e');}break;
  case 'snowguns':R(g,x-8,y-2,3,12,K);R(g,x-11,y-6,9,6,K);R(g,x-10,y-5,7,4,'#ffc727');for(let k=0;k<10;k++)R(g,x-1+k*2,y-8-(k%3),2,2,'#ffffff');break;
  case 'bluerun':R(g,x-9,y-7,16,16,K);R(g,x-8,y-6,14,14,'#2f5fae');pole(x+10,y-6,16,'#2f5fae');break;
  case 'redrun':C(x-1,y,8,'#e03a4e');pole(x+11,y-6,16,'#e03a4e');break;
  case 'moguls':for(let k=0;k<6;k++){const a=-10+(k%3)*10,b2=-4+(k>>1)*4+(k%2)*2;C(x+a,y+b2,3,'#f4f8ff');R(g,x+a-2,y+b2+3,5,1,MC.sh);}break;
  case 'slalom':for(let k=0;k<3;k++){pole(x-12+k*12,y-8+k*5,10,k%2?'#2f5fae':'#e03a4e');}break;
  case 'terrain':R(g,x-14,y+2,14,8,K);for(let r=0;r<8;r++)R(g,x-13,y+3+r,Math.round(12*(r+1)/8),1,'#9fd4f4');R(g,x+2,y,14,2,K);R(g,x+3,y,12,1,'#ffc727');R(g,x+4,y+2,1,5,K);R(g,x+13,y+2,1,5,K);break;
  case 'gondola':R(g,x-16,y-10,32,1,'#2a2a36');R(g,x-1,y-10,1,4,K);R(g,x-5,y-6,10,10,K);R(g,x-4,y-5,8,8,'#e03a4e');R(g,x-3,y-3,6,3,'#bfe6ff');mMountain(g,x+11,y+10,6,10,4);break;
  case 'apres':shadow(30);mChalet(g,x-13,y-8,18,17,4);for(let k=0;k<8;k++)R(g,x-14+k*4,y-11+(k%2),2,2,['#ffd23f','#ff4fa3','#7ad3ff'][k%3]);R(g,x+7,y+2,8,4,'#a8673a');break;
  case 'snowshoe':pine(x-10,y+8,13);pine(x+10,y+6,11);for(let k=0;k<6;k++)R(g,x-4+((k%2)*3),y+8-k*3,2,1,'#8793a8');break;
  case 'blackrun':for(let r=0;r<8;r++){R(g,x-1-r,y-8+r,2*r+3,1,K);R(g,x-1-r,y+6-r,2*r+3,1,K);}mRock(g,x+6,y+2,10,7);break;
  case 'glacier':ice(x-15,y-2,30,12);mMountain(g,x-4,y+2,10,14,6);R(g,x+6,y-6,10,2,K);R(g,x+8,y-4,6,4,'#e03a4e');break;
  case 'grandslalom':R(g,x-14,y-10,3,20,K);R(g,x+11,y-10,3,20,K);R(g,x-14,y-12,28,6,K);for(let k=0;k<7;k++)R(g,x-13+k*4,y-11,2,2,'#f4f8ff');for(let k=0;k<7;k++)R(g,x-11+k*4,y-9,2,2,'#f4f8ff');R(g,x-13,y-11,26,4,'rgba(42,42,54,0.0)');break;
  // ---------------- Mountain Pass
  case 'hairpin':case 'switchbacks':{const n=id==='hairpin'?3:4;for(let k=0;k<n;k++){const yy=y-10+k*(20/(n-1))|0;R(g,x-13,yy,26,3,'#4a5068');R(g,(k%2?x-14:x+11),yy,3,(20/(n-1))|0,'#4a5068');}break;}
  case 'snowshed':R(g,x-15,y-1,30,9,'#4a5068');R(g,x-12,y-6,22,14,K);R(g,x-11,y-5,20,12,'#a9b4c6');R(g,x-11,y-5,20,3,MC.snow);for(let k=0;k<4;k++)R(g,x-11+k*6,y+5,2,3,'#6a7896');break;
  case 'tunnel':mMountain(g,x,y+10,15,20,9);R(g,x-5,y+1,10,9,K);R(g,x-4,y+2,8,8,'#2a2a36');R(g,x-6,y,12,2,'#c6c0b0');break;
  case 'rockfall':mRock(g,x-12,y-2,10,8);mRock(g,x+2,y-8,9,7);mRock(g,x+4,y+3,8,6);R(g,x-15,y-10,1,20,'#2a2a36');for(let yy=y-10;yy<y+10;yy+=2)R(g,x-14,yy,3,1,'#55607a');break;
  case 'mhut':shadow(28);mCabin(g,x-12,y-8,24,18,5);R(g,x+10,y-12,1,8,K);R(g,x+11,y-12,4,3,'#e03a4e');break;
  case 'avalanche':for(let k=0;k<3;k++){R(g,x-14+k*4,y-8+k*7,22,3,K);R(g,x-13+k*4,y-7+k*7,20,1,'#55607a');}break;
  case 'weather':shadow(28);B(x-12,y-2,14,12,'#c6d0dc');C(x+8,y-2,6,'#f4f8ff');R(g,x-8,y-14,1,12,K);R(g,x-11,y-12,7,1,K);break;
  case 'waterfall':mRock(g,x-15,y-10,10,20);mRock(g,x+5,y-10,10,20);R(g,x-5,y-10,10,20,'#bfe6ff');for(let k=0;k<5;k++)R(g,x-4+k*2,y-10,1,14+(k%3)*2,'#e8f6ff');break;
  case 'viewpoint':R(g,x-15,y+4,30,6,'#4a5068');R(g,x-6,y-6,2,10,K);R(g,x-8,y-8,7,3,K);R(g,x-7,y-7,5,1,'#8793a8');R(g,x+4,y,9,2,'#8a5a34');mMountain(g,x+10,y-2,6,10,2);break;
  case 'gorge':mRock(g,x-15,y-4,12,14);mRock(g,x+3,y-4,12,14);R(g,x-4,y-2,8,12,'#2a2a36');R(g,x-15,y-6,30,4,K);R(g,x-14,y-5,28,2,'#a8673a');break;
  case 'icecaves':mMountain(g,x,y+10,15,18,11);g.fillStyle=K;pixCircle(g,x,y+6,6);g.fillStyle='#7ad3ff';pixCircle(g,x,y+6,5);R(g,x-6,y+7,12,4,'#7ad3ff');break;
  case 'cliffroad':mRock(g,x-15,y-12,12,24);R(g,x-3,y-12,9,24,'#4a5068');R(g,x+6,y-12,1,24,K);for(let yy=y-12;yy<y+12;yy+=4)R(g,x+6,yy,2,1,'#c6d0dc');break;
  case 'summit':R(g,x-12,y-8,24,10,K);R(g,x-11,y-7,22,8,'#8a5a34');R(g,x-9,y-5,18,1,'#ffd23f');R(g,x-9,y-2,12,1,'#f4f8ff');R(g,x-8,y+2,2,8,K);R(g,x+6,y+2,2,8,K);break;
  case 'blizzard':for(let k=0;k<12;k++)R(g,x-14+((k*7)%28),y-10+((k*5)%20),3,1,'#ffffff');C(x,y,7,'#f4f8ff');R(g,x-3,y-2,2,2,K);R(g,x+2,y-2,2,2,K);R(g,x-2,y+3,5,1,K);break;
  // ---------------- Frozen North
  case 'huskies':mTent(g,x-14,y-8,14,15,'#f07a1a','#ffc727');R(g,x+2,y+1,4,9,K);R(g,x+12,y+1,1,9,K);R(g,x+3,y+3,9,5,'#8a5a34');for(const a of [4,9])R(g,x+a,y-4,3,3,'#8793a8');break;
  case 'penguins':ice(x-15,y-2,30,12);for(const a of [-9,-3,3]){R(g,x+a,y-7,4,8,K);R(g,x+a+1,y-6,2,6,'#f4f8ff');R(g,x+a+1,y-8,2,2,K);}C(x+10,y-2,5,'#e8f6ff');break;
  case 'igloos':mIgloo(g,x-7,y+1);mIgloo(g,x+8,y-3);break;
  case 'research':shadow(30);B(x-14,y-2,18,11,'#f07a1a');C(x+9,y-1,6,'#f4f8ff');R(g,x-11,y-14,1,12,K);R(g,x-14,y-14,7,1,K);break;
  case 'icefield':for(let k=0;k<3;k++){const yy=y-8+k*7;for(let xx=x-15;xx<x+15;xx+=4)R(g,xx+((k%2)*2),yy-(xx%3),3,3,'#c6e4fa');}pole(x+10,y-8,14,'#e03a4e');break;
  case 'frozenlake':mPond(g,x,y+1,14,8);R(g,x-8,y-6,7,6,K);R(g,x-7,y-5,5,4,'#a8673a');C(x+6,y+3,1,'#2a4a7a');break;
  case 'aurora':for(let xx=x-15;xx<x+15;xx++){const yy=Math.round(y-6+4*Math.sin(xx*0.3));R(g,xx,yy,1,8,'rgba(90,255,170,0.55)');R(g,xx,yy-2,1,2,'rgba(190,120,255,0.55)');}mMountain(g,x,y+10,12,9,13);break;
  case 'snowmen':for(const [a,b2] of [[-10,4],[0,0],[10,5]])mSnowmanTo(g,x+a,y+b2,0);break;
  case 'polartrail':for(let k=0;k<4;k++)pole(x-12+k*8,y-6+(k%2)*6,10,'#e03a4e');for(let k=0;k<12;k++)R(g,x-14+k*2,y+8-(k%3),1,1,'#8793a8');break;
  case 'spires':for(const [a,h] of [[-10,16],[-3,22],[5,14],[11,19]]){for(let r=0;r<h;r++){const hw=Math.round(1+r*0.18);R(g,x+a-hw,y+10-h+r,hw*2,1,r<2?'#ffffff':'#9fd4f4');}}break;
  case 'gardens2':R(g,x-15,y-4,12,10,K);R(g,x-14,y-3,10,8,'#c6e4fa');R(g,x+3,y-4,12,10,K);R(g,x+4,y-3,10,8,'#c6e4fa');C(x,y+6,3,'#9fd4f4');break;
  case 'northpole':R(g,x-2,y-14,5,24,K);for(let yy=y-13;yy<y+10;yy++)R(g,x-1,yy,3,1,((yy>>1)%2)?'#e03a4e':'#f4f8ff');C(x,y-15,3,'#ffd23f');R(g,x+5,y+4,8,6,K);R(g,x+6,y+5,6,4,'#d8364b');break;
  case 'palacegates':for(const a of [-13,8]){R(g,x+a,y-8,5,18,K);R(g,x+a+1,y-7,3,17,'#c6e4fa');}for(let k=0;k<26;k++){const yy=Math.round(y-8-6*Math.sin(Math.PI*k/25));R(g,x-13+k,yy-1,1,3,k%5===2?'#ffffff':'#9fd4f4');}break;
  case 'greathall':shadow(30);B(x-14,y-6,28,16,'#c6e4fa');for(let k=0;k<5;k++)R(g,x-11+k*5,y-3,2,13,'#e8f6ff');roof(x,y-13,30,7,'#9fd4f4');R(g,x-2,y+2,4,8,'#d8364b');break;
  case 'icepalace':{for(const [a,h] of [[-12,18],[-4,24],[4,22],[12,16]]){R(g,x+a-3,y+10-h,6,h,K);R(g,x+a-2,y+11-h,4,h-1,'#c6e4fa');R(g,x+a-1,y+11-h,1,h-1,'#ffffff');for(let r=0;r<4;r++)R(g,x+a-r+1,y+6-h-r+4,2*r,1,'#9b5fd6');}R(g,x-14,y+4,28,6,K);R(g,x-13,y+5,26,4,'#e8f6ff');R(g,x-2,y+5,4,5,'#3a2a6a');break;}
  default:return false;}
  return true;}
"""
rep("const BAND_DECOR={};", "const BAND_DECOR={};"+JS)
# draw them in every band, before the random fill, reserving their spot
rep("  if(BAND_DECOR[opts.decor||id])BAND_DECOR[opts.decor||id](g,put,res,y0,y1);",
    "  if(BAND_DECOR[opts.decor||id])BAND_DECOR[opts.decor||id](g,put,res,y0,y1);\n  for(const L of LEVELS){const lm=LANDMARK[L.id];if(!lm||L.area==='suburbs'||L.area==='secret'||lm[1]<y0||lm[1]>=y1)continue;if(!MAPPOS[L.id]||!L.data)continue;res(lm[0]-17,lm[1]-16,34,30);put(lm[1]+10,G2=>lmArt(G2,L.id,lm[0],lm[1]));}")
open(f,'w',encoding='utf-8').write(s)
s=open(f,encoding='utf-8').read()
rep("ground:(G2,a,b2)=>{for(let k=0;k<6;k++){const x=20+hash(k,77)%140;for(let y=a+10;y<b2-10;y+=2)R(G2,x+Math.round(Math.sin(y*0.04+k)*14),y,2,1,'#dfe8f5');}}",
    "ground:(G2,a,b2)=>{for(let k=0;k<3;k++){const x0=[34,92,148][k];for(let y=a+10;y<b2-10;y++){const xx=x0+Math.round(Math.sin(y*0.012+k*2)*10);R(G2,xx-4,y,9,1,'#e6eef9');if(y%3===0)R(G2,xx-3,y,7,1,'#d6e2f2');R(G2,xx-5,y,1,1,'#c6d4e8');R(G2,xx+5,y,1,1,'#c6d4e8');}}"
    "for(const lx of [62,120]){for(let y=a+14;y<b2-14;y++)R(G2,lx,y,1,1,'#55607a');for(let y=a+30;y<b2-20;y+=70){R(G2,lx-1,y,3,8,K);R(G2,lx-3,y,7,2,K);}for(let y=a+20;y<b2-20;y+=26){R(G2,lx-2,y,5,3,K);R(G2,lx-1,y+1,3,1,(y>>3)%2?'#e03a4e':'#3f86d6');}}}")
open(f,'w',encoding='utf-8').write(s)
s=open(f,encoding='utf-8').read()
# remember which landmarks the bands drew; draw the rest (the Frozen North above its strip) on top at the end
rep("put(lm[1]+10,G2=>lmArt(G2,L.id,lm[0],lm[1]));}","put(lm[1]+10,G2=>lmArt(G2,L.id,lm[0],lm[1]));LM_DONE.add(L.id);}")
rep("const BAND_DECOR={};","const BAND_DECOR={};const LM_DONE=new Set();")
rep("   if(typeof genNewBands==='function')genNewBands(nbg,nog);}","   if(typeof genNewBands==='function')genNewBands(nbg,nog);\n    for(const L of LEVELS){const lm=LANDMARK[L.id];if(!lm||LM_DONE.has(L.id)||!L.data||L.area==='suburbs'||L.area==='secret')continue;nog.clearRect(lm[0]-16,lm[1]-17,32,30);lmArt(nog,L.id,lm[0],lm[1]);LM_DONE.add(L.id);}}")
open(f,'w',encoding='utf-8').write(s)
