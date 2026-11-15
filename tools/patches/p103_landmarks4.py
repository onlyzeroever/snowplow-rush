import sys,re
f=sys.argv[1];s=open(f,encoding='utf-8').read()
a0=s.index('function lmArt(');a1=s.index('\n  default:return false;}',a0)
body=s[a0:a1]
def case(cid,new):
    global body
    head="case '%s':"%cid
    assert body.count(head)==1,cid
    p=body.index(head);m=re.compile(r"case '[a-z0-9_]+':").search(body,p+len(head))
    e=m.start() if m else len(body)
    tail=body[p:e];ws=tail[len(tail.rstrip()):]
    body=body[:p]+new+(ws if m else '')+body[e:]
# Landmarks audit, part 4 (Nov 16): the 35 map landmarks that still graded B against the redrawn ones.
N={}
N['stables']="""case 'stables':{shadow(32);B(x-15,y-3,30,12,'#a8673a');for(let k=0;k<28;k+=3)R(g,x-14+k,y-2,1,10,'#94592f');roof(x,y-10,32,8,'#7a4a2a');R(g,x-2,y-15,4,4,K);R(g,x-1,y-14,2,2,'#f4f8ff');R(g,x,y-18,1,3,K);R(g,x-1,y-18,3,1,'#ffd23f');
  for(let k=0;k<4;k++){const dx=x-12+k*7;R(g,dx,y+1,5,8,K);R(g,dx+1,y+2,3,2,'#3a2414');R(g,dx+1,y+5,3,3,'#55321d');R(g,dx+1,y+4,3,1,'#c98d4a');}
  R(g,x-11,y+1,3,3,'#7a4a2a');R(g,x-11,y+1,1,1,K);R(g,x+3,y+1,3,3,'#e8e0d0');R(g,x+5,y+1,1,1,K);R(g,x+15,y+5,6,5,K);R(g,x+16,y+6,4,3,'#e8c87a');R(g,x+17,y+6,1,3,'#8a5a34');}break;"""
N['farmcafe']="""case 'farmcafe':{shadow(30);B(x-14,y-4,20,13,'#f4e3c4');for(const bx of [-10,-2])R(g,x+bx,y-3,1,12,'#8a5a34');R(g,x-13,y+1,18,1,'#8a5a34');roof(x-4,y-11,24,8,'#2f8a5a');
  R(g,x-9,y-2,5,4,K);R(g,x-8,y-1,3,2,'#ffe27a');R(g,x-9,y+2,5,1,'#d8364b');R(g,x-1,y+2,4,7,K);R(g,x,y+3,2,6,'#7a4a2a');mStall(g,x+5,y+1,'#d8364b');for(const [a,c] of [[5,'#f07a1a'],[8,'#f07a1a'],[11,'#33b24a'],[14,'#f07a1a']])C(x+a,y+12,1,c);}break;"""
N['maze']="""case 'maze':{const M=['##############','#....#.......#','#.##.#.#####.#','#.#..#.#...#.#','#.#.##.#.#.#.#','#.#....#.#...#','#.######.###.#','#............#','######.#######'];R(g,x-15,y-10,30,20,K);
  for(let r=0;r<M.length;r++)for(let k=0;k<14;k++){const px=x-14+k*2,py=y-9+r*2;if(M[r][k]==='#'){R(g,px,py,2,2,'#2f8a4a');R(g,px,py,2,1,(k+r)%3?'#4fae62':MC.snow);if(r+1<M.length&&M[r+1][k]==='.')R(g,px,py+1,2,1,'#1d5e34');}else R(g,px,py,2,2,'#c2ad80');}
  R(g,x-1,y-3,3,3,K);R(g,x,y-3,1,2,'#c6ccd8');}break;"""
N['mill']="""case 'mill':{shadow(30);B(x-14,y-6,18,16,'#c6b49a');for(let yy=y-4;yy<y+9;yy+=3)for(let xx=x-13+(((yy-y)>>1)&1)*2;xx<x+3;xx+=4)R(g,xx,yy,3,1,'#ab9a7c');roof(x-5,y-13,22,7,'#7a4a2a');R(g,x-10,y-1,4,4,K);R(g,x-9,y,2,2,'#ffe27a');R(g,x-3,y+3,4,7,K);R(g,x-2,y+4,2,6,'#55321d');
  ice(x+2,y+8,16,4);R(g,x+3,y+9,4,1,'#e8f6ff');C(x+10,y+1,6,'#6b4426');g.fillStyle='#a8743f';pixCircle(g,x+10,y+1,5);g.fillStyle='#6b4426';pixCircle(g,x+10,y+1,3);
  for(let k=0;k<8;k++){const t=k/8*Math.PI*2;for(let d=2;d<6;d++)R(g,x+10+Math.round(Math.cos(t)*d),y+1+Math.round(Math.sin(t)*d),1,1,'#55321d');}R(g,x+9,y,3,3,K);R(g,x+10,y+1,1,1,'#c6ccd8');}break;"""
