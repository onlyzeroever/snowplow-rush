import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:90])
    s=s.replace(a,b)
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
def swapstmt(prefix,new):
    global s
    assert s.count(prefix)==1,prefix
    a=s.index(prefix);e=s.index(']);',a)
    s=s[:a]+new+s[e+3:]
# Props art pass, batch 1 (Nov 15): the weakest high-use props redrawn to the character standard (outline,
# three-tone shading lit from the top left, readable shapes). Every canvas size and footprint is unchanged, so
# collisions and level layouts are exactly as before.
swapfn('mooringSprite',"""function mooringSprite(){return spr(["..KKKK..",".KccUUK.","KcUUUUXK","KKKKKKKK",".KcUUXK.","KLLLLLlK","KlllllhK",".KcUUXK.","KKKKKKKK"],{c:'#8793a8',U:'#55607a',X:'#2a2a36',L:'#d9a464',l:'#a8743f',h:'#6b4426'});}""")
swapfn('benchSprite',"""function benchSprite(){return spr(["KKKKKKKKKKKK","KELLLLLLLLlK","KXKKKKKKKKXK","KELLLLLLLLlK","KlllllllllhK",".KX......XK."],{L:'#c98d4a',l:'#8a5a2c',E:'#f0c48a',h:'#55321d',X:'#3a3f55'});}""")
swapfn('statueSprite',"""function statueSprite(){return spr(["...KK...","..KeaK..","..KabK..",".KKKKKK.","KeaaaabK","KeKaaKbK",".KKabbK.","..KaKbK.","KKKKKKKK","KCCCCCcK","KKKKKKKK"],{e:'#e8b878',a:'#c08a4a',b:'#8a5a2c',C:'#d6dee9',c:'#8793a8'});}""")
swapfn('barrelSprite',"""function barrelSprite(){return spr([".KKKKKK.","KlOOOOlK","KKKKKKKK","KOLLLLlK","KOLLLLlK","KXXXXXXK","KOLLLLlK","KOLLLLlK","KlLLLLlK",".KKKKKK."],{L:'#b8501a',l:'#7a3a12',O:'#f07a1a',X:'#2a2a36'});}""")
swapfn('coneSprite',"""function coneSprite(){return spr(["...K...","..KOK..","..KWK..",".KOOoK.",".KWWwK.",".KOOoK.","KOOOOoK","KXXXXXK","KKKKKKK"],{o:'#b8501a',X:'#2a2a36'});}""")
swapstmt('SPR.trash=spr([',"""SPR.trash=spr([".KKKKK.","KCCCCcK","KKKKKKK","KQGgGgK","KQGgGgK","KQGgGgK","KQGGGgK",".KKKKK."],{Q:'#5fd07a',G:'#2f9a4e',g:'#1f6e38',C:'#d6dee9',c:'#8793a8'});""")
swapstmt('SPR.hydrant=spr([',"""SPR.hydrant=spr(["..KKK..",".KpRrK.",".KKKKK.","KKpRrKK","KrpRrrK","KKpRrKK",".KpRrK.","KKKKKKK"]);""")
swapfn('hutSprite',"""function hutSprite(a){const i=a%4,A=['#d8364b','#3f86d6','#33b24a','#ffc727'][i],sh=['#9c2236','#2a5fa8','#1f7a33','#d49a12'][i],hi=['#f0687a','#7ab4f0','#6fd67f','#ffe27a'][i];
  return spr(["......KKKK......","....KKUUXXKK....","..KKUUUUXXXXKK..",".KUUUUUUXXXXXXK.","KKKKKKKKKKKKKKKK",".KeAAAAAAAAAAaK.",".KeAAAAAAAAAAaK.",".KeKKKKAAKKKKaK.",".KeKYYKAAKTTKaK.",".KeKYYKAAKTTKaK.",".KeKKKKAAKTTKaK.",".KeAAAAAAKTTKaK.",".KeAAAAAAKTYKaK.",".KaaaaaaaKTTKaK.",".KaaaaaaaKTTKaK.",".KKKKKKKKKKKKKK."],{A:A,a:sh,e:hi,U:'#8793a8',X:'#55607a',T:'#55321d',Y:'#ffd23f'});}""")
