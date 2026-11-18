import sys,re
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
def refn(name,body):
    global s;i=s.find('function %s(){'%name);assert i>=0 and s.count('function %s('%name)==1,name;j=s.find('return c;}',i)+10;s=s[:i]+body+s[j:]
# Alex, Nov 19 02:38: "you told me you revamped every asset, but the trolley wasn't - what else did you miss?"
# The art pass covered map props, buildings and landmarks. Things drawn apart from that (movers, pickups, a few junk props)
# kept their first-draft art. Census of every sprite drawn in a job (tools/audit/spritecensus.js) -> these were below
# the standard and are redrawn at the same size (same collision boxes):
#  farm tractor + hay trailer (crossing), sled train (crossing), airport baggage tug, hay bale, tyre stack, sledging kid,
#  stadium mascot, tennis balls from the ball machine, buried presents (were a lone bow on the snow).

refn('crossSprite',"""function crossSprite(){const c=mk(44,16),g=c.getContext('2d');
  // flatbed trailer with hay bales
  R(g,0,9,25,4,K);R(g,1,10,23,2,'#a8673a');R(g,1,10,23,1,'#c98d4a');R(g,24,10,4,2,K);
  const bale=(x,y,w)=>{R(g,x,y,w,6,K);R(g,x+1,y+1,w-2,4,'#e8c87a');R(g,x+1,y+1,w-2,1,'#f6e0a0');R(g,x+1,y+4,w-2,1,'#c9a85a');for(let k=x+2;k<x+w-2;k+=2)R(g,k,y+2+(k&1),1,1,'#d8b060');R(g,x+Math.round(w/3),y+1,1,4,'#8a5a34');R(g,x+Math.round(2*w/3),y+1,1,4,'#8a5a34');};
  bale(1,4,12);bale(12,4,12);bale(6,0,12);
  for(const wx of [5,18]){g.fillStyle=K;pixCircle(g,wx,13,2);R(g,wx,13,1,1,'#8793a8');}
  // tractor: cab, long green bonnet, exhaust, big back wheel, small front wheel
  R(g,33,5,10,6,K);R(g,34,6,8,4,'#33b24a');R(g,34,6,8,1,'#7fe08a');R(g,34,9,8,1,'#1f7a33');R(g,36,7,5,1,'#1f7a33');R(g,42,7,2,3,K);R(g,42,8,1,1,'#ffe9a8');
  R(g,38,0,2,6,K);R(g,38,0,2,1,'#55607a');
  R(g,25,0,10,10,K);R(g,26,1,8,1,'#33b24a');R(g,26,2,8,4,'#cfe9f7');R(g,27,2,2,4,'#ffffff');R(g,26,6,8,3,'#33b24a');R(g,26,8,8,1,'#1f7a33');
  g.fillStyle=K;pixCircle(g,30,10,5);g.fillStyle='#2a2a36';pixCircle(g,30,10,4);g.fillStyle='#ffc727';pixCircle(g,30,10,2);R(g,30,10,1,1,'#c98a12');
  for(const [dx,dy] of [[0,-4],[4,0],[0,4],[-4,0],[3,-3],[3,3],[-3,3],[-3,-3]])R(g,30+dx,10+dy,1,1,'#55586a');
  g.fillStyle=K;pixCircle(g,40,12,3);g.fillStyle='#2a2a36';pixCircle(g,40,12,2);R(g,40,12,1,1,'#ffc727');return c;}""")

