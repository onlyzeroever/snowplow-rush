import sys,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
J=json.load(open(''+__import__('os').path.join(__import__('os').path.dirname(__file__),'..','art','js.json')+''))
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:90])
    s=s.replace(a,b)
def swapfn(name,new):
    global s
    a=s.index('function '+name+'(');e=s.index('\n',a)
    # function bodies here are one or two lines; find the end by matching braces
    depth=0;i=s.index('{',a)
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
# Creatures and characters redrawn (Nov 15): Holstein cow with head, horns, patches and udder; fluffy sheep with a
# black face; horses with an arched neck, mane, tail and hooves; skiers with helmet, goggles, striped jacket, poles
# and skis; a proper sheet ghost with a wavy hem; polar bear with a shoulder hump, snout and paws; gull and dog.
swapfn('sheepSprite',J['sheep'])
swapfn('horseSprite',J['horse'])
swapfn('skierSprite',J['skier'])
swapfn('ghostSprite',J['ghost'])
swapfn('bearSprite',J['bear'])
swapfn('gullSprite',J['gull'])
swapfn('forkliftSprite',J['fork'])
swapfn('bumperCarSprite',J['bump'])
# dog: new 14x10 art
a=s.index('SPR.dog=spr([');e=s.index(']);',a)
s=s[:a]+'SPR.dog=spr('+J['dog']+s[e+1:]
# cow: 16x12 now, so the places that centre it move by 2 and 3 pixels
rep('COW=spr(COW_ROWS,{p:\'#f28b8b\'})','COW=cowSprite()')
s=s.replace('const COW_ROWS=',J['cow']+'\nconst COW_ROWS=',1)
rep("b.drawImage(shadowOf(cw.flip?COWL:COW),Math.round(cw.x)-6+sp[0],Math.round(cw.y)-7+sp[1]);","b.drawImage(shadowOf(cw.flip?COWL:COW),Math.round(cw.x)-8+sp[0],Math.round(cw.y)-10+sp[1]);")
rep("baseShadow(cw.x-5,cw.y-3,10,5);","baseShadow(cw.x-7,cw.y-3,14,5);")
rep("const cyo=cy2-7-Math.round(cw.z)","const cyo=cy2-10-Math.round(cw.z)")
rep("b.drawImage(outlineOf(cw.flip?COWL:COW),cx2-7,cyo-1);b.drawImage(bright(cw.flip?COWL:COW),cx2-6,cyo);","b.drawImage(outlineOf(cw.flip?COWL:COW),cx2-9,cyo-1);b.drawImage(bright(cw.flip?COWL:COW),cx2-8,cyo);")
rep("text(b,'MOO?',cx2,cy2-18-Math.round(cw.z)","text(b,'MOO?',cx2,cy2-21-Math.round(cw.z)")
rep("R(b,x+1,sy(cw.y)+8,10,2,'rgba(27,31,59,0.2)');b.drawImage(cw.d>0?COWL:COW,x,y);","R(b,x+1,sy(cw.y)+11,14,2,'rgba(27,31,59,0.2)');b.drawImage(cw.d>0?COWL:COW,x,y);")
rep("btn('cow'+x+cw.y,x-2,y-2,16,14,","btn('cow'+x+cw.y,x-2,y-2,20,16,")

# Rocks/boulders: a rounded boulder with light and dark faces, a crack and a snow cap (was a flat grey box).
swapfn('rockSprite',"function rockSprite(w,h){const c=mk(w,h),g=c.getContext('2d'),a=h*0.5,sp=[];for(let y=0;y<h;y++){const k=y<a?Math.sqrt(Math.max(0,1-Math.pow((a-y-0.5)/a,2))):1-0.1*(y-a)/(h-a);const hw=Math.max(1,Math.round(k*(w/2-0.5)));sp.push([Math.round(w/2-hw),Math.round(w/2+hw)-1]);}"
  "for(let y=0;y<h;y++){const [x0,x1]=sp[y];R(g,x0,y,x1-x0+1,1,K);}"
  "for(let y=1;y<h-1;y++){const [x0,x1]=sp[y];for(let x=x0+1;x<x1;x++){const u=(x-x0)/Math.max(1,x1-x0);let col='#8793a8';if(u<0.42&&y<h*0.7)col='#a9b4c8';else if(u>0.58&&y>h*0.42)col='#6a7896';if(y>=h-2)col='#55607a';R(g,x,y,1,1,col);}}"
  "const cxk=Math.round(w*0.56);for(let i=0;i<Math.max(2,Math.round(h*0.3));i++)R(g,cxk+(i>>1),Math.round(h*0.38)+i,1,1,'#55607a');"
  "const cap=Math.max(1,Math.round(h*0.3));for(let y=1;y<=cap;y++){const [x0,x1]=sp[y];R(g,x0+1,y,Math.max(0,x1-x0-1),1,y===1?'#ffffff':PAL.W);}"
  "{const [x0,x1]=sp[cap+1]||sp[cap];for(let x=x0+2;x<x1-1;x+=3)R(g,x,cap+1,1,1,PAL.W);}return c;}")

# Sheep are now 15x11 (cream wool so they read on snow): centre them over their feet; horses/penguins/gulls unchanged.
rep("const mv=Math.hypot(hz.vx,hz.vy)>6?Math.floor(hz.anim*8)%2:0,fr=hz.peng?PENG_FR[mv]:hz.gull?GULL_FR[Math.floor(hz.anim*10)%2]:hz.horse?HORSE_FR[hz.col+mv]:SHEEP_FR[mv];",
    "const mv=Math.hypot(hz.vx,hz.vy)>6?Math.floor(hz.anim*8)%2:0,fr=hz.peng?PENG_FR[mv]:hz.gull?GULL_FR[Math.floor(hz.anim*10)%2]:hz.horse?HORSE_FR[hz.col+mv]:SHEEP_FR[mv],ox=(hz.horse||hz.peng||hz.gull)?1:3,oy=hz.horse?6:(hz.peng||hz.gull)?3:5;")
rep("b.drawImage(fr,-1,hy-(hz.horse?6:3));b.restore();}else b.drawImage(fr,hx-1,hy-(hz.horse?6:3));","b.drawImage(fr,-ox,hy-oy);b.restore();}else b.drawImage(fr,hx-ox,hy-oy);")
open(f,'w',encoding='utf-8').write(s)