swapfn('rockSprite',"""function rockSprite(w,h){const c=mk(w,h),g=c.getContext('2d');let sd=(w*73+h*151+7)>>>0;const rnd=()=>{sd=(Math.imul(sd,1103515245)+12345)>>>0;return ((sd>>>16)&0x7fff)/32768;};
  const a=h*0.58,sp=[];for(let y=0;y<h;y++){let k;if(y<a){const u=(a-y-0.5)/a;k=Math.sqrt(Math.max(0,1-u*u));}else k=1-0.12*Math.pow((y-a)/Math.max(1,h-a),2);
    let hw=k*(w/2-0.5);if(y>1&&y<h-2&&rnd()<0.3)hw-=1;hw=Math.max(1,Math.round(hw));sp.push([Math.round(w/2-hw),Math.round(w/2+hw)-1]);}
  for(let y=0;y<h;y++){const [x0,x1]=sp[y];R(g,x0,y,x1-x0+1,1,K);}
  const T=['#c3cbdb','#a3adc0','#8793a8','#6a7896','#55607a'];
  for(let y=1;y<h-1;y++){const [x0,x1]=sp[y];const hw=Math.max(1,(x1-x0)/2),cx=(x0+x1+1)/2;for(let x=x0+1;x<x1;x++){const u=(x+0.5-cx)/hw,v=(y+0.5)/h;const l=0.55*u+1.1*(v-0.35);
    let t=l<-0.35?0:l<0.05?1:l<0.45?2:l<0.8?3:4;if(y>=h-2)t=4;R(g,x,y,1,1,T[t]);}}
  const nc=Math.max(1,Math.round(w/20));for(let n=0;n<nc;n++){let x=Math.round(w*(0.3+0.4*rnd())),y=Math.round(h*(0.42+0.16*rnd()));const L=Math.max(2,Math.round(h*0.22));
    for(let i=0;i<L&&y<h-2;i++){const [x0,x1]=sp[y];if(x>x0&&x<x1)R(g,x,y,1,1,'#3e4762');y++;if(rnd()<0.45)x+=rnd()<0.5?-1:1;}}
  const cap=Math.max(1,Math.round(h*0.28));for(let y=1;y<=cap;y++){const [x0,x1]=sp[y];R(g,x0+1,y,Math.max(0,x1-x0-1),1,y===1?'#ffffff':PAL.W);}
  {const y=cap+1;if(y<h-1){const [x0,x1]=sp[y];for(let x=x0+1;x<x1;x++)if(rnd()<0.45)R(g,x,y,1,1,PAL.W);else if(rnd()<0.3)R(g,x,y,1,1,'#d3e3f7');}}
  return c;}""")
swapfn('bollardSprite',"""function bollardSprite(){return spr([".KKK.","KcUXK","KcUXK","KYYdK","KcUXK","KcUXK","KYYdK","KcUXK","KKKKK"],{c:'#8793a8',U:'#55607a',X:'#2a2a36',d:'#c98a12'});}""")
swapfn('tireSprite',"""function tireSprite(){const c=mk(11,11),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,5,5,5);
  for(let y=0;y<11;y++)for(let x=0;x<11;x++){const dx=x-5,dy=y-5,d=Math.sqrt(dx*dx+dy*dy);if(d<=4.4&&d>2.3){let col=(dx+dy)<0?'#55586a':'#33364a';if(d>3.5&&Math.floor((Math.atan2(dy,dx)+Math.PI)/(Math.PI/6))%2)col='#1b1f3b';R(g,x,y,1,1,col);}}
  g.fillStyle=K;pixCircle(g,5,5,2);g.fillStyle='#8793a8';pixCircle(g,5,5,1);R(g,5,5,1,1,'#55607a');R(g,4,4,1,1,'#d6dee9');R(g,3,1,3,1,'#6b6f82');return c;}""")
