import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# World map, landmark pass 2 (Nov 16): theme park gates, windmill, snow shed, frozen waterfall, gorge bridge,
# rockfall, snowshoe trail, polar trail, ice-fishing huts and the car ferry.
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
N["case 'gates':"]="""case 'gates':{shadow(30);const tw=tx=>{R(g,tx,y-8,6,18,K);R(g,tx+1,y-7,4,16,'#9b5fd6');R(g,tx+1,y-7,1,16,'#c49af0');for(let k=0;k<4;k++)R(g,tx+1,y-5+k*4,4,1,'#f4f8ff');R(g,tx-1,y-11,8,4,K);R(g,tx,y-10,6,2,'#e03a4e');R(g,tx+2,y-13,2,2,K);R(g,tx+2,y-14,2,1,'#ffd23f');};tw(x-15);tw(x+9);
  R(g,x-9,y-11,18,6,K);R(g,x-8,y-10,16,4,'#ffc727');R(g,x-8,y-10,16,1,'#ffe27a');for(let k=0;k<6;k++)R(g,x-7+k*3,y-8,1,1,k%2?'#e03a4e':'#3f86d6');for(let k=0;k<3;k++){R(g,x-6+k*5,y+4,2,5,K);R(g,x-7+k*5,y+5,4,1,'#8793a8');}}break;"""
N["case 'windmill':"]="""case 'windmill':{for(let r=0;r<18;r++){const hw=Math.round(3+r*0.22);R(g,x-hw-1,y-8+r,hw*2+3,1,K);R(g,x-hw,y-8+r,hw*2+1,1,'#e9edf4');R(g,x+1,y-8+r,hw,1,'#c6ccd6');}R(g,x-1,y+5,3,5,K);R(g,x,y+6,1,4,'#7a4a2a');R(g,x-1,y-2,3,3,K);R(g,x,y-1,1,1,'#ffd77a');roof(x,y-13,10,6,'#a8673a');
  for(let k=0;k<4;k++){const an=k*Math.PI/2+0.5,ca=Math.cos(an),sa=Math.sin(an);for(let d=2;d<14;d++){const px=Math.round(x+ca*d),py=Math.round(y-10+sa*d);if(d>4){R(g,Math.round(px-sa*2),Math.round(py+ca*2),1,1,'#f4f8ff');R(g,Math.round(px-sa),Math.round(py+ca),1,1,(d%2)?'#c98d4a':'#f4f8ff');}R(g,px,py,1,1,K);}}R(g,x-1,y-11,3,3,K);R(g,x,y-10,1,1,'#c98d4a');break;}"""
N["case 'snowshed':"]="""case 'snowshed':{mMountain(g,x-8,y+2,10,14,5);R(g,x-15,y-4,30,4,K);R(g,x-14,y-3,28,2,'#c6d0e0');R(g,x-14,y-3,28,1,MC.snow);R(g,x-15,y-6,30,2,MC.snow);
  R(g,x-15,y,30,9,K);R(g,x-14,y+1,28,7,'#2a2a36');for(let k=0;k<6;k++){R(g,x-14+k*5,y,2,9,K);R(g,x-13+k*5,y+1,1,7,'#a9b4c6');}R(g,x-15,y+6,30,3,'#55607a');for(let k=0;k<5;k++)R(g,x-12+k*6,y+7,3,1,'#ffd23f');R(g,x-11,y+3,3,2,'#ffd77a');}break;"""
N["case 'waterfall':"]="""case 'waterfall':{mRock(g,x-15,y-12,11,22);mRock(g,x+4,y-12,11,22);R(g,x-5,y-12,10,20,K);for(let c=0;c<8;c++){const L=16+((c*5)%5);R(g,x-4+c,y-12,1,L,c%3===0?'#ffffff':c%3===1?'#bfe6ff':'#8fd0f5');}R(g,x-4,y-12,8,1,'#ffffff');
  R(g,x-9,y+6,18,5,K);R(g,x-8,y+7,16,3,'#7fbaf2');R(g,x-8,y+7,16,1,'#c8e6ff');for(const [a2,b2] of [[-6,5],[-2,4],[3,5],[6,4]])R(g,x+a2,y+b2,1,1,'#ffffff');}break;"""
N["case 'gorge':"]="""case 'gorge':{mRock(g,x-15,y-6,11,16);mRock(g,x+4,y-6,11,16);R(g,x-4,y-4,8,14,'#3a3f55');R(g,x-4,y+4,8,6,'#2a2a36');R(g,x-3,y-4,1,8,'#55607a');
  for(let t=0;t<=30;t++){const xx=x-15+t,sag=Math.round(2*Math.sin(Math.PI*t/30));R(g,xx,y-5+sag,1,2,K);if(t%2===0)R(g,xx,y-5+sag,1,1,'#c98d4a');R(g,xx,y-9+sag,1,1,'#8a5a2c');if(t%5===0)R(g,xx,y-9+sag,1,4,'#8a5a2c');}}break;"""
