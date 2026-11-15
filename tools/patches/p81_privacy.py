import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:90])
    s=s.replace(a,b)
# Privacy notice (Alex, Nov 15): a one-time card on the map, in the game's own panel style, that slides up above the
# bottom bar. It informs (anonymous, no names, no ads) and offers Settings; it never blocks play. Settings also says
# it is anonymous under the switch.
rep("if(overlayOpen()){ui=[];scrollAreas=[];}","if(overlayOpen()){ui=[];scrollAreas=[];}\n  if(state==='map'&&!overlayOpen()&&!save.privSeen)drawPrivacyCard(dtD);")
rep("function openShop(){","let privT=0;\nfunction drawPrivacyCard(dt){privT=Math.min(1,privT+(dt||0.016)*3.5);const e=1-Math.pow(1-privT,3),x=6,w=W-12,h=58,y=Math.round(NAV_Y-h-6+(1-e)*70);\n"
  "  btn('privbg',x,y,w,h,()=>{});panel(x,y,w,h,'#13306b','#ffd23f');b.drawImage(SPR.frost,x+6,y+5);text(b,'ANONYMOUS PLAY DATA',x+18,y+6,'#ffd23f',{outline:null});\n"
  "  text(b,'WE COUNT PLOWS, NOT PEOPLE.',W/2,y+17,'#ffffff',{align:'center',outline:null});text(b,'IT HELPS US MAKE THE GAME BETTER,',W/2,y+26,'#9fc0e8',{align:'center',outline:null});text(b,'AND WE NEVER SELL IT.',W/2,y+34,'#9fc0e8',{align:'center',outline:null});\n"
  "  button('privok',x+w/2-56,y+42,52,13,'green','GOT IT',()=>{save.privSeen=true;track('privacy_notice',{choice:'got_it'});persist();sfx('click');});\n"
  "  button('privset',x+w/2+4,y+42,52,13,'navy','SETTINGS',()=>{save.privSeen=true;track('privacy_notice',{choice:'settings'});persist();settingsOpen=true;sfx('click');});}\nfunction openShop(){")
# Settings: say it plainly under the switch
rep("panel(14,60,152,192,'#13306b','#ffd23f');","panel(14,60,152,204,'#13306b','#ffd23f');")
rep("persist();sfx('click');});\n  button('rst',24,198,132,16,","persist();sfx('click');});\n  text(b,'ANONYMOUS AND NEVER SOLD',W/2,195,'#9fc0e8',{align:'center',outline:null});\n  button('rst',24,204,132,16,")
rep("button('close',54,226,72,18,'orange','DONE',","button('close',54,234,72,18,'orange','DONE',")
open(f,'w',encoding='utf-8').write(s)