refn('sledSprite',"""function sledSprite(){const c=mk(70,16),g=c.getContext('2d');
  const box=(x,y,w,h,col,rib)=>{R(g,x,y,w,h,K);R(g,x+1,y+1,w-2,h-2,col);R(g,x+1,y+1,w-2,1,'rgba(255,255,255,0.45)');R(g,x+(w>>1),y+1,1,h-2,rib);R(g,x+1,y+(h>>1),w-2,1,rib);};
  const cols=[['#e03a4e','#ffd23f'],['#3f86d6','#f4f8ff'],['#33b24a','#e03a4e']];
  for(let k=0;k<3;k++){const x=k*15;
    R(g,x,14,14,1,K);R(g,x+1,13,12,1,'#c6d0e0');R(g,x+13,11,2,3,K);R(g,x+13,11,1,2,'#c6d0e0');R(g,x+3,12,1,1,K);R(g,x+10,12,1,1,K);
    R(g,x,9,14,3,K);R(g,x+1,10,12,1,'#c98d4a');R(g,x+1,9,12,1,'#e8b070');
    box(x+1,4,6,6,cols[k][0],cols[k][1]);box(x+7,2,6,8,cols[(k+1)%3][0],cols[(k+1)%3][1]);
    R(g,x+14,10,1,1,'#55321d');}
  R(g,45,10,3,1,'#55321d');
  // snowmobile with a rider
  R(g,47,10,12,5,K);R(g,48,11,10,3,'#2a2a36');for(let x=48;x<58;x+=2)R(g,x,14,1,1,'#55586a');
  R(g,58,14,12,1,K);R(g,59,13,10,1,'#c6d0e0');R(g,68,11,2,3,K);
  R(g,48,6,20,6,K);R(g,49,7,18,4,'#d8364b');R(g,49,7,18,1,'#ff6a7a');R(g,49,10,18,1,'#a82639');R(g,66,8,2,2,'#ffe9a8');
  R(g,62,2,4,5,K);R(g,63,3,2,3,'#8fd3ff');R(g,50,5,8,2,K);R(g,51,5,6,1,'#2a2a36');
  R(g,53,0,6,4,K);R(g,54,1,4,2,'#3f86d6');R(g,57,1,1,2,'#cfe9f7');R(g,52,3,6,4,K);R(g,53,4,4,2,'#2f5fae');R(g,57,4,5,1,K);return c;}""")

refn('tugSprite',"""function tugSprite(){const c=mk(32,12),g=c.getContext('2d');
  const bag=(x,y,w,h,col)=>{R(g,x,y,w,h,K);R(g,x+1,y+1,w-2,h-2,col);R(g,x+1,y+1,w-2,1,'rgba(255,255,255,0.4)');R(g,x+(w>>1)-1,y-1,2,1,K);};
  for(const [cx,a,b2] of [[0,'#3f86d6','#e03a4e'],[11,'#ffc727','#33b24a']]){R(g,cx,7,10,3,K);R(g,cx+1,8,8,1,'#8793a8');R(g,cx+1,10,2,2,K);R(g,cx+7,10,2,2,K);bag(cx+1,2,4,5,a);bag(cx+5,3,4,4,b2);R(g,cx+10,8,1,1,K);}
  R(g,21,3,11,7,K);R(g,22,4,9,5,'#ffc727');R(g,22,4,9,1,'#ffe27a');R(g,22,8,9,1,'#e29a1c');R(g,30,5,1,2,'#ffe9a8');
  R(g,22,0,6,4,K);R(g,23,1,4,3,'#8fd3ff');R(g,23,1,1,3,'#ffffff');R(g,24,0,2,1,'#f07a1a');
  R(g,22,9,4,3,K);R(g,23,10,2,1,'#55586a');R(g,28,9,4,3,K);R(g,29,10,2,1,'#55586a');return c;}""")

refn('haySprite',"""function haySprite(){const c=mk(12,8),g=c.getContext('2d');R(g,1,0,10,8,K);R(g,0,1,12,6,K);R(g,1,1,10,6,'#e8c87a');R(g,1,1,10,1,'#f6e0a0');R(g,1,6,10,1,'#c9a85a');
  for(let y=2;y<6;y++)for(let x=1;x<11;x+=2)R(g,x+(y&1),y,1,1,y&1?'#d8b060':'#f0d48a');R(g,3,1,1,6,'#8a5a34');R(g,8,1,1,6,'#8a5a34');R(g,1,1,1,1,'#fff3c8');return c;}""")

refn('tireSprite',"""function tireSprite(){return spr(["..KKKKKKK..",".KUUUUUUUK.","KUUKKKKKUUK","KUUUKKKUUUK","KXUUUUUUUXK","KXXXXXXXXXK","KXuXuXuXuXK","KKKKKKKKKKK","KXXXXXXXXXK","KXuXuXuXuXK",".KKKKKKKKK."],{U:'#6b6f82',X:'#33364a',u:'#5a5e74'});}""")

