import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def swapfn(name,new):
    global s
    assert s.count('function '+name+'(')==1,name
    a=s.index('function '+name+'(');depth=0;i=s.index('{',a)
    while True:
        ch=s[i]
        if ch=='{':depth+=1
        elif ch=='}':
            depth-=1
            if depth==0:break
        elif ch in "'\"":
            q=ch;i+=1
            while s[i]!=q:
                if s[i]=='\\':i+=1
                i+=1
        i+=1
    s=s[:a]+new+s[i+1:]
# Map: the Mansion's map icon now matches the new in-game mansion (cream Georgian house: centre block with a
# columned portico and cupola, two forward wings, chimneys, lit windows). Same 50x32 footprint.
swapfn('mMansion',"""function mMansion(g,x,y){// 50x32
  const ST='#f1e6cf',STd='#d4c3a0',chim=(cx,cy)=>{R(g,cx,cy,4,7,K);R(g,cx+1,cy+1,2,6,MC.brick);R(g,cx-1,cy-1,6,2,K);R(g,cx,cy-1,4,1,MC.snow);};
  chim(x+16,y+1);chim(x+30,y+1);mRoof(g,x+13,y+3,24,9,4);
  R(g,x+21,y-1,8,6,K);R(g,x+22,y+1,6,3,ST);R(g,x+24,y+2,2,2,MC.lit);R(g,x+21,y-2,8,3,K);R(g,x+22,y-1,6,1,'#5fa89a');R(g,x+24,y-3,2,1,K);
  R(g,x+14,y+13,22,18,K);R(g,x+15,y+13,20,17,ST);R(g,x+15,y+13,20,1,STd);mWin(g,x+16,y+15,true);mWin(g,x+29,y+15,true);mWin(g,x+16,y+23,true);mWin(g,x+29,y+23,true);
  for(let r=0;r<5;r++){const hw=Math.round((r+1)/5*7);R(g,x+25-hw-1,y+10+r,hw*2+2,1,K);R(g,x+25-hw,y+10+r,hw*2,1,r<1?MC.snow:'#fbf5e8');}
  R(g,x+18,y+15,14,1,K);for(const cx of [x+19,x+22,x+26,x+29]){R(g,cx,y+16,2,14,'#fbfbff');R(g,cx+1,y+16,1,14,'#d6dee9');}
  R(g,x+23,y+22,4,8,K);R(g,x+24,y+23,2,7,'#5a3420');R(g,x+24,y+21,2,1,MC.lit);R(g,x+20,y+30,10,1,'#c6ccd8');
  for(const wx of [x,x+34]){mRoof(g,wx,y+7,16,8,3);R(g,wx+1,y+16,14,15,K);R(g,wx+2,y+16,12,14,ST);R(g,wx+2,y+16,12,1,STd);mWin(g,wx+3,y+18,true);mWin(g,wx+9,y+18,true);mWin(g,wx+3,y+24,true);mWin(g,wx+9,y+24,true);}
  chim(x+3,y+4);chim(x+43,y+4);R(g,x,y+31,50,1,K);}""")
open(f,'w',encoding='utf-8').write(s)
print('p104 map mansion')
