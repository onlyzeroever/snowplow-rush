const nmTyre=(g,tx,ty,w,h,fr)=>{R(g,tx,ty,w,h,K);R(g,tx+1,ty+1,w-2,h-2,'#2a2a36');for(let i=0;i<Math.floor(h/3);i++){const yy=ty+1+((i*3+fr)%(h-2));R(g,tx+1,yy,w-2,1,'#3c3f52');R(g,tx,yy,1,1,K);R(g,tx+w-1,yy,1,1,K);}R(g,tx+1,ty+1,w-2,1,'#55586a');};
const nmTrack=(g,tx,ty,w,h,fr,cleat)=>{R(g,tx,ty,w,h,K);R(g,tx+1,ty+1,w-2,h-2,'#343a4c');for(let i=0;i<Math.floor(h/4)+1;i++){const yy=ty+1+((i*4+(fr%4))%(h-2));R(g,tx+1,yy,w-2,2,cleat||'#5f6880');}R(g,tx+1,ty+1,w-2,1,'#8793a8');};
const nmPuff=(g,px,py,fr,n,dx)=>{for(let i=0;i<n;i++){const k=(i+fr)%n,yy=py-k*3,xx=px+Math.round(k*(dx||0.6));R(g,xx-1,yy-1,4,3,'rgba(214,222,236,'+(0.9-k*0.18).toFixed(2)+')');}};
// ---- FRONT LOADER: articulated loader; yellow bucket on lift arms, 4 tall tyres, hinge in the middle, cab, striped counterweight
function drawLoader(g,ox,oy,fr,c){const x=ox-13,y=oy-22,on=fr%2===0;
  // lift arms (body colour) from the bucket back to the front frame
  for(const ax of [x+3,x+20]){R(g,ax,y-3,4,13,K);R(g,ax+1,y-2,2,11,c.b);R(g,ax+1,y-2,1,11,c.l);}
  R(g,x+3,y+3,20,3,K);R(g,x+4,y+4,18,1,c.d);
  nmTyre(g,x-4,y+3,8,14,fr);nmTyre(g,x+22,y+3,8,14,fr);
  // front frame
  R(g,x+5,y+6,16,12,K);R(g,x+6,y+7,14,10,c.b);R(g,x+6,y+7,14,1,c.l);R(g,x+18,y+8,2,8,c.d);
  R(g,x+6,y+8,3,2,'#ffef7a');R(g,x+17,y+8,3,2,'#ffef7a');R(g,x+11,y+6,4,9,K);R(g,x+12,y+7,2,7,'#55607a');R(g,x+12,y+7,1,7,'#9aa6ba');
  // hinge: a narrow neck with a pivot pin and a striped guard
  R(g,x+8,y+17,10,6,K);R(g,x+9,y+18,8,4,'#2a2a36');R(g,x+9,y+19,8,2,'#ffc727');for(let i=0;i<4;i++)R(g,x+9+i*2,y+19,1,2,'#2a2a36');R(g,x+12,y+17,2,6,'#c6d0dc');
  nmTyre(g,x-4,y+29,8,14,fr);nmTyre(g,x+22,y+29,8,14,fr);
  // rear frame with the cab (black safety frame round the glass)
  R(g,x+3,y+22,20,21,K);R(g,x+4,y+23,18,19,c.b);R(g,x+4,y+23,18,1,c.l);R(g,x+4,y+23,1,19,c.l);R(g,x+20,y+24,1,17,c.d);
  R(g,x+5,y+23,16,12,K);R(g,x+6,y+24,14,4,'#8fd3ff');R(g,x+7,y+24,3,2,'#d8f2ff');R(g,x+12,y+25,3,2,curHat().c);R(g,x+6,y+29,14,5,'#3a3f52');R(g,x+6,y+29,14,1,'#55607a');
  R(g,x+12,y+30,2,2,on?'#ffb43a':'#c45a10');if(on){R(g,x+11,y+30,1,1,'#ffe0a0');R(g,x+14,y+31,1,1,'#ffe0a0');}
  // engine hood with louvres, exhaust stack
  R(g,x+6,y+36,14,6,K);R(g,x+7,y+37,12,4,c.d);for(let i=0;i<4;i++)R(g,x+8+i*3,y+37,1,4,'#2a2a36');
  R(g,x+17,y+33,4,4,K);R(g,x+18,y+34,2,2,'#1b1f3b');if(!on)nmPuff(g,x+19,y+31,fr,3,0.8);
  // counterweight
  R(g,x+2,y+42,22,5,K);for(let i=0;i<20;i++)R(g,x+3+i,y+43,1,3,((i>>1)%2)?'#2a2a36':'#ffc727');}