rep("""SPR.sled=spr(["......KKK.......",".....KPZPK......",".....KSSSK......","....KDDDDDK.....","...KBBBBBBBK..KK","KKKKKKKKKKKKKKRK","KRRRRRRRRRRRRRRK",".KrrrrrrrrrrrrK.","..KcKKKKKKKKcK.."],{P:'#9b5fd6',Z:'#ffffff',D:'#ffc727',c:'#8793a8'});""",
    """SPR.sled=spr(["......Z.........",".....KRK........","....KRRRK.......","....KSKSK.......","...KYYYYKK......","..KBBBBBBBKK..K.","KKKKKKKKKKKKKKKK","KLLLLLLLLLLLLLLK",".KcK.......KcKK."],{R:'#e03a4e',Z:'#ffffff',Y:'#ffc727',L:'#c98d4a',c:'#8793a8'});""")

rep("""MASCOT=spr(["..KKKK..",".KYYYYK.","KYKYYKYK","KYYYYYYK",".KRRRRK.","KRRRRRRK","KRRRRRRK",".KJ..JK.",".KK..KK."]);""",
    """MASCOT=spr(["..KK..KK..",".KYYKKYYK.",".KYYYYYYK.","KYKYYYYKYK","KYYYKKYYYK",".KYYYYYYK.","KRRZRRZRRK","KRRRZZRRRK",".KRRKKRRK.",".KKK..KKK."],{Y:'#c98d4a',Z:'#ffffff'});""")

# tennis balls: a round lime ball with a seam, not a 4 px square
rep("R(b,sx-2,sy2+1,4,1,'rgba(27,31,59,0.25)');R(b,sx-2,sy2-3,4,4,K);R(b,sx-1,sy2-2,2,2,'#d7f03a');",
    "R(b,sx-2,sy2+2,5,1,'rgba(27,31,59,0.25)');R(b,sx-1,sy2-3,3,1,K);R(b,sx-2,sy2-2,5,3,K);R(b,sx-1,sy2+1,3,1,K);R(b,sx-1,sy2-2,3,3,'#d7f03a');R(b,sx-1,sy2-2,1,1,'#f4ffb0');R(b,sx,sy2-1,2,1,'#ffffff');")

# buried presents: a gift box poking out of the snow (with a glint), not a lone bow
rep("b.drawImage(SPR.bow,pr.x-4,pr.y-3-bob);",
    "b.drawImage(giftSnowSpr(),pr.x-6,pr.y-7);if(bob&&Math.floor(tNow*2+pr.x)%3===0){R(b,pr.x+4,pr.y-9,1,3,'#ffffff');R(b,pr.x+3,pr.y-8,3,1,'#ffffff');}")
rep("function sprAlpha(c){",
    "function giftSnowSpr(){if(giftSnowSpr.c)return giftSnowSpr.c;const c=mk(12,10),g=c.getContext('2d');R(g,2,3,8,5,K);R(g,3,4,6,3,'#e03a4e');R(g,3,4,6,1,'#ff7a8a');R(g,5,3,2,5,K);R(g,5,4,2,3,'#ffd23f');\n"
    "  R(g,1,0,4,3,K);R(g,2,1,2,1,'#ffd23f');R(g,7,0,4,3,K);R(g,8,1,2,1,'#ffd23f');R(g,4,1,4,2,K);R(g,5,1,2,1,'#ffd23f');R(g,1,7,10,1,'#f4f8ff');R(g,0,8,12,2,'#f4f8ff');R(g,0,9,12,1,'#c6d9f3');R(g,2,7,2,1,'#ffffff');giftSnowSpr.c=c;return c;}\n"
    "function sprAlpha(c){")

open(f,'w',encoding='utf-8').write(s)
print('p142 movers art: tractor+trailer, sled train, baggage tug, hay, tyres, sledging kid, mascot, tennis balls, buried presents')
