import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:80],s.count(a));s=s.replace(a,b_)
# Menus pass (Nov 16), following what polished mobile games do:
# 1. Title screen: a living scene (village with chimney smoke on the hill, a plow truck clearing the road with spray),
#    a soft pulsing TAP TO PLAY instead of a hard blink, and a small version tag.
rep("const pine=TITLE_PINE||(TITLE_PINE=pineSprite(24));",
    "for(const [hx,hy,c] of [[14,146,0],[60,140,2],[112,143,4],[150,149,1]]){const cp=mHouse(b,hx,hy,16,16,HOUSE_COLS[c][0],HOUSE_COLS[c][1],HOUSE_COLS[c][2],1,hx);if(cp)for(let k=0;k<3;k++){const ph=(tNow*0.55+k/3+hx*0.013)%1;b.globalAlpha=0.85*(1-ph);R(b,Math.round(cp.x+Math.sin(ph*6+hx)*2)-1,Math.round(cp.y-ph*14),2,2,'#f4f8ff');b.globalAlpha=1;}}\n  const pine=TITLE_PINE||(TITLE_PINE=pineSprite(24));")
rep("const prog=(tNow*18)%120;R(b,20,214,prog,12,'#4a5068');for(let x=20;x<20+prog;x+=6)R(b,x,214,3,1,'#58607a');R(b,20,226,prog,1,'#a6c2ea');\n  drawRig(b,'shovel',30+prog-4,226,1,14,2,Math.floor(tNow*6)%2,0,false);",
    "const px=Math.round((tNow*24)%220-30);if(px>0){R(b,0,210,px,20,'#4a5068');R(b,0,210,px,1,'#a6c2ea');R(b,0,229,px,1,'#a6c2ea');for(let x=4;x<px-10;x+=12)R(b,x,219,6,1,'#ffd23f');}\n"
    "  drawRig(b,'truck',px,220,1,30,3,Math.floor(tNow*6)%2,Math.floor(tNow*8),false);for(let k=0;k<7;k++){const t2=(tNow*2.6+k/7)%1;const sx=px+17+Math.round(t2*16),sy=Math.round(206+k%3*3-Math.sin(t2*Math.PI)*12);R(b,sx,sy,k%2?2:1,k%2?2:1,'#ffffff');if(k%2)R(b,sx+1,sy+1,1,1,'#a6c2ea');}")
rep("if(Math.floor(tNow*2)%2===0)text(b,'TAP TO PLAY',W/2,258,'#ffffff',{align:'center',scale:2});\n  text(b,'PROTOTYPE V0.8.0',W/2,300,'#4f6fa0',{align:'center',outline:null});",
    "{b.globalAlpha=0.55+0.45*(0.5+0.5*Math.sin(tNow*4));text(b,'TAP TO PLAY',W/2,258+(Math.sin(tNow*4)>0.6?-1:0),'#ffffff',{align:'center',scale:2});b.globalAlpha=1;}\n  text(b,'PLAYTEST V0.8.0',W/2,304,'#8fa8cc',{align:'center',outline:null});")
# 2. Popups fade up into place (0.14s) instead of snapping on; switching between Jobs / Upgrades / Garage eases in.
rep("  if(jobInfo>=0)drawJobInfo();\n  if(weeklyOpen)drawWeekly();",
    "  const ovk=(jobInfo>=0?'j'+jobInfo:'')+(weeklyOpen?'w':'')+(skinFor?'s':'')+(outfitsOpen?'o':'')+(trailsOpen?'t':'')+(bookOpen?'b':'')+(storyOpen&&state==='map'?'y':'')+(settingsOpen?'g':'')+(trophiesOpen?'r':'')+(dailyOpen?'d':'')+(winterOpen?'n':'')+(shopOpen?'h':'');\n"
    "  if(ovk!==draw.ovk){if(ovk&&ovk.length>(draw.ovk||'').length)draw.ovT=tNow;draw.ovk=ovk;}\n"
    "  if(state!==draw.st){if(draw.st&&['map','upgrades','garage'].includes(state)&&['map','upgrades','garage'].includes(draw.st))draw.stT=tNow;draw.st=state;}\n"
    "  if(draw.stT!=null&&tNow-draw.stT<0.16&&!ovk){b.fillStyle='rgba(11,24,56,'+(0.45*(1-(tNow-draw.stT)/0.16)).toFixed(2)+')';b.fillRect(0,0,W,NAV_Y);}\n"
    "  const ovA=ovk&&draw.ovT!=null?Math.min(1,(tNow-draw.ovT)/0.14):1;if(ovA<1){b.save();b.globalAlpha=ovA;b.translate(0,Math.round((1-ovA)*5));}\n"
    "  if(jobInfo>=0)drawJobInfo();\n  if(weeklyOpen)drawWeekly();")