function bladeLoader(g,cx,y,bw,bt,c){const x=cx-Math.floor(bw/2);// bucket: yellow back wall, steel floor, cutting edge with teeth
  R(g,x,y,bw,bt,K);R(g,x+1,y+1,bw-2,bt-2,c.b);R(g,x+1,y+bt-3,bw-2,1,c.d);R(g,x+3,y+2,bw-6,bt-5,'#8793a8');R(g,x+3,y+2,bw-6,1,'#c6d0dc');R(g,x+3,y+bt-4,bw-6,1,'#55607a');
  for(let i=x+3;i<=x+bw-5;i+=5){R(g,i,y-2,3,3,K);R(g,i+1,y-1,1,2,'#e8eef8');}R(g,x+1,y+1,1,bt-2,c.l);}
// ---- ICEBREAKER: a red ice-ship on tracks; a long pointed bow throws a bow wave, white bridge, funnel, stern helipad
function drawIcebreaker(g,ox,oy,fr,c){const x=ox-14,y=oy-24,on=fr%2===0;
  nmTrack(g,x-2,y+18,5,28,fr);nmTrack(g,x+25,y+18,5,28,fr);
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
  R(g,x+10,y+31,8,6,K);R(g,x+11,y+32,6,4,c.b);R(g,x+11,y+33,6,1,'#ffffff');R(g,x+12,y+32,4,1,'#2a2a36');nmPuff(g,x+13,y+30,fr,4,0.9);
  // lifeboats
  for(const lx of [x+3,x+22]){R(g,lx,y+24,4,8,K);R(g,lx+1,y+25,2,6,'#ff8a1a');R(g,lx+1,y+25,2,1,'#ffc06a');}
  // round helipad with a helicopter
  R(g,x+7,y+37,14,9,K);R(g,x+8,y+38,12,7,'#3f6a4a');R(g,x+9,y+38,10,7,'#4a7a56');R(g,x+10,y+39,8,5,'#ffffff');R(g,x+11,y+40,6,3,'#4a7a56');
  R(g,x+12,y+38,4,7,K);R(g,x+13,y+39,2,5,'#ffc727');R(g,x+13,y+39,2,1,'#fff3a0');R(g,x+13,y+44,2,3,K);
  if(on){R(g,x+7,y+41,15,1,'#1b1f3b');R(g,x+14,y+36,1,10,'#1b1f3b');}else for(let d=-6;d<=6;d++){R(g,x+14+d,y+41+Math.round(d*0.6),1,1,'#1b1f3b');R(g,x+14+d,y+41-Math.round(d*0.6),1,1,'#1b1f3b');}}
function bladeIcebreaker(g,cx,y,bw,bt,c,fr){// a heavy steel V-plow on the bow: the apex cuts in front, the arms sweep back, ice flies off the tips
  const half=Math.floor(bw/2),ph=(fr||0)%2,drop=bt+1;
  for(let i=0;i<=half;i++){const yy=y+Math.round(i*drop/half);R(g,cx-i-1,yy-1,1,6,K);R(g,cx+i,yy-1,1,6,K);}
  for(let i=0;i<half;i++){const yy=y+Math.round(i*drop/half);R(g,cx-i-1,yy,1,4,'#9aa6ba');R(g,cx+i,yy,1,4,'#7a869c');R(g,cx-i-1,yy,1,1,'#ffffff');R(g,cx+i,yy,1,1,'#d8e0ea');
    R(g,cx-i-1,yy+2,1,1,c.b);R(g,cx+i,yy+2,1,1,c.d);if(i%5===2){R(g,cx-i-1,yy+3,1,1,'#55607a');R(g,cx+i,yy+3,1,1,'#3c4558');}}
  R(g,cx-1,y-2,2,2,K);R(g,cx-1,y-1,2,1,'#ffffff');
  for(const sd of [-1,1]){const tx=cx+(sd<0?-half-2:half+1),ty=y+drop;for(let k=0;k<4;k++){R(g,tx+sd*(k+((k+ph)%2)),ty-k-ph,1,1,k%2?'#bfe6ff':'#ffffff');}
    R(g,tx+sd*2,ty-3-ph,2,2,'#bfe6ff');R(g,tx+sd*2,ty-3-ph,1,1,'#ffffff');R(g,tx+sd*(4+ph),ty+1,1,1,'#ffffff');}}
