import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Two strikes for the combo (Alex, Nov 16). A bump used to wipe the combo. Now the first bump halves it and the bar
# blinks CAREFUL! for COMBO_CRACK seconds; a second bump inside that window wipes it. The fade timer is topped up to
# cover the stun, so the bounce itself doesn't end the combo. Same rule for props and hazards.
# Combo model (tools/sim/combo): about +2.4% coins at 8 bumps a run; most combos still end from the 0.75 s fade.
rep("const COMBO_MAX=20,COMBO_KEEP=0.75;","const COMBO_MAX=20,COMBO_KEEP=0.75,COMBO_CRACK=3;")
rep("if(run.combo>=2)run.cBonk=(run.cBonk||0)+1;run.combo=0;run.comboProg=0;run.hits++;",
    "if(run.combo>=2&&!(run.crackT>0)){run.combo=Math.floor(run.combo/2);run.comboProg=0;run.crackT=COMBO_CRACK;run.comboT=Math.max(run.comboT,COMBO_KEEP+P.stun);run.cHalf=(run.cHalf||0)+1;sfx('cfade');}"
    "else{if(run.combo>=2){run.cBonk=(run.cBonk||0)+1;sfx('cend');if(run.combo>=5)addFloat(P.x,P.y-30,'COMBO LOST','#ff8a98',1.0);}run.combo=0;run.comboProg=0;run.crackT=0;}run.hits++;")
rep("run.comboT-=dt;if(run.comboT<=0&&run.combo>0){",
    "if(run.crackT>0)run.crackT=Math.max(0,run.crackT-dt);run.comboT-=dt;if(run.comboT<=0&&run.combo>0){run.crackT=0;")
# HUD: while cracked, the combo text and bar blink red/white and CAREFUL! shows under the bar
rep("text(b,'x'+m+' COMBO!',W/2,VIEW_Y+10-Math.min(2,bounce),run.combo>=10?'#ffd23f':'#ff4fa3',{align:'center',scale:2});{const k=clamp(run.comboT/COMBO_KEEP,0,1),bw2=60;R(b,W/2-bw2/2-1,VIEW_Y+24,bw2+2,4,K);R(b,W/2-bw2/2,VIEW_Y+25,Math.round(bw2*k),2,k<0.35?'#ff6a7a':run.combo>=10?'#ffd23f':'#ff4fa3');}}",
    "const crk=run.crackT>0,blink=crk&&Math.floor(tNow*8)%2===0;"
    "text(b,'x'+m+' COMBO!',W/2,VIEW_Y+10-Math.min(2,bounce),blink?'#ffffff':crk?'#ff4a5a':run.combo>=10?'#ffd23f':'#ff4fa3',{align:'center',scale:2});{const k=clamp(run.comboT/COMBO_KEEP,0,1),bw2=60;R(b,W/2-bw2/2-1,VIEW_Y+24,bw2+2,4,K);R(b,W/2-bw2/2,VIEW_Y+25,Math.round(bw2*k),2,blink?'#ffffff':crk?'#ff4a5a':k<0.35?'#ff6a7a':run.combo>=10?'#ffd23f':'#ff4fa3');"
    "if(crk){for(const [cx2,cy2] of [[-9,0],[-8,1],[-7,0],[6,1],[7,0],[8,1]])R(b,W/2+cx2,VIEW_Y+25+cy2,1,1,K);text(b,'CAREFUL!',W/2,VIEW_Y+31,blink?'#ffffff':'#ff8a98',{align:'center'});}}}")
rep("track('job_end',Object.assign(phJob(),{combo_best:","track('job_end',Object.assign(phJob(),{combo_halved:run.cHalf||0,combo_best:")
open(f,'w',encoding='utf-8').write(s)
print('p118 combo: two strikes (halve, then wipe within %ss)'%3)