N['treefarm']="""case 'treefarm':{for(let k=0;k<6;k++)pine(x-14+(k%3)*9,y+(k<3?1:10),9+((k*7)%3));R(g,x+9,y-1,10,7,K);R(g,x+10,y,8,5,'#c98d4a');R(g,x+10,y,8,1,MC.snow);R(g,x+12,y+2,4,1,'#2f8a5a');R(g,x+13,y+6,1,5,K);R(g,x+16,y+6,1,5,K);
  R(g,x+8,y+9,11,3,K);R(g,x+9,y+10,9,1,'#d8364b');pine(x+13,y+10,5);}break;"""
N['harvestfair']="""case 'harvestfair':{mTent(g,x-15,y-9,18,18,'#d8364b','#f4f8ff');mTent(g,x+2,y-5,14,14,'#ffc727','#f4f8ff');R(g,x-16,y-13,33,1,K);for(let k=0;k<8;k++){const fx=x-15+k*4;R(g,fx,y-12,3,1,['#d8364b','#3f86d6','#ffc727','#4fd36a'][k%4]);R(g,fx+1,y-11,1,1,['#d8364b','#3f86d6','#ffc727','#4fd36a'][k%4]);}
  for(const [a,b2] of [[-3,9],[0,10],[3,9]])C(x+a,y+b2,2,'#f07a1a');R(g,x,y+6,1,2,'#2f8a5a');R(g,x+12,y+8,6,4,K);R(g,x+13,y+9,4,2,'#e8c87a');}break;"""
N['cityhall']="""case 'cityhall':{shadow(32);B(x-15,y-3,30,12,'#e8dcc4');for(let k=0;k<6;k++){R(g,x-13+k*5,y-1,2,9,'#fbf6e8');R(g,x-12+k*5,y-1,1,9,'#c6b49a');}R(g,x-15,y-3,30,2,'#c6b49a');
  for(let r=0;r<6;r++){const hw=Math.round((r+1)/6*16);R(g,x-hw-1,y-9+r,hw*2+2,1,K);R(g,x-hw,y-9+r,hw*2,1,r<2?MC.snow:'#e8dcc4');}
  R(g,x-15,y+8,30,3,K);R(g,x-14,y+8,28,1,'#e3e9f2');R(g,x-13,y+9,26,1,'#c6ccd8');
  R(g,x-4,y-17,9,8,K);R(g,x-3,y-16,7,6,'#e8dcc4');C(x+1,y-13,2,'#f4f8ff');R(g,x+1,y-14,1,2,K);R(g,x-3,y-20,7,3,K);R(g,x-2,y-19,5,2,'#5fa89a');pole(x+1,y-26,6,'#3f86d6');}break;"""
N['chinatown']="""case 'chinatown':{shadow(32);for(const px of [-13,10]){R(g,x+px,y-6,4,16,K);R(g,x+px+1,y-6,2,15,'#d8364b');R(g,x+px+1,y-6,1,15,'#ff6a7a');R(g,x+px-1,y+8,6,3,K);R(g,x+px,y+9,4,1,'#c6ccd8');}
  R(g,x-16,y-9,32,4,K);R(g,x-15,y-8,30,2,'#d8364b');R(g,x-6,y-8,12,2,'#ffd23f');R(g,x-5,y-8,10,1,K);
  for(let r=0;r<5;r++){const hw=12+r*2;R(g,x-hw-1,y-14+r,hw*2+2,1,K);R(g,x-hw,y-14+r,hw*2,1,r===0?MC.snow:r<3?'#2f8a5a':'#1f6a44');}R(g,x-21,y-11,3,1,K);R(g,x+18,y-11,3,1,K);R(g,x-22,y-12,1,1,K);R(g,x+21,y-12,1,1,K);R(g,x-1,y-16,2,2,'#ffd23f');
  for(const lx of [-7,0,7]){R(g,x+lx,y-5,1,2,K);C(x+lx,y-1,2,'#e03a4e');R(g,x+lx-1,y-2,1,1,'#ff9aa8');R(g,x+lx,y+2,1,2,'#ffd23f');}}break;"""
