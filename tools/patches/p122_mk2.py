import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Mk II (Alex, Nov 17): once a machine's SPEED and SIZE are both maxed, one last upgrade turns it into the Mk II:
# +8% speed and +10% coins with that machine, a gold "II" badge on its sprite and "MK II" after its name.
# It costs 2.5x the last speed level, so each machine gets one more goal. Not in the weekly challenge.
MK2_SPEED=1.08; MK2_COINS=1.10
rep("function mLv(tid){",
    "const MK2_SPEED=%s,MK2_COINS=%s;\n"
    "function isMk2(tid){return !!(save.mk2&&save.mk2[tid]);}\n"
    "function mk2Cost(tid){return Math.floor(mspec(tid).upBase*Math.pow(MUP_GROWTH,MUP_LV)*2.5);}\n"
    "function mk2Ready(){const id=curMachine(),m=mLv(id);return !chal()&&m.speed>=MUP_LV&&m.size>=MUP_LV&&!isMk2(id);}\n"
    "function buyMk2(){const id=curMachine(),c=mk2Cost(id);if(!mk2Ready())return;if(save.coins<c){sfx('deny');showToast('NEED '+fmt(c)+' COINS','#ff9aa8');return;}\n"
    "  save.coins-=c;save.mk2=save.mk2||{};save.mk2[id]=true;_tc.k='';vcache.clear();sfx('fanfare');buzz(30);showToast(TOOLS[toolIdx(id)].name+' MK II!','#ffd23f');track('upgrade_buy',{upgrade:'mk2',machine:id,cost:c});persist();}\n"
    "function mLv(tid){"%(MK2_SPEED,MK2_COINS))
rep("function moveSpeed(){return tool().speed*(1+mspec(tool().id).speedPer*curLv().speed);}",
    "function moveSpeed(){return tool().speed*(1+mspec(tool().id).speedPer*curLv().speed)*(isMk2(tool().id)&&!chal()&&!drv()&&!msn()?MK2_SPEED:1);}")
rep("function valueMult(){return tool().value*(1+UPG.value.per*curLv().value)",
    "function valueMult(){return tool().value*(isMk2(tool().id)&&!chal()?MK2_COINS:1)*(1+UPG.value.per*curLv().value)")
# sprite: a gold II badge on the rear of the body
rep("const key=tid+'|'+bw+'|'+pl+'|'+(fr%2)+'|'+save.outfit+save.hat+'|'+si+'|'+(isGold(tid)?1:0);",
    "const key=tid+'|'+bw+'|'+pl+'|'+(fr%2)+'|'+save.outfit+save.hat+'|'+si+'|'+(isGold(tid)?1:0)+(isMk2(tid)?'m':'');")
rep("if(pl>0&&sp.bt&&tid!=='rotary')drawPile(g,ox,oy-sp.hh-sp.bt,bw-4,pileH,'up');",
    "if(pl>0&&sp.bt&&tid!=='rotary')drawPile(g,ox,oy-sp.hh-sp.bt,bw-4,pileH,'up');\n"
    "  if(isMk2(tid)){const bx=ox-4,by=oy+sp.hh-9;R(g,bx,by,9,6,K);R(g,bx+1,by+1,7,4,'#ffd23f');R(g,bx+1,by+1,7,1,'#fff3a0');R(g,bx+3,by+2,1,3,'#8a5a00');R(g,bx+5,by+2,1,3,'#8a5a00');}")
# names
rep("text(b,(gold?'GOLDEN ':'')+t.name,x+37,y+5,","text(b,(gold?'GOLDEN ':'')+t.name+(isMk2(t.id)?' MK II':''),x+37,y+5,")
# Upgrades screen: the SPEED row offers the Mk II once speed and size are maxed, and shows it once owned
rep("const what={speed:'MOVE FASTER',size:'PLOW WIDER',value:'MORE COINS',bumper:'SOFTER BUMPS',helpers:'ALWAYS EARNING'}[k];",
    "const mkr=k==='speed'&&max&&mk2Ready(),mko=k==='speed'&&isMk2(curMachine());\n"
    "    const what=mkr?'MK II IS READY!':mko?'MK II: +8% SPEED':{speed:'MOVE FASTER',size:'PLOW WIDER',value:'MORE COINS',bumper:'SOFTER BUMPS',helpers:'ALWAYS EARNING'}[k];")
rep("text(b,what,x+43,y+27,'#4f6fa0',{outline:null});","text(b,what,x+43,y+27,mkr||mko?'#b07a10':'#4f6fa0',{outline:null});")
rep("if(max){text(b,cur,x+43,y+35,'#13306b',{outline:null});text(b,'MAXED OUT',x+47+textW(cur),y+35,'#b07a10',{outline:null});}",
    "if(mkr)text(b,'+8% SPEED, +10% COINS',x+43,y+35,'#1f8a3a',{outline:null});\n"
    "    else if(max){text(b,cur,x+43,y+35,'#13306b',{outline:null});text(b,mko?'AND +10% COINS':'MAXED OUT',x+47+textW(cur),y+35,'#b07a10',{outline:null});}")
rep("if(max){maxPlate(x+w-46,y+7,42,30,true);btn('u'+k,x+w-46,y+7,42,30,()=>{sfx('click');showToast('MAXED OUT!','#ffd23f');});}",
    "if(mkr){const mc=mk2Cost(curMachine());button('umk2',x+w-46,y+7,42,30,save.coins>=mc?'gold':'grey',null,buyMk2);text(b,'MK II',x+w-25,y+12,'#ffffff',{align:'center'});priceRow(SPR.coinS,fmt(mc),x+w-25,y+24,save.coins>=mc?'#ffffff':'#ffd0d6');}\n"
    "    else if(max){maxPlate(x+w-46,y+7,42,30,true,mko?'MK II':null);btn('u'+k,x+w-46,y+7,42,30,()=>{sfx('click');showToast(mko?'MK II: FULLY UPGRADED':'MAXED OUT!','#ffd23f');});}")
rep("function maxPlate(x,y,w,h,big){","function maxPlate(x,y,w,h,big,lbl){")
rep("if(big){b.drawImage(STAR_W,x+Math.floor(w/2)-2,y+5);text(b,'MAX',x+w/2,y+h-12,'#ffffff',{align:'center'});}","if(big){b.drawImage(STAR_W,x+Math.floor(w/2)-2,y+5);text(b,lbl||'MAX',x+w/2,y+h-12,'#ffffff',{align:'center'});}")
# Upgrades screen: long machine names ran under the BUY button ("ROTARY BLOWER SPEE"); use a short name when needed
rep("function upName(k){return MACHINE_UPG.includes(k)?TOOLS[useIdx()].name+' '+",
    "const SHORT_NAME={rotary:'ROTARY',monster:'MONSTER',dragon:'DRAGON',mech:'MECH',jet:'JET TRUCK',super:'SUPER PLOW',truck:'PLOW TRUCK'};\n"
    "function upName(k){if(MACHINE_UPG.includes(k)){const t=TOOLS[useIdx()],sfx2={speed:'SPEED',size:'WIDTH',bumper:'BUMPER'}[k],full=t.name+' '+sfx2;return textW(full)<=80?full:(SHORT_NAME[t.id]||t.name.split(' ')[0])+' '+sfx2;}return upNameOld(k);}\n"
    "function upNameOld(k){return MACHINE_UPG.includes(k)?TOOLS[useIdx()].name+' '+")
open(f,'w',encoding='utf-8').write(s)
print('p122 Mk II: +8% speed, +10% coins, badge, upgrade in the SPEED row')
