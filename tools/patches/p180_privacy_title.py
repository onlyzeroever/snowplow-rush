# Title screen without the privacy small print (Alex, Nov 21 23:28: "don't think we need this on the first page? doesn't
# feel professional"). LIVE. The same note now comes as the existing "ANONYMOUS PLAY DATA" card (GOT IT / SETTINGS) on
# the first visit to the map, after the first job, and stays in Settings. In the apps, EU/UK players also get the consent
# step of the ads/consent flow before anything is recorded (SRNative.recordOK()).
# The card moves to the top of the map so it never covers job 1 at the bottom.
# The first tap on the title no longer counts as having seen the note (privacy_notice now comes from the card:
# got_it / settings); offers and the fun question still wait until the note has been seen.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("\n    if(!save.privSeen){const c='#5b7bab';text(b,'WE COUNT PLOWS, NOT PEOPLE.',W/2,274,c,{align:'center',outline:null});text(b,'WE MAY RECORD YOUR FIRST PLAYS,',W/2,282,c,{align:'center',outline:null});text(b,'ANONYMOUSLY. WE NEVER SELL IT.',W/2,290,c,{align:'center',outline:null});}","")
rep("function titleGo(){sfx('click');const fresh=!save.privSeen;if(fresh){save.privSeen=true;track('privacy_notice',{choice:'title'});persist();}",
    "function titleGo(){sfx('click');const fresh=!save.privSeen;")
# the card sits at the top of the map (under the event banner), so it never covers the first jobs at the bottom
rep("const e=1-Math.pow(1-privT,3),x=6,w=W-12,h=58,y=Math.round(NAV_Y-h-6+(1-e)*70);","const e=1-Math.pow(1-privT,3),x=6,w=W-12,h=58,y=Math.round(MAP_VY+16-(1-e)*10);b.globalAlpha=Math.min(1,0.15+e);")
# a short drop and fade under the top bar (it used to slide 90 px over the coin bar)
rep("track('privacy_notice',{choice:'settings'});persist();settingsOpen=true;sfx('click');});}","track('privacy_notice',{choice:'settings'});persist();settingsOpen=true;sfx('click');});b.globalAlpha=1;}")
open(f,'w',encoding='utf-8').write(s)
print('p180 title screen without the privacy small print; the note comes as the card on the first map visit')
