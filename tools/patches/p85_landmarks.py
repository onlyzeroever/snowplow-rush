import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# World map, landmark pass 1 (Nov 16): the 29 flattest level landmarks on the world map redrawn with outlines,
# shading and recognisable detail (sheep, traffic lights, bumper cars, a log flume, gates, piste signs, penguins...).
# Each stays inside the same area around its job node.
a=s.index('function lmArt(g,id,x,y){');depth=0;i=s.index('{',a)
while True:
    ch=s[i]
    if ch=='{':depth+=1
    elif ch=='}':
        depth-=1
        if depth==0:break
    i+=1
body=s[a:i+1]
def case(head,new):
    global body
    assert body.count(head)==1,head
    p=body.index(head);e=body.index('break;',p)+6
    if body[p+len(head)]=='{':
        assert body[e]=='}',head;e+=1
    body=body[:p]+new+body[e:]
N={}
N["case 'sheepfields':"]="""case 'sheepfields':{mFenceH(g,x-15,y+7,30);const sh=(sx,sy,f)=>{R(g,sx,sy,7,4,K);R(g,sx+1,sy+1,5,2,'#f4f8ff');R(g,sx+1,sy+2,5,1,'#d6dee9');R(g,sx+2,sy+1,2,1,'#ffffff');const hx=f?sx-2:sx+5;R(g,hx,sy-1,3,3,K);R(g,hx+1,sy,1,1,'#55607a');R(g,sx+1,sy+4,1,1,K);R(g,sx+5,sy+4,1,1,K);};
  sh(x-12,y-6,0);sh(x+3,y-8,1);sh(x-4,y,0);sh(x+8,y-1,1);}break;"""
N["case 'junction':"]="""case 'junction':{R(g,x-15,y-3,30,9,K);R(g,x-4,y-14,9,27,K);R(g,x-15,y-2,30,7,'#55607a');R(g,x-3,y-13,7,25,'#55607a');
  for(let k=0;k<5;k++){const xx=x-14+k*6;if(xx<x-6||xx>x+4)R(g,xx,y+1,3,1,'#f4f8ff');}for(let k=0;k<4;k++){const yy=y-12+k*7;if(yy<y-6||yy>y+5)R(g,x,yy,1,3,'#f4f8ff');}for(let k=0;k<4;k++)R(g,x-3+k*2,y-6,1,2,'#f4f8ff');
  R(g,x+7,y-14,5,9,K);R(g,x+8,y-13,3,2,'#e03a4e');R(g,x+8,y-11,3,2,'#5a5030');R(g,x+8,y-9,3,2,'#33b24a');R(g,x+9,y-5,1,3,K);R(g,x-13,y-2,7,4,K);R(g,x-12,y-1,5,2,'#3f86d6');R(g,x-11,y-1,2,1,'#9fd4f4');}break;"""
N["case 'icerink':"]="""case 'icerink':{for(let dy=-8;dy<=8;dy++){const hw=Math.round(15*Math.sqrt(1-(dy*dy)/72));R(g,x-hw-1,y+dy,hw*2+2,1,K);if(Math.abs(dy)<8)R(g,x-hw,y+dy,hw*2,1,'#e03a4e');}
  for(let dy=-6;dy<=6;dy++){const hw=Math.round(13*Math.sqrt(1-(dy*dy)/49));R(g,x-hw,y+dy,hw*2,1,dy<-4?'#ffffff':'#cfeefd');}for(let dy=-7;dy<=7;dy+=2){const hw=Math.round(15*Math.sqrt(1-(dy*dy)/72));R(g,x-hw,y+dy,1,1,'#f4f8ff');R(g,x+hw-1,y+dy,1,1,'#f4f8ff');}
  for(const [a,b2] of [[-8,0],[-6,2],[-3,3],[1,3],[5,2]])R(g,x+a,y+b2,2,1,'#a8dcfa');const sk=(sx,sy,c)=>{R(g,sx,sy+3,3,1,'#a6c2ea');R(g,sx,sy,2,1,'#f6c7a1');R(g,sx,sy+1,2,2,c);R(g,sx-1,sy+1,1,1,c);};sk(x-6,y-3,'#e03a4e');sk(x+4,y-1,'#2f5fae');}break;"""
