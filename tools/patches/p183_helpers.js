// ---- p183: what fills the screen around the game column (margins), drawn every frame into cbx before the column
const MG={k:'',pine:null,pineS:null};
function mgHash(a,c){let h=(a*374761393+c*668265263)|0;h=Math.imul(h^(h>>>13),1274126177);return ((h^(h>>>16))>>>0)/4294967296;}
function mgPines(){if(!MG.pine){MG.pine=pineSprite(15);MG.pineS=shadowOf(MG.pine);MG.pine2=pineSprite(11);MG.pine2S=shadowOf(MG.pine2);}}
// snowy ground with pines and a little snow texture, in world coordinates (wx0,wy0 = the world point drawn at x0,y0):
// the same world point always gets the same tree, so the scenery scrolls with the map or the job and never flickers
function mgScene(g,x0,y0,w,h,wx0,wy0,ground,dens,skip){if(w<=0||h<=0)return;mgPines();g.save();g.beginPath();g.rect(x0,y0,w,h);g.clip();
  g.fillStyle=ground||'#f4f8ff';g.fillRect(x0,y0,w,h);const C=17,ox=x0-wx0,oy=y0-wy0;
  const c0=Math.floor((wx0-12)/C),c1=Math.ceil((wx0+w+12)/C),r0=Math.floor((wy0-6)/C),r1=Math.ceil((wy0+h+22)/C);
  g.fillStyle='#e3ecf8';for(let r=r0;r<=r1;r++)for(let c=c0;c<=c1;c++){const q=mgHash(c*3+1,r*5+2);if(q<0.55)g.fillRect(Math.round(c*C+q*C*1.7)+ox,Math.round(r*C+mgHash(c,r+9)*C)+oy,q<0.2?3:2,1);}
  for(let r=r0;r<=r1;r++)for(let c=c0;c<=c1;c++){const q=mgHash(c,r);if(q>(dens==null?0.42:dens))continue;const big=mgHash(c+5,r+3)<0.6,sp=big?MG.pine:MG.pine2,ss=big?MG.pineS:MG.pine2S,
    px=Math.round(c*C+mgHash(c+11,r)*(C-6)),py=Math.round(r*C+mgHash(c,r+13)*(C-4));if(skip&&skip(px,py,sp))continue;
    g.globalAlpha=0.22;g.drawImage(ss,px+1+ox,py+2+oy);g.globalAlpha=1;g.drawImage(sp,px+ox,py-sp.height+oy+4);}
  g.restore();}
