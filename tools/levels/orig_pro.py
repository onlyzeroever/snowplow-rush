"""The original 18 jobs, raised to the pro look WITHOUT touching layout, size or difficulty: the hand-built levels stay
exactly as they are; on top go only (1) a remap of plain concrete to proper paving, (2) painted ground detail (manholes,
drains, oil, cracks, frozen puddles, grates) placed only where the ground under them is the right type, and (3)
overhead strings of lights and banners. None of these block anything.  -> orig_pro.json (installed by p68)"""
import json, random

D = json.load(open('/home/claude/levels/orig_dump.json'))
T_GRASS, T_ASPH, T_CONC, T_YEL, T_WHT, T_ICE, T_BLOCK = 0, 1, 2, 3, 4, 5, 9

REMAP = dict(driveway='slab', gardens='pave', culdesac='slab', park='gravel', school='slab', maple='slab', farmyard='cobble',
             orchard='gravel', pond='stone', retreat='stone', village='cobble', shops='slab', lot='slab', street='slab',
             mansion='pave', stadium='slab')
# overhead pieces per job: (kind, every px, style list) placed across the widest paved run at that height
OVERS = dict(gardens=('lights', 160), culdesac=('lights', 200), park=('lights', 220), school=('lights', 260), maple=('lights', 180),
             farmyard=('lights', 300), retreat=('lights', 260), village=('lights', 200), shops=('lights', 220), lot=('lights', 360),
             street=('lights', 240), mansion=('lights', 320), stadium=('lights', 340), airport=('lights', 600))
BANNERS = dict(village=[(700, 1)], shops=[(300, 3), (1200, 0)], street=[(500, 1), (1500, 3), (2500, 0)], stadium=[(400, 0), (1600, 3)],
               school=[(120, 1)], maple=[(380, 1)], airport=[(300, 0)])
DENS = dict(driveway=1.6, gardens=1.4, culdesac=1.3)          # small early jobs get relatively more detail


def build(jid):
    j = D[jid]; cols, rows, T, pw, ph = j['cols'], j['rows'], j['type'], j['pw'], j['ph']
    r = random.Random(sum(ord(c) * (i + 1) for i, c in enumerate(jid)))
    def t_at(x, y):
        cx, cy = int(x) // 2, int(y) // 2
        return T[cy * cols + cx] if 0 <= cx < cols and 0 <= cy < rows else T_BLOCK
    def all_of(x, y, w, h, kinds):
        for yy in range(int(y), int(y + h), 2):
            for xx in range(int(x), int(x + w), 2):
                if t_at(xx, yy) not in kinds: return False
        return True
    used = []
    def free(x, y, w, h, pad=6):
        return all(x + w + pad < a or a + c + pad < x or y + h + pad < b or b + d + pad < y for a, b, c, d in used)
    dec = []
    def put(kind, x, y, w, h, kinds, *args):
        if all_of(x, y, w, h, kinds) and free(x, y, w, h):
            dec.append([kind, int(x), int(y)] + list(args)); used.append((x, y, w, h)); return True
        return False
    dens = DENS.get(jid, 1.0)
    n_area = pw * ph / 10000.0
    asph = (T_ASPH,); paved = (T_CONC,); grass = (T_GRASS,)
    tries = int(260 * n_area * dens)
    counts = dict(manhole=0, drain=0, oil=0, crack=0, puddle=0, grate=0)
    target = dict(manhole=0.55, drain=0.7, oil=0.5, crack=0.6, puddle=0.35, grate=0.25)
    for k in range(tries):
        x, y = r.randint(2, pw - 20), r.randint(10, ph - 20)
        kind = r.choice(list(target))
        if counts[kind] >= target[kind] * n_area * dens: continue
        if kind == 'manhole': ok = put('manhole', x, y, 11, 11, asph)
        elif kind == 'drain':
            # a drain sits on the road right against its kerb
            if t_at(x, y) == T_ASPH and t_at(x - 4, y) != T_ASPH: ok = put('drain', x, y, 10, 5, asph)
            elif t_at(x + 10, y) == T_ASPH and t_at(x + 14, y) != T_ASPH: ok = put('drain', x, y, 10, 5, asph)
            else: ok = False
        elif kind == 'oil': a = r.choice((5, 6, 7)); ok = put('oil', x, y, a * 2, a * 2, asph, a, r.randint(1, 9))
        elif kind == 'crack': a = r.choice((18, 22, 26)); ok = put('crack', x, y, a, a, asph + paved, a, r.randint(1, 9))
        elif kind == 'puddle': a = r.choice((5, 6, 7, 8)); ok = put('puddle', x, y, a * 2 + 1, a + 1, asph + paved + grass, a, r.randint(1, 9))
        else: ok = put('grate', x, y, 16, 16, paved)
        if ok: counts[kind] += 1
    over = []
    if jid in OVERS:
        kind, every = OVERS[jid]; style = 0
        for y in range(every // 2, ph - 40, every):
            # the widest run of open (non-blocked) ground at this height
            best, cur, x0 = (0, 0), 0, 0
            for x in range(0, pw, 2):
                if t_at(x, y) != T_BLOCK and t_at(x, y - 20) != T_BLOCK:
                    if cur == 0: x0 = x
                    cur += 2
                    if cur > best[1]: best = (x0, cur)
                else: cur = 0
            if best[1] >= 60:
                over.append([kind, best[0], y, best[1], style % 4]); style += 1
    for (y, wi) in BANNERS.get(jid, []):
        if y >= ph - 40: continue
        best, cur, x0 = (0, 0), 0, 0
        for x in range(0, pw, 2):                    # across the widest open run at this height (the road), not the houses
            if t_at(x, y) not in (T_BLOCK, T_GRASS) and t_at(x, y + 20) != T_BLOCK:
                if cur == 0: x0 = x
                cur += 2
                if cur > best[1]: best = (x0, cur)
            else: cur = 0
        if best[1] >= 50: over.append(['banner', best[0], y, best[1], wi])
    return dict(remap=REMAP.get(jid), decals=dec, over=over)


OUT = {jid: build(jid) for jid in D}
json.dump(OUT, open('/home/claude/levels/orig_pro.json', 'w'))
print({k: (len(v['decals']), len(v['over']), v['remap']) for k, v in OUT.items()})