N['station']="""case 'station':{shadow(34);B(x-15,y-5,30,10,'#c6b49a');for(let k=0;k<5;k++){R(g,x-12+k*6,y-2,3,4,K);R(g,x-11+k*6,y-1,1,3,'#ffe27a');}R(g,x-16,y-9,32,5,K);R(g,x-15,y-8,30,3,'#2f5fae');R(g,x-15,y-8,30,1,MC.snow);C(x,y-11,2,'#f4f8ff');R(g,x,y-12,1,1,K);
  R(g,x-17,y+5,34,7,'#8a8f9f');for(let k=0;k<17;k++)R(g,x-17+k*2,y+6,1,5,'#6b4a2c');R(g,x-17,y+7,34,1,'#c6d0e0');R(g,x-17,y+10,34,1,'#c6d0e0');
  R(g,x+2,y+5,14,7,K);R(g,x+3,y+6,12,5,'#d8364b');R(g,x+12,y+6,3,5,'#ffd23f');R(g,x+4,y+7,2,2,'#8fd3ff');R(g,x+7,y+7,2,2,'#8fd3ff');}break;"""
N['hospital']="""case 'hospital':{shadow(30);B(x-13,y-9,26,19,'#f4f8ff');R(g,x-12,y-8,24,1,MC.snow);for(let r=0;r<2;r++)for(let k=0;k<5;k++){if(r===1&&k===2)continue;R(g,x-11+k*5,y-4+r*5,4,4,K);R(g,x-10+k*5,y-3+r*5,2,2,'#7fbaf2');R(g,x-10+k*5,y-3+r*5,1,1,'#d8f2ff');}
  R(g,x-3,y-15,7,7,K);R(g,x-2,y-14,5,5,'#f4f8ff');R(g,x,y-14,1,5,'#e03a4e');R(g,x-2,y-12,5,1,'#e03a4e');R(g,x-3,y+5,7,5,K);R(g,x-2,y+6,5,4,'#8fd3ff');R(g,x,y+6,1,4,'#c6ccd8');
  R(g,x+12,y+3,10,7,K);R(g,x+13,y+4,8,5,'#f4f8ff');R(g,x+13,y+6,8,1,'#e03a4e');R(g,x+18,y+4,3,2,'#8fd3ff');R(g,x+14,y+3,3,1,'#3f86d6');}break;"""
N['museum']="""case 'museum':{shadow(32);B(x-15,y-2,30,11,'#e8e0d0');for(let k=0;k<6;k++){R(g,x-13+k*5,y,2,8,'#fbf6e8');R(g,x-12+k*5,y,1,8,'#c6c0b0');}R(g,x-8,y,2,5,'#d8364b');R(g,x+7,y,2,5,'#2f5fae');
  for(let r=0;r<7;r++){const hw=Math.round((r+1)/7*16);R(g,x-hw-1,y-9+r,hw*2+2,1,K);R(g,x-hw,y-9+r,hw*2,1,r<2?MC.snow:'#e8e0d0');}R(g,x-3,y-5,6,2,'#c6c0b0');
  R(g,x-16,y+9,32,3,K);R(g,x-15,y+9,30,1,'#e3e9f2');R(g,x-14,y+10,28,1,'#c6ccd8');pine(x+19,y+10,9);}break;"""
N['parade']="""case 'parade':{R(g,x-16,y+6,32,5,'#55607a');for(let k=0;k<8;k++)R(g,x-15+k*4,y+8,2,1,'#f4f8ff');
  R(g,x-9,y+1,16,6,K);R(g,x-8,y+2,14,4,'#ff4fa3');R(g,x-8,y+2,14,1,'#ff9ad0');R(g,x-6,y-3,6,5,K);R(g,x-5,y-2,4,3,'#ffd23f');for(const wx of [-7,3])C(x+wx,y+7,1,K);
  for(const [a,b2,c] of [[-13,-12,'#d8364b'],[-4,-15,'#ffc727'],[9,-11,'#3f86d6'],[14,-15,'#33b24a']]){C(x+a,y+b2,3,c);R(g,x+a-1,y+b2-2,1,1,'#ffffff');R(g,x+a,y+b2+4,1,8,'#55607a');}
  for(let k=0;k<10;k++)R(g,x-15+((k*13)%30),y-6+((k*7)%10),1,1,['#ff4fa3','#ffd23f','#7ad3ff','#9cff7a'][k%4]);}break;"""