function mgBar(g,y,h,col,line,lineY){g.fillStyle=col;g.fillRect(0,y,SCW,h);if(line){g.fillStyle=line;g.fillRect(0,lineY,SCW,1);}}
function paintMargins(){const g=cbx,L=COX,Rx=COX+W,top=COY,bot=COY+H;g.globalAlpha=1;
  const sides=(fn)=>{if(L>0)fn(0,L);if(SCW-Rx>0)fn(Rx,SCW-Rx);};
  if(state==='title'){const ty=top+TTL_OY;g.fillStyle='#9fd0f2';g.fillRect(0,0,SCW,SCH);
    sides((x0,w)=>{g.fillStyle='#bfe0f7';for(let y=60;y<140;y+=2)for(let x=x0+((y+x0-COX)&1);x<x0+w;x+=2)g.fillRect(x,ty+y,1,1);g.fillRect(x0,ty+140,w,SCH-ty-140);
      g.fillStyle='#e9f3fd';for(let x=x0;x<x0+w;x++){const xr=x-COX,hh=Math.round(30+Math.sin(xr*0.045)*14+Math.sin(xr*0.13)*5);g.fillRect(x,ty+170-hh,1,hh);}
      g.fillStyle='#c6d9f3';for(let x=x0;x<x0+w;x++){const xr=x-COX,hh=Math.round(16+Math.sin(xr*0.07+2)*9);g.fillRect(x,ty+178-hh,1,hh);}
      const pine=TITLE_PINE||(TITLE_PINE=pineSprite(24));g.save();g.beginPath();g.rect(x0,0,w,SCH);g.clip();
      for(let k=Math.floor((x0-COX+6)/19)-1;k<=Math.ceil((x0+w-COX+6)/19);k++){const xr=-6+k*19,m=((xr%3)+3)%3;g.globalAlpha=0.26;g.drawImage(shadowOf(pine),COX+xr+1,ty+159+m);g.globalAlpha=1;g.drawImage(pine,COX+xr,ty+158+m);}
      g.fillStyle='#f4f8ff';g.fillRect(x0,ty+182,w,SCH-ty-182);g.fillStyle='#e9f1fd';for(let k=Math.floor((x0-COX)/7)-1;k<=Math.ceil((x0+w-COX)/7);k++){const xr=k*7,m=((xr%5)+5)%5;g.fillRect(COX+xr+m,ty+190+(((xr*7)%60)+60)%60,3,1);}
      g.restore();});
    g.fillStyle='#f4f8ff';g.fillRect(0,bot,SCW,SCH-bot);}
  else if(state==='play'&&G){const cy=Math.round(camY);g.fillStyle='#0b1838';g.fillRect(0,0,SCW,SCH);
    sides((x0,w)=>mgScene(g,x0,top+VIEW_Y,w,VIEW_H,x0-COX,cy,'#f4f8ff',0.42));
    mgBar(g,0,top+HUD_H,'#0b1838','#4f8fdc',top+HUD_H-1);mgBar(g,bot-BAR_H,SCH-bot+BAR_H,'#0b1838','#4f8fdc',bot-BAR_H);}
  else if(state==='map'){const oy=MAP_OY,vy=top+MAP_VY;g.fillStyle='#0b1838';g.fillRect(0,0,SCW,SCH);
    sides((x0,w)=>{let y=0;while(y<MAP_VH){const wy=oy+y,B=biomeAt(wy),y2=Math.min(MAP_VH,B.y1-oy),hh=Math.max(1,y2-y),storm=fogStormY>0&&wy<fogStormY;
        if(storm){const h2=Math.min(hh,fogStormY-wy);g.fillStyle='#3d4b74';g.fillRect(x0,vy+y,w,h2);for(let k=0;k<h2;k+=6){const r=mgHash(Math.floor((wy+k)/6),x0);g.fillStyle=['#4a5a85','#56688f','#4f5f8a'][Math.floor(r*3)];g.fillRect(x0,vy+y+k,w,3);}y+=h2;continue;}
        mgScene(g,x0,vy+y,w,hh,x0-COX,wy,B.ground,B.id==='city'?0.22:B.id==='farm'?0.3:0.45);y+=hh;}});
    mgBar(g,0,top+22,'#0b1838','#4f8fdc',top+22);mgBar(g,top+NAV_Y-2,SCH-top-NAV_Y+2,'#0b1838','#4f8fdc',top+NAV_Y-2);}
  else if(state==='upgrades'){g.fillStyle='#8a5a2c';g.fillRect(0,0,SCW,top+NAV_Y);for(let k=Math.floor(-COX/12)-1;k*12+COX<SCW;k++){const x=COX+k*12;g.fillStyle='#6b3f22';g.fillRect(x,0,1,top+NAV_Y);g.fillStyle='#9a6a3a';g.fillRect(x+5,0,1,top+NAV_Y);}
    g.fillStyle='#6b3f22';for(let y=40;y<NAV_Y;y+=53)g.fillRect(0,top+y,SCW,1);mgBar(g,top+NAV_Y-2,SCH-top-NAV_Y+2,'#0b1838','#4f8fdc',top+NAV_Y-2);}
  else if(state==='garage'){g.fillStyle='#5b6478';g.fillRect(0,0,SCW,top+NAV_Y);g.fillStyle='#4c5468';for(let y=top%8;y<top+NAV_Y;y+=8)g.fillRect(0,y,SCW,1);
    mgBar(g,0,top+22,'#0b1838');mgBar(g,top+NAV_Y-2,SCH-top-NAV_Y+2,'#0b1838','#4f8fdc',top+NAV_Y-2);}
  else{g.fillStyle='#0b1838';g.fillRect(0,0,SCW,SCH);}
  for(const [st,al] of FRAME_DIMS){g.globalAlpha=al;g.fillStyle=st;g.fillRect(0,0,SCW,SCH);}g.globalAlpha=1;}
