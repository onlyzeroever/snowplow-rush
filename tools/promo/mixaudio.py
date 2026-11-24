"""Rebuilds the game's sound effects for a recorded clip, in sync with its frames.

    python3 -I tools/promo/mixaudio.py <capture dir> <out.wav> [first_frame=1] [last_frame=end] [--audio <game audio dir>]

Uses the sound log written by tools/promo/capture.js: one-shots (playBuf: name, volume, pitch, pan), the looping
engine / scrape / jet sounds (loopSet every frame: volume and pitch, smoothed the way Web Audio smooths them),
synth blips (tone) and stopLoops. Music is left out: the video tool lays its own music bed.
Output: 48 kHz stereo float WAV, frame 1 of the range at 0 s.
"""
import json, os, subprocess, sys
import numpy as np
import soundfile as sf
from scipy.signal import lfilter

SR = 48000
_cache = {}


def load(name, audio_dir):
    if name in _cache:
        return _cache[name]
    p = os.path.join(audio_dir, name + '.mp3')
    if not os.path.exists(p):
        _cache[name] = None
        return None
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
    _cache[name] = x
    return x


def smooth(target, tau):
    a = 1.0 - np.exp(-1.0 / (tau * SR))
    y = lfilter([a], [1, -(1 - a)], target)
    return y


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    audio_dir = '/home/claude/snowplow-rush/audio'
    if '--audio' in sys.argv:
        audio_dir = sys.argv[sys.argv.index('--audio') + 1]
        args = [a for a in args if a != audio_dir]
    cap, out = args[0], args[1]
    meta = json.load(open(os.path.join(cap, 'meta.json')))
    snd = json.load(open(os.path.join(cap, 'sounds.json')))
    fps = meta['fps']
    f0 = int(args[2]) if len(args) > 2 else 1
    f1 = int(args[3]) if len(args) > 3 else meta['frames']
    n = int((f1 - f0 + 1) / fps * SR)
    mix = np.zeros((n, 2), dtype=np.float64)
    vol = meta['SFX_VOL']
    loops_cfg = meta['SFX_LOOPS']
    master = 0.9
    # events are stamped with the 0-based frame index of the clip; keep a little history before f0 for loop state
    t_of = lambda fr: (fr - (f0 - 1)) / fps
    # one-shots and tones
    for e in snd:
        kind = e[1]
        t = t_of(e[0])
        if kind == 'b':
            if t < 0 or t >= n / SR:
                continue
            _, _, name, v, rate, pan = e
            x = load(name, audio_dir)
            if x is None:
                continue
            if rate and abs(rate - 1) > 1e-3:
                L = int(len(x) / rate)
                idx = np.arange(L) * rate
                x = np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in (0, 1)], axis=1)
            g = (v if v is not None else 1) * vol.get(name, 0.6) * master
            th = (max(-1, min(1, pan or 0)) + 1) * np.pi / 4
            gl, gr = np.cos(th) * np.sqrt(2), np.sin(th) * np.sqrt(2)
            s = int(t * SR)
            m = min(len(x), n - s)
            mix[s:s + m, 0] += x[:m, 0] * g * gl
            mix[s:s + m, 1] += x[:m, 1] * g * gr
        elif kind == 't':
            _, _, f, dur, typ, v, slide, delay = e
            t2 = t + (delay or 0)
            if t2 < 0 or t2 >= n / SR:
                continue
            L = int((dur + 0.02) * SR)
            tt = np.arange(L) / SR
            if slide:
                fr = f * (slide / f) ** np.clip(tt / dur, 0, 1)
            else:
                fr = np.full(L, float(f))
            ph = 2 * np.pi * np.cumsum(fr) / SR
            if typ == 'sine':
                w = np.sin(ph)
            elif typ == 'triangle':
                w = 2 / np.pi * np.arcsin(np.sin(ph))
            elif typ == 'sawtooth':
                w = 2 * ((ph / (2 * np.pi)) % 1) - 1
            else:
                w = np.sign(np.sin(ph))
            env = (v or 0.1) * (0.0001 / (v or 0.1)) ** np.clip(tt / dur, 0, 1)
            y = w * env * master * 0.6
            s = int(t2 * SR)
            m = min(L, n - s)
            mix[s:s + m, 0] += y[:m]
            mix[s:s + m, 1] += y[:m]
    # loops: per-frame targets, held between calls, smoothed like setTargetAtTime
    names = sorted({e[2] for e in snd if e[1] == 'l'})
    stops = sorted(t_of(e[0]) for e in snd if e[1] == 's')
    for name in names:
        x = load(name, audio_dir)
        if x is None:
            continue
        ls, le = loops_cfg.get(name, [0, len(x) / SR])
        ev = [(t_of(e[0]), e[3], e[4]) for e in snd if e[1] == 'l' and e[2] == name]
        gt = np.zeros(n)
        rt = np.ones(n)
        g_cur, r_cur, k = 0.0, 1.0, 0
        # state before the clip starts
        while k < len(ev) and ev[k][0] < 0:
            g_cur = ev[k][1]
            r_cur = ev[k][2] or r_cur
            k += 1
        last = 0
        for (t, g, r) in ev[k:] + [(n / SR, None, None)]:
            s = min(n, max(0, int(t * SR)))
            gt[last:s] = g_cur
            rt[last:s] = r_cur
            last = s
            if g is None:
                break
            g_cur = g
            if r:
                r_cur = r
        for st in stops:
            s = int(st * SR)
            if 0 <= s < n:
                gt[s:] = 0
        g = smooth(gt, 0.06)
        r = smooth(rt, 0.1)
        L0, L1 = int(ls * SR), int(le * SR)
        span = max(1, L1 - L0)
        pos = L0 + (np.cumsum(r) + 0.37 * span) % span
        for c in (0, 1):
            mix[:, c] += np.interp(pos, np.arange(len(x)), x[:, c]) * g * master
    peak = float(np.max(np.abs(mix))) if n else 0
    sf.write(out, mix.astype(np.float32), SR, subtype='FLOAT')
    print(f"game audio {n / SR:.1f}s ({len(snd)} sound calls, loops {names}), peak {peak:.2f} -> {out}")


if __name__ == '__main__':
    main()
