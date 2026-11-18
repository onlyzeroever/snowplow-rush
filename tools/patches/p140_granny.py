import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Alex, Nov 19 02:38: the yellow outline round a granny's path looks weird; and her speech bubble shows "..."
# over her head while her words pop up as loose text somewhere else. Now: no outline; she speaks in her own
# bubble right above her head (kept on screen, tail pointing at her): "..." from afar, CLEAR MY PATH, DEAR!
# when you're close, OH, LOVELY! when the path is clear, THANKS, DEAR! at the door (the coin tip still floats up).

# update: lines go into her bubble, not floats
rep("if(nb.state==='wait'&&!nb.asked&&Math.hypot(P.x-nb.x,P.y-nb.y)<70){nb.asked=1;addFloat(clamp(nb.x,46,G.pw-46),nb.y-30,'CLEAR MY PATH, DEAR!','#ffd23f',1.8);}",
    "if(nb.sayT>0)nb.sayT-=dt;if(nb.state==='wait'&&!nb.asked&&Math.hypot(P.x-nb.x,P.y-nb.y)<110)nb.asked=1;")
rep("sfx('neighbour');addFloat(nb.x,nb.y-18,'OH, LOVELY!','#ffd23f',1.2);",
    "sfx('neighbour');nb.say='OH, LOVELY!';nb.sayT=1.4;")
rep("addFloat(nb.x,nb.y-18,'THANKS, DEAR!'+cplus(tip),'#7fe08a',1.6);",
    "nb.say='THANKS, DEAR!';nb.sayT=2;{const cp=cplus(tip).trim();if(cp)addFloat(nb.x+18,nb.y-6,cp,'#ffd23f',1.4);}")

# draw: no dashed outline round the path, no separate "..." bubble in her sprite
a=s.find("    if(nb.state==='wait'&&Math.hypot(P.x-nb.x,P.y-nb.y)<120&&Math.floor(tNow*2.5)%2===0)for(const rc of nb.rects){")
b_=s.find("ents.push({base:nb.y+1,",a)
assert a>0 and 0<b_-a<600,(a,b_)
s=s[:a]+"    "+s[b_:]
rep("if(nb.state==='wait'&&Math.floor(tNow*1.5)%2===0){R(b,nx-8,ny-26,17,9,K);R(b,nx-7,ny-25,15,7,'#ffffff');R(b,nx,ny-17,2,2,K);text(b,'...',nx,ny-24,'#13306b',{align:'center',outline:null});}","")

# she was standing behind her own house while she waited (only the bubble showed): until she leaves the house's
# footprint she is drawn in front of it, on her doorstep
rep("ents.push({base:nb.y+1,draw:()=>{",
    "if(nb.fb==null){nb.fb=nb.y+1;for(const o of G.obstacles.concat(G.scenery))if(nb.x>=o.sx&&nb.x<=o.sx+o.spr.width&&nb.y>=o.sy&&nb.y<o.base+2)nb.fb=Math.max(nb.fb,o.base+1);}\n"
    "    ents.push({base:nb.state==='done'?nb.y+1:Math.max(nb.y+1,nb.fb),draw:()=>{")

# her bubble, drawn after the scene so nothing covers it
rep("  ents.sort((a,c)=>a.base-c.base);for(const e of ents)e.draw();\n",
    "  ents.sort((a,c)=>a.base-c.base);for(const e of ents)e.draw();\n  for(const nb of G.neighbours)if(nb.y>top&&nb.y<bot)drawNbBubble(nb);\n")
rep("function sprAlpha(c){",
    "function nbLine(nb){if(nb.sayT>0&&nb.say)return nb.say;if(nb.state!=='wait')return null;if(P&&Math.hypot(P.x-nb.x,P.y-nb.y)<110)return 'CLEAR MY PATH, DEAR!';return Math.floor(tNow*1.5)%2===0?'...':null;}\n"
    "function nbBubble(nb,s2){const w=textW(s2)+8,h=11,nx=Math.round(nb.x),ny=Math.round(nb.y),bx=clamp(nx-(w>>1),2,G.pw-w-2),by=ny-30;return {x:bx,y:by,w,h,tx:clamp(nx,bx+3,bx+w-4)};}\n"
    "function drawNbBubble(nb){const s2=nbLine(nb);if(!s2)return;const r=nbBubble(nb,s2),{x,y,w,h,tx}=r;R(b,x+1,y+h,w-1,1,'rgba(30,40,80,0.25)');R(b,x,y,w,h,K);R(b,x+1,y+1,w-2,h-2,'#ffffff');\n"
    "  R(b,tx-1,y+h-1,3,1,'#ffffff');R(b,tx-2,y+h,1,1,K);R(b,tx-1,y+h,3,1,'#ffffff');R(b,tx+2,y+h,1,1,K);R(b,tx-1,y+h+1,1,1,K);R(b,tx,y+h+1,1,1,'#ffffff');R(b,tx+1,y+h+1,1,1,K);R(b,tx,y+h+2,1,1,K);\n"
    "  text(b,s2,x+(w>>1),y+3,s2==='THANKS, DEAR!'?'#1f7a33':'#13306b',{align:'center',outline:null});}\n"
    "function sprAlpha(c){")

open(f,'w',encoding='utf-8').write(s)
print('p140 granny: speaks in her own bubble above her head; no path outline')