N['carousel']="""case 'carousel':{shadow(30);R(g,x-13,y+3,26,7,K);R(g,x-12,y+4,24,5,'#c98d4a');R(g,x-12,y+4,24,1,'#e0b070');
  for(let k=0;k<5;k++){const hx=x-10+k*5;R(g,hx,y-3,1,8,'#ffd23f');R(g,hx-1,y+1+(k%2),3,2,['#f4f8ff','#c98d4a','#f4f8ff','#8a5a34','#f4f8ff'][k]);R(g,hx-1,y+1+(k%2),1,1,K);}
  for(let r=0;r<8;r++){const hw=Math.round(3+r*1.7);R(g,x-hw-1,y-12+r,hw*2+2,1,K);for(let xx=-hw;xx<hw;xx++)R(g,x+xx,y-12+r,1,1,((xx+40)>>2)%2?'#d8364b':'#f4f8ff');}
  R(g,x-15,y-4,30,1,K);for(let k=0;k<8;k++)R(g,x-14+k*4,y-4,2,2,'#ffd23f');R(g,x,y-15,1,3,K);R(g,x-1,y-16,3,2,'#ffd23f');}break;"""
N['games']="""case 'games':{mStall(g,x-15,y-1,'#d8364b');mStall(g,x+1,y-1,'#2f8a5a');R(g,x-16,y-9,30,1,K);for(let k=0;k<8;k++)R(g,x-15+k*4,y-8,1,1,['#ffd23f','#ff4fa3','#7ad3ff','#9cff7a'][k%4]);
  R(g,x+15,y-14,3,24,K);R(g,x+16,y-13,1,22,'#f4f8ff');for(let yy=y-12;yy<y+8;yy+=4)R(g,x+16,yy,1,2,'#d8364b');C(x+16,y-15,1,'#ffd23f');R(g,x+14,y+8,5,2,K);}break;"""
N['food']="""case 'food':{mStall(g,x-16,y-3,'#ffc727');R(g,x+1,y-6,15,11,K);R(g,x+2,y-5,13,9,'#e8eef8');R(g,x+2,y-5,13,1,MC.snow);R(g,x+3,y-3,8,3,K);R(g,x+4,y-2,6,1,'#ffe27a');R(g,x+2,y-1,13,1,'#d8364b');R(g,x+12,y-3,3,3,'#8fd3ff');for(const wx of [4,12])C(x+wx,y+5,1,K);
  R(g,x+5,y-10,1,2,'#f4f8ff');R(g,x+7,y-12,1,3,'#f4f8ff');R(g,x-6,y+7,12,2,K);R(g,x-5,y+7,10,1,'#c98d4a');R(g,x-5,y+9,1,2,K);R(g,x+4,y+9,1,2,K);}break;"""
N['haunted']="""case 'haunted':{shadow(28);B(x-11,y-5,20,15,'#55607a');for(let yy=y-3;yy<y+9;yy+=3)R(g,x-10,yy,18,1,'#4a5068');roof(x-1,y-12,22,7,'#2a2a36');
  R(g,x+6,y-14,7,14,K);R(g,x+7,y-13,5,12,'#4a5068');for(let r=0;r<6;r++)R(g,x+9-Math.floor(r/2),y-20+r,1+Math.floor(r/2)*2,1,K);R(g,x+8,y-10,3,3,'#9cff7a');
  R(g,x-8,y-2,4,4,K);R(g,x-7,y-1,2,2,'#ffd23f');R(g,x-8,y-1,4,1,'#7a4a2a');R(g,x+1,y-2,4,4,K);R(g,x+2,y-1,2,2,'#ffd23f');R(g,x-3,y+3,4,7,K);R(g,x-2,y+4,2,6,'#2a2a36');
  R(g,x-17,y-10,4,6,'#f4f8ff');R(g,x-18,y-9,6,4,'#f4f8ff');R(g,x-16,y-9,1,1,K);R(g,x-14,y-9,1,1,K);R(g,x-17,y-4,1,1,'#f4f8ff');R(g,x-15,y-4,1,1,'#f4f8ff');
  for(const [a,b2] of [[-6,-17],[2,-19]]){R(g,x+a,y+b2,1,1,K);R(g,x+a-2,y+b2-1,2,1,K);R(g,x+a+1,y+b2-1,2,1,K);}}break;"""