N["case 'bumpers':"]="""case 'bumpers':{R(g,x-15,y-9,30,19,K);R(g,x-14,y-8,28,17,'#ffd23f');for(let k=0;k<14;k++){R(g,x-14+k*2,y-8,1,1,K);R(g,x-13+k*2,y+8,1,1,K);}R(g,x-13,y-7,26,15,'#3a3f55');for(let k=0;k<6;k++)R(g,x-12+k*5,y-6+(k%2)*7,1,1,'#55607a');
  const car=(cx,cy,c,d)=>{R(g,cx,cy,7,6,K);R(g,cx+1,cy+1,5,4,c);R(g,cx+1,cy+4,5,1,d);R(g,cx+2,cy+2,2,2,'#f6c7a1');R(g,cx+2,cy+2,2,1,'#55321d');R(g,cx+5,cy+1,1,1,'#ffffff');};
  car(x-11,y-5,'#e03a4e','#a82639');car(x+1,y-6,'#33b24a','#1f7a33');car(x-4,y+1,'#3f86d6','#2a5fa8');car(x+6,y+1,'#ffc727','#d49a12');}break;"""
N["case 'flume':"]="""case 'flume':{R(g,x-15,y+1,23,7,K);R(g,x-14,y+2,21,5,'#a8673a');R(g,x-14,y+3,21,3,'#7fbaf2');R(g,x-14,y+3,21,1,'#c8e6ff');
  R(g,x+7,y-13,8,21,K);R(g,x+8,y-12,6,19,'#c98d4a');for(let k=0;k<4;k++)R(g,x+8,y-10+k*5,6,1,'#7a4a2a');R(g,x+8,y-12,1,19,'#e0b070');
  for(let i=0;i<14;i++)R(g,x+6-i,y-12+i,3,3,K);for(let i=0;i<14;i++)R(g,x+7-i,y-11+i,1,1,'#7fbaf2');
  R(g,x-14,y+1,7,4,K);R(g,x-13,y+2,5,2,'#8a5a34');R(g,x-13,y+2,5,1,'#b07a44');R(g,x-13,y,2,2,'#ffc727');R(g,x-10,y,2,2,'#e03a4e');for(const [a,b2] of [[-6,-1],[-4,-2],[-3,0],[-5,1]])R(g,x+a,y+b2,1,1,'#ffffff');}break;"""
N["case 'drop':"]="""case 'drop':{R(g,x-6,y+7,13,4,K);R(g,x-5,y+8,11,2,'#8793a8');R(g,x-5,y+8,11,1,'#c6d0dc');R(g,x-3,y-16,7,24,K);R(g,x-2,y-15,5,23,'#c6d0dc');R(g,x-2,y-15,1,23,'#e3ebf6');for(let k=0;k<7;k++)R(g,x-2,y-13+k*3,5,1,'#8793a8');
  R(g,x-4,y-19,9,4,K);R(g,x-3,y-18,7,2,'#e03a4e');R(g,x-3,y-18,7,1,'#ffd23f');R(g,x-8,y-6,17,5,K);R(g,x-7,y-5,15,3,'#3f86d6');for(let k=0;k<5;k++)R(g,x-6+k*3,y-5,1,1,'#ffd23f');R(g,x-7,y-3,15,1,'#2a5fa8');}break;"""
N["case 'fishmarket':"]="""case 'fishmarket':{shadow(30);B(x-14,y-5,28,13,'#dfe5ef');R(g,x-15,y-9,30,5,K);for(let k=0;k<14;k++)R(g,x-14+k*2,y-8,2,3,k%2?'#2f5fae':'#f4f8ff');for(let k=0;k<7;k++)R(g,x-13+k*4,y-5,2,1,K);
  R(g,x-12,y+1,24,5,K);R(g,x-11,y+2,22,3,'#c98d4a');R(g,x-11,y+1,22,1,'#e8f6ff');for(const [a,c] of [[-10,'#9aa6ba'],[-6,'#e07a8a'],[-2,'#9aa6ba'],[2,'#e07a8a'],[6,'#9aa6ba']]){R(g,x+a,y+1,3,1,c);R(g,x+a+3,y+1,1,1,K);}R(g,x-4,y-3,8,3,K);R(g,x-3,y-2,6,1,'#2f5fae');}break;"""
