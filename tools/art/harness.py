# Tiny pixel-art harness: designs are lists of rects (x,y,w,h,col). Renders previews and emits JS R() code.
from PIL import Image, ImageDraw, ImageFont
PAL={'K':'#1b1f3b','W':'#f4f8ff','w':'#c6d9f3','Y':'#ffc727','y':'#e29a1c','H':'#7a4a2a','h':'#55321d','S':'#f6c7a1','s':'#e0a07f','p':'#f28b8b','t':'#e2546b','k':'#7a1f33','R':'#e03a4e','r':'#a82639','M':'#8a5a34','J':'#2f5fae','j':'#244a87','T':'#6b3f22','G':'#1f7a5c','g':'#145146','L':'#c98d4a','l':'#8a5a2c','B':'#3f86d6','b':'#2a5fa8','O':'#f07a1a','o':'#b8501a','C':'#d6dee9','c':'#8793a8','D':'#ffd23f','d':'#c98a12','X':'#2a2a36','E':'#ffe9a8','V':'#7ad3ff','N':'#ff4fa3','P':'#9b5fd6','Z':'#ffffff','Q':'#33b24a','q':'#1f7a33','U':'#55607a'}
def render(w,h,rects,extra=None):
    pal=dict(PAL); pal.update(extra or {})
    im=Image.new('RGBA',(w,h),(0,0,0,0)); px=im.load()
    for (x,y,ww,hh,col) in rects:
        c=pal.get(col,col); c=tuple(int(c[i:i+2],16) for i in (1,3,5))+(255,)
        for yy in range(max(0,y),min(h,y+hh)):
            for xx in range(max(0,x),min(w,x+ww)): px[xx,yy]=c
    return im
def sheet(items,out,S=10,bg='#dfe9f5'):
    # items: list of (label, PIL image)
    cw=max(i.width for _,i in items)*S+20; ch=max(i.height for _,i in items)*S+34
    cols=min(6,len(items)); rows=(len(items)+cols-1)//cols
    o=Image.new('RGB',(cols*cw,rows*ch),bg); d=ImageDraw.Draw(o); F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
    for k,(lab,im) in enumerate(items):
        x=(k%cols)*cw+10; y=(k//cols)*ch+24; d.text((x,4+(k//cols)*ch),lab,font=F,fill='#13306b')
        o.paste(im.resize((im.width*S,im.height*S),Image.NEAREST),(x,y),im.resize((im.width*S,im.height*S),Image.NEAREST))
    o.save(out)
def js(rects,var='g'):
    out=[]
    for (x,y,w,h,col) in rects:
        c="K" if col=='K' else ("'"+PAL.get(col,col)+"'")
        out.append(f"R({var},{x},{y},{w},{h},{c});")
    return ''.join(out)
def rows(rs,extra=None):
    w=max(len(x) for x in rs); h=len(rs); r=[]
    for y,row in enumerate(rs):
        for x,ch in enumerate(row):
            if ch!='.': r.append((x,y,1,1,ch))
    return render(w,h,r,extra)
