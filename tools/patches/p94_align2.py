import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:70]); s=s.replace(a,b)
# Alignment pass 2 (Nov 16), from a capture of every screen:
#  - Outfits: 5-wide grid so all 17 outfits fit above the name (the 17th card sat under CLASSIC and the hat swatches)
#  - Prices in small cards use a compact format (2K, 8K, 25K, 1.5M) so they fit inside the card, centred
#  - Treasure Book: DONE sits inside the book frame
#  - Results: long hint lines are condensed to fit the panel; the RETRY highlight is an even 1px frame that
#    no longer touches JOBS; trophy banners show under the results panel instead of over its title
#  - Tutorial box grows to fit the arrow-keys line
#  - Trails: the trail in use shows an IN USE badge like the garage
#  - Ad screen: reward icon + amount centred
#  - Shop: Premium line shortened so it no longer runs into the price button
rep("function fmt(n){","function fmtC(n){n=Math.floor(n);if(n<1000)return ''+n;const u=['K','M','B','T','Q'];let i=-1,v=n;while(v>=1000&&i<u.length-1){v/=1000;i++;}const r=v<10?Math.floor(v*10)/10:Math.floor(v);return (''+r).replace(/\\.0$/,'')+u[i];}\nfunction fmt(n){")
rep("function priceDraw(price,x,y,col,align){const s2=price.c!=null?fmt(price.c):",
    "function priceDraw(price,x,y,col,align,cmp){const s2=price.c!=null?(cmp?fmtC(price.c):fmt(price.c)):")
rep("priceDraw(skinPrice(tid,k),x+12,y+31,'#13306b','center')","priceDraw(skinPrice(tid,k),x+12,y+31,'#13306b','center',1)")
# outfits grid
rep("const x=10+(k%4)*40,y=28+Math.floor(k/4)*44","const x=8+(k%5)*33,y=28+Math.floor(k/5)*42")
rep("card(x,y,38,42,","card(x,y,32,40,")
rep("b.drawImage(ks.down,x+5,y+3,28,36)","b.drawImage(ks.down,x+2,y+2,28,36)")
rep("R(b,x+2,y+32,34,8,'rgba(19,48,107,0.85)');priceDraw(o.price,x+19,y+33,'#ffffff','center')","R(b,x+2,y+30,28,8,'rgba(19,48,107,0.85)');priceDraw(o.price,x+16,y+31,'#ffffff','center',1)")
rep("b.drawImage(SPR.trophy,x+29,y+31)","b.drawImage(SPR.trophy,x+23,y+29)")
rep("text(b,'FREE!',x+19,y+33","text(b,'FREE!',x+16,y+31")
rep("R(b,x+30,y+3,5,5,K);R(b,x+31,y+4,3,3,'#4fd36a')","R(b,x+25,y+2,5,5,K);R(b,x+26,y+3,3,3,'#4fd36a')")
rep("btn('of'+k,x,y,38,42,","btn('of'+k,x,y,32,40,")
rep("text(b,fmt(ht.cost),sx+11,sy2+16","text(b,fmtC(ht.cost),sx+11,sy2+16")
# treasure book
rep("panel(6,30,168,250,'#5a3a1e','#ffd23f');R(b,10,34,160,242,'#f4e8c8');","panel(6,30,168,278,'#5a3a1e','#ffd23f');R(b,10,34,160,242,'#f4e8c8');")
# results: fitted lines
rep("function nextGoal(){","function rLine(s,y,col,ol){if(textW(s)<=148)text(b,s,W/2,y,col,{align:'center',outline:ol===false?null:undefined});else condText(b,s,W/2,y,col,ol===false?null:K);}\nfunction nextGoal(){")
rep("else if(kids.length)text(b,LEVELS[kids[0]].name+' UNLOCKED!',W/2,ly,'#ffd23f',{align:'center'});","else if(kids.length)rLine(LEVELS[kids[0]].name+' UNLOCKED!',ly,'#ffd23f');")
rep("else if(gated.length)text(b,'NEXT AREA NEEDS A '+TOOLS[toolIdx(LEVELS[gated[0]].gate)].name,W/2,ly,'#9fd8ff',{align:'center'});","else if(gated.length)rLine('NEXT AREA NEEDS A '+TOOLS[toolIdx(LEVELS[gated[0]].gate)].name,ly,'#9fd8ff');")
rep("if(ng){text(b,ng.s,W/2,ly,ng.col,{align:'center'});","if(ng){rLine(ng.s,ly,ng.col);")
rep("if(ng){text(b,ng.s,W/2,ly+10,ng.col,{align:'center',outline:null});","if(ng){rLine(ng.s,ly+10,ng.col,false);")
rep("R(b,15,py+173,52,2,'#ffd23f');R(b,15,py+199,52,2,'#ffd23f');R(b,15,py+173,2,28,'#ffd23f');R(b,65,py+173,2,28,'#ffd23f');",
    "R(b,16,py+174,50,1,'#ffd23f');R(b,16,py+199,50,1,'#ffd23f');R(b,16,py+174,1,26,'#ffd23f');R(b,65,py+174,1,26,'#ffd23f');")
