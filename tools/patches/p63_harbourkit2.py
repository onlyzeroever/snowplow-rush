import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# Harbour detail: mooring bollards, buoys, lobster pots, net piles, life-ring posts, pallets, fish boxes, a tug.
KIT=r"""
function mooringSprite(){const c=mk(8,9),g=c.getContext('2d');R(g,0,3,8,6,K);R(g,1,4,6,4,'#2a2a36');R(g,1,1,6,4,K);R(g,2,2,4,2,'#55607a');R(g,2,1,4,1,PAL.W);return c;}
function buoySprite(a){const c=mk(12,14),g=c.getContext('2d'),col=['#e03a4e','#ffc727','#33b24a'][a%3];g.fillStyle=K;pixCircle(g,6,8,5);g.fillStyle=col;pixCircle(g,6,8,4);R(g,2,7,8,2,'#f4f8ff');R(g,5,0,2,5,K);R(g,4,0,4,2,col);return c;}
function potsSprite(){const c=mk(20,16),g=c.getContext('2d');for(const [x,y] of [[0,6],[10,6],[5,0]]){R(g,x,y,10,10,K);R(g,x+1,y+1,8,8,'#8a5a34');for(let i=x+2;i<x+9;i+=2)R(g,i,y+1,1,8,'#c98d4a');R(g,x+1,y+1,8,1,PAL.W);}return c;}
function netsSprite(){const c=mk(22,12),g=c.getContext('2d');R(g,1,2,20,10,K);R(g,2,3,18,8,'#2f8a6a');for(let x=3;x<20;x+=3)for(let y=4;y<11;y+=3)R(g,x,y,1,1,'#145146');R(g,4,1,6,3,'#e03a4e');R(g,12,2,5,2,'#ffc727');R(g,2,3,18,1,PAL.W);return c;}
function lifeRingSprite(){const c=mk(12,22),g=c.getContext('2d');R(g,5,8,2,14,K);R(g,0,0,12,12,K);g.fillStyle='#f07a1a';pixCircle(g,6,6,5);g.fillStyle=K;pixCircle(g,6,6,2);R(g,1,5,2,2,'#f4f8ff');R(g,9,5,2,2,'#f4f8ff');return c;}
function palletSprite(){const c=mk(20,14),g=c.getContext('2d');R(g,0,4,20,10,K);R(g,1,5,18,8,'#c98d4a');for(let x=1;x<19;x+=4)R(g,x,5,3,8,'#a8673a');R(g,2,0,16,6,K);R(g,3,1,14,4,'#c6d0dc');R(g,3,1,14,1,PAL.W);return c;}
function fishboxSprite(){const c=mk(14,10),g=c.getContext('2d');R(g,0,0,14,10,K);R(g,1,1,12,8,'#3f86d6');R(g,2,2,10,4,'#c6d9f3');R(g,3,3,3,2,'#8793a8');R(g,7,3,4,2,'#9aa6ba');return c;}
function warehouseSprite(w,h,a){const c=mk(w,h),g=c.getContext('2d'),wall=['#a8574a','#8793a8','#6b7fa8','#c98d4a'][a%4],dk=['#7a3a30','#6a7896','#4f5f8a','#a8673a'][a%4];R(g,0,2,w,h-2,K);R(g,1,3,w-2,h-4,wall);for(let y=6;y<h-2;y+=4)for(let x=1+((y/4)%2)*3;x<w-1;x+=7)R(g,x,y,5,1,dk);
  snowCap(g,0,0,w,4,w*7+a);icicles(g,1,8,w-2,w+a,3);const dw=Math.min(30,w-16),dx=(w-dw)>>1;R(g,dx,h-30,dw,30,K);R(g,dx+1,h-29,dw-2,29,'#9aa6ba');for(let y=h-27;y<h;y+=3)R(g,dx+1,y,dw-2,1,'#6a7896');R(g,dx,h-31,dw,2,PAL.W);
  for(const x of [3,w-11])if(dx>12){R(g,x,14,8,7,K);R(g,x+1,15,6,5,'#ffd77a');ledge(g,x-1,21,10);}const nm=['WAREHOUSE','BOAT SHED','STORE','DEPOT'][a%4];R(g,dx-2,h-42,dw+4,9,K);R(g,dx-1,h-41,dw+2,7,'#13306b');fitText(g,nm,w>>1,h-40,dw,'#ffd23f',null);drift(g,0,h-1,5,4);drift(g,w-11,h-1,5,4);return c;}
function tugSprite(){const c=mk(30,56),g=c.getContext('2d');for(let y=0;y<56;y++){const hw=Math.round(14*Math.min(1,(y+6)/22));R(g,15-hw,y,hw*2,1,K);if(y>0)R(g,16-hw,y,hw*2-2,1,y<44?'#e03a4e':'#2a2a36');}R(g,6,18,18,20,K);R(g,7,19,16,18,'#f4f8ff');R(g,9,21,12,5,'#8fd3ff');R(g,12,8,6,8,K);R(g,13,9,4,6,'#ffc727');R(g,2,40,26,4,'#2a2a36');for(let y=6;y<50;y+=10){R(g,0,y,2,4,'#2a2a36');R(g,28,y,2,4,'#2a2a36');}return c;}
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){", KIT+"\nfunction buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("  iceblock:{arg:14,","  mooring:{make:()=>scnSpr('mo',mooringSprite),foot:()=>[0,3,8,6]},\n  buoy:{arg:0,min:0,max:2,make:a=>buoySprite(a),foot:()=>[1,4,10,9]},\n  pots:{make:()=>scnSpr('pt',potsSprite),foot:()=>[0,6,20,10]},\n  nets:{junk:true,make:()=>scnSpr('nt',netsSprite),foot:()=>[1,2,20,10]},\n  lifering:{make:()=>scnSpr('lr',lifeRingSprite),foot:()=>[3,18,6,4]},\n  pallet:{make:()=>scnSpr('pl2',palletSprite),foot:()=>[0,4,20,10]},\n  fishbox:{junk:true,make:()=>scnSpr('fb',fishboxSprite),foot:()=>[0,0,14,10]},\n  warehouse:{arg:0,min:0,max:3,make:a=>warehouseSprite(56,72,a),foot:()=>[0,0,56,72]},\n  tug:{make:()=>scnSpr('tg',tugSprite),foot:()=>[1,2,28,52]},\n  iceblock:{arg:14,")
open(f,'w',encoding='utf-8').write(s)
