import sys,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# The 9 new Suburbs jobs (built from /home/claude/levels/suburbs.py, checked with checkJob and bot runs).
D=json.load(open('/home/claude/levels/suburbs.json'))
for k,v in D.items():
    for x in ('id','name','area'): v.pop(x,None)
rep("const BASE_LEVELS=18;","const BASE_LEVELS=18;\nconst SUB_DATA="+json.dumps(D,separators=(',',':'))+";\n"
    "for(const L of LEVELS){const D2=SUB_DATA[L.id];if(!D2)continue;L.data=D2;for(const k of ['h','time','value','stars','presents'])if(D2[k]!=null)L[k]=D2[k];}")
# ?review=1: a separate save that starts with the first 6 Suburbs jobs done and a blower, so the new jobs can be
# reviewed straight away without touching the real save. (Preview convenience; remove before shipping to the App Store.)
rep("const TEST_MODE=/[?&]test=1/.test(location.search);const SAVE_KEY=TEST_MODE?'snowplowRush.test':'snowplowRush.proto.v2';",
    "const TEST_MODE=/[?&]test=1/.test(location.search),REVIEW_MODE=/[?&]review=(1|all)/.test(location.search);const SAVE_KEY=TEST_MODE?'snowplowRush.test':REVIEW_MODE?(/[?&]review=all/.test(location.search)?'snowplowRush.reviewAll':'snowplowRush.review'):'snowplowRush.proto.v2';")
rep("function loadSave(){try{const s=JSON.parse(localStorage.getItem(SAVE_KEY)||'null');if(s){",
    "function loadSave(){try{let s=JSON.parse(localStorage.getItem(SAVE_KEY)||'null');\n"
    "  if(!s&&REVIEW_MODE){s={v:6,tut:true,story:{suburbs:true},coins:4000,tool:2,use:2,gems:20,mlv:{shovel:{speed:3,size:3,bumper:1},pusher:{speed:6,size:6,bumper:2},blower:{speed:1,size:1,bumper:0}},lv:{speed:0,size:0,value:6,bumper:0,helpers:3},stars:[],best:[]};\n"
    "    for(const id of ['driveway','gardens','culdesac','park','school','maple']){const i=LEVELS.findIndex(L=>L.id===id);s.stars[i]=2;s.best[i]=70;}\n"
    "    if(/[?&]review=all/.test(location.search)){s.tool=5;s.use=5;s.coins=5e6;s.areaSeen=7;s.tolls={retreat:true,stadium:true};s.story={suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true};LEVELS.forEach((L,i)=>{if(L.area!=='secret'){s.stars[i]=1;s.best[i]=40;}});}}\n"
    "  if(s){")
open(f,'w',encoding='utf-8').write(s);print('p47 ok')
