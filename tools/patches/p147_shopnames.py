# p147 (Alex, Nov 20 22:34: "I don't like how repetitive the shop/building names are, feels poorly thought").
# Main Street had 52 shops with 8 names (ICE CREAM 10 times, TOYS 9); Chinatown 35 shops with 10 names.
# Now: 80 new themed names (theme park treats and stalls, Chinatown, harbour, high street, farm, ski, north),
# and every job swaps a name it has already used for a fresh one from its area's list (only once the whole list is
# used does a name come back, and never within 640px, two and a half screens). Landmark names (CITY HALL, STATION...) appear once and are never swapped.
import sys
f=sys.argv[1];s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n==cnt,(a[:90],n)
    s=s.replace(a,b)

NEW={
 'themepark':['POPCORN','CANDY FLOSS','FUDGE','PRETZELS','WAFFLES','CHURROS','HOT COCOA','DONUTS','CUPCAKES','SHAKES',
              'HOT DOGS','LEMONADE','PANCAKES','TOFFEE APPLES','SWEET SHOP','JOKE SHOP','MAGIC SHOP','PHOTO BOOTH','HAT SHOP',
              'PLUSH TOYS','BALLOONS','T-SHIRTS','SNOW GLOBES','PIN SHOP','MUSIC BOX','PUPPETS','FACE PAINT','LOCKERS',
              'FIRST AID','GUEST INFO','PRIZE DESK','FUN HOUSE','PENNY ARCADE','YO-YOS','COMICS','TEDDY BEARS'],
 'chinatown':['DIM SUM','BUBBLE TEA','LANTERNS','SILK SHOP','JADE','ROAST DUCK','RICE CAKES','PORCELAIN','PAPER ART',
              'WONTONS','CONGEE','SPICE SHOP','FAN SHOP','TOFU HOUSE'],
 'harbour':['CHANDLERY','NET LOFT','SAIL LOFT','ROPE WORKS','OYSTER BAR','CHIP SHOP','SMOKEHOUSE','TACKLE SHOP',
            'COASTGUARD','CRAB SHACK','ICE HOUSE','SEAFOOD','MARINA'],
 'city':['NEWSAGENT','HARDWARE','OPTICIAN','BIKE SHOP','BOUTIQUE','CAMERAS','SWEETS','FISH SHOP','GROCER','CHEESE','BAGELS'],
 'farm':['FEED STORE','SADDLERY','CIDER','HONEY','EGGS'],
 'ski':['BOOT HIRE','BOARD SHOP','FONDUE','SKI SHOP','SLEDS','GOGGLES'],
}
# shop colours reuse the existing palette (wall, brickwork, sign) so the new signs match the old ones
PAL=[['#3f86d6','#2a5fa8','#d8364b'],['#e8c87a','#c98d4a','#a8673a'],['#e07a8a','#b04a5a','#7a1f33'],['#8fbf5a','#5e8a3a','#1f7a5c'],
     ['#f4f8ff','#c6d9f3','#ff4fa3'],['#ffc727','#e29a1c','#9b5fd6'],['#c6d9f3','#8793a8','#33b24a'],['#9b5fd6','#6b4fa8','#ffc727'],
     ['#d8364b','#a82639','#ffc727'],['#7a4a2a','#55321d','#ffc727'],['#13306b','#0b1838','#ff4fa3'],['#e8e0cc','#d6cdb4','#13306b']]
rows=[];k=0
for area,names in NEW.items():
    for n in names:
        p=PAL[(k*5+3)%len(PAL)];k+=1
        rows.append("['%s','%s','%s','%s']"%(n.replace("'","\\'"),p[0],p[1],p[2]))
