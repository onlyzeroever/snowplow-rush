// Concept sprites for new machines (design sheet only; not in the game yet). Same conventions as drawSuper/drawRotary:
// faces up, (ox,oy) = centre, K outlines, c.b/c.l/c.d body shades, the kid's hat shows in the windscreen.
const tyreV=(g,tx,ty,w,h,fr)=>{R(g,tx,ty,w,h,K);R(g,tx+1,ty+1,w-2,h-2,'#2a2a36');for(let i=0;i<Math.floor(h/3);i++){const yy=ty+1+((i*3+fr)%(h-2));R(g,tx+1,yy,w-2,1,'#3c3f52');R(g,tx,yy,1,1,K);R(g,tx+w-1,yy,1,1,K);}R(g,tx+1,ty+1,w-2,1,'#55586a');};
const trackV=(g,tx,ty,w,h,fr,cleat)=>{R(g,tx,ty,w,h,K);R(g,tx+1,ty+1,w-2,h-2,'#343a4c');for(let i=0;i<Math.floor(h/4)+1;i++){const yy=ty+1+((i*4+(fr%4))%(h-2));R(g,tx+1,yy,w-2,2,cleat||'#5f6880');}R(g,tx+1,ty+1,w-2,1,'#8793a8');};
const puff=(g,px,py,fr,n,dx)=>{for(let i=0;i<n;i++){const k=(i+fr)%n,yy=py-k*3,xx=px+Math.round(k*(dx||0.6));R(g,xx-1,yy-1,4,3,'rgba(214,222,236,'+(0.9-k*0.18).toFixed(2)+')');}};
const hazard=(g,x,y,w,h,ph)=>{R(g,x,y,w,h,'#ffc727');for(let i=-h;i<w;i+=4)for(let d=0;d<h;d++){const xx=x+i+d+(ph||0);if(xx>=x&&xx<x+w&&((i/4)|0)%1===0)R(g,xx,y+d,1,1,'#2a2a36');if(xx+1>=x&&xx+1<x+w)R(g,xx+1,y+d,1,1,'#2a2a36');}};

// ---- WHEEL LOADER: articulated loader; yellow bucket on lift arms, 4 tall tyres, hinge in the middle, cab, striped counterweight
function drawLoader(g,ox,oy,fr,c){const x=ox-13,y=oy-22,on=fr%2===0;
  // lift arms (body colour) from the bucket back to the front frame
  for(const ax of [x+3,x+20]){R(g,ax,y-3,4,13,K);R(g,ax+1,y-2,2,11,c.b);R(g,ax+1,y-2,1,11,c.l);}
  R(g,x+3,y+3,20,3,K);R(g,x+4,y+4,18,1,c.d);
  tyreV(g,x-4,y+3,8,14,fr);tyreV(g,x+22,y+3,8,14,fr);
  // front frame
  R(g,x+5,y+6,16,12,K);R(g,x+6,y+7,14,10,c.b);R(g,x+6,y+7,14,1,c.l);R(g,x+18,y+8,2,8,c.d);
  R(g,x+6,y+8,3,2,'#ffef7a');R(g,x+17,y+8,3,2,'#ffef7a');R(g,x+11,y+6,4,9,K);R(g,x+12,y+7,2,7,'#55607a');R(g,x+12,y+7,1,7,'#9aa6ba');
  // hinge: a narrow neck with a pivot pin and a striped guard
  R(g,x+8,y+17,10,6,K);R(g,x+9,y+18,8,4,'#2a2a36');R(g,x+9,y+19,8,2,'#ffc727');for(let i=0;i<4;i++)R(g,x+9+i*2,y+19,1,2,'#2a2a36');R(g,x+12,y+17,2,6,'#c6d0dc');
  tyreV(g,x-4,y+29,8,14,fr);tyreV(g,x+22,y+29,8,14,fr);
  // rear frame with the cab (black safety frame round the glass)
  R(g,x+3,y+22,20,21,K);R(g,x+4,y+23,18,19,c.b);R(g,x+4,y+23,18,1,c.l);R(g,x+4,y+23,1,19,c.l);R(g,x+20,y+24,1,17,c.d);
  R(g,x+5,y+23,16,12,K);R(g,x+6,y+24,14,4,'#8fd3ff');R(g,x+7,y+24,3,2,'#d8f2ff');R(g,x+12,y+25,3,2,curHat().c);R(g,x+6,y+29,14,5,'#3a3f52');R(g,x+6,y+29,14,1,'#55607a');
  R(g,x+12,y+30,2,2,on?'#ffb43a':'#c45a10');if(on){R(g,x+11,y+30,1,1,'#ffe0a0');R(g,x+14,y+31,1,1,'#ffe0a0');}
  // engine hood with louvres, exhaust stack
  R(g,x+6,y+36,14,6,K);R(g,x+7,y+37,12,4,c.d);for(let i=0;i<4;i++)R(g,x+8+i*3,y+37,1,4,'#2a2a36');
  R(g,x+17,y+33,4,4,K);R(g,x+18,y+34,2,2,'#1b1f3b');if(!on)puff(g,x+19,y+31,fr,3,0.8);
  // counterweight
  R(g,x+2,y+42,22,5,K);for(let i=0;i<20;i++)R(g,x+3+i,y+43,1,3,((i>>1)%2)?'#2a2a36':'#ffc727');}