N['minigolf']="""case 'minigolf':{R(g,x-15,y-7,30,15,K);R(g,x-14,y-6,28,13,'#3fa85a');R(g,x-14,y-6,28,1,MC.snow);R(g,x-14,y+6,28,1,'#2f8a4a');for(let k=0;k<4;k++)R(g,x-12+k*7,y-3+((k*3)&3),2,1,'#4fbf6a');
  R(g,x-1,y-7,2,9,'#c98d4a');R(g,x+7,y-1,2,2,K);pole(x+8,y-11,10,'#e03a4e');C(x-9,y+3,1,'#f4f8ff');
  R(g,x-12,y-10,6,6,K);R(g,x-11,y-9,4,4,'#d8364b');R(g,x-11,y-9,4,1,MC.snow);for(let k=0;k<5;k++){R(g,x-9-k,y-12+k,1,1,K);R(g,x-9+k,y-12+k,1,1,K);}}break;"""
N['lake']="""case 'lake':{mPond(g,x,y+2,14,7);R(g,x-16,y-1,6,2,K);R(g,x-15,y-1,4,1,'#c98d4a');mBoat(g,x+1,y-2,10,'#f4f8ff');
  for(const [cx,cy,c] of [[-8,-12,'#ff4fa3'],[6,-15,'#ffd23f'],[14,-9,'#7ad3ff']]){for(let k=0;k<8;k++){const t=k/8*Math.PI*2;R(g,x+cx+Math.round(Math.cos(t)*3),y+cy+Math.round(Math.sin(t)*3),1,1,c);}R(g,x+cx,y+cy,1,1,'#ffffff');}
  for(const rx of [-14,-12,12])R(g,x+rx,y+5,1,3,'#7a6a3a');}break;"""
N['openingday']="""case 'openingday':{shadow(32);for(const px of [-14,10]){R(g,x+px,y-10,5,20,K);R(g,x+px+1,y-9,3,18,'#9b5fd6');R(g,x+px+1,y-9,1,18,'#c4a0f5');}R(g,x-16,y-14,32,6,K);R(g,x-15,y-13,30,4,'#ffc727');R(g,x-15,y-13,30,1,'#fff08a');for(let k=0;k<6;k++)R(g,x-12+k*5,y-12,2,2,'#d8364b');
  R(g,x-9,y+2,19,1,'#e03a4e');R(g,x,y+1,2,3,'#e03a4e');for(const [a,b2,c] of [[-17,-18,'#ff4fa3'],[-14,-21,'#7ad3ff'],[13,-20,'#9cff7a'],[16,-17,'#ffd23f']]){C(x+a,y+b2,2,c);R(g,x+a,y+b2+3,1,5,'#55607a');}
  for(let k=0;k<5;k++)R(g,x-15+k*7,y+9,4,2,['#ff4fa3','#ffd23f','#7ad3ff','#9cff7a','#ff7a3a'][k]);}break;"""
N['quay']="""case 'quay':{ice(x-16,y+3,32,8);for(let k=0;k<5;k++)R(g,x-14+k*7,y+6,4,1,'#bfe6ff');R(g,x-16,y-4,32,7,K);R(g,x-15,y-3,30,5,'#8793a8');for(let k=0;k<30;k+=5)R(g,x-15+k,y-3,1,5,'#6a7896');R(g,x-15,y-3,30,1,MC.snow);
  for(let k=0;k<4;k++){R(g,x-12+k*8,y-6,3,3,K);R(g,x-11+k*8,y-5,1,1,'#55607a');}mBoat(g,x-7,y+2,14,'#d8364b');
  R(g,x+8,y-11,6,6,K);R(g,x+9,y-10,4,4,'#c98d4a');R(g,x+9,y-10,4,1,MC.snow);R(g,x+2,y-9,5,4,K);R(g,x+3,y-8,3,2,'#2f5fae');}break;"""
N['lighthouse']="""case 'lighthouse':{mRock(g,x-11,y+6,8,6);mRock(g,x+5,y+7,8,5);for(let yy=-11;yy<10;yy++){const hw=3+Math.round((yy+11)*0.12);R(g,x-hw-1,y+yy,hw*2+3,1,K);R(g,x-hw,y+yy,hw*2+1,1,((yy+20)>>2)%2?'#e03a4e':'#f4f8ff');R(g,x-hw,y+yy,1,1,'#ffffff');}
  R(g,x-1,y+5,3,5,K);R(g,x,y+6,1,4,'#55321d');R(g,x,y-4,1,2,'#7fbaf2');
  R(g,x-6,y-13,13,2,K);R(g,x-5,y-13,11,1,'#55607a');R(g,x-4,y-18,9,5,K);R(g,x-3,y-17,7,3,'#ffe27a');R(g,x-1,y-17,3,3,'#fff8c0');R(g,x-3,y-21,7,3,K);R(g,x-2,y-20,5,1,'#e03a4e');R(g,x,y-23,1,2,K);
  for(let k=1;k<6;k++){R(g,x+4+k*2,y-16-k,2,1,'#fff3b0');R(g,x-6-k*2,y-16-k,2,1,'#fff3b0');}}break;"""