swapfn('churnSprite',"""function churnSprite(){return spr(["..KKK..",".KCCcK.",".KKKKK.","..KCK..",".KWCcK.","KWCCCcK","KcccccK","KWCCCcK","KWCCccK",".KKKKK."],{C:'#c6d0e0',c:'#8793a8',W:'#f4f8ff'});}""")
swapfn('speakerSprite',"""function speakerSprite(){return spr(["KKKKKKKKKK","KcUUUUUUXK","KcUUKKUUXK","KcUKcXKUXK","KcUUKKUUXK","KcUUUUUUXK","KcUKKKKUXK","KcKccUUKXK","KcKcKKUKXK","KcKUKKXKXK","KcKUXXXKXK","KcUKKKKUXK","KXXXXXXXXK","KKKKKKKKKK"],{c:'#8793a8',U:'#55607a',X:'#2a2a36'});}""")
swapfn('meterSprite',"""function meterSprite(){return spr([".KKKK.","KcUUXK","KcVVXK","KcVRXK","KcUUXK","KcUUXK",".KKKK.","..KK..","..KK..","..KK..","..KK..","..KK..","..KK..","..KK..",".KKKK.","KKKKKK"],{c:'#8793a8',U:'#55607a',X:'#2a2a36'});}""")
swapfn('turnstileSprite',"""function turnstileSprite(){return spr(["..KKKK..",".KCCCcK.",".KCccXK.","KKKKKKKK","KCCCCccK","KKKCcKKK","..KCcK..","..KCcK..","..KCcK..","..KCcK..",".KKCcKK.",".KKKKKK."],{C:'#d6dee9',c:'#8793a8',X:'#2a2a36'});}""")
swapfn('sacksSprite',"""function sacksSprite(){const c=mk(16,10),g=c.getContext('2d');const S=["..KK..",".KllK.","KhSSsK","KSSSsK","KSSssK",".KKKK."],P={K:K,l:'#8a5a2c',h:'#f6ecd0',S:'#e8d9b0',s:'#c9a85a'};
  const put=(ox,oy)=>{for(let y=0;y<6;y++)for(let x=0;x<6;x++){const ch=S[y][x];if(ch!=='.')R(g,ox+x,oy+y,1,1,P[ch]);}};put(2,0);put(8,0);put(0,4);put(5,4);put(10,4);return c;}""")
swapfn('cabinSprite',"""function cabinSprite(){const c=mk(44,26),g=c.getContext('2d');
  R(g,33,0,6,6,K);R(g,34,1,4,5,'#9aa1b5');R(g,34,1,1,5,'#c6d0e0');R(g,37,1,1,5,'#6a7286');
  R(g,0,3,44,8,K);R(g,1,4,42,6,'#6b3f22');for(let x=2;x<42;x+=4)R(g,x,5,2,4,'#55321d');R(g,1,4,42,1,'#8a5a34');
  R(g,0,10,44,16,K);R(g,1,11,42,14,'#8a5a34');for(let y=11;y<25;y+=3){R(g,1,y,42,1,'#c98d4a');if(y+2<25)R(g,1,y+2,42,1,'#55321d');R(g,1,y,2,2,'#e0b070');R(g,41,y,2,2,'#e0b070');}
  for(const wx of [5,30]){R(g,wx,13,9,7,K);R(g,wx+1,14,7,5,'#ffe27a');R(g,wx+1,14,7,1,'#fff6c8');R(g,wx+4,14,1,5,K);R(g,wx+1,16,7,1,K);}
  R(g,18,14,8,12,K);R(g,19,15,6,10,'#55321d');R(g,19,15,6,1,'#6b3f22');R(g,21,15,1,10,'#6b3f22');R(g,23,20,1,1,'#ffc727');return c;}""")
