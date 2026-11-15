import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# PER-MACHINE UPGRADES (agreed with Alex, Nov 15): Speed, Width and Bumper belong to each machine
# and start at 0 when you buy a new one (kept if you switch back). Snow Value and Helpers stay
# global. Each machine's speed and width top out just below the next machine's starting stats,
# so a new machine is always a clear step up. 6 levels for speed and width, 5 for bumper.
# Machine speeds were spread so each step is ~15-20% faster: 32/38/44/52/62/74.
# ---------------------------------------------------------------------------------------------
# early machine prices re-simmed for per-machine upgrades (sim/econ5.py): pusher ~run 3, blower ~run 15, tractor as the Suburbs boss falls
rep("{id:'pusher', name:'PUSHER',     cost:610,     width:12, speed:34, value:1.5},","{id:'pusher', name:'PUSHER',     cost:900,     width:12, speed:38, value:1.5},")
rep("{id:'blower', name:'BLOWER',     cost:3000,   width:15, speed:38, value:2.2},","{id:'blower', name:'BLOWER',     cost:7000,   width:15, speed:44, value:2.2},")
rep("{id:'tractor',name:'TRACTOR',    cost:18000,  width:21, speed:46, value:3.2},","{id:'tractor',name:'TRACTOR',    cost:32000,  width:21, speed:52, value:3.2},")
rep("value:  {name:'SNOW VALUE', base:30,  growth:1.62, max:20, per:0.12},","value:  {name:'SNOW VALUE', base:30,  growth:1.72, max:20, per:0.12},")
rep("{id:'truck',  name:'PLOW TRUCK', cost:82000,   width:29, speed:56, value:4.5},","{id:'truck',  name:'PLOW TRUCK', cost:82000,   width:29, speed:62, value:4.5},")
rep("{id:'super',  name:'SUPER PLOW', cost:680000, width:40, speed:70, value:6.5},","{id:'super',  name:'SUPER PLOW', cost:680000, width:40, speed:74, value:6.5},")

rep("const BASE_TOOLS=6;",r"""const BASE_TOOLS=6;
const MACHINE_UPG=['speed','size','bumper'],MUP_LV=6,MUP_BUMP=5,MUP_GROWTH=1.45,MUP_COST=0.06;
const _mspec={};
function mspec(tid){if(_mspec[tid])return _mspec[tid];const i=TOOLS.findIndex(t=>t.id===tid),t=TOOLS[i];let scap,wcap,nxt;
  if(i>=0&&i<BASE_TOOLS-1){const n=TOOLS[i+1];scap=0.97*n.speed/t.speed;wcap=0.95*n.width/t.width;nxt=n.cost;}
  else if(i===BASE_TOOLS-1){scap=1.15;wcap=1.3;nxt=t.cost*4;}else{scap=1.15;wcap=1.25;nxt=t.cost*1.5;}
  return _mspec[tid]={speedPer:(scap-1)/MUP_LV,sizePer:(wcap-1)/MUP_LV,upBase:Math.max(8,Math.round(nxt*MUP_COST))};}
function mLv(tid){save.mlv=save.mlv||{};return save.mlv[tid]||(save.mlv[tid]={speed:0,size:0,bumper:0});}
function curMachine(){return TOOLS[useIdx()].id;}
function lvOf(k){return MACHINE_UPG.includes(k)?mLv(curMachine())[k]:save.lv[k];}
function upMax(k){return k==='bumper'?MUP_BUMP:MACHINE_UPG.includes(k)?MUP_LV:UPG[k].max;}
function upPer(k){const m=mspec(curMachine());return k==='speed'?m.speedPer:k==='size'?m.sizePer:k==='bumper'?0.1:UPG[k].per;}
function upName(k){return MACHINE_UPG.includes(k)?TOOLS[useIdx()].name+' '+{speed:'SPEED',size:'WIDTH',bumper:'BUMPER'}[k]:UPG[k].name;}""")

# levels in play: the current machine's own, plus the global ones
rep("function curLv(){return chal()?ZERO_LV:save.lv;}",
    "function curLv(){if(chal())return ZERO_LV;const m=mLv(curMachine());return {speed:m.speed,size:m.size,bumper:m.bumper,value:save.lv.value,helpers:save.lv.helpers};}")