rep("  if(shopOpen)drawShop();\n  if(adScreen)drawAd();","  if(shopOpen)drawShop();\n  if(ovA<1){b.restore();b.globalAlpha=1;}\n  if(adScreen)drawAd();")
# 3. Settings: Reset is a destructive action, so it reads as one (red label on a quiet button), separate from the rest.
rep("button('rst',24,204,132,16,confirmReset>0?'red':'grey',confirmReset>0?'TAP AGAIN TO RESET':'RESET PROGRESS',()=>{",
    "if(!(confirmReset>0)){R(b,24,203,132,1,'#2a4a8a');}button('rst',24,206,132,15,confirmReset>0?'red':'navy',confirmReset>0?'TAP AGAIN TO RESET':null,()=>{")
rep("if(confirmReset>0){resetSave();confirmReset=0;showToast('PROGRESS RESET');}else confirmReset=2.5;});",
    "if(confirmReset>0){resetSave();confirmReset=0;showToast('PROGRESS RESET');}else confirmReset=2.5;});if(!(confirmReset>0))text(b,'RESET PROGRESS',W/2,210,'#ff8f9e',{align:'center'});")
# 4. Skins preview: a snowy stage with a soft spotlight instead of lined notebook paper.
rep("R(b,30,36,120,92,K);R(b,31,37,118,90,'#cfe3f8');for(let y=37;y<127;y+=6)R(b,31,y,118,1,'#bcd4ee');",
    "R(b,30,36,120,92,K);R(b,31,37,118,90,'#a8d4f2');for(let y=37;y<97;y+=2)dither(31,y,118,1,'#bfe0f7');R(b,31,97,118,30,'#f4f8ff');R(b,31,97,118,1,'#c6d9f3');for(let dy=0;dy<8;dy++){const hw=Math.round(42*Math.sqrt(1-((dy-4)/4.5)**2));R(b,90-hw,103+dy,hw*2,1,dy<2||dy>5?'#e8f0fb':'#dfe9f8');}\n"
    "  for(const [fx,fy] of [[40,45],[70,52],[128,44],[110,70],[52,80],[138,86]])R(b,fx,fy+Math.round(Math.sin(tNow*2+fx)*1),1,1,'#ffffff');")
# 5. Results: when "N% off your first star" is already shown, don't repeat it with "GET N% FOR A STAR".
rep("else if(r.stars===0)text(b,'GET '+G.def.stars[0]+'% FOR A STAR',W/2,ly,'#ff9aa8',{align:'center'});",
    "else if(r.stars===0){if(!close)text(b,'GET '+G.def.stars[0]+'% FOR A STAR',W/2,ly,'#ff9aa8',{align:'center'});else{const ng=nextGoal();if(ng){rLine(ng.s,ly,ng.col);btn('rgoal',14,ly-2,152,10,()=>{sfx('click');ng.go();});}}}")
rep("if(!r.challenge&&(r.stars===0||kids.length||gated.length)&&ly+10<=py+132)","if(!r.challenge&&((r.stars===0&&!close)||kids.length||gated.length)&&ly+10<=py+132)")
open(f,'w',encoding='utf-8').write(s)
print('p106 menus pass')
