# Snowplow Rush sounds: instructions for the Claude making them

You're making the whole soundtrack for **Snowplow Rush**, a cozy pixel-art snowplow game. It has to sound like one top-tier set, with nothing jarring between sounds. There are two spec files. Each lists every file with its exact name, length, priority and prompt, plus the shared palette and style that every item follows.

- **Part 1: `snowplow-rush-audio-spec.json`.** 22 new effects, 5 music tracks and 6 voice lines. That's 94 generations.
- **Part 2: `snowplow-rush-audio-spec-part2.json`.** 41 remakes of the effects the game already has. That's 123 generations.

## Before you generate anything

Tell the owner of the Fish Audio account what part 1 will cost in credits (94 generations) and wait for their OK. Do the same before part 2 (123 generations). Use a paid Fish Audio plan: paid plans include commercial rights, and this is going into a commercial game.

## How to make them

1. **Follow `order` in each spec.** Part 1 stops after its 8 priority-A effects. Send those to the owner so Alex can hear them in the game, and continue only once he says they fit. This is how the set stays consistent.
2. **Effects:** generate each item's prompt as written, at about its `seconds` length. `loop: true` items must loop seamlessly. Make the number of takes in `takes`.
3. **Music:** make `music_job` first. Make the other four with the same palette, giving `music_job` as the reference track wherever the tool takes one. Every track is a seamless loop with no vocals.
4. **Voice:** use one voice for all six lines, as described in `voice`. Each line is exactly the words given.
5. **Never improvise.** Don't change a prompt, a name or a length. If the tool can't make something as written, stop and tell the owner.

## Delivering

- **Format: WAV, 44.1 kHz, 16-bit.** WAV is lossless. MP3 adds silence at the start and end, which breaks seamless loops. The game's final files are made from these.
- **Every take, numbered:** `<name>_1.wav`, `<name>_2.wav`, `<name>_3.wav` (music has 2 takes). Don't choose; Alex chooses by listening in the game.
- **One zip per part:**

```
snowplow-rush-audio.zip            snowplow-rush-audio-part2.zip
  manifest.csv                       manifest.csv
  sfx/    sweep_1.wav ...            sfx/   click_1.wav ...
  music/  music_job_1.wav ...
  voice/  vo_sweep_1.wav ...
```

- **manifest.csv:** one row per file, with these columns: `file,type,take,seconds_actual,prompt_used,notes`.
- **Hand-off:** give the zips to the account owner to send to Alex.