rep("function bladeCells(t){t=t||tool();return Math.min(80,Math.round(t.width*(1+UPG.size.per*curLv().size)));}",
    "function bladeCells(t){t=t||tool();return Math.min(80,Math.round(t.width*(1+mspec(t.id).sizePer*(chal()?0:mLv(t.id).size))));}")
rep("function moveSpeed(){return tool().speed*(1+UPG.speed.per*curLv().speed);}",
    "function moveSpeed(){return tool().speed*(1+mspec(tool().id).speedPer*curLv().speed);}")
rep("function bumperRed(){return Math.max(0.4,1-UPG.bumper.per*curLv().bumper);}","function bumperRed(){return Math.max(0.5,1-0.1*curLv().bumper);}")
rep("function upgCost(k){return Math.floor(UPG[k].base*Math.pow(UPG[k].growth,save.lv[k]));}",
    "function upgCost(k){if(MACHINE_UPG.includes(k))return Math.floor(mspec(curMachine()).upBase*(k==='bumper'?1.2:1)*Math.pow(MUP_GROWTH,lvOf(k)));return Math.floor(UPG[k].base*Math.pow(UPG[k].growth,save.lv[k]));}")
# rubber guards grow at bumper levels 2 and 4 (out of 5)
rep("function drawGuards(g,x0,y0,w,h,horiz){const lv=curLv().bumper|0;if(lv<=0)return;const t=lv<4?1:lv<8?2:3,cw=t+1;",
    "function drawGuards(g,x0,y0,w,h,horiz){const lv=curLv().bumper|0;if(lv<=0)return;const t=lv<2?1:lv<4?2:3,cw=t+1;")
# buying
rep("const u=UPG[k];if(save.lv[k]>=u.max){sfx('deny');showToast('MAXED OUT');return;}","const u=UPG[k];if(lvOf(k)>=upMax(k)){sfx('deny');showToast('MAXED OUT');return;}")
rep("save.coins-=c;save.lv[k]++;sfx('buy');buzz(15);vcache.clear();","save.coins-=c;if(MACHINE_UPG.includes(k))mLv(curMachine())[k]++;else save.lv[k]++;sfx('buy');buzz(15);vcache.clear();")
# Upgrades screen: this machine's three first, then the two that are for every machine
rep("const rows=[['speed',SPR.boot],['size',SPR.bladeIco],['value',SPR.coinBig],['bumper',SPR.helmet],['helpers',SPR.helper]];",
    "const rows=[['speed',SPR.boot],['size',SPR.bladeIco],['bumper',SPR.helmet],['value',SPR.coinBig],['helpers',SPR.helper]];")
rep("rows.forEach(([k,ico],i)=>{const y=46+i*48,x=4,w=172,h=44;const u=UPG[k],lv=save.lv[k],max=lv>=u.max,cost=upgCost(k),afford=save.coins>=cost;",
    "rows.forEach(([k,ico],i)=>{const y=44+i*47+(i>=3?4:0),x=4,w=172,h=44;const u=UPG[k],lv=lvOf(k),max=lv>=upMax(k),cost=upgCost(k),afford=save.coins>=cost;")
rep("text(b,u.name,x+43,y+6,'#13306b',{outline:null});","text(b,upName(k),x+43,y+6,MACHINE_UPG.includes(k)?'#13306b':'#5a2a8a',{outline:null});")
rep("const pips=10,filled=Math.round(lv/u.max*pips);","const pips=10,filled=Math.round(lv/upMax(k)*pips);")
rep("const pc=(l)=>k==='bumper'?'-'+Math.round(Math.min(0.6,u.per*l)*100)+'%':'+'+Math.round(u.per*l*100)+'%';",
    "const pc=(l)=>k==='bumper'?'-'+Math.round(Math.min(0.5,0.1*l)*100)+'%':'+'+Math.round(upPer(k)*l*100)+'%';")
rep("const what={speed:'MOVE FASTER',size:'PLOW WIDER',value:'MORE COINS',bumper:'SOFTER BUMPS',helpers:'ALWAYS EARNING'}[k];",
    "const what={speed:'MOVE FASTER',size:'PLOW WIDER',value:'MORE COINS',bumper:'SOFTER BUMPS',helpers:'ALWAYS EARNING'}[k];")