N['icebreaker']="""case 'icebreaker':{ice(x-17,y-4,34,15);R(g,x-17,y-1,14,8,'#4a7aa8');R(g,x-17,y-1,14,1,'#6f9fd0');
  pxPolyO(g,[[x-14,y-4],[x+8,y-4],[x+14,y+1],[x+8,y+6],[x-14,y+6]],'#d8364b');R(g,x-13,y+3,21,2,'#2a2a36');R(g,x-13,y-3,22,1,'#ff6a7a');
  B(x-9,y-9,11,7,'#f4f8ff');R(g,x-8,y-6,9,1,'#7fbaf2');R(g,x-3,y-13,4,5,K);R(g,x-2,y-12,2,3,'#ffc727');
  for(const [a,b2] of [[16,-2],[17,3],[15,7]]){R(g,x+a,y+b2,3,2,K);R(g,x+a,y+b2,2,1,'#e8f6ff');}}break;"""
N['lift']="""case 'lift':{shadow(20);R(g,x-16,y-7,32,1,'#2a2a36');R(g,x-16,y-4,32,1,'#2a2a36');R(g,x-2,y-9,5,20,K);R(g,x-1,y-8,3,18,'#8793a8');for(let yy=y-6;yy<y+9;yy+=3){R(g,x-1,yy,1,1,'#55607a');R(g,x+1,yy+1,1,1,'#55607a');}
  R(g,x-6,y-10,13,3,K);R(g,x-5,y-9,11,1,'#c6ccd8');C(x-5,y-7,1,'#55607a');C(x+5,y-4,1,'#55607a');
  for(const [a,cy,c] of [[-12,-7,'#3f86d6'],[9,-4,'#e03a4e']]){R(g,x+a,y+cy,1,4,K);R(g,x+a-3,y+cy+4,7,3,K);R(g,x+a-2,y+cy+5,5,1,'#55607a');R(g,x+a-2,y+cy+2,2,2,c);R(g,x+a+1,y+cy+2,2,2,'#ffc727');}}break;"""
N['gondola']="""case 'gondola':{mMountain(g,x+11,y+10,7,12,4);R(g,x-17,y-12,34,1,'#2a2a36');R(g,x-16,y-10,32,1,'#55607a');R(g,x-1,y-12,1,4,K);R(g,x-3,y-12,5,1,K);
  R(g,x-6,y-8,12,12,K);R(g,x-5,y-7,10,10,'#e03a4e');R(g,x-5,y-7,10,1,'#ff6a7a');R(g,x-4,y-5,8,4,'#bfe6ff');R(g,x-4,y-5,2,1,'#e8f6ff');R(g,x-1,y-5,1,4,'#e03a4e');R(g,x-6,y-8,12,1,MC.snow);R(g,x-5,y+3,10,1,'#a8283d');
  B(x-17,y+1,9,9,'#c6b49a');R(g,x-15,y+3,5,3,'#ffe27a');}break;"""
N['glacier']="""case 'glacier':{mMountain(g,x-2,y+2,13,16,6);pxPolyO(g,[[x-10,y-1],[x+6,y-1],[x+16,y+10],[x-16,y+10]],'#bfe6ff');R(g,x-9,y,15,1,'#e8f6ff');for(const [a,b2,l] of [[-8,3,6],[0,5,8],[-4,7,5],[6,8,6]])R(g,x+a,y+b2,l,1,'#6aa6d8');
  for(const a of [-12,10]){R(g,x+a,y+6,3,4,K);R(g,x+a+1,y+7,1,2,'#e8f6ff');}pole(x-2,y-20,6,'#e03a4e');}break;"""
N['grandslalom']="""case 'grandslalom':{for(const px of [-15,11]){R(g,x+px,y-12,4,22,K);R(g,x+px+1,y-11,2,21,'#e03a4e');R(g,x+px+1,y-11,1,21,'#ff6a7a');}R(g,x-15,y-15,30,6,K);R(g,x-14,y-14,28,4,'#13306b');for(let k=0;k<7;k++){R(g,x-13+k*4,y-14,2,2,'#f4f8ff');R(g,x-11+k*4,y-12,2,2,'#f4f8ff');}
  R(g,x-5,y-6,10,5,K);R(g,x-4,y-5,8,3,'#11131f');R(g,x-3,y-4,2,1,'#ff4a4a');R(g,x,y-4,2,1,'#ff4a4a');
  for(const [a,b2,c] of [[-8,4,'#3f86d6'],[4,7,'#e03a4e']]){R(g,x+a,y+b2,1,5,K);R(g,x+a+1,y+b2,3,3,c);}}break;"""
