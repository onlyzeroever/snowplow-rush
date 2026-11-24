# Promo video tools

Free, repeatable short-form videos made from the real game: the test bot plays a job, every frame and every sound is
recorded, an original story is read by an open-source voice, and the video is put together with captions.
Nothing here costs credits. Plan, formats and rules: the project doc `claude/promo-playbook.md`.

Not served by the website (`.vercelignore`). Outputs and voice models stay in the workspace, never in git.

## One-time setup (per workspace)

```bash
pip install --break-system-packages kokoro-onnx soundfile scipy
mkdir -p /home/claude/promo/models && cd /home/claude/promo/models
curl -sL -o kokoro-v1.0.int8.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
curl -sL -o voices-v1.0.bin      https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
bash tools/promo/serve.sh        # the game builds on :8765 (needs Playwright + Chrome, as the audits do)
```

Kokoro is Apache-2.0 (free for commercial use). Voices: `af_heart` (best US female), `af_bella`, `am_michael`,
`bf_emma` (UK female), `bm_george` (UK male).

## Make a video (3 steps)

```bash
# 1. record gameplay: ~5 s per 40 s of footage. `list` shows job and machine ids.
node tools/promo/capture.js job=driveway tool=truck lv=4 seed=1 from=1 secs=40
node tools/promo/capture.js job=culdesac tool=super lv=4 seed=2 from=1 secs=40

# 2. narration with word timings (~75 s on the CPU for a 45 s story)
python3 -I tools/promo/tts.py tools/promo/stories/s001_stolen_snow.json /home/claude/promo/work/s001

# 3. the video (1080x1920, 30 fps, -14 LUFS): ~30 s
python3 -I tools/promo/compose.py /home/claude/promo/cuts/s001_split.json            # --preview 1,8,30 for stills first
```

A cut file lists the story, the narration folder, the layout (`split` = story on top / gameplay below, `full` =
gameplay full screen), the clips (`cap`, `from`, `to` frame numbers) and the levels (`music_db`, `sfx_db`).
See `compose.py` for every field. Check footage before using it: the bot sometimes waits behind a pedestrian, and
a job that is nearly cleared is boring to watch (use the first 20-30 s of each job, then cut to the next).

## Files

- `capture.js`: plays and records one job (frames `fNNNNN.png` at 180 x H, `sounds.json`, `pos.json`, `meta.json`).
  Uses the bot in `tools/audit/botplay.js` (`window.__onStep` hook). `coins=` sets a believable wallet for the HUD.
- `mixaudio.py`: rebuilds the game's sound effects for a stretch of frames (one-shots, engine/scrape loops, blips).
- `tts.py`: Kokoro narration + word times.
- `compose.py`: story card, 1-3 word captions (spoken word in yellow), 6x gameplay, watermark, end card, audio mix
  (voice, game sounds, music bed), loudness -14 LUFS.
- `stories/`: original story scripts (fiction written for the game; never copied Reddit posts).
- `serve.sh`: serves the website and app builds for capture.
