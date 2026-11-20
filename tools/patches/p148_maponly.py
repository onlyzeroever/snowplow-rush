# Alex, Nov 21 00:34: "do we need the switcher that shows the job list + map? ... hide it for now and then we can
# decide if we wanna bring it back". The map is the job screen; the map/list toggle is hidden (LIST_TOGGLE brings it
# back), a saved 'list' view opens the map, and WEEKLY / SHOP widen to fill the row.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("function drawMap(){const dt=mapDrawT==null?0:Math.min(0.05,Math.max(0,tNow-mapDrawT));mapDrawT=tNow;ensureMapArt();\n  if(save.mapView==='list')drawJobList(dt);else drawWorld(dt);drawMapChrome();}",
    "const LIST_TOGGLE=false; // Nov 21: map only (Alex); true brings back the map/list switcher\n"
    "function drawMap(){const dt=mapDrawT==null?0:Math.min(0.05,Math.max(0,tNow-mapDrawT));mapDrawT=tNow;ensureMapArt();if(!LIST_TOGGLE&&save.mapView==='list')save.mapView='map';\n  if(save.mapView==='list')drawJobList(dt);else drawWorld(dt);drawMapChrome();}")
rep("  if(dailyOn()){button('weekly',29,by,44,18,'gold','WEEKLY',()=>{weeklyOpen=true;weeklyTab=0;save.weeklySeen=weekNo();sfx('click');persist();});if(!weeklyState().claimed&&save.weeklySeen!==weekNo()){R(b,68,by-2,6,6,K);R(b,69,by-1,4,4,'#e8283f');}}\n  button('shopb',121,by,40,18,'green','SHOP',",
    "  const ww=LIST_TOGGLE?44:62,sx=LIST_TOGGLE?121:95,sw=LIST_TOGGLE?40:66;\n"
    "  if(dailyOn()){button('weekly',29,by,ww,18,'gold','WEEKLY',()=>{weeklyOpen=true;weeklyTab=0;save.weeklySeen=weekNo();sfx('click');persist();});if(!weeklyState().claimed&&save.weeklySeen!==weekNo()){R(b,29+ww-5,by-2,6,6,K);R(b,29+ww-4,by-1,4,4,'#e8283f');}}\n"
    "  button('shopb',sx,by,sw,18,'green','SHOP',")
rep("  // map / list toggle\n  const tx=77,lv=save.mapView==='list';","  // map / list toggle (hidden while LIST_TOGGLE is false)\n  if(LIST_TOGGLE){const tx=77,lv=save.mapView==='list';")
rep("btn('vlist',tx+20,by,20,18,()=>{if(save.mapView!=='list'){save.mapView='list';sfx('click');persist();}});",
    "btn('vlist',tx+20,by,20,18,()=>{if(save.mapView!=='list'){save.mapView='list';sfx('click');persist();}});}")
open(f,'w',encoding='utf-8').write(s)
print('p148 map only: list switcher hidden')