N['tunnel']="""case 'tunnel':{mMountain(g,x,y+10,16,20,9);R(g,x-7,y-1,14,11,K);R(g,x-6,y,12,10,'#c6c0b0');for(let k=0;k<12;k+=3)R(g,x-6+k,y,1,2,'#a8a090');g.fillStyle=K;pixCircle(g,x,y+5,4);R(g,x-4,y+5,9,5,K);g.fillStyle='#2a2a36';pixCircle(g,x,y+5,3);R(g,x-3,y+5,7,5,'#2a2a36');R(g,x-5,y+1,1,1,'#ffd23f');R(g,x+5,y+1,1,1,'#ffd23f');R(g,x-1,y+7,3,1,'#3a3f55');
  R(g,x-3,y+10,7,2,'#55607a');R(g,x,y+10,1,2,'#ffd23f');}break;"""
N['icecaves']="""case 'icecaves':{mMountain(g,x,y+10,16,19,11);g.fillStyle=K;pixCircle(g,x,y+5,7);R(g,x-7,y+5,15,6,K);g.fillStyle='#3f86d6';pixCircle(g,x,y+5,6);R(g,x-6,y+5,13,5,'#3f86d6');g.fillStyle='#7ad3ff';pixCircle(g,x,y+6,4);R(g,x-4,y+6,9,4,'#7ad3ff');R(g,x-1,y+5,3,5,'#d8f2ff');
  for(let k=-5;k<=5;k+=2)R(g,x+k,y-1+(Math.abs(k)>>1),1,2+((k+9)%3),'#e8f6ff');for(const [a,b2] of [[-13,6],[12,7]]){R(g,x+a,y+b2,2,4,'#9fd4f4');R(g,x+a,y+b2,1,2,'#ffffff');}}break;"""
N['summit']="""case 'summit':{mMountain(g,x-4,y+10,15,22,13);R(g,x+5,y-2,12,7,K);R(g,x+6,y-1,10,5,'#8a5a34');R(g,x+7,y,8,1,'#ffd23f');R(g,x+7,y+2,6,1,'#f4f8ff');R(g,x+8,y+5,1,5,K);R(g,x+13,y+5,1,5,K);
  R(g,x-6,y-15,5,4,K);R(g,x-5,y-14,3,2,'#8793a8');pole(x-4,y-21,6,'#e03a4e');}break;"""
N['frozenlake']="""case 'frozenlake':{mPond(g,x,y+1,15,8);for(const [a,b2,l] of [[-8,0,6],[2,3,5],[-3,-3,4]])R(g,x+a,y+b2,l,1,'#e8f6ff');R(g,x+6,y-2,1,4,'#6aa6d8');
  for(const [a,b2,c] of [[-6,-4,'#e03a4e'],[4,1,'#3f86d6']]){R(g,x+a,y+b2-4,2,2,'#f6c7a1');R(g,x+a,y+b2-2,2,3,c);R(g,x+a,y+b2+1,1,1,K);R(g,x+a+1,y+b2+1,1,1,K);}
  R(g,x-17,y+6,8,3,K);R(g,x-16,y+6,6,1,'#c98d4a');}break;"""
N['spires']="""case 'spires':{for(const [a,h] of [[-10,16],[-3,22],[5,14],[11,19]]){for(let r=0;r<h;r++){const hw=Math.round(1+r*0.2);R(g,x+a-hw-1,y+10-h+r,hw*2+2,1,K);R(g,x+a-hw,y+10-h+r,hw,1,'#d4f0ff');R(g,x+a,y+10-h+r,hw,1,'#8fc8f0');}R(g,x+a-1,y+11-h,1,Math.round(h*0.4),'#ffffff');}
  R(g,x-15,y+9,30,3,K);R(g,x-14,y+9,28,2,MC.snow);for(const [a,b2] of [[-14,-8],[14,-4],[1,-15]]){R(g,x+a,y+b2,1,1,'#ffffff');R(g,x+a-1,y+b2+1,3,1,'#e8f6ff');}}break;"""