rep("y=state==='play'?VIEW_Y+4:(state==='title'?4:NAV_Y-30)","y=state==='play'?(run&&run.ended?VIEW_Y+VIEW_H-26:VIEW_Y+4):(state==='title'?4:NAV_Y-30)")
rep("else{const ng=nextGoal();if(ng){rLine(ng.s,ly,ng.col);btn('rgoal',14,ly-2,152,10,()=>{sfx('click');ng.go();});}else text(b,'UPGRADE AND GO AGAIN!',W/2,ly,'#ffffff',{align:'center'});}",
    "else if(ly<=py+134){const ng=nextGoal();if(ng){rLine(ng.s,ly,ng.col);btn('rgoal',14,ly-2,152,10,()=>{sfx('click');ng.go();});}else text(b,'UPGRADE AND GO AGAIN!',W/2,ly,'#ffffff',{align:'center'});}")
rep("text(b,run.hits+' HITS  '+run.gifts+' GIFTS',W-24,py+109,","text(b,run.hits+(run.hits===1?' HIT  ':' HITS  ')+run.gifts+(run.gifts===1?' GIFT':' GIFTS'),W-24,py+109,")
rep("text(b,'YOU: PLAY THE WEEKLY TO GET A RANK',W/2,y0+145,","text(b,'PLAY THE WEEKLY TO GET A RANK',W/2,y0+145,")
rep("""  text(b,'STREAK',18,y+1,'#9fc0e8',{outline:null});text(b,sn+(sn===1?' DAY':' DAYS'),18,y+8,sn?'#ffd23f':'#6a7896',{outline:null});
  for(let i=0;i<7;i++){const big=i===6,x=60+i*15,yy=big?y-1:y,w=big?15:13,on=i<filled,isT=i===today;
    const pop=isT&&done&&streakPop>0?Math.round(streakPop*2):0;
    R(b,x-pop,yy-pop,w+pop*2,w+pop*2,K);R(b,x+1-pop,yy+1-pop,w-2+pop*2,w-2+pop*2,on?(big?'#ffd23f':'#7fe08a'):big?'#a05ad8':'#24406f');
    b.drawImage(SPR.gemS,x+Math.floor((w-5)/2),yy+1+(big?1:0));ctext(''+STREAK_GEMS[i],x,w,yy+7+(big?1:0),on?'#13306b':big?'#ffd23f':'#9fc0e8',{outline:null});
    if(isT&&!done&&Math.floor(tNow*3)%2===0){R(b,x-1,yy-1,w+2,1,'#ffd23f');R(b,x-1,yy+w,w+2,1,'#ffd23f');R(b,x-1,yy-1,1,w+2,'#ffd23f');R(b,x+w,yy-1,1,w+2,'#ffd23f');}}
  if(s&&s.savers>0)text(b,'STREAK SAVER x'+s.savers,W-14,y+17,'#9fd8ff',{align:'right',outline:null});}""",
"""  text(b,'STREAK',18,y+2,'#9fc0e8',{outline:null});text(b,sn+(sn===1?' DAY':' DAYS'),18,y+10,sn?'#ffd23f':'#6a7896',{outline:null});
  for(let i=0;i<7;i++){const big=i===6,x=60+i*15,yy=big?y-1:y,w=big?15:13,h=big?18:16,on=i<filled,isT=i===today;
    const pop=isT&&done&&streakPop>0?Math.round(streakPop*2):0;
    R(b,x-pop,yy-pop,w+pop*2,h+pop*2,K);R(b,x+1-pop,yy+1-pop,w-2+pop*2,h-2+pop*2,on?(big?'#ffd23f':'#7fe08a'):big?'#a05ad8':'#24406f');
    b.drawImage(SPR.gemS,x+Math.floor((w-5)/2),yy+(big?3:2));ctext(''+STREAK_GEMS[i],x,w,yy+(big?10:9),on?'#13306b':big?'#ffd23f':'#9fc0e8',{outline:null});
    if(isT&&!done&&Math.floor(tNow*3)%2===0){R(b,x-1,yy-1,w+2,1,'#ffd23f');R(b,x-1,yy+h,w+2,1,'#ffd23f');R(b,x-1,yy-1,1,h+2,'#ffd23f');R(b,x+w,yy-1,1,h+2,'#ffd23f');}}
  if(s&&s.savers>0)text(b,'STREAK SAVER x'+s.savers,W-14,y+20,'#9fd8ff',{align:'right',outline:null});}""")
# tutorial box
rep("if(!run.moved&&!run.ended){panel(20,VIEW_Y+VIEW_H-110,140,36,'#13306b','#ffd23f');",
    "if(!run.moved&&!run.ended){const kb=!('ontouchstart' in window)&&!navigator.maxTouchPoints;panel(20,VIEW_Y+VIEW_H-110,140,kb?46:36,'#13306b','#ffd23f');")
# trails in-use badge
rep("if(on)text(b,'ON',140,y+20,'#1f7a33',{align:'center'});","if(on)button('treon'+k,116,y+15,48,16,'green','IN USE',null,{active:true});")
# ad screen reward row
rep("b.drawImage(adScreen.gems?SPR.gem:SPR.coin,W/2-26,166);text(b,'+'+fmt(adScreen.reward)+(adScreen.gems?' GEMS':''),W/2-16,167,adScreen.gems?'#ff8fc8':'#ffd23f',{scale:1});",
    "{const ic=adScreen.gems?SPR.gem:SPR.coin,s2='+'+fmt(adScreen.reward)+(adScreen.gems?' GEMS':''),tw=ic.width+3+textW(s2),sx=Math.round(W/2-tw/2);b.drawImage(ic,sx,166);text(b,s2,sx+ic.width+3,167,adScreen.gems?'#ff8fc8':'#ffd23f');}")
rep("'EVERY AD REWARD, NO AD'","'REWARDS WITHOUT ADS'")
open(f,'w',encoding='utf-8').write(s)
print('p94 align 2')