function bladeLoader(g,cx,y,bw,bt,c){const x=cx-Math.floor(bw/2);// bucket: yellow back wall, steel floor, cutting edge with teeth
  R(g,x,y,bw,bt,K);R(g,x+1,y+1,bw-2,bt-2,c.b);R(g,x+1,y+bt-3,bw-2,1,c.d);R(g,x+3,y+2,bw-6,bt-5,'#8793a8');R(g,x+3,y+2,bw-6,1,'#c6d0dc');R(g,x+3,y+bt-4,bw-6,1,'#55607a');
  for(let i=x+3;i<=x+bw-5;i+=5){R(g,i,y-2,3,3,K);R(g,i+1,y-1,1,2,'#e8eef8');}R(g,x+1,y+1,1,bt-2,c.l);}

// ---- GLACIER TITAN: a black-and-hazard mining crawler; a hot cutter drum that glows and steams, headlight eyes,
//      a raised cab tower, a conveyor carrying snow back to a rear chute, a glowing core
function drawTitan(g,ox,oy,fr,c){const x=ox-15,y=oy-24,on=fr%2===0;
  for(const ax of [x+2,x+24]){R(g,ax,y-3,5,9,K);R(g,ax+1,y-2,3,7,'#3a3f52');R(g,ax+1,y-2,3,1,'#6a7088');}
  trackV(g,x-3,y+3,10,44,fr,'#5a6078');trackV(g,x+23,y+3,10,44,fr,'#5a6078');
  R(g,x+4,y+1,22,46,K);R(g,x+5,y+2,20,44,c.b);R(g,x+5,y+2,20,1,c.l);R(g,x+5,y+2,1,44,c.l);R(g,x+23,y+3,2,42,c.d);
  for(let i=0;i<20;i++)R(g,x+5+i,y+2,1,2,((i>>1)%2)?'#2a2a36':'#ffc727');
  // headlight eyes
  for(const ex of [x+6,x+19]){R(g,ex,y+5,5,4,K);R(g,ex+1,y+6,3,2,on?'#fff3b0':'#ffd23f');R(g,ex+1,y+6,1,1,'#ffffff');}
  // raised cab tower with a ladder
  R(g,x+8,y+10,14,11,K);R(g,x+9,y+11,12,4,'#ff9a3a');R(g,x+10,y+11,3,1,'#ffd9a8');R(g,x+15,y+12,3,2,curHat().c);R(g,x+9,y+16,12,4,c.d);R(g,x+9,y+16,12,1,c.l);
  R(g,x+13,y+17,4,2,K);R(g,x+14,y+17,2,1,on?'#ff4a1a':'#8a2a10');for(let i=0;i<3;i++)R(g,x+6,y+12+i*3,2,1,'#9aa6ba');R(g,x+6,y+11,1,9,'#6a7088');
  // conveyor carrying snow back
  R(g,x+10,y+21,10,15,K);R(g,x+11,y+22,8,13,'#1b1f3b');for(let i=0;i<4;i++)R(g,x+11,y+22+((i*4+fr*2)%13),8,1,'#3a3f52');
  for(let i=0;i<3;i++){const yy=y+22+((i*5+fr*2)%12);R(g,x+12+(i%2)*3,yy,3,2,'#ffffff');R(g,x+12+(i%2)*3,yy+1,3,1,'#c6d9f3');}
  // side vents with a hot glow, twin stacks
  for(const vx of [x+6,x+21]){for(let i=0;i<3;i++){R(g,vx,y+22+i*4,3,3,K);R(g,vx+1,y+23+i*4,1,1,(fr+i)%3===0?'#ffe0a0':'#ff7a1a');}}
  for(const sx of [x+6,x+20]){R(g,sx,y+35,4,4,K);R(g,sx+1,y+36,2,2,'#1b1f3b');R(g,sx+1,y+36,2,1,on?'#ff8a3a':'#c45a10');}puff(g,x+7,y+33,fr,3,-0.8);puff(g,x+21,y+33,fr+1,3,0.8);
  // glowing core and the rear chute throwing snow out to the side
  R(g,x+11,y+37,8,8,K);R(g,x+12,y+38,6,6,'#2a1a10');const pulse=fr%4<2;R(g,x+14,y+40,2,2,pulse?'#fff3b0':'#ff7a1a');R(g,x+13,y+39,4,4,pulse?'rgba(255,140,40,0.55)':'rgba(255,90,20,0.35)');R(g,x+14,y+40,2,2,pulse?'#ffffff':'#ffb43a');
  R(g,x+22,y+43,4,5,K);R(g,x+23,y+44,2,3,'#ffc727');for(let i=0;i<4;i++){const k=(i+fr)%4;R(g,x+26+k*3,y+46+k,3,2,'#ffffff');}}
