# weekly challenge: upgrades are off, so the in-run bar is locked and buying is refused (it used to charge you for nothing)
import sys
p=sys.argv[1];s=open(p).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)
rep("function buyUpg(k){const u=UPG[k];",
    "function buyUpg(k){if(chal()){sfx('deny');showToast('NO UPGRADES IN THE WEEKLY','#ff9aa8');return;}const u=UPG[k];")
rep("  const defs=[['speed','SPEED','blue',SPR.boot],['size','SIZE','green',SPR.bladeIco],['value','VALUE','purple',SPR.coinBig]];\n",
    "  const defs=[['speed','SPEED','blue',SPR.boot],['size','SIZE','green',SPR.bladeIco],['value','VALUE','purple',SPR.coinBig]];\n"
    "  if(chal()){defs.forEach(([k,label,col,ico],i)=>{const x=3+i*59,y=y0+3,w=56,h=34;R(b,x,y,w,h,K);R(b,x+1,y+1,w-2,h-2,'#3a4462');b.globalAlpha=0.45;b.drawImage(ico,x+w/2-Math.floor(ico.width/2),y+3);b.globalAlpha=1;\n"
    "      text(b,label,x+w/2,y+14,'#9aa6bc',{align:'center',outline:null});b.drawImage(SPR.lock,x+w/2-3,y+23);});\n"
    "    if(run&&run.time>G.def.time-4){const t='WEEKLY: SAME LOANER, NO UPGRADES',tw=textW(t)+8;R(b,Math.round(W/2-tw/2),y0-11,tw,10,K);R(b,Math.round(W/2-tw/2)+1,y0-10,tw-2,8,'#5c0e1e');text(b,t,W/2,y0-9,'#ffd23f',{align:'center',outline:null});}return;}\n")
open(p,'w').write(s);print('p6 ok')