swapfn('wellSprite',"""function wellSprite(){const c=mk(17,17),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,8,8,8);
  for(let y=0;y<17;y++)for(let x=0;x<17;x++){const dx=x-8,dy=y-8,d=Math.sqrt(dx*dx+dy*dy);if(d<=7.4&&d>4.5){const seg=Math.floor((Math.atan2(dy,dx)+Math.PI)/(Math.PI/6));let col=seg%2?'#a3adc0':'#c3cbdb';if(dx+dy>3)col=seg%2?'#6a7896':'#8793a8';R(g,x,y,1,1,col);}}
  g.fillStyle=K;pixCircle(g,8,8,4);g.fillStyle='#244a87';pixCircle(g,8,8,3);g.fillStyle='#3f6fc0';pixCircle(g,7,7,2);R(g,6,6,2,1,'#bfe4ff');
  R(g,0,7,17,3,K);R(g,1,8,15,1,'#c98d4a');R(g,1,8,4,1,'#e0b070');R(g,8,10,1,2,'#e8d9b0');R(g,7,12,3,2,K);R(g,8,12,1,1,'#c98d4a');return c;}""")
swapfn('logSprite',"""function logSprite(){const c=mk(14,28),g=c.getContext('2d');
  R(g,2,0,10,28,K);R(g,0,3,14,22,K);R(g,1,1,12,26,K);R(g,2,1,10,26,'#8a5a34');R(g,1,3,12,22,'#8a5a34');R(g,1,3,2,22,'#b07a44');R(g,11,3,2,22,'#5e3c22');
  for(let y=4;y<24;y+=5){R(g,1,y,1,2,'#6b4426');R(g,12,y+2,1,2,'#3d2716');}R(g,4,0,6,2,'#c98d4a');R(g,5,1,4,1,'#e0b070');
  R(g,3,4,8,21,K);R(g,4,5,6,19,'#4a2f1c');R(g,4,5,6,1,'#2e1d11');
  const rider=(y,hat,coat)=>{R(g,3,y+3,8,4,K);R(g,4,y+4,6,2,coat);R(g,3,y+4,1,1,'#f6c7a1');R(g,10,y+4,1,1,'#f6c7a1');R(g,5,y,4,4,K);R(g,6,y+1,2,2,hat);R(g,6,y,2,1,'#f6c7a1');R(g,7,y+2,1,1,'#ffffff');};
  rider(7,'#ffc727','#a82639');rider(15,'#33b24a','#2a5fa8');return c;}""")
swapfn('cairnSprite',"""function cairnSprite(){const c=mk(14,16),g=c.getContext('2d');const st=(x,y,w,h)=>{R(g,x+1,y,w-2,h,K);R(g,x,y+1,w,h-2,K);R(g,x+1,y+1,w-2,h-2,'#8f9ab0');R(g,x+1,y+1,w-2,1,'#c3cbdb');R(g,x+1,y+1,1,h-3,'#b0bacc');R(g,x+1,y+h-2,w-2,1,'#6a7590');R(g,x+w-2,y+2,1,h-3,'#6a7590');};
  st(0,11,14,5);st(1,7,11,5);st(3,4,8,4);st(4,1,5,4);return c;}""")
swapfn('deckchairSprite',"""function deckchairSprite(a){const i=a%3;return spr(["KKKKKKKKKK","KLWWWWWwlK","KLWWWWWwlK","KLAAAAAalK","KLAAAAAalK","KLWWWWWwlK","KLWWWWWwlK","KKKKKKKKKK","KLAAAAAalK","KLAAAAAalK","KLWWWWWwlK","KLWWWWWwlK","KLAAAAAalK","KKKKKKKKKK"],{A:['#e03a4e','#3f86d6','#ffc727'][i],a:['#a82639','#2a5fa8','#d49a12'][i],L:'#c98d4a',l:'#8a5a2c'});}""")
open(f,'w',encoding='utf-8').write(s)
print('p82 props batch 1: 22 props redrawn')