function bladeTitan(g,cx,y,bw,bt,c,fr){const x=cx-Math.floor(bw/2);// hot cutter drum: dark steel with glowing teeth, steam off the ends
  R(g,x,y,bw,bt,K);R(g,x+1,y+1,bw-2,bt-2,'#2a2a36');R(g,x+1,y+1,bw-2,1,'#55607a');R(g,x+1,y+bt-2,bw-2,1,'#1b1f3b');
  const ph=(fr||0)%2*3;for(let i=x+2+ph;i<x+bw-3;i+=6){R(g,i,y-2,3,3,K);R(g,i+1,y-1,1,1,'#ffe0a0');R(g,i,y+2,3,bt-4,'#ff7a1a');R(g,i+1,y+2,1,bt-4,'#ffc06a');R(g,i+3,y+3,2,bt-6,'#a83a10');}
  for(const ex of [x-3,x+bw-2]){R(g,ex,y-2,5,bt+4,K);R(g,ex+1,y-1,3,bt+2,'#ffc727');for(let k=0;k<4;k++)R(g,ex+1,y+k*3,3,1,'#2a2a36');}
  if((fr||0)%2){R(g,x-5,y-3,3,2,'rgba(230,236,246,0.8)');R(g,x+bw+2,y-3,3,2,'rgba(230,236,246,0.8)');}}

