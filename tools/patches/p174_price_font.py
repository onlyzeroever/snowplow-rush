# Store prices in the pixel font (HELD from the live web game; in the lab and the app build). Nov 21.
# The font only had $ for money, so a store price like '£4.99', '4,99 €' or '¥800' would have shown as ' 4.99' in the
# apps: the pound, euro and yen signs were drawn as blanks.
#  - adds £ € ¥ ₩ ₹ ₺ ₪ ₱ to the font
#  - fontPrice(): makes a store price safe for the font: capitals, accents dropped ('KČ' -> 'KC', 'ZŁ' -> 'ZL'),
#    Arabic digits to 0-9, odd spaces to plain ones, direction marks removed. If something still can't be drawn, it is
#    built again from {amount, currency} when the app gives them ('SAR 18.99'); otherwise the unknown signs are dropped
#  - IAP.prices() runs every store price through fontPrice(); SRNative.prices() may now give
#    {productId: {price, amount, currency}} (RevenueCat: priceString, price, currencyCode) as well as plain strings
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("'$':['.###','#.#.','.##.','.#.#','###.'],",
    "'$':['.###','#.#.','.##.','.#.#','###.'],"
    "'£':['..##','.#..','###.','.#..','####'],'€':['..##','.#..','###.','.#..','..##'],'¥':['#.#','.#.','###','.#.','.#.'],"
    "'₩':['#...#','#.#.#','#####','#.#.#','.#.#.'],'₹':['####','...#','####','.#..','..##'],'₺':['.#..','.###','###.','.#.#','.##.'],"
    "'₪':['###.#','#.#.#','#.#.#','#...#','#.###'],'₱':['###.','####','###.','#...','#...'],")
rep("const gcache=new Map();",
    "// store prices made safe for the pixel font (p174)\n"
    "const FONT_MAP={'Ł':'L','Ø':'O','Đ':'D','Ð':'D','Æ':'AE','Œ':'OE','Þ':'TH','Ħ':'H','Ŧ':'T','ı':'I'};\n"
    "function fontNorm(v){return [...String(v==null?'':v).replace(/[\\u200e\\u200f\\u061c\\u202a-\\u202e\\u2066-\\u2069]/g,'').replace(/[\\u00a0\\u202f\\u2007\\u2009]/g,' ')\n"
    "  .replace(/[\\u0660-\\u0669]/g,c=>String(c.charCodeAt(0)-0x660)).replace(/[\\u06f0-\\u06f9]/g,c=>String(c.charCodeAt(0)-0x6f0)).replace(/\\u066b/g,'.').replace(/\\u066c/g,',')\n"
    "  .toUpperCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')].map(c=>FONT_MAP[c]!=null?FONT_MAP[c]:c).join('').replace(/ +/g,' ').trim();}\n"
    "function fontSafe(v){const s=fontNorm(v);return s&&[...s].every(c=>FONT[c])?s:null;}\n"
    "function fontPrice(v){if(v==null)return null;\n"
    "  if(typeof v==='object'){const a=fontSafe(v.price);if(a)return a;const n=Number(v.amount);\n"
    "    if(v.amount!=null&&isFinite(n)&&v.currency)for(const d of ['symbol','code'])try{const t=fontSafe(new Intl.NumberFormat('en-US',{style:'currency',currency:String(v.currency),currencyDisplay:d}).format(n));if(t)return t;}catch(e){}\n"
    "    v=v.price;if(v==null)return null;}\n"
    "  const a=fontSafe(v);if(a)return a;const t=[...fontNorm(v)].filter(c=>FONT[c]).join('').replace(/ +/g,' ').trim().replace(/^[.,:\\/ -]+|[.,:\\/ -]+$/g,'');\n"
    "  return /\\d/.test(t)?t:null;}\n"
    "const gcache=new Map();")
rep("const P=k=>p[this.ids[k]];","const P=k=>fontPrice(p[this.ids[k]]);")
open(f,'w',encoding='utf-8').write(s)
print('p174 store prices in the pixel font: £ € ¥ ₩ ₹ ₺ ₪ ₱, fontPrice() for every store price')