# in-run strip and the results screen's next goal
rep("const max=save.lv[k]>=UPG[k].max,cost=upgCost(k),afford=!max&&save.coins>=cost;","const max=lvOf(k)>=upMax(k),cost=upgCost(k),afford=!max&&save.coins>=cost;")
rep("text(b,'LV'+save.lv[k],x+3,y+3+oy,'#ffffff',{outline:null});","text(b,'LV'+lvOf(k),x+3,y+3+oy,'#ffffff',{outline:null});")
rep("for(const k in UPG){const lv=save.lv[k];if(lv>=UPG[k].max)continue;opts.push({need:upgCost(k)-c,label:UPG[k].name+' LV'+(lv+1),go:goUpgrades});}",
    "for(const k in UPG){const lv=lvOf(k);if(lv>=upMax(k))continue;opts.push({need:upgCost(k)-c,label:upName(k)+' LV'+(lv+1),go:goUpgrades});}")
# the job checker uses each machine's own increments
rep("const bw=Math.min(80,Math.round(T.width*(1+UPG.size.per*(lvSize||0))))*2,sp=T.speed*(1+UPG.speed.per*(lvSpeed||0));",
    "const ms2=mspec(T.id),bw=Math.min(80,Math.round(T.width*(1+ms2.sizePer*Math.min(MUP_LV,lvSize||0))))*2,sp=T.speed*(1+ms2.speedPer*Math.min(MUP_LV,lvSpeed||0));")
# a New Winter resets every machine's upgrades too
rep("lv:{speed:0,size:0,value:0,bumper:0,helpers:0},stars:Array(NL).fill(0),best:Array(NL).fill(0),winterCoins:0,",
    "lv:{speed:0,size:0,value:0,bumper:0,helpers:0},mlv:{},stars:Array(NL).fill(0),best:Array(NL).fill(0),winterCoins:0,")
# old saves: speed/width/bumper were global; refund what they cost so players can buy the new ones
rep("for(const k of ['stars','best','fails']){const a=Array(NL).fill(0);(s[k]||[]).forEach((v,i)=>{if(i<NL)a[i]=v;});save[k]=a;}}}catch(e){}}",
    r"""for(const k of ['stars','best','fails']){const a=Array(NL).fill(0);(s[k]||[]).forEach((v,i)=>{if(i<NL)a[i]=v;});save[k]=a;}
  if(!s.mlv){const OLD={speed:[25,1.62],size:[35,1.64],bumper:[60,1.7]};let refund=0;for(const k in OLD){const n=save.lv[k]|0;for(let l=0;l<n;l++)refund+=Math.floor(OLD[k][0]*Math.pow(OLD[k][1],l));save.lv[k]=0;}
    save.mlv={};if(refund>0){save.coins+=refund;save.upgRefund=refund;}}}}catch(e){}}""")
rep("const save={coins:0,tool:0,lv:{speed:0,size:0,value:0,bumper:0,helpers:0},","const save={coins:0,tool:0,mlv:{},lv:{speed:0,size:0,value:0,bumper:0,helpers:0},")
# tell refunded players once, on the map
rep("function drawWorld(dt){",
    "function drawRefundNote(){if(!save.upgRefund||overlayOpen())return;panel(14,96,152,86,'#13306b','#ffd23f');text(b,'NEW: MACHINE UPGRADES',W/2,104,'#ffd23f',{align:'center'});\n"
    "  text(b,'SPEED, WIDTH AND BUMPER NOW',W/2,118,'#ffffff',{align:'center',outline:null});text(b,'BELONG TO EACH MACHINE.',W/2,127,'#ffffff',{align:'center',outline:null});\n"
    "  text(b,'WE REFUNDED YOUR OLD ONES:',W/2,140,'#9fc0e8',{align:'center',outline:null});b.drawImage(SPR.coin,W/2-26,150);text(b,'+'+fmt(save.upgRefund),W/2-14,151,'#ffd23f',{scale:2});\n"
    "  button('refundok',54,166,72,14,'green','GREAT!',()=>{save.upgRefund=0;sfx('buy');persist();});}\nfunction drawWorld(dt){")
rep("b.restore();clipUI(uiFrom,MAP_VY,MAP_VY+MAP_VH);drawBiomeRail(oy);}","b.restore();clipUI(uiFrom,MAP_VY,MAP_VY+MAP_VH);drawBiomeRail(oy);drawRefundNote();}")
rep("upg:{buyUpg,","upg:{lvOf,upMax,mLv,mspec,curMachine,buyUpg,")
rep("PROTOTYPE V0.7.8","PROTOTYPE V0.8.0")
open(f,'w',encoding='utf-8').write(s);print('p45 ok')
