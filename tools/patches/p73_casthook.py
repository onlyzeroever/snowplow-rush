import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# Test-only hook: every character/creature sprite in one place, for the art contact sheets.
a="window.__SR={"
assert s.count(a)==1
s=s.replace(a,"if(TEST_MODE)window.__AUD=()=>({OVERS,CHASERS,HAZ,PROPS,GROUND_T,wildSpr,srng,SFX_FILES:typeof SFX_FILES!=='undefined'?SFX_FILES:null});\nif(TEST_MODE)window.__CAST=()=>({kid:[SPR.kidDown,SPR.kidUp,SPR.kidSide],peds:SPR.peds,thrower:[SPR.thrower,SPR.throwerWind],granny:[SPR.granny],dog:[SPR.dog],cow:[COW],sheep:SHEEP_FR,horse:HORSE_FR,peng:PENG_FR,gull:GULL_FR,ghost:GHOST_FR,skier:SKIER_FR,sled:[SPR.sled],cart:[CART],tug:[TUG],fork:FORK_FR,bumper:BUMPER_FR,rock:[ROCK_SPR],chasers:Object.fromEntries(Object.entries(CHASERS).map(([k,v])=>[k,v.frames]))});\n"+a,1)

# Test-only fast stepping for the audit bot: hold the real loop and step the game manually.
b="try{update(dt);draw();}catch(err){console.error(err);}"
assert s.count(b)==1
s=s.replace(b,"if(!(TEST_MODE&&window.__HOLD))try{update(dt);draw();}catch(err){console.error(err);}")
c="window.__MONEY={"
assert s.count(c)==1
s=s.replace(c,"if(TEST_MODE)window.__STEP=(n,dt,dr)=>{for(let i=0;i<n;i++){if(window.__botTick)window.__botTick();update(dt||1/30);if(dr&&i%dr===0)draw();}draw();};\n"+c)

# Test-only UI hooks for the button fuzzer: list the buttons drawn this frame, press one by id.
c2="window.__MONEY={"
s=s.replace(c2,"if(TEST_MODE)window.__UI={list:()=>ui.map(q=>q.id),rects:()=>ui.map(q=>[q.id,q.x,q.y,q.w,q.h]),press:id=>{const q=ui.find(z=>z.id===id);if(!q)return false;q.fn();return true;},get state(){return state;}};\n"+c2,1)
open(f,'w',encoding='utf-8').write(s)