N["case 'drawbridge':"]="""case 'drawbridge':{ice(x-15,y+2,30,9);B(x-15,y-2,6,9,'#c6d0e0');B(x+9,y-2,6,9,'#c6d0e0');R(g,x-10,y-1,11,4,K);R(g,x-9,y,9,2,'#a8673a');R(g,x-9,y,9,1,'#c98d4a');
  for(let i=0;i<9;i++)R(g,x+1+i,y-2-i,2,4,K);for(let i=0;i<8;i++)R(g,x+2+i,y-1-i,1,2,'#a8673a');B(x+10,y-11,5,9,'#e03a4e');R(g,x+11,y-8,3,2,'#9fd4f4');R(g,x+9,y-12,7,1,K);
  R(g,x-13,y-4,1,4,K);R(g,x-13,y-5,8,2,K);for(let k=0;k<3;k++)R(g,x-12+k*2,y-5,2,1,k%2?'#f4f8ff':'#e03a4e');}break;"""
N["case 'pier':"]="""case 'pier':{ice(x-15,y-4,30,15);for(let k=0;k<4;k++){R(g,x-5,y-11+k*6,1,2,K);R(g,x+4,y-11+k*6,1,2,K);}R(g,x-4,y-14,8,24,K);R(g,x-3,y-13,6,22,'#c98d4a');for(let yy=y-12;yy<y+9;yy+=2)R(g,x-3,yy,6,1,'#a8673a');R(g,x-3,y-13,1,22,'#e0b070');
  R(g,x-1,y-18,1,5,K);R(g,x-2,y-19,3,2,K);R(g,x-1,y-19,1,1,'#ffd77a');R(g,x+7,y,8,5,K);R(g,x+8,y+1,6,3,'#e03a4e');R(g,x+8,y+1,6,1,'#f4f8ff');R(g,x+10,y-2,1,3,K);}break;"""
N["case 'customs':"]="""case 'customs':{shadow(26);B(x-12,y-5,12,13,'#f4f8ff');R(g,x-13,y-8,14,4,K);R(g,x-12,y-7,12,2,'#2f5fae');R(g,x-10,y-2,8,4,K);R(g,x-9,y-1,6,2,'#9fd4f4');R(g,x-9,y-1,2,1,'#e8f6ff');
  R(g,x+1,y-1,3,9,K);R(g,x+2,y,1,7,'#ffc727');R(g,x+3,y,13,3,K);for(let k=0;k<4;k++)R(g,x+4+k*3,y+1,3,1,k%2?'#f4f8ff':'#e03a4e');pole(x-12,y-14,6,'#2f5fae');}break;"""
N["case 'locks':"]="""case 'locks':{R(g,x-15,y-5,30,11,'#9fd4f4');R(g,x-15,y-5,12,11,'#7ab0dc');R(g,x-15,y-5,30,1,'#e8f6ff');R(g,x-15,y-9,30,4,K);R(g,x-14,y-8,28,2,'#c6d0e0');R(g,x-14,y-8,28,1,'#e3ebf6');R(g,x-15,y+6,30,4,K);R(g,x-14,y+7,28,2,'#c6d0e0');
  for(const gx of [x-4,x+8]){R(g,gx,y-5,3,11,K);R(g,gx+1,y-4,1,9,'#a8673a');R(g,gx-4,y-8,5,1,'#7a4a2a');R(g,gx-4,y+7,5,1,'#7a4a2a');}R(g,x,y-2,7,5,K);R(g,x+1,y-1,5,3,'#f4f8ff');R(g,x+2,y-1,3,1,'#e03a4e');}break;"""
