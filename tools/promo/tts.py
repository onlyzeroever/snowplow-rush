"""Narration for promo videos with Kokoro (open model, Apache-2.0, runs on the CPU, free to use commercially).

    python3 -I tools/promo/tts.py <story.json> <outdir> [--models /home/claude/promo/models]

story.json: {"voice": "af_heart", "speed": 1.1, "lines": ["first line is the hook", "...", ...],
             "gap": 0.14, "hook_gap": 0.35}
Writes <outdir>/narration.wav (24 kHz mono) and <outdir>/words.json: one entry per word with its start and end
(seconds) and the line it belongs to. Word times inside a line are estimated from the pauses Kokoro leaves
plus the length of each word: close enough for word-by-word captions.

Model files (once): https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
  kokoro-v1.0.int8.onnx and voices-v1.0.bin into the models folder.
"""
import json, os, re, sys
import numpy as np
import soundfile as sf


def speech_spans(x, sr, thr=0.012, min_gap=0.075):
    """(start, end) sample ranges of speech, split at pauses longer than min_gap."""
    hop = int(sr * 0.01)
    n = len(x) // hop
    env = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
    on = env > thr
    spans, i = [], 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            spans.append([i * hop, j * hop])
            i = j
        else:
            i += 1
    merged = []
    for s in spans:
        if merged and (s[0] - merged[-1][1]) < min_gap * sr:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    return merged


def weight(w):
    core = re.sub(r"[^A-Za-z0-9']", '', w)
    return 1.2 + len(core) * 0.55


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    models = '/home/claude/promo/models'
    if '--models' in sys.argv:
        models = sys.argv[sys.argv.index('--models') + 1]
        args = [a for a in args if a != models]
    story = json.load(open(args[0]))
    out = args[1]
    os.makedirs(out, exist_ok=True)
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(models, 'kokoro-v1.0.int8.onnx'), os.path.join(models, 'voices-v1.0.bin'))
    voice, speed = story.get('voice', 'af_heart'), float(story.get('speed', 1.1))
    gap, hook_gap = float(story.get('gap', 0.14)), float(story.get('hook_gap', 0.35))
    audio, words, t = [], [], 0.0
    sr = 24000
    for li, line in enumerate(story['lines']):
        x, sr = k.create(line, voice=voice, speed=speed, lang=story.get('lang', 'en-us'))
        x = np.asarray(x, dtype=np.float32)
        spans = speech_spans(x, sr)
        if not spans:
            continue
        a, b = max(0, spans[0][0] - int(0.02 * sr)), min(len(x), spans[-1][1] + int(0.04 * sr))
        x = x[a:b]
        spans = [[s0 - a, s1 - a] for s0, s1 in spans]
        toks = line.split()
        # clauses end at , . ? ! ; : and dashes: match them to the pauses when the counts agree
        groups, cur = [], []
        for w in toks:
            cur.append(w)
            if re.search(r"[,.?!;:—-]$", w):
                groups.append(cur); cur = []
        if cur:
            groups.append(cur)
        if len(groups) == len(spans):
            parts = list(zip(groups, spans))
        else:
            parts = [(toks, [spans[0][0], spans[-1][1]])]
        for g, (s0, s1) in parts:
            tot = sum(weight(w) for w in g)
            pos = s0
            for w in g:
                d = (s1 - s0) * weight(w) / tot
                words.append({'w': w, 't0': round(t + pos / sr, 3), 't1': round(t + (pos + d) / sr, 3), 'line': li})
                pos += d
        audio.append(x)
        t += len(x) / sr
        pause = float(story.get('pauses', {}).get(str(li), hook_gap if li == 0 else gap))  # pause after this line
        audio.append(np.zeros(int(pause * sr), dtype=np.float32))
        t += pause
    y = np.concatenate(audio)
    sf.write(os.path.join(out, 'narration.wav'), y, sr)
    json.dump({'voice': voice, 'speed': speed, 'sr': sr, 'dur': round(len(y) / sr, 3), 'lines': story['lines'], 'words': words},
              open(os.path.join(out, 'words.json'), 'w'), indent=0)
    print(f"narration {len(y) / sr:.1f}s, {len(words)} words, voice {voice} x{speed} -> {out}")


if __name__ == '__main__':
    main()