N["case 'rockfall':"]="""case 'rockfall':{R(g,x-15,y-12,9,24,K);R(g,x-14,y-11,7,22,MC.rock);R(g,x-14,y-11,2,22,MC.rockL);for(let yy=y-9;yy<y+10;yy+=4)R(g,x-14,yy,7,1,MC.rockD);
  mRock(g,x-4,y-9,7,6);mRock(g,x+1,y-2,8,6);mRock(g,x+6,y+5,9,6);for(const [a2,b2] of [[-6,-7],[-5,-4],[0,-6],[3,1]])R(g,x+a2,y+b2,1,1,'#8793a8');R(g,x+10,y-12,1,9,K);R(g,x+7,y-15,7,5,K);R(g,x+8,y-14,5,3,'#ffc727');R(g,x+10,y-14,1,2,K);}break;"""
N["case 'snowshoe':"]="""case 'snowshoe':{pine(x-10,y+8,13);pine(x+10,y+6,11);for(let k=0;k<7;k++){const tx=x-4+((k%2)*3),ty=y+9-k*3;R(g,tx,ty,2,2,'#a6c2ea');R(g,tx,ty,2,1,'#8fb0dc');}
  R(g,x-3,y-16,2,1,'#f6c7a1');R(g,x-4,y-15,4,4,K);R(g,x-3,y-14,2,2,'#e03a4e');R(g,x-3,y-11,1,2,K);R(g,x-2,y-11,1,2,K);R(g,x-5,y-15,1,5,'#8a5a2c');R(g,x-4,y-9,4,1,'#55607a');}break;"""
N["case 'polartrail':"]="""case 'polartrail':{for(let t=0;t<30;t++){const yy=y+6-Math.round(t*0.45+Math.sin(t/4)*2);R(g,x-15+t,yy,1,1,'#a6c2ea');R(g,x-15+t,yy+3,1,1,'#a6c2ea');}
  for(let k=0;k<3;k++)pole(x-13+k*8,y-4-k*3+(k%2)*2,9,'#f07a1a');R(g,x+11,y-1,1,9,K);R(g,x+8,y-3,7,3,K);R(g,x+9,y-2,4,1,'#c98d4a');R(g,x+14,y-2,1,1,K);}break;"""
N["case 'icefish':"]="""case 'icefish':{ice(x-15,y-4,30,15);const ht=(hx,c,d)=>{R(g,hx,y-10,10,9,K);R(g,hx+1,y-6,8,4,c);R(g,hx+7,y-6,1,4,d);for(let r=0;r<4;r++)R(g,hx+4-r,y-10+r,2+r*2,1,r<1?MC.snow:'#55607a');R(g,hx+4,y-5,2,3,'#2a2a36');};ht(x-14,'#e03a4e','#a82639');ht(x+3,'#3f86d6','#2a5fa8');
  C(x-2,y+5,2,'#2a4a7a');R(g,x-2,y+2,1,3,'#55607a');R(g,x-4,y+1,3,1,'#8a5a2c');R(g,x+4,y+5,4,2,K);R(g,x+5,y+5,2,1,'#9aa6ba');R(g,x+8,y+5,1,1,'#9aa6ba');}break;"""
N["case 'ferry':"]="""case 'ferry':{ice(x-15,y+5,30,6);R(g,x-15,y-2,30,8,K);R(g,x-14,y-1,28,6,'#f4f8ff');R(g,x-14,y+3,28,2,'#2f5fae');R(g,x-14,y+5,28,1,'#e03a4e');R(g,x+13,y-1,2,4,K);
  for(let k=0;k<3;k++){R(g,x-12+k*5,y-4,4,3,K);R(g,x-11+k*5,y-3,2,1,['#e03a4e','#ffc727','#33b24a'][k]);}R(g,x+2,y-9,11,8,K);R(g,x+3,y-8,9,6,'#f4f8ff');for(let k=0;k<4;k++)R(g,x+4+k*2,y-7,1,1,'#2f5fae');R(g,x+7,y-13,3,5,K);R(g,x+8,y-12,1,3,'#e03a4e');R(g,x+8,y-14,1,1,'#c6d9f3');}break;"""
for h,n in N.items(): case(h,n)
s=s[:a]+body+s[i+1:]
open(f,'w',encoding='utf-8').write(s)
print('p86 landmarks pass 2:',len(N),'redrawn')