N["case 'gullisland':"]="""case 'gullisland':{ice(x-15,y+2,30,9);for(let k=0;k<5;k++)R(g,x-14+k*6,y+6,3,1,'#e8f6ff');mRock(g,x-11,y-5,22,11);
  const sit=(sx,sy)=>{R(g,sx,sy,4,3,K);R(g,sx+1,sy+1,2,1,'#f4f8ff');R(g,sx+3,sy+1,1,1,'#f07a1a');};sit(x-6,y-7);sit(x+2,y-8);
  const fly=(fx,fy)=>{R(g,fx,fy,2,1,'#f4f8ff');R(g,fx+3,fy,2,1,'#f4f8ff');R(g,fx+2,fy+1,1,1,'#f4f8ff');R(g,fx-1,fy-1,1,1,K);R(g,fx+5,fy-1,1,1,K);R(g,fx+2,fy+2,1,1,K);};fly(x-12,y-13);fly(x+7,y-15);}break;"""
N["case 'snowguns':"]="""case 'snowguns':{shadow(20);R(g,x-10,y+1,1,9,K);R(g,x-6,y+1,1,9,K);R(g,x-8,y+3,1,7,K);R(g,x-13,y-7,11,9,K);R(g,x-12,y-6,9,7,'#ffc727');R(g,x-12,y-6,9,1,'#ffe27a');R(g,x-4,y-6,1,7,'#d49a12');R(g,x-11,y-5,5,5,K);R(g,x-10,y-4,3,3,'#55607a');R(g,x-9,y-3,1,1,'#c6d0dc');R(g,x-2,y-6,2,7,K);
  for(let k=0;k<16;k++){R(g,x+k,y-3-(k>>1)+((k*5)%3)-1,1,1,k%3?'#ffffff':'#c6d9f3');if(k>4)R(g,x+k,y-1-(k>>2)+((k*7)%3),1,1,'#e3ebf6');}}break;"""
N["case 'moguls':"]="""case 'moguls':{const mo=(cx,cy)=>{R(g,cx-3,cy+2,8,1,'#a6c2ea');R(g,cx-3,cy,7,2,'#e3ebf6');R(g,cx+1,cy,3,2,'#c6d9f3');R(g,cx-2,cy-1,5,1,'#ffffff');R(g,cx-1,cy-2,3,1,'#ffffff');R(g,cx-3,cy+1,1,1,'#c6d9f3');};
  for(let k=0;k<6;k++)mo(x-10+(k%3)*10,y-5+(k>>1)*3+(k%2)*4);for(let t=0;t<22;t++)R(g,x-12+t,y-10+Math.round(t*0.7+Math.sin(t/2.5)*2),1,1,'#a6c2ea');
  R(g,x+1,y-12,4,1,K);R(g,x+2,y-15,2,3,'#e03a4e');R(g,x+2,y-16,2,1,'#f6c7a1');R(g,x+4,y-14,2,1,K);}break;"""
N["case 'slalom':"]="""case 'slalom':{for(let t=0;t<26;t++)R(g,x-13+t,y-11+Math.round(t*0.8+Math.sin(t/2)*3),1,1,'#a6c2ea');
  const gate=(gx,gy,c,c2)=>{R(g,gx,gy,1,10,K);R(g,gx+6,gy,1,10,K);R(g,gx,gy,7,5,K);R(g,gx+1,gy+1,5,3,c);R(g,gx+1,gy+1,5,1,c2);R(g,gx-1,gy+10,9,1,'#c6d9f3');};
  gate(x-15,y-13,'#e03a4e','#f28b8b');gate(x-3,y-6,'#2f5fae','#7ab4f0');gate(x+8,y,'#e03a4e','#f28b8b');}break;"""
N["case 'terrain':"]="""case 'terrain':{for(let r=0;r<9;r++){const w=Math.round(14*(r+1)/9);R(g,x-1-w,y+1+r,w+1,1,K);if(w>1)R(g,x-w,y+1+r,w-1,1,r<2?'#e3ebf6':r<5?'#c6d9f3':'#a6c2ea');}R(g,x-15,y+10,15,1,K);
  R(g,x+3,y,13,3,K);R(g,x+4,y+1,11,1,'#ffc727');R(g,x+5,y+3,1,6,K);R(g,x+13,y+3,1,6,K);R(g,x+3,y+9,13,1,'#c6d9f3');
  R(g,x-7,y-6,7,1,'#e03a4e');R(g,x-5,y-9,2,3,'#2f5fae');R(g,x-5,y-10,2,1,'#f6c7a1');R(g,x-8,y-8,1,1,K);R(g,x-1,y-8,1,1,K);for(const [a,b2] of [[-12,-6],[-11,-4],[-10,-2]])R(g,x+a,y+b2,2,1,'#c6d9f3');}break;"""
