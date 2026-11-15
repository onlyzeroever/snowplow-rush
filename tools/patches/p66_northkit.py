import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# Frozen North detail: expedition tents, dog sleds, icebergs, gift piles, decorated trees, the striped pole, Santa's
# sleigh, reindeer, ice columns; overhead: aurora curtains, ice arches, chandeliers.
KIT=r"""
function tentSprite(a){const c=mk(30,24),g=c.getContext('2d'),col=['#f07a1a','#e03a4e','#ffc727'][a%3],dk=['#a8501a','#a02236','#c8961a'][a%3];
  for(let y=2;y<24;y++){const hw=Math.max(1,Math.round(14*Math.sqrt(Math.max(0,1-((23-y)/21)**2))));R(g,15-hw-1,y,hw*2+2,1,K);}
  for(let y=3;y<23;y++){const hw=Math.max(0,Math.round(14*Math.sqrt(Math.max(0,1-((23-y)/21)**2)))-1);R(g,15-hw,y,hw*2,1,col);R(g,15-hw,y,Math.max(1,hw>>1),1,dk);}
  R(g,14,3,2,20,dk);for(let y=14;y<23;y++){const hw=Math.round((y-14)*0.6);R(g,15-hw,y,hw*2+1,1,'#2a2a36');}R(g,0,22,2,2,K);R(g,28,22,2,2,K);return c;}
function dogSledSprite(){const c=mk(16,30),g=c.getContext('2d');R(g,2,0,2,30,K);R(g,12,0,2,30,K);R(g,2,0,12,2,K);R(g,3,6,10,18,K);R(g,4,7,8,16,'#8a5a34');for(let y=9;y<22;y+=3)R(g,4,y,8,1,'#6b4a2c');
  R(g,5,9,6,7,K);R(g,6,10,4,5,'#e03a4e');R(g,1,26,14,2,K);R(g,2,26,12,1,'#c6d0dc');return c;}
function icebergSprite(a){const c=mk(44,34),g=c.getContext('2d');const B=[[14,18,13],[28,16,14],[22,10,10],[34,22,9],[10,24,8]];g.fillStyle=K;for(const [x,y,r] of B)pixCircle(g,x,y,r+1);
  g.fillStyle='#b8daf5';for(const [x,y,r] of B)pixCircle(g,x,y,r);g.fillStyle='#e8f4ff';for(const [x,y,r] of B)pixCircle(g,x-2,y-3,Math.max(2,r-3));g.fillStyle='#ffffff';pixCircle(g,20,8,4);R(g,6,30,32,2,'#7ab0dc');return c;}
function giftsSprite(a){const c=mk(26,20),g=c.getContext('2d');const B=[[0,8,12,12,'#e03a4e','#ffd23f'],[12,10,14,10,'#2f8a5a','#f4f8ff'],[5,0,12,9,'#3f86d6','#ffd23f']];
  for(const [x,y,w,h,col,rb] of B){R(g,x,y,w,h,K);R(g,x+1,y+1,w-2,h-2,col);R(g,x+(w>>1),y+1,2,h-2,rb);R(g,x+1,y+(h>>1),w-2,2,rb);R(g,x+(w>>1)-2,y-1,6,2,rb);}return c;}
function xmasTreeSprite(){const c=mk(32,48),g=c.getContext('2d');R(g,13,38,6,8,K);R(g,14,38,4,8,'#6b4a2c');
  for(let t=0;t<3;t++){const y0=4+t*11,hh=16;for(let y=0;y<hh;y++){const hw=Math.round(2+y*(0.75+t*0.12));R(g,16-hw-1,y0+y,hw*2+2,1,K);}for(let y=1;y<hh-1;y++){const hw=Math.round(2+y*(0.75+t*0.12))-1;R(g,16-hw,y0+y,hw*2,1,y%3?'#2f8a5a':'#1f6a44');}}
  for(let k=0;k<16;k++){const y=8+k*2+((k*7)%3),hw=Math.round(2+((y-4)%11)*0.8),x=16+Math.round(Math.sin(k*1.7)*Math.max(1,hw-1));R(g,x,y,1,1,'#fff3a0');}
  R(g,12,46,8,2,'#55607a');return c;}
function polePostSprite(){const c=mk(14,56),g=c.getContext('2d');R(g,3,10,8,46,K);for(let y=11;y<56;y++)R(g,4,y,6,1,((y>>2)%2)?'#e03a4e':'#f4f8ff');g.fillStyle=K;pixCircle(g,7,6,6);g.fillStyle='#ffd23f';pixCircle(g,7,6,5);R(g,5,3,2,2,'#fff3a0');R(g,0,52,14,4,K);R(g,1,53,12,2,'#c6d0dc');return c;}
function sleighSprite(){const c=mk(42,36),g=c.getContext('2d');R(g,2,4,2,32,K);R(g,38,4,2,32,K);R(g,2,2,38,3,K);R(g,4,2,34,1,'#ffd23f');
  R(g,5,8,32,24,K);R(g,6,9,30,22,'#e03a4e');R(g,6,9,30,2,'#ffd23f');R(g,6,29,30,2,'#ffd23f');R(g,8,12,26,8,'#a02236');R(g,10,20,22,8,'#8a5a34');
  R(g,9,13,24,6,'#3f86d6');for(let x=10;x<33;x+=4)R(g,x,13,2,6,'#7fbaf2');R(g,9,21,24,6,'#2f8a5a');return c;}
function reindeerSprite(a){const c=mk(20,24),g=c.getContext('2d');R(g,3,10,14,9,K);R(g,4,11,12,7,'#8a5a34');R(g,4,11,12,2,'#a8673a');R(g,4,18,2,6,K);R(g,14,18,2,6,K);R(g,7,18,2,5,K);R(g,11,18,2,5,K);
  R(g,13,4,6,8,K);R(g,14,5,4,6,'#8a5a34');R(g,18,8,2,2,a?'#e03a4e':'#2a2a36');R(g,14,0,1,5,'#6b4a2c');R(g,17,0,1,5,'#6b4a2c');R(g,12,1,3,1,'#6b4a2c');R(g,17,1,3,1,'#6b4a2c');R(g,15,6,1,1,K);R(g,4,13,2,2,'#f4f8ff');return c;}
function iceColSprite(){const c=mk(14,36),g=c.getContext('2d');R(g,0,0,14,6,K);R(g,1,1,12,4,'#e8f4ff');R(g,2,6,10,24,K);R(g,3,6,8,24,'#b8daf5');R(g,4,6,2,24,'#e8f4ff');R(g,9,6,1,24,'#7ab0dc');R(g,0,30,14,6,K);R(g,1,31,12,4,'#c6d9f3');return c;}
function auroraOverSprite(w){const c=mk(w,96),g=c.getContext('2d');for(let x=0;x<w;x++){const y0=Math.round(30+14*Math.sin(x*0.045)+6*Math.sin(x*0.13)),L=40+Math.round(16*Math.sin(x*0.07+1));
  for(let y=0;y<L;y++){const t=y/L,a=(0.10+0.22*(1-t))*(0.6+0.4*Math.sin(x*0.5)**2);g.fillStyle=t<0.25?'rgba(190,120,255,'+a.toFixed(3)+')':'rgba(90,255,170,'+a.toFixed(3)+')';g.fillRect(x,y0+y,1,1);}}c.noFrost=true;return c;}
function iceArchOverSprite(w){const c=mk(w,44),g=c.getContext('2d');for(const x of [0,w-14]){R(g,x,6,14,38,K);R(g,x+1,7,12,36,'#b8daf5');R(g,x+2,7,3,36,'#e8f4ff');}
  for(let x=0;x<w;x++){const t=x/(w-1),yy=Math.round(14-12*Math.sin(Math.PI*t));R(g,x,yy-1,1,12,K);R(g,x,yy,1,10,'#c6e4fa');R(g,x,yy,1,2,'#ffffff');if(x%7===3)R(g,x,yy+10,1,3+(x%3),'#e8f4ff');}
  c.noFrost=true;return c;}
function chandelierOverSprite(){const c=mk(44,34),g=c.getContext('2d');R(g,21,0,2,10,'#55607a');g.fillStyle=K;pixCircle(g,22,20,13);g.fillStyle='#ffd23f';pixCircle(g,22,20,12);g.fillStyle='rgba(0,0,0,0)';g.clearRect(13,14,19,12);
  R(g,13,14,18,12,'rgba(0,0,0,0)');for(let k=0;k<8;k++){const a=k*Math.PI/4,x=Math.round(22+12*Math.cos(a)),y=Math.round(20+12*Math.sin(a));R(g,x-1,y-5,3,5,'#f4f8ff');R(g,x,y-8,1,3,'#ffd23f');R(g,x-1,y,3,3,'#7ad3ff');}c.noFrost=true;return c;}
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){", KIT+"\nfunction buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("  iceblock:{arg:14,","  tent:{arg:0,min:0,max:2,make:a=>tentSprite(a),foot:()=>[1,8,28,15]},\n  dogsled:{make:()=>scnSpr('dsl',dogSledSprite),foot:()=>[2,4,12,24]},\n  iceberg:{make:()=>scnSpr('ibg',icebergSprite),foot:()=>[2,8,40,24]},\n  gifts:{make:()=>scnSpr('gft',giftsSprite),foot:()=>[0,6,26,14]},\n  xmastree:{make:()=>scnSpr('xmt',xmasTreeSprite),foot:()=>[6,36,20,12]},\n  polepost:{make:()=>scnSpr('ppo',polePostSprite),foot:()=>[2,48,10,8]},\n  sleigh:{make:()=>scnSpr('slg',sleighSprite),foot:()=>[2,4,38,32]},\n  reindeer:{arg:0,min:0,max:1,make:a=>reindeerSprite(a),foot:()=>[3,12,14,10]},\n  icecol:{make:()=>scnSpr('icl',iceColSprite),foot:()=>[0,26,14,10]},\n  iceblock:{arg:14,")
rep("const OVERS={shed:","const OVERS={aurora:a=>auroraOverSprite(a||180),icearch:a=>iceArchOverSprite(a||120),chandelier:()=>chandelierOverSprite(),shed:")
open(f,'w',encoding='utf-8').write(s)
