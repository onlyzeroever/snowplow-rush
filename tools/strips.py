# usage: python3 strips.py in.png out.png [seg=600] [zoom=2] [half=right|left]  -> job cut into columns, side by side
import sys
from PIL import Image
im=Image.open(sys.argv[1]); seg=int(sys.argv[3]) if len(sys.argv)>3 else 600; z=int(sys.argv[4]) if len(sys.argv)>4 else 2
half=sys.argv[5] if len(sys.argv)>5 else 'right'
w=(im.width-8)//2; src=im.crop((w+8,0,im.width,im.height)) if half=='right' else im.crop((0,0,w,im.height))
n=(src.height+seg-1)//seg
o=Image.new('RGB',(n*(w*z+8)-8,seg*z),'#13306b')
for k in range(n):
    c=src.crop((0,k*seg,w,min(src.height,(k+1)*seg))).resize((w*z,min(seg,src.height-k*seg)*z),Image.NEAREST); o.paste(c,(k*(w*z+8),0))
o.save(sys.argv[2]); print(o.size)