N["case 'hairpin':case 'switchbacks':"]="""case 'hairpin':case 'switchbacks':{const n=id==='hairpin'?3:4,sp=20/(n-1),ys=[];for(let k=0;k<n;k++)ys.push(Math.round(y-11+k*sp));
  for(let k=0;k<n;k++){R(g,x-15,ys[k]-1,30,5,K);if(k<n-1){const e=k%2?x-15:x+10;R(g,e,ys[k]-1,5,ys[k+1]-ys[k]+5,K);}}
  for(let k=0;k<n;k++){R(g,x-14,ys[k],28,3,'#55607a');if(k<n-1){const e=k%2?x-14:x+11;R(g,e,ys[k],3,ys[k+1]-ys[k]+3,'#55607a');}}
  for(let k=0;k<n;k++)for(let j=0;j<4;j++)R(g,x-9+j*6,ys[k]+1,3,1,'#ffd23f');R(g,x-6,ys[1],4,3,K);R(g,x-5,ys[1],2,2,'#e03a4e');R(g,x-5,ys[1],2,1,'#f28b8b');
  break;}"""
N["case 'avalanche':"]="""case 'avalanche':{mMountain(g,x-3,y+6,12,20,7);const P2=[[x+2,y+4,4],[x+8,y+2,4],[x+12,y+6,3],[x-4,y+7,3],[x+5,y+8,3]];g.fillStyle='#a6c2ea';P2.forEach(p=>pixCircle(g,p[0],p[1],p[2]+1));g.fillStyle='#ffffff';P2.forEach(p=>pixCircle(g,p[0],p[1],p[2]));
  for(const [a,b2] of [[-1,-6],[2,-4],[4,-1]])R(g,x+a,y+b2,2,2,'#ffffff');R(g,x-13,y-4,1,12,K);R(g,x-15,y-9,5,5,K);R(g,x-14,y-8,3,3,'#ffc727');R(g,x-13,y-8,1,1,K);R(g,x-13,y-6,1,1,K);}break;"""
N["case 'weather':"]="""case 'weather':{shadow(28);R(g,x-12,y+3,1,6,K);R(g,x-3,y+3,1,6,K);R(g,x-13,y-4,12,8,K);R(g,x-12,y-3,10,6,'#f4f8ff');for(let k=0;k<3;k++)R(g,x-12,y-2+k*2,10,1,'#c6d0dc');R(g,x-14,y-5,14,1,K);
  C(x+8,y-1,6,'#f4f8ff');R(g,x+5,y-5,6,1,'#c6d0dc');R(g,x+3,y-1,11,1,'#d6dee9');R(g,x+5,y+3,6,1,'#c6d0dc');R(g,x+6,y-5,2,2,'#ffffff');R(g,x+2,y+6,13,2,K);
  R(g,x-7,y-17,1,12,K);R(g,x-11,y-16,9,1,K);R(g,x-12,y-17,2,2,'#e03a4e');R(g,x-3,y-17,2,2,'#e03a4e');R(g,x-10,y-13,6,1,K);R(g,x-11,y-14,2,3,K);}break;"""
N["case 'viewpoint':"]="""case 'viewpoint':{mMountain(g,x+8,y+2,8,14,3);R(g,x-15,y+3,24,6,K);R(g,x-14,y+4,22,4,'#c98d4a');R(g,x-14,y+4,22,1,'#e0b070');for(let k=0;k<5;k++)R(g,x-12+k*5,y+5,1,3,'#a8673a');
  for(let k=0;k<5;k++)R(g,x-14+k*5,y-1,1,4,K);R(g,x-14,y-1,22,1,K);R(g,x-13,y-2,21,1,'#c6d0dc');R(g,x-7,y-5,1,8,K);R(g,x-10,y-9,7,4,K);R(g,x-9,y-8,5,2,'#2f5fae');R(g,x-9,y-8,5,1,'#5a8ad6');R(g,x-4,y-8,1,2,'#9fd4f4');}break;"""
