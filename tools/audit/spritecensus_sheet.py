# sheet for tools/audit/spritecensus.js output
import json,base64,io,hashlib
import os; os.makedirs('/tmp/va',exist_ok=True)
from PIL import Image,ImageDraw,ImageFont
o=json.load(open('/tmp/va/allspr.json'));font=ImageFont.load_default()
# dedupe hazard sprites by pixel hash
seen=set();items=[]
for x in o:
    raw=base64.b64decode(x['u'].split(',')[1]);im=Image.open(io.BytesIO(raw)).convert('RGBA')
    h=hashlib.md5(im.tobytes()).hexdigest()
    if h in seen:continue
    seen.add(h);items.append((x,im))
print(len(items))
grporder={'SPR':0,'const':1,'frames':2,'chaser':3,'hazard':4,'pickup':5}
items.sort(key=lambda t:(grporder[t[0]['grp']],t[0]['name']))
PW=1500;pages=[];pg=Image.new('RGB',(PW,1100),(200,214,232));d=ImageDraw.Draw(pg);x=6;y=6;rowh=0;idx=0
for n,(it,im) in enumerate(items):
    s=4 if max(im.size)<=24 else 3 if max(im.size)<=48 else 2 if max(im.size)<=110 else 1
    im2=im.resize((im.width*s,im.height*s),Image.NEAREST)
    if im2.height>900:im2=im2.crop((0,0,im2.width,900))
    cw=max(im2.width,96)+8;ch=im2.height+26
    if x+cw>PW:x=6;y+=rowh+4;rowh=0
    if y+ch>1100:pages.append(pg);pg=Image.new('RGB',(PW,1100),(200,214,232));d=ImageDraw.Draw(pg);x=6;y=6;rowh=0
    pg.paste(im2,(x,y),im2);d.text((x,y+im2.height+2),f"{n} {it['name'][:18]}",fill=(19,48,107),font=font);d.text((x,y+im2.height+13),f"{it['w']}x{it['h']}",fill=(80,80,100),font=font)
    x+=cw;rowh=max(rowh,ch)
pages.append(pg)
for i,p in enumerate(pages):p.save(f'/tmp/va/allspr_{i}.png')
json.dump([(n,it['name'],it['w'],it['h']) for n,(it,im) in enumerate(items)],open('/tmp/va/allspr_idx.json','w'))
print(len(pages))
