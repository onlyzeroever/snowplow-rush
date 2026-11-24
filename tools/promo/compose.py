"""Builds a finished 9:16 promo video (1080 x 1920, 30 fps, H.264 + AAC): a narrated story over real gameplay.

    python3 -I tools/promo/compose.py <cut.json>

cut.json
{
  "story": "tools/promo/stories/s001_stolen_snow.json",   title for the story card
  "narration": "/home/claude/promo/work/s001",             narration.wav + words.json from tts.py
  "layout": "split",                                       split = story on top, gameplay below; full = gameplay full screen
  "clips": [{"cap": "/home/claude/promo/work/driveway_truck_1", "from": 1, "to": 600}, ...],   recordings from capture.js
  "channel": "Snow Stories", "byline": "a Snowplow Rush channel",
  "music_db": -27, "sfx_db": -15, "tail": 0.5, "end_card": 2.8,
  "end_lines": ["PLAY FREE", "snowplowrush.app"],
  "out": "/home/claude/promo/out/s001_split.mp4"
}
Clips play in order (looping if the story runs longer); the game's own sounds are rebuilt per clip by mixaudio.py.
Captions: 1-3 words at a time, the spoken word in yellow, so nobody can read ahead. Gameplay is scaled up 6x with
nearest-neighbour, so the pixel art stays sharp.
"""
import json, math, os, re, subprocess, sys
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
FONT = '/usr/share/fonts/opentype/inter/'
W, H, FPS, S = 1080, 1920, 30, 6
SR = 48000
YELLOW, WHITE, NAVY, NAVY2 = (255, 216, 74), (255, 255, 255), (11, 24, 56), (19, 48, 107)


def font(name, size):
    return ImageFont.truetype(FONT + name, size)


def rounded(size, r, fill):
    im = Image.new('RGBA', size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=fill)
    return im


