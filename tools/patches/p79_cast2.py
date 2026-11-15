import sys,json,os
f=sys.argv[1];s=open(f,encoding='utf-8').read()
J=json.load(open(''+__import__('os').path.join(__import__('os').path.dirname(__file__),'..','art','js.json')+''))['cast2']
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:90])
    s=s.replace(a,b)
def swapfn(name,new):
    global s
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
# The last eight characters redrawn (Nov 15): Mrs Grimshaw (curlers, glasses, spotted dressing gown, clipboard,
# slippers), the warden (cap badge, moustache, hi-vis with reflective band, ticket machine), the goose (thick neck),
# the yeti (shaggy, fangs, claws), the sledder, the shopping trolley and the rolling snowball (shading, stones, twigs).
for k,nm in [('grim','grimshawSprite'),('warden','wardenSprite'),('goose','gooseSprite'),('yeti','yetiSprite'),('cart','cartSprite'),('snowball','snowballSprite')]:
    swapfn(nm,J[k])
a=s.index('SPR.sled=spr([');e=s.index(']);',a)
s=s[:a]+'SPR.sled='+J['sled']+';'+s[e+3:]
open(f,'w',encoding='utf-8').write(s)
