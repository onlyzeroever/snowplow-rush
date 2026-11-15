import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# World map, landmark pass 3 (Nov 16): roller coaster, helter skelter, boatyard and the husky camp.
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
N["case 'coaster':"]="""case 'coaster':{const ty=k=>Math.round(y-2-9*Math.sin(k*0.21));for(let k=0;k<30;k+=3){const yy=ty(k);R(g,x-15+k,yy+2,1,y+9-yy-2,'#8793a8');}for(let k=0;k<30;k+=6){const yy=ty(k);R(g,x-15+k,yy+3,1,y+9-yy-3,'#c6d0dc');}
  for(let k=0;k<30;k++)R(g,x-15+k,ty(k)-1,1,4,K);for(let k=0;k<30;k++){const yy=ty(k);R(g,x-15+k,yy,1,1,'#e03a4e');R(g,x-15+k,yy+1,1,1,'#a82639');}
  const cx=x-7,cy=ty(8);R(g,cx-2,cy-5,7,5,K);R(g,cx-1,cy-4,5,3,'#ffc727');R(g,cx-1,cy-4,5,1,'#ffe27a');R(g,cx,cy-6,1,2,'#f6c7a1');R(g,cx+2,cy-6,1,2,'#f6c7a1');R(g,x-15,y+9,30,2,K);R(g,x-14,y+9,28,1,'#8793a8');break;}"""
N["case 'helter':"]="""case 'helter':{for(let r=0;r<20;r++){const hw=Math.round(2+r*0.25);R(g,x-hw-1,y-12+r,hw*2+2,1,K);const st=((r+(r>>1))>>1)%2;R(g,x-hw,y-12+r,hw*2,1,st?'#d8364b':'#f4f8ff');R(g,x+hw-2,y-12+r,2,1,st?'#a82639':'#c6d0dc');}
  for(let r=2;r<20;r+=4){const hw=Math.round(2+r*0.25)+1;R(g,x-hw-1,y-12+r,2,2,'#ffc727');R(g,x-hw-1,y-10+r,1,1,K);}R(g,x-1,y+4,3,4,K);R(g,x,y+5,1,3,'#2a2a36');R(g,x-1,y-16,1,5,K);R(g,x,y-16,3,2,'#ffc727');R(g,x-6,y+8,13,1,K);}break;"""
N["case 'boatyard':"]="""case 'boatyard':{R(g,x-15,y+9,30,2,K);R(g,x-14,y+9,28,1,'#a8673a');mBoat(g,x-12,y-3,26,'#3f86d6');R(g,x-11,y+3,24,1,'#e03a4e');for(const px of [x-9,x+8]){R(g,px,y+7,2,3,K);R(g,px-2,y+8,6,1,K);}
  for(let i=0;i<4;i++){R(g,x-12-i,y+5+i,1,1,K);R(g,x+13+i>x+15?x+15:x+13+i,y+5+i,1,1,K);}R(g,x-15,y-5,1,14,K);R(g,x-13,y-5,1,14,K);for(let k=0;k<5;k++)R(g,x-14,y-4+k*3,1,1,'#c98d4a');}break;"""
N["case 'huskies':"]="""case 'huskies':{mTent(g,x-15,y-8,14,15,'#f07a1a','#ffc727');R(g,x-1,y+2,7,4,K);R(g,x,y+3,5,2,'#8a5a34');R(g,x,y+3,5,1,'#c98d4a');R(g,x-2,y+6,9,1,K);R(g,x+6,y+5,1,1,K);
  const hk=(dx,dy)=>{R(g,dx,dy,7,4,K);R(g,dx+1,dy+1,5,2,'#8793a8');R(g,dx+1,dy+2,5,1,'#f4f8ff');R(g,dx+5,dy-2,4,4,K);R(g,dx+6,dy-1,2,2,'#8793a8');R(g,dx+7,dy,1,1,'#f4f8ff');R(g,dx+6,dy-3,1,1,K);R(g,dx-1,dy-2,2,3,K);R(g,dx-1,dy-1,1,1,'#f4f8ff');R(g,dx+1,dy+4,1,1,K);R(g,dx+5,dy+4,1,1,K);};
  hk(x+7,y-2);hk(x+7,y+5);R(g,x+6,y+1,2,1,'#55321d');R(g,x+6,y+4,2,1,'#55321d');}break;"""
for h,n in N.items(): case(h,n)
s=s[:a]+body+s[i+1:]
open(f,'w',encoding='utf-8').write(s)
print('p87 landmarks pass 3:',len(N),'redrawn')