def with_shadow(im, blur=16, off=(0, 10), alpha=110):
    pad = blur * 3
    base = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, alpha))
    sh.putalpha(im.split()[3].point(lambda a: a * alpha // 255))
    base.paste(sh, (pad + off[0], pad + off[1]), sh)
    base = base.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(im, (pad, pad))
    return base, pad


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def story_card(title, channel, byline, width=960):
    d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    tf = font('Inter-ExtraBold.otf', 52)
    lines = wrap(d0, title, tf, width - 64)
    h = 150 + len(lines) * 64 + 34
    card = rounded((width, h), 38, (255, 255, 255, 255))
    d = ImageDraw.Draw(card)
    icon = Image.open(os.path.join(REPO, 'apple-touch-icon.png')).convert('RGBA').resize((88, 88), Image.LANCZOS)
    m = Image.new('L', (88, 88), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 87, 87], fill=255)
    card.paste(icon, (32, 30), m)
    d.text((138, 32), channel, font=font('Inter-Bold.otf', 42), fill=(17, 17, 17))
    d.text((138, 82), byline, font=font('Inter-Medium.otf', 30), fill=(107, 114, 128))
    y = 146
    for ln in lines:
        d.text((32, y), ln, font=tf, fill=(17, 17, 17))
        y += 64
    return with_shadow(card)


def caption_chunks(words, offset):
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        txt = ' '.join(x['w'] for x in cur)
        end = re.search(r"[.?!,;:]$", w['w'])
        if end or len(cur) >= 3 or len(txt) >= 13:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        t0 = c[0]['t0'] + offset
        nxt = chunks[i + 1][0]['t0'] + offset if i + 1 < len(chunks) else c[-1]['t1'] + offset + 0.6
        t1 = min(nxt, c[-1]['t1'] + offset + 0.45)
        out.append({'words': c, 't0': t0, 't1': t1})
    return out


def show_word(w):
    w = w.upper()
    return re.sub(r"[.,;:\"“”]+$", '', re.sub(r"^[\"“]", '', w))


_cap_cache = {}


def caption_img(chunk, active, maxw=960):
    key = (id(chunk), active)
    if key in _cap_cache:
        return _cap_cache[key]
    words = [show_word(w['w']) for w in chunk['words']]
    size = 104
    while True:
        f = font('Inter-Black.otf', size)
        d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
        sp = d0.textlength(' ', font=f)
        ws = [d0.textlength(w, font=f) for w in words]
        tw = sum(ws) + sp * (len(words) - 1)
        if tw <= maxw or size <= 70:
            break
        size -= 6
    stroke = max(8, size // 9)
    im = Image.new('RGBA', (int(tw) + stroke * 2 + 40, size + stroke * 2 + 50), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(sh)
    x = stroke + 20
    for i, w in enumerate(words):
        ds.text((x, stroke + 18 + 8), w, font=f, fill=(0, 0, 0, 150), stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
        d.text((x, stroke + 18), w, font=f, fill=YELLOW if i == active else WHITE, stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        x += ws[i] + sp
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    sh.alpha_composite(im)
    _cap_cache[key] = sh
    return sh


def logo_from_og(width):
    og = Image.open(os.path.join(REPO, 'og.png')).convert('RGBA')
    lg = og.crop((40, 92, 596, 308))
    return lg.resize((width, int(lg.height * width / lg.width)), Image.LANCZOS)


def db(x):
    return 10 ** (x / 20)


def load_audio(path, ch=2):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, ch).astype(np.float64)


def main():
    cut = json.load(open(sys.argv[1]))
    story = json.load(open(os.path.join(REPO, cut['story']) if not os.path.isabs(cut['story']) else cut['story']))
    nar = json.load(open(os.path.join(cut['narration'], 'words.json')))
    layout = cut.get('layout', 'split')
    lead = cut.get('lead', 0.25)
    narr_end = lead + nar['dur']
    tail, endc = cut.get('tail', 0.5), cut.get('end_card', 2.8)
    total = narr_end + tail + endc
    N = int(math.ceil(total * FPS))
    out = cut['out']
    os.makedirs(os.path.dirname(out), exist_ok=True)
    work = out[:-4] + '_work'
    os.makedirs(work, exist_ok=True)

    # gameplay frames in order: (capture dir, frame number); one audio segment per stretch of a clip
    line_t0 = {}
    for w in nar['words']:
        line_t0.setdefault(w['line'], w['t0'])
    seq, segs, k = [], [], 0
    while len(seq) < N:
        c = cut['clips'][k % len(cut['clips'])]
        k += 1
        f0, f1 = c.get('from', 1), c.get('to')
        meta = json.load(open(os.path.join(c['cap'], 'meta.json')))
        f1 = min(f1 or meta['frames'], meta['frames'])
        pos = json.load(open(os.path.join(c['cap'], 'pos.json')))
        want = N - len(seq)
        if 'until_line' in c and c['until_line'] in line_t0 and k <= len(cut['clips']):
            want = max(1, min(want, int(round((lead + line_t0[c['until_line']]) * FPS)) - len(seq)))
        while want > 0:  # a clip shorter than its beat plays again from its first frame
            take = min(f1 - f0 + 1, want)
            seq += [(c['cap'], f, pos[f - 1] if f - 1 < len(pos) else [90, 160], len(segs)) for f in range(f0, f0 + take)]
            segs.append((c['cap'], f0, f0 + take - 1))
            want -= take
            if 'until_line' not in c:
                break

    # ---- audio: narration + game sounds (rebuilt per clip) + music bed
    sfx_parts = []
    for i, (cap, f0, f1) in enumerate(segs):
        p = os.path.join(work, f'sfx_{i}.wav')
        subprocess.run([sys.executable, '-I', os.path.join(HERE, 'mixaudio.py'), cap, p, str(f0), str(f1)], check=True, capture_output=True)
        a, _ = sf.read(p, dtype='float64')
        fl = int(0.03 * SR)
        a[:fl] *= np.linspace(0, 1, fl)[:, None]
        a[-fl:] *= np.linspace(1, 0, fl)[:, None]
        sfx_parts.append(a)
    sfx = np.concatenate(sfx_parts)
    n = int(total * SR)
    mix = np.zeros((n, 2))
    sfx = sfx[:n]
    g_sfx = np.full(len(sfx), db(cut.get('sfx_db', -15)))
    e0 = int((narr_end + tail) * SR)
    if e0 < len(sfx):
        g_sfx[e0:] *= np.linspace(1, 0.25, len(sfx) - e0)
    mix[:len(sfx)] += sfx * g_sfx[:, None]
    narr = load_audio(os.path.join(cut['narration'], 'narration.wav'))
    s = int(lead * SR)
    mix[s:s + len(narr)] += narr[:n - s]
    mus_path = cut.get('music', os.path.join(REPO, 'audio', 'music_lofi.mp3'))
    if mus_path:
        m = load_audio(mus_path)
        a, b = int(0.5 * SR), min(len(m), int(47.33714 * SR))
        loop = m[a:b]
        reps = int(math.ceil(n / len(loop))) + 1
        bed = np.concatenate([loop] * reps)[:n]
        gm = np.full(n, db(cut.get('music_db', -27)))
        gm[e0:] = np.linspace(db(cut.get('music_db', -27)), db(cut.get('music_db', -27) + 9), n - e0) if e0 < n else gm[e0:]
        fo = int(0.8 * SR)
        gm[-fo:] *= np.linspace(1, 0, fo)
        mix += bed * gm[:, None]
    sf.write(os.path.join(work, 'mix.wav'), mix.astype(np.float32), SR, subtype='FLOAT')

    # ---- pictures
    card, cpad = story_card(story['title'], cut.get('channel', 'Snow Stories'), cut.get('byline', 'a Snowplow Rush channel'))
    card_style = cut.get('card', 'story')
    head = None
    if card_style == 'headline':
        hf = font('Inter-Black.otf', 68)
        d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
        hl = wrap(d0, cut.get('headline', story['title']).upper(), hf, 960)
        head = Image.new('RGBA', (W, 520), (0, 0, 0, 0))
        hd = ImageDraw.Draw(head)
        for yy in range(520):  # soft shade behind the title so it reads over snow
            a = int(150 * max(0, min(1, (yy - 40) / 120)) * max(0, min(1, (500 - yy) / 160)))
            hd.line([(0, yy), (W, yy)], fill=(5, 12, 30, a))
        y = 260 - len(hl) * 41
        for ln in hl:
            hd.text((W // 2, y), ln, font=hf, fill=WHITE, anchor='ma', stroke_width=8, stroke_fill=(0, 0, 0))
            y += 82
    popf = font('Inter-ExtraBold.otf', 50)
    pop_imgs = []
    for pp in cut.get('pops', []):
        d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
        tw = int(d0.textlength(pp['text'].upper(), font=popf))
        im = rounded((tw + 130, 96), 26, (11, 24, 56, 225))
        di = ImageDraw.Draw(im)
        di.rounded_rectangle([22, 22, 74, 74], 10, fill=(64, 200, 96))
        di.line([(34, 49), (45, 61), (64, 35)], fill=WHITE, width=8)
        di.text((96, 48), pp['text'].upper(), font=popf, fill=WHITE, anchor='lm')
        t_on = lead + line_t0.get(pp['line'], 0)
        t_off = lead + line_t0[pp['until_line']] if pp.get('until_line') in line_t0 else narr_end
        pop_imgs.append((t_on, t_off, im))
    chunks = [c for c in caption_chunks(nar['words'], lead) if c['words'][0]['line'] > 0 or cut.get('card', 'story') != 'story']
    hook_end = lead + max(w['t1'] for w in nar['words'] if w['line'] == 0)
    wm = logo_from_og(250)
    wm_bg = rounded((wm.width + 24, wm.height + 16), 18, (11, 24, 56, 200))
    wm_bg.alpha_composite(wm, (12, 8))
    end_logo = logo_from_og(880)
    endf1, endf2 = font('Inter-Black.otf', 92), font('Inter-ExtraBold.otf', 64)
    end_lines = cut.get('end_lines', ['PLAY FREE', 'snowplowrush.app'])
    rng = np.random.default_rng(7)
    flakes = [(rng.uniform(0, W), rng.uniform(0, 960), rng.uniform(25, 80), int(rng.choice([6, 6, 6, 12])), rng.uniform(0, 6.28)) for _ in range(70)]
    topbg = Image.new('RGB', (W, 960))
    tb = ImageDraw.Draw(topbg)
    for y in range(960):
        q = y / 959
        tb.line([(0, y), (W, y)], fill=tuple(int(NAVY[i] + (NAVY2[i] - NAVY[i]) * q) for i in range(3)))
    # follow the machine smoothly in split layout (the crop is 160 game pixels tall)
    sm, last_seg, cy = [], None, None
    for (_, _, p, sg) in seq[:N]:
        if sg != last_seg or cy is None:
            cy = p[1]
            last_seg = sg
        cy += (p[1] - cy) * 0.08
        sm.append(cy)

    ff = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
          '-i', os.path.join(work, 'mix.wav'), '-map', '0:v', '-map', '1:a',
          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-tune', 'animation', '-pix_fmt', 'yuv420p',
          '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', '-movflags', '+faststart', out]
    preview = [int(float(x) * FPS) for x in sys.argv[sys.argv.index('--preview') + 1].split(',')] if '--preview' in sys.argv else None
    enc = None if preview else subprocess.Popen(ff, stdin=subprocess.PIPE)
    for fi in range(N):
        if preview and fi not in preview:
            continue
        t = fi / FPS
        cap, f, p, sg = seq[fi]
        key = (cap, f)
        g = Image.open(os.path.join(cap, f'f{f:05d}.png')).convert('RGB')
        frame = Image.new('RGB', (W, H), NAVY)
        if layout == 'full':
            frame.paste(g.resize((W, H), Image.NEAREST), (0, 0))
        else:
            gh = g.height
            y0 = int(round(min(max(sm[fi] - 80, 22), gh - 40 - 160)))  # play view only: below the top bar, above the 40 px button bar
            frame.paste(g.crop((0, y0, 180, y0 + 160)).resize((W, 960), Image.NEAREST), (0, 960))
            top = topbg.copy()
            dt = ImageDraw.Draw(top)
            for (x, y, v, sz, ph) in flakes:
                yy = (y + v * t) % 960
                xx = (x + 14 * math.sin(ph + t * 0.9)) % W
                c = 230 if sz == 6 else 255
                dt.rectangle([xx, yy, xx + sz - 1, yy + sz - 1], fill=(c, c, 255))
            frame.paste(top, (0, 0))
            ImageDraw.Draw(frame).rectangle([0, 954, W, 965], fill=NAVY)
        fr = frame.convert('RGBA')
        # story card: always on top in split; only during the hook in full
        endq = min(1, max(0, (t - narr_end - tail) / 0.35))
        if head is not None:
            if endq < 1:
                h3 = head if endq == 0 else Image.blend(Image.new('RGBA', head.size, (0, 0, 0, 0)), head, 1 - endq)
                fr.alpha_composite(h3, (0, 0))
        elif card_style == 'none':
            pass
        elif layout != 'full' and endq < 1:
            c3 = card if endq == 0 else Image.blend(Image.new('RGBA', card.size, (0, 0, 0, 0)), card, 1 - endq)
            fr.alpha_composite(c3, (60 - cpad, 150 - cpad))
        elif t < hook_end + 0.6:
            k2 = min(1, max(0, (t - hook_end - 0.35) / 0.25))
            yy = int(170 - k2 * 420)
            pop = min(1, t / 0.18)
            c2 = card if pop >= 1 else card.resize((int(card.width * (0.9 + 0.1 * pop)), int(card.height * (0.9 + 0.1 * pop))))
            fr.alpha_composite(c2, (W // 2 - c2.width // 2, yy - cpad))
        # watermark on the gameplay
        pops_up = any(a <= t < b for (a, b, _) in pop_imgs)
        if t < narr_end + tail and not (pops_up and layout == 'full'):
            fr.alpha_composite(wm_bg, (22, 986 if layout != 'full' else 1330))
        # checklist pops (stacked, slide in from the left)
        slot = 0
        for (t_on, t_off, im) in pop_imgs:
            if t_on <= t < t_off and endq == 0:
                sl = min(1, (t - t_on) / 0.15)
                fr.alpha_composite(im, (int(-im.width + (60 + im.width) * sl), 1140 + slot * 112))
                slot += 1
        # captions
        cy_cap = 720 if layout != 'full' else 690
        for ch in chunks:
            if ch['t0'] <= t < ch['t1']:
                act = 0
                for i, w in enumerate(ch['words']):
                    if t >= w['t0'] + lead:
                        act = i
                im = caption_img(ch, act)
                age = t - ch['t0']
                if age < 0.07:
                    sc = 0.86 + 0.14 * age / 0.07
                    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))))
                fr.alpha_composite(im, (W // 2 - im.width // 2, cy_cap - im.height // 2))
                break
        # end card
        if t >= narr_end + tail:
            q = min(1, (t - narr_end - tail) / 0.35)
            ov = Image.new('RGBA', (W, H), (11, 24, 56, int(205 * q)))
            fr.alpha_composite(ov)
            if q > 0.3:
                pop = min(1, (q - 0.3) / 0.5)
                lg = end_logo if pop >= 1 else end_logo.resize((int(end_logo.width * (0.85 + 0.15 * pop)), int(end_logo.height * (0.85 + 0.15 * pop))))
                fr.alpha_composite(lg, (W // 2 - lg.width // 2, 800 - lg.height // 2))
                de = ImageDraw.Draw(fr)
                de.text((W // 2, 1075), end_lines[0], font=endf1, fill=WHITE, anchor='mm', stroke_width=8, stroke_fill=(0, 0, 0))
                if len(end_lines) > 1:
                    de.text((W // 2, 1185), end_lines[1], font=endf2, fill=YELLOW, anchor='mm', stroke_width=6, stroke_fill=(0, 0, 0))
        if preview:
            fr.convert('RGB').save(os.path.join(work, f'preview_{t:05.1f}.png'))
            continue
        enc.stdin.write(fr.convert('RGB').tobytes())
    if preview:
        print('previews in', work)
        return
    enc.stdin.close()
    enc.wait()
    print(f"{out}: {total:.1f}s, {N} frames, layout {layout}, {len(segs)} clip(s), {len(chunks)} captions")


if __name__ == '__main__':
    main()