N["case 'cliffroad':"]="""case 'cliffroad':{R(g,x-15,y-13,12,26,K);R(g,x-14,y-12,10,24,MC.rock);R(g,x-14,y-12,3,24,MC.rockL);for(let yy=y-10;yy<y+12;yy+=4){R(g,x-14,yy,10,1,MC.rockD);R(g,x-13,yy-1,4,1,MC.snow);}R(g,x-7,y-12,2,24,MC.rockD);
  R(g,x-4,y-13,10,26,K);R(g,x-3,y-12,8,24,'#55607a');for(let k=0;k<5;k++)R(g,x+1,y-11+k*5,1,3,'#ffd23f');R(g,x+6,y-13,1,26,K);for(let k=0;k<7;k++)R(g,x+7,y-12+k*4,2,2,K);R(g,x+7,y-12,1,24,'#c6d0dc');R(g,x+9,y-13,6,26,'#c6d9f3');R(g,x+9,y-13,1,26,MC.sh2);}break;"""
N["case 'blizzard':"]="""case 'blizzard':{const CL=[[-7,-6,5],[1,-8,6],[9,-5,4]];g.fillStyle=K;CL.forEach(c=>pixCircle(g,x+c[0],y+c[1],c[2]+1));R(g,x-12,y-5,25,6,K);g.fillStyle='#55607a';CL.forEach(c=>pixCircle(g,x+c[0],y+c[1],c[2]));R(g,x-11,y-4,23,4,'#55607a');
  g.fillStyle='#8793a8';pixCircle(g,x-8,y-7,2);pixCircle(g,x,y-10,3);R(g,x-11,y,23,1,'#3a3f55');for(let k=0;k<16;k++){const px=x-13+((k*7)%27),py=y+3+((k*5)%9);R(g,px,py,2,1,'#ffffff');R(g,px-1,py+1,1,1,'#c6d9f3');}
  for(const [a,b2,l] of [[-14,4,8],[3,7,9],[-6,10,7]])R(g,x+a,y+b2,l,1,'#a6c2ea');}break;"""
N["case 'research':"]="""case 'research':{shadow(30);for(const a of [-13,-8,-2,3])R(g,x+a,y+5,1,4,K);B(x-14,y-5,20,11,'#f07a1a');R(g,x-13,y+3,18,2,'#b8501a');for(let k=0;k<4;k++){R(g,x-12+k*4,y-2,3,3,K);R(g,x-11+k*4,y-1,1,1,'#9fd4f4');}
  R(g,x-6,y-9,1,4,K);R(g,x-9,y-11,7,2,K);R(g,x-8,y-11,5,1,'#f4f8ff');R(g,x-13,y-15,1,10,K);R(g,x-13,y-16,1,1,'#e03a4e');C(x+10,y,5,'#f4f8ff');R(g,x+6,y-2,8,1,'#d6dee9');R(g,x+6,y+2,8,1,'#d6dee9');R(g,x+8,y-4,2,1,'#ffffff');pole(x+1,y-13,8,'#2f5fae');}break;"""
N["case 'icefield':"]="""case 'icefield':{const sh=(bx,by,h,w)=>{for(let r=0;r<h;r++){const hw=Math.max(0,Math.round(w*r/h));R(g,bx-hw-1,by-h+r,hw*2+3,1,K);R(g,bx-hw,by-h+r,hw+1,1,r<2?'#ffffff':'#d4f0ff');if(hw>0)R(g,bx+1,by-h+r,hw,1,r<2?'#e8f6ff':'#7dbfe8');}R(g,bx-w-1,by,w*2+3,1,K);};
  R(g,x-15,y+5,30,4,'#d4f0ff');R(g,x-15,y+5,30,1,'#a8dcfa');sh(x-10,y+6,9,4);sh(x-2,y+6,13,5);sh(x+6,y+7,8,4);sh(x+12,y+6,6,3);pole(x+8,y-12,10,'#e03a4e');}break;"""