// ---- ICEBREAKER: a red ice-ship on tracks; a long pointed bow throws a bow wave, white bridge, funnel, stern helipad
function drawIcebreaker(g,ox,oy,fr,c){const x=ox-14,y=oy-24,on=fr%2===0;
  trackV(g,x-2,y+18,5,28,fr);trackV(g,x+25,y+18,5,28,fr);
  const hw=r=>r<20?Math.max(1,Math.round(14*Math.sqrt(r/20))):r>44?14-(r-44):14;
  for(let r=0;r<48;r++){const w=hw(r);R(g,ox-w-1,y+r,w*2+2,1,K);}
  for(let r=1;r<47;r++){const w=hw(r)-1;if(w<0)continue;R(g,ox-w-1,y+r,w*2+2,1,c.b);R(g,ox-w-1,y+r,1,1,'#5a1018');R(g,ox+w,y+r,1,1,'#5a1018');if(w>1){R(g,ox-w,y+r,1,1,c.l);R(g,ox+w-1,y+r,1,1,c.d);}}
  // fore deck: grey deck plate, anchor winch, chain
  for(let r=8;r<46;r++){const w=hw(r)-3;if(w>0)R(g,ox-w-1,y+r,w*2+2,1,'#9aa6ba');}for(let r=10;r<45;r+=3){const w=hw(r)-3;if(w>0)R(g,ox-w-1,y+r,w*2+2,1,'#8793a8');}
  R(g,ox-1,y+3,2,8,'#5a1018');R(g,ox-3,y+11,6,3,K);R(g,ox-2,y+12,4,1,'#c6d0dc');
  // superstructure: white deckhouse + bridge with a window band
  R(g,x+5,y+17,18,14,K);R(g,x+6,y+18,16,12,'#f4f8ff');R(g,x+6,y+18,16,1,'#ffffff');R(g,x+20,y+19,2,10,'#c6d0dc');
  R(g,x+6,y+19,16,4,K);R(g,x+7,y+20,14,2,'#8fd3ff');R(g,x+8,y+20,3,1,'#d8f2ff');R(g,x+13,y+20,3,2,curHat().c);
  R(g,x+12,y+25,4,3,K);R(g,x+13,y+26,2,1,on?'#ff4a4a':'#7a1f33');
  // funnel
  R(g,x+10,y+31,8,6,K);R(g,x+11,y+32,6,4,c.b);R(g,x+11,y+33,6,1,'#ffffff');R(g,x+12,y+32,4,1,'#2a2a36');puff(g,x+13,y+30,fr,4,0.9);
  // lifeboats
  for(const lx of [x+3,x+22]){R(g,lx,y+24,4,8,K);R(g,lx+1,y+25,2,6,'#ff8a1a');R(g,lx+1,y+25,2,1,'#ffc06a');}
  // round helipad with a helicopter
  R(g,x+7,y+37,14,9,K);R(g,x+8,y+38,12,7,'#3f6a4a');R(g,x+9,y+38,10,7,'#4a7a56');R(g,x+10,y+39,8,5,'#ffffff');R(g,x+11,y+40,6,3,'#4a7a56');
  R(g,x+12,y+38,4,7,K);R(g,x+13,y+39,2,5,'#ffc727');R(g,x+13,y+39,2,1,'#fff3a0');R(g,x+13,y+44,2,3,K);
  if(on){R(g,x+7,y+41,15,1,'#1b1f3b');R(g,x+14,y+36,1,10,'#1b1f3b');}else for(let d=-6;d<=6;d++){R(g,x+14+d,y+41+Math.round(d*0.6),1,1,'#1b1f3b');R(g,x+14+d,y+41-Math.round(d*0.6),1,1,'#1b1f3b');}}
function bladeIcebreaker(g,cx,y,bw,bt,c,fr){// bow wave thrown off both sides of the prow
  const half=Math.floor(bw/2),ph=(fr||0)%2;for(let i=0;i<half;i++){const yy=y+bt+2+Math.round(i*0.55);const h=1+((i+ph)%3===0?1:0);R(g,cx-i-1,yy-h,1,h+1,'#ffffff');R(g,cx+i,yy-h,1,h+1,'#ffffff');
    if((i+ph)%4===0){R(g,cx-i-2,yy-h-2,1,1,'#ffffff');R(g,cx+i+1,yy-h-2,1,1,'#ffffff');}R(g,cx-i-1,yy+1,1,1,'#c6d9f3');R(g,cx+i,yy+1,1,1,'#c6d9f3');}}