by=lambda *names:'['+','.join("'%s'"%n for n in names)+']'
pools={
 'themepark':by('TICKETS','SOUVENIRS','ARCADE','BURGERS','ICE CREAM','CAFE','TOYS','PIZZA','GIFTS','BAKERY','COFFEE','DINER','KITES',*NEW['themepark']),
 'chinatown':by('NOODLES','TEA HOUSE','DUMPLINGS','HERBALIST','BAO BAR','MAHJONG','LUCKY CAT','HOT POT','KITES','GIFTS','BAKERY',*NEW['chinatown']),
 'harbour':by('FISH MARKET','WAREHOUSE','CUSTOMS','FERRIES','BOAT SHED','CAFE','DINER','COFFEE',*NEW['harbour']),
 'city':by('CORNER SHOP','BAKERY','CAFE','BOOKS','FLOWERS','TOYS','BUTCHER','CHEMIST','PET SHOP','BANK','BARBER','DELI','SHOES','PIZZA','GIFTS',
           'COFFEE','CINEMA','POST OFFICE','LIBRARY','DINER','RECORDS','GALLERY','TAILOR','LAUNDRY','JEWELLER','FLORIST',*NEW['city']),
 'farm':by('FARM SHOP','DAIRY','TEA ROOM','BAKERY','BUTCHER','CAFE',*NEW['farm']),
 'ski':by('SKI SCHOOL','SKI HIRE','APRES','CAFE','COFFEE','HOT COCOA',*NEW['ski']),
}
pools['suburbs']=pools['city'];pools['pass']=pools['ski'];pools['north']=pools['ski']
poolJs='{'+','.join('%s:%s'%(k2,v) for k2,v in pools.items())+'}'

rep("function buildLevel(idx){","SHOPS.push("+",".join(rows)+");  // p147: appended after every older entry so level data indices keep their names\nfunction buildLevel(idx){")
rep("const SHOPS=[","""// p147: a job never shows the same shop name twice within 640px; the next fresh name comes from its area's list
const SHOP_POOL_N=%s;let SHOP_POOL=null;
function shopPick(kind,a,g){if(kind!=='shop'&&kind!=='shopv'&&kind!=='big')return a;if(!SHOP_POOL){SHOP_POOL={};for(const k in SHOP_POOL_N)SHOP_POOL[k]=SHOP_POOL_N[k].map(n=>SHOPS.findIndex(S=>S[0]===n)).filter(i=>i>=0);}
  const L=g.def,y=g._shopY||0,used=g._shopUsed||(g._shopUsed=new Map()),i0=((a%%SHOPS.length)+SHOPS.length)%%SHOPS.length,ok=i=>{const u=used.get(SHOPS[i][0]);return !u||u.every(v=>Math.abs(v-y)>640);};
  const fresh=i=>!used.has(SHOPS[i][0]);let i=i0;if(!fresh(i)){const pool=SHOP_POOL[L.id==='chinatown'?'chinatown':L.area]||SHOP_POOL.city;let h=0;for(const ch of L.id)h=(h*31+ch.charCodeAt(0))>>>0;const st=(h+(g._shopN||0)*7)%%pool.length;
    let pick=-1;for(let k=0;k<pool.length&&pick<0;k++){const j=pool[(st+k)%%pool.length];if(fresh(j))pick=j;}
    for(let k=0;k<pool.length&&pick<0;k++){const j=pool[(st+k)%%pool.length];if(ok(j))pick=j;}if(pick>=0)i=pick;}
  g._shopN=(g._shopN||0)+1;const nm=SHOPS[i][0];if(!used.has(nm))used.set(nm,[]);used.get(nm).push(y);return i;}
const SHOPS=["""%poolJs)
rep("  for(const p of D.scen||[]){const P2=PROPS[p[0]];if(!P2)continue;const a=p[3]!=null?p[3]:P2.arg,sp=P2.make(a),f2=P2.foot(a);",
    "  for(const p of D.scen||[]){const P2=PROPS[p[0]];if(!P2)continue;g._shopY=p[2];const a=shopPick(p[0],p[3]!=null?p[3]:P2.arg,g),sp=P2.make(a),f2=P2.foot(a);")
open(f,'w').write(s)
print('p147 shop names: %d new names, no repeats until an area runs out'%len(rows))