N["case 'gardens2':"]="""case 'gardens2':{const hd=hx=>{R(g,hx,y+1,11,8,K);R(g,hx+1,y+2,9,6,'#a8dcfa');R(g,hx+1,y+2,9,1,'#e8f6ff');R(g,hx+8,y+3,2,5,'#7dbfe8');for(let k=0;k<3;k++)R(g,hx+2+k*3,y+5,1,1,'#ffffff');};hd(x-15);hd(x+4);
  for(let r=0;r<12;r++){const hw=Math.round(r*0.45);R(g,x-hw-1,y-13+r,hw*2+3,1,K);R(g,x-hw,y-13+r,hw+1,1,'#c8ecff');if(hw>0)R(g,x+1,y-13+r,hw,1,'#7dbfe8');}R(g,x-1,y-1,3,3,K);R(g,x,y-1,1,2,'#a8dcfa');R(g,x,y-15,1,1,'#ffffff');R(g,x-1,y-14,3,1,'#ffffff');}break;"""
N["case 'bluerun':"]="""case 'bluerun':{R(g,x-9,y-11,14,13,K);R(g,x-8,y-10,12,11,'#f4f8ff');R(g,x-7,y-9,10,9,'#2f5fae');R(g,x-7,y-9,10,1,'#5a8ad6');R(g,x-3,y+2,2,8,K);R(g,x+9,y-9,3,19,K);R(g,x+10,y-8,1,17,'#2f5fae');for(let k=0;k<4;k++)R(g,x+10,y-6+k*4,1,2,'#f4f8ff');}break;"""
N["case 'redrun':"]="""case 'redrun':{C(x-2,y-5,6,'#f4f8ff');g.fillStyle='#e03a4e';pixCircle(g,x-2,y-5,5);R(g,x-4,y-9,3,1,'#f28b8b');R(g,x-3,y+2,2,8,K);R(g,x+9,y-9,3,19,K);R(g,x+10,y-8,1,17,'#e03a4e');for(let k=0;k<4;k++)R(g,x+10,y-6+k*4,1,2,'#f4f8ff');}break;"""
N["case 'blackrun':"]="""case 'blackrun':{for(let r=0;r<7;r++){R(g,x-3-r,y-11+r,r*2+3,1,K);R(g,x-3-r,y+1-r,r*2+3,1,K);}for(let r=1;r<7;r++){R(g,x-3-r+1,y-11+r,r*2+1,1,'#f4f8ff');R(g,x-3-r+1,y+1-r,r*2+1,1,'#f4f8ff');}for(let r=2;r<7;r++){R(g,x-3-r+2,y-11+r,r*2-1,1,K);R(g,x-3-r+2,y+1-r,r*2-1,1,K);}
  R(g,x-3,y+2,2,8,K);R(g,x+9,y-9,3,19,K);R(g,x+10,y-8,1,17,'#2a2a36');for(let k=0;k<4;k++)R(g,x+10,y-6+k*4,1,2,'#f4f8ff');mRock(g,x-15,y+4,8,6);}break;"""
N["case 'penguins':"]="""case 'penguins':{ice(x-15,y+1,30,10);R(g,x+8,y+6,7,3,'#3a6fa8');R(g,x+7,y+6,9,1,'#e8f6ff');const pg=spr([".KKK.","KWKWK","KKOKK","KWWWK","KWWWK","KWWWK",".KKK.",".O.O."],{W:'#f4f8ff',O:'#f07a1a'});for(const [a,b2] of [[-13,-6],[-7,-4],[-1,-7]])g.drawImage(pg,x+a,y+b2);
  R(g,x+1,y+2,8,3,K);R(g,x+2,y+3,5,1,'#f4f8ff');R(g,x+7,y+2,2,2,K);R(g,x+9,y+3,1,1,'#f07a1a');for(let k=0;k<3;k++)R(g,x-4+k*2,y+4,1,1,'#c8e6ff');}break;"""
for h,n in N.items(): case(h,n)
s=s[:a]+body+s[i+1:]
open(f,'w',encoding='utf-8').write(s)
print('p85 landmarks pass 1:',len(N),'redrawn')
