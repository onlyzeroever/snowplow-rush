import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:70],s.count(a));s=s.replace(a,b_)
# Maxed upgrades (Nov 16): a maxed upgrade used a grey "MAX", the same look as "can't afford". Now it is a reward:
# gold trim, a full gold meter, a gold MAX plate with a star and a light shine sweeping across it every few
# seconds, and a friendly "MAXED OUT!" pop instead of the error buzz. Same treatment on the in-game bar.
rep("function priceRow(","""const STAR_W=spr(["..D..",".DDD.","DDDDD",".DDD.",".D.D."],{D:'#ffffff'});
function shine(x,y,w,h,per,off){const ph=((tNow+(off||0))%per)/0.55;if(ph>1)return;const bx=Math.round(x-8+ph*(w+16));for(let r=0;r<h;r++){const sx=bx-(r>>1);for(let k=0;k<3;k++){const xx=sx+k;if(xx>=x&&xx<x+w)R(b,xx,y+r,1,1,k===1?'rgba(255,255,255,0.75)':'rgba(255,255,255,0.4)');}}}
function maxPlate(x,y,w,h,big){R(b,x+1,y,w-2,h,K);R(b,x,y+1,w,h-2,K);R(b,x+1,y+1,w-2,h-2,'#c98a12');R(b,x+1,y+1,w-2,h-3,'#f2b81a');R(b,x+2,y+2,w-4,1,'#ffe27a');R(b,x+1,y+h-2,w-2,1,'#a8740a');
  if(big){b.drawImage(STAR_W,x+Math.floor(w/2)-2,y+5);text(b,'MAX',x+w/2,y+h-12,'#ffffff',{align:'center'});}
  else{const tw=textW('MAX'),sx=Math.round(x+w/2-(tw+14)/2);R(b,sx+1,y+2,1,3,'#ffffff');R(b,sx,y+3,3,1,'#ffffff');text(b,'MAX',sx+7,y+1,'#5a3a00',{outline:null});R(b,sx+tw+12,y+2,1,3,'#ffffff');R(b,sx+tw+11,y+3,3,1,'#ffffff');}
  shine(x+1,y+1,w-2,h-2,2.8,x*0.013);}
function priceRow(""")
rep("if(lvOf(k)>=upMax(k)){sfx('deny');showToast('MAXED OUT');return;}","if(lvOf(k)>=upMax(k)){sfx('click');showToast('MAXED OUT!','#ffd23f');return;}")
# upgrades screen card
rep("card(x,y,w,h);R(b,x+4,y+4,34,36,K);R(b,x+5,y+5,32,34,'#cfe3f8');",
    "if(max)card(x,y,w,h,'#fff8e6','#f2b81a');else card(x,y,w,h);if(max)R(b,x+2,y+2,w-4,1,'#ffe9a8');R(b,x+4,y+4,34,36,K);R(b,x+5,y+5,32,34,max?'#ffefc2':'#cfe3f8');")
rep("R(b,x+43,y+15,22,9,'#13306b');text(b,'LV'+lv,x+54,y+17,'#ffffff',{align:'center',outline:null});",
    "R(b,x+43,y+15,22,9,max?K:'#13306b');if(max){R(b,x+44,y+16,20,7,'#f2b81a');R(b,x+44,y+16,20,1,'#ffe27a');}text(b,max?'MAX':'LV'+lv,x+54,y+17,max?'#5a3a00':'#ffffff',{align:'center',outline:null});")
rep("for(let p=0;p<pips;p++)R(b,x+68+p*5,y+17,4,5,p<filled?'#33b24a':'#b8c2d4');",
    "for(let p=0;p<pips;p++){if(max){R(b,x+68+p*5,y+17,4,5,'#f2b81a');R(b,x+68+p*5,y+17,4,1,'#fff08a');R(b,x+68+p*5,y+21,4,1,'#c98a12');}else R(b,x+68+p*5,y+17,4,5,p<filled?'#33b24a':'#b8c2d4');}")
rep("if(max)text(b,cur+' MAX',x+43,y+35,'#13306b',{outline:null});",
    "if(max){text(b,cur,x+43,y+35,'#13306b',{outline:null});text(b,'MAXED OUT',x+47+textW(cur),y+35,'#b07a10',{outline:null});}")
rep("if(max)button('u'+k,x+w-46,y+7,42,30,'grey','MAX',()=>sfx('deny'));",
    "if(max){maxPlate(x+w-46,y+7,42,30,true);btn('u'+k,x+w-46,y+7,42,30,()=>{sfx('click');showToast('MAXED OUT!','#ffd23f');});}")
# in-game bottom bar
rep("R(b,x+4,y+22+oy,w-8,9,K);R(b,x+5,y+23+oy,w-10,7,'#0b1838');\n    if(max)text(b,'MAX',x+w/2,y+24+oy,'#b8c2d4',{align:'center',outline:null});",
    "if(max){R(b,x+1,y+1+oy,w-2,1,'#ffd23f');R(b,x+1,y+1+oy,1,h-3,'#ffd23f');R(b,x+w-2,y+1+oy,1,h-3,'#ffd23f');maxPlate(x+4,y+22+oy,w-8,9,false);}\n    else{R(b,x+4,y+22+oy,w-8,9,K);R(b,x+5,y+23+oy,w-10,7,'#0b1838');}\n    if(max){}")
rep("text(b,'LV'+lvOf(k),x+3,y+3+oy,'#ffffff',{outline:null});if(!afford&&!max)",
    "text(b,max?'MAX':'LV'+lvOf(k),x+3,y+3+oy,max?'#ffd23f':'#ffffff',{outline:null});if(!afford&&!max)")
open(f,'w',encoding='utf-8').write(s)
print('p98 maxed upgrades look')
