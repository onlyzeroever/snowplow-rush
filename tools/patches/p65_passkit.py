import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# Mountain Pass detail: snow-shed galleries and tunnels (overhead), rockfall nets, avalanche fences, hairpin chevrons,
# the pass summit sign, solar panels and a radar dome.
KIT=r"""
function shedOverSprite(w,h){const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,'#a9b4c6');for(let y=8;y<h-4;y+=16){R(g,1,y,w-2,3,'#8793a8');R(g,1,y,w-2,1,'#c6d0dc');}
  for(let y=4;y<h-4;y+=32){R(g,0,y,5,10,K);R(g,1,y+1,3,8,'#6a7896');R(g,w-5,y,5,10,K);R(g,w-4,y+1,3,8,'#6a7896');}
  g.fillStyle=PAL.W;for(let y=0;y<h;y+=3){const a=Math.round(5+3*Math.sin(y*0.21)),b=Math.round(w*0.5+6*Math.sin(y*0.13));R(g,a,y,b-a,3,'#f4f8ff');}R(g,1,1,w-2,2,'#f4f8ff');R(g,1,h-3,w-2,2,'#55607a');return c;}
function tunnelOverSprite(w,h){const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,'#55607a');let sd=w*7+h;const rn=()=>{sd=(sd*16807)%2147483647;return sd/2147483647;};
  for(let k=0;k<w*h/60;k++){const x=rn()*w|0,y=rn()*h|0,r=2+rn()*5|0;R(g,x,y,r*2,r,['#6a7896','#4a5468','#8793a8'][k%3]);}
  for(let k=0;k<w*h/90;k++){const x=rn()*w|0,y=rn()*h|0;R(g,x,y,6+rn()*10|0,2,'#f4f8ff');}
  for(const y0 of [0,h-12]){R(g,0,y0,w,12,K);R(g,1,y0+1,w-2,10,'#c6c0b0');for(let x=4;x<w-4;x+=8)R(g,x,y0+3,6,1,'#9a948a');R(g,1,y0+1,w-2,2,PAL.W);}
  return c;}
function rockNetSprite(h){const c=mk(8,h),g=c.getContext('2d');for(let y=0;y<h;y+=28){R(g,2,y,4,6,K);R(g,3,y,2,6,'#55607a');}R(g,1,0,6,h,'rgba(42,42,54,0.0)');for(let y=0;y<h;y+=3){R(g,1+((y/3)%2)*3,y,3,1,'#2a2a36');}R(g,0,0,1,h,'#2a2a36');R(g,7,0,1,h,'#2a2a36');return c;}
function avFenceSprite(w){const c=mk(w,10),g=c.getContext('2d');R(g,0,3,w,6,K);R(g,0,4,w,4,'#55607a');for(let x=1;x<w;x+=3)R(g,x,4,1,4,'#8793a8');for(let x=0;x<w;x+=20){R(g,x,0,3,10,K);R(g,x+1,1,1,8,'#2a2a36');}R(g,0,3,w,1,PAL.W);return c;}
function chevronSprite(a){const c=mk(18,20),g=c.getContext('2d');R(g,7,12,3,8,K);R(g,8,12,1,8,'#55607a');R(g,0,0,18,12,K);R(g,1,1,16,10,'#e03a4e');for(let k=0;k<3;k++){const x=a?3+k*5:13-k*5;for(let i=0;i<4;i++){R(g,a?x+i:x-i,2+i,2,1,'#f4f8ff');R(g,a?x+i:x-i,9-i,2,1,'#f4f8ff');}}R(g,1,1,16,1,PAL.W);return c;}
function passSignSprite(){const c=mk(76,40),g=c.getContext('2d');R(g,8,24,4,16,K);R(g,64,24,4,16,K);R(g,0,0,76,28,K);R(g,1,1,74,26,'#6b4a2c');R(g,3,3,70,22,'#8a5a34');R(g,1,1,74,2,PAL.W);
  sprText(g,'SUMMIT',38-sprTextW('SUMMIT')/2|0,5,'#ffd23f');sprText(g,'2486 M',38-sprTextW('2486 M')/2|0,15,'#f4f8ff');return c;}
function solarSprite(){const c=mk(30,16),g=c.getContext('2d');R(g,0,0,30,12,K);R(g,1,1,28,10,'#2f5fae');for(let x=1;x<29;x+=7)R(g,x,1,1,10,'#7ad3ff');R(g,1,6,28,1,'#7ad3ff');R(g,1,1,28,1,PAL.W);R(g,6,12,2,4,K);R(g,22,12,2,4,K);return c;}
function radarSprite(){const c=mk(36,40),g=c.getContext('2d');R(g,6,26,24,14,K);R(g,7,27,22,12,'#8793a8');g.fillStyle=K;pixCircle(g,18,17,15);g.fillStyle='#f4f8ff';pixCircle(g,18,17,14);g.fillStyle='#d8e4f4';for(let y=6;y<30;y+=5)R(g,5,y,26,1,'#c6d0dc');R(g,16,1,4,4,'#e03a4e');return c;}
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){", KIT+"\nfunction buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("  iceblock:{arg:14,","  rocknet:{arg:120,min:20,max:600,make:a=>rockNetSprite(a),foot:a=>[0,0,8,a]},\n  avfence:{arg:60,min:20,max:180,make:a=>avFenceSprite(a),foot:a=>[0,3,a,6]},\n  chevron:{arg:0,min:0,max:1,make:a=>chevronSprite(a),foot:()=>[6,16,6,4]},\n  passsign:{make:()=>scnSpr('psg',passSignSprite),foot:()=>[6,30,64,10]},\n  solar:{make:()=>scnSpr('sol',solarSprite),foot:()=>[0,2,30,12]},\n  radar:{make:()=>scnSpr('rad',radarSprite),foot:()=>[4,24,28,16]},\n  iceblock:{arg:14,")
rep("const OVERS={gondola:","const OVERS={shed:(a,b)=>shedOverSprite(a||80,b||200),tunnel:(a,b)=>tunnelOverSprite(a||120,b||300),gondola:")
open(f,'w',encoding='utf-8').write(s)
