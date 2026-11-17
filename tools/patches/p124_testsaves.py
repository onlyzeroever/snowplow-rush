import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Skip-ahead test saves for the late-game playtest (plan doc, phase 1). Each link starts its own save, kept apart from the
# player's real one, at the point a typical player reaches that area (economy sim, real combo levels):
#   ?review=themepark  Super Plow (speed 4, width 4), Suburbs to City done, 500K coins
#   ?review=ski        Snowcat maxed, up to Harbour done, 10M coins
#   ?review=pass       Rotary (speed 4, width 3), up to Ski done, 2.7M coins
#   ?review=north      Rotary maxed, up to the Pass done, 26M coins
# Earlier jobs have 2 stars, value and helpers are maxed. Analytics tags these runs build 'review' + rv '<stage>', so the
# dashboard leaves them out and they can be read on their own.
rep("REVIEW_MODE=/[?&]review=(1|all)/.test(location.search);",
    "REVIEW_MODE=/[?&]review=(1|all|themepark|ski|pass|north)/.test(location.search);const RV=(location.search.match(/[?&]review=(themepark|ski|pass|north)/)||[])[1]||null;")
rep("REVIEW_MODE?(/[?&]review=all/.test(location.search)?'snowplowRush.reviewAll':'snowplowRush.review'):'snowplowRush.proto.v2';",
    "REVIEW_MODE?(RV?'snowplowRush.review_'+RV:/[?&]review=all/.test(location.search)?'snowplowRush.reviewAll':'snowplowRush.review'):'snowplowRush.proto.v2';")
rep("  if(!s&&REVIEW_MODE){s={v:6,tut:true,",
    "  if(!s&&RV){const ix=id=>TOOLS.findIndex(t=>t.id===id),AR=['suburbs','farm','city','themepark','harbour','ski','pass','north'],\n"
    "    P={themepark:{m:'super',lv:[4,4,2],coins:5e5},ski:{m:'snowcat',lv:[6,6,5],coins:1e7},pass:{m:'rotary',lv:[4,3,2],coins:2.7e6},north:{m:'rotary',lv:[6,6,5],coins:2.6e7}}[RV],done=AR.slice(0,AR.indexOf(RV));\n"
    "    s={v:6,tv:2,tut:true,coins:P.coins,tool:ix(P.m),use:ix(P.m),gems:40,mlv:{},lv:{speed:0,size:0,value:20,bumper:0,helpers:20},stars:[],best:[],story:{},tolls:{},areaSeen:done.length,rvStage:RV};\n"
    "    for(let i=0;i<=ix(P.m);i++)s.mlv[TOOLS[i].id]=i===ix(P.m)?{speed:P.lv[0],size:P.lv[1],bumper:P.lv[2]}:{speed:6,size:6,bumper:5};\n"
    "    for(const a of done)s.story[a]=true;LEVELS.forEach((L,i)=>{if(done.includes(L.area)){s.stars[i]=2;s.best[i]=70;if(L.toll)s.tolls[L.id]=true;}});}\n"
    "  if(!s&&REVIEW_MODE){s={v:6,tut:true,")
# analytics: tag the stage
rep("REVIEW_MODE?'review':'live',v:'0.8.0',winter:winterNo(),","REVIEW_MODE?'review':'live',rv:RV,v:'0.8.0',winter:winterNo(),")
open(f,'w',encoding='utf-8').write(s)
print('p124 skip-ahead test saves: ?review=themepark|ski|pass|north')
