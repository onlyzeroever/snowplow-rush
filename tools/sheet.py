# usage: python3 sheet.py dir ids,comma out.png [title] [numbers start]  -> numbered contact sheet of jobs (snowy ground view), 2 columns per job
import sys, json
from PIL import Image, ImageDraw, ImageFont
d, ids, out = sys.argv[1], sys.argv[2].split(','), sys.argv[3]; title = sys.argv[4] if len(sys.argv) > 4 else ''
names = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28); f2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
ims = []
for i in ids:
    im = Image.open('%s/%s.png' % (d, i)); w = (im.width - 8) // 2; ims.append((i, im.crop((w + 8, 0, im.width, im.height))))
H = max(im.height for _, im in ims); colH = (H + 1) // 2
cw = 180 * 2 + 12; W = len(ims) * (cw + 20) + 20
o = Image.new('RGB', (W, colH + 110), '#13306b'); dr = ImageDraw.Draw(o)
if title: dr.text((20, 12), title, fill='#ffd23f', font=F)
for k, (i, im) in enumerate(ims):
    x = 20 + k * (cw + 20); lab = names.get(i, i)
    dr.text((x, 56), lab, fill='#ffffff', font=f2)
    half = (im.height + 1) // 2
    o.paste(im.crop((0, 0, 180, half)), (x, 90)); o.paste(im.crop((0, half, 180, im.height)), (x + 192, 90))
o.save(out); print(out, o.size)