// ---- SNOW CRUISER: a huge expedition land-ship on balloon tyres, a ski-plane parked on the roof, steel V-plow
function drawCruiser(g,ox,oy,fr,c){const x=ox-14,y=oy-24,on=fr%2===0;
  tyreV(g,x-5,y+2,10,16,fr);tyreV(g,x+23,y+2,10,16,fr);tyreV(g,x-5,y+30,10,16,fr);tyreV(g,x+23,y+30,10,16,fr);
  R(g,x+3,y,22,48,K);R(g,x+1,y+2,26,44,K);R(g,x+4,y+1,20,46,c.b);R(g,x+2,y+3,24,42,c.b);R(g,x+2,y+3,1,42,c.l);R(g,x+4,y+1,20,1,c.l);R(g,x+25,y+3,1,42,c.d);
  R(g,x+3,y+3,22,6,K);R(g,x+4,y+4,20,4,'#8fd3ff');R(g,x+5,y+4,4,2,'#d8f2ff');R(g,x+12,y+5,3,2,curHat().c);R(g,x+18,y+4,4,1,'#d8f2ff');
  R(g,x+2,y+10,24,2,'#ffffff');R(g,x+2,y+42,24,2,'#ffffff');
  for(let i=0;i<4;i++){R(g,x+1,y+14+i*7,2,3,K);R(g,x+1,y+15+i*7,1,1,'#8fd3ff');R(g,x+25,y+14+i*7,2,3,K);R(g,x+26,y+15+i*7,1,1,'#8fd3ff');}
  // the ski-plane on the roof
  const px=ox,py=y+13;R(g,x+3,py+6,22,5,K);R(g,x+4,py+7,20,3,'#ffc727');R(g,x+4,py+7,20,1,'#fff3a0');R(g,x+4,py+9,20,1,'#d89a12');R(g,x+8,py+7,2,3,'#e03a4e');R(g,x+18,py+7,2,3,'#e03a4e');
  R(g,px-2,py,4,23,K);R(g,px-1,py+1,2,21,'#ffc727');R(g,px-1,py+1,1,21,'#fff3a0');R(g,px-1,py+11,2,3,'#8fd3ff');
  R(g,px-6,py+19,12,4,K);R(g,px-5,py+20,10,2,'#ffc727');R(g,px-5,py+20,10,1,'#fff3a0');R(g,px-1,py+17,2,6,K);R(g,px,py+18,1,4,'#e03a4e');
  if(on)R(g,px-4,py-1,8,1,'#2a2a36');else R(g,px,py-3,1,4,'#2a2a36');
  // radio mast with a flag, rear hatch
  R(g,x+21,y+37,2,9,K);R(g,x+22,y+38,1,7,'#c6d0dc');R(g,x+23,y+37+(fr%2),4,3,'#3f86d6');R(g,x+23,y+37+(fr%2),4,1,'#7fbaf2');
  R(g,x+5,y+38,12,4,K);R(g,x+6,y+39,10,2,c.d);}
function bladeCruiser(g,cx,y,bw,bt,c){const half=Math.floor(bw/2);// thick steel V-plow, apex at the front
  for(let i=0;i<=half;i++){const yy=y+Math.round(i*(bt-4)/half);R(g,cx-i-1,yy,2,5,K);R(g,cx+i-1,yy,2,5,K);}
  for(let i=0;i<half;i++){const yy=y+1+Math.round(i*(bt-4)/half);R(g,cx-i-1,yy,2,3,'#9aa6ba');R(g,cx+i-1,yy,2,3,'#8793a8');R(g,cx-i-1,yy,2,1,'#ffffff');R(g,cx+i-1,yy,2,1,'#e8eef8');R(g,cx-i-1,yy+2,2,1,'#55607a');R(g,cx+i-1,yy+2,2,1,'#55607a');}
  R(g,cx-2,y-1,4,3,K);R(g,cx-1,y,2,1,'#ffffff');}