N['northpole']="""case 'northpole':{shadow(14);R(g,x-2,y-14,5,24,K);for(let yy=y-13;yy<y+10;yy++)R(g,x-1,yy,3,1,(((yy-y)>>1)&1)?'#e03a4e':'#f4f8ff');R(g,x-1,y-13,1,23,'#ffffff');C(x,y-16,3,'#ffd23f');R(g,x-1,y-18,1,1,'#fff8c0');
  R(g,x+3,y-8,11,4,K);R(g,x+4,y-7,9,2,'#2f8a5a');R(g,x+13,y-7,1,2,K);R(g,x+14,y-6,1,1,K);R(g,x-14,y-4,11,4,K);R(g,x-13,y-3,9,2,'#2f5fae');R(g,x-15,y-3,1,2,K);R(g,x-16,y-2,1,1,K);
  R(g,x+6,y+4,8,6,K);R(g,x+7,y+5,6,4,'#d8364b');R(g,x+9,y+5,2,4,'#ffd23f');R(g,x+7,y+6,6,1,'#ffd23f');}break;"""
N['palacegates']="""case 'palacegates':{shadow(30);for(const a of [-14,9]){R(g,x+a,y-8,6,18,K);R(g,x+a+1,y-7,4,17,'#c6e4fa');R(g,x+a+1,y-7,1,17,'#ffffff');R(g,x+a-1,y-10,8,3,K);R(g,x+a,y-9,6,1,'#e8f6ff');R(g,x+a+2,y-13,2,3,K);R(g,x+a+2,y-13,2,1,'#9fd4f4');}
  for(let k=0;k<23;k++){const yy=Math.round(y-9-5*Math.sin(Math.PI*k/22));R(g,x-8+k,yy-1,1,3,K);R(g,x-8+k,yy,1,1,k%4===1?'#ffffff':'#9fd4f4');}
  for(let k=0;k<6;k++){const hh=Math.round(2*Math.sin(Math.PI*k/5));R(g,x-7+k*3,y-5-hh,1,15+hh,'#6f8fb8');}R(g,x-8,y+3,17,1,'#6f8fb8');R(g,x-1,y-12,3,3,'#ffd23f');}break;"""
N['greathall']="""case 'greathall':{shadow(32);B(x-15,y-5,30,15,'#c6e4fa');for(let k=0;k<6;k++){R(g,x-13+k*5,y-3,2,13,'#e8f6ff');R(g,x-12+k*5,y-3,1,13,'#9fc8e8');}R(g,x-3,y+2,6,8,K);R(g,x-2,y+3,4,7,'#d8364b');R(g,x-1,y+3,2,7,'#ff6a7a');
  for(let r=0;r<8;r++){const hw=Math.round((r+1)/8*17);R(g,x-hw-1,y-13+r,hw*2+2,1,K);R(g,x-hw,y-13+r,hw*2,1,r<2?MC.snow:'#9fd4f4');}R(g,x-2,y-9,4,3,'#ffd23f');R(g,x-2,y-10,1,1,'#ffd23f');R(g,x+1,y-10,1,1,'#ffd23f');
  R(g,x-16,y+10,32,2,K);R(g,x-15,y+10,30,1,'#e8f6ff');for(const a of [-11,9])R(g,x+a,y-2,2,5,'#9b5fd6');}break;"""
N['icepalace']="""case 'icepalace':{shadow(32);for(const [a,h] of [[-12,18],[-4,24],[4,22],[12,16]]){R(g,x+a-3,y+10-h,7,h,K);R(g,x+a-2,y+11-h,5,h-1,'#c6e4fa');R(g,x+a-2,y+11-h,1,h-1,'#ffffff');R(g,x+a+2,y+11-h,1,h-1,'#9fc8e8');R(g,x+a-1,y+14-h,2,3,'#ffe27a');
    for(let r=0;r<6;r++){const hw=Math.round((r+1)/6*4);R(g,x+a-hw,y+4-h+r,hw*2+1,1,K);if(hw>0)R(g,x+a-hw+1,y+4-h+r,hw*2-1,1,r<1?'#ffffff':'#9b5fd6');}R(g,x+a,y+1-h,1,3,K);R(g,x+a+1,y+1-h,2,1,'#ffd23f');}
  R(g,x-15,y+3,30,8,K);R(g,x-14,y+4,28,6,'#e8f6ff');for(let k=0;k<7;k++)R(g,x-14+k*4,y+2,2,2,K);R(g,x-3,y+4,6,6,K);R(g,x-2,y+5,4,5,'#3a2a6a');R(g,x-1,y+5,2,1,'#ffd23f');}break;"""
for k,v in N.items():case(k,v)
s=s[:a0]+body+s[a1:]
open(f,'w',encoding='utf-8').write(s)
print('p103 landmarks part 4:',len(N))
