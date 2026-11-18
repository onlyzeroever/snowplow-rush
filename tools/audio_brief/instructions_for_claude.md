# Snowplow Rush sounds: instructions for the Claude making them

You're making the sound effects and voice lines for **Snowplow Rush**, a cozy pixel-art snowplow game. It has to sound like one top-tier set, with nothing jarring between sounds. There are two spec files. Each lists every file with its exact name, prompt, priority and length, plus the shared palette and style that every item follows.

- **Part 1: `snowplow-rush-audio-spec.json`.** 22 new effects and 6 voice lines.
- **Part 2: `snowplow-rush-audio-spec-part2.json`.** 41 remakes of the effects the game already has.

Only items with `make: true` are generated: 32 effects and 6 voice lines, one take each. The rest (`make: false`) are built in editing from those. **Hard limit: 1,000,000 Fish credits for everything; use as few as possible.**

The music is made separately in Suno, so leave it out.

## Before you generate anything

Tell the owner of the Fish Audio account what each batch will cost in credits and wait for their OK. Use a paid Fish Audio plan: paid plans include commercial rights, and this is going into a commercial game.

## How to make them

1. **Follow `order` in each spec.** Part 1 stops after its 8 priority-A effects. Send those, then wait until Alex has heard them in the game and says they fit.
2. **Lengths.** Fish takes whole seconds, so ask for each effect's `request_seconds`. The prompts already say the sound happens right at the start and the rest is silence. Deliver the files untrimmed; they're trimmed to `trim_to` when they go into the game. Effects with `loop: true` must loop seamlessly.
3. **Takes.** One take per sound, in the batches given by `batch`. Make a second take only for a sound that comes back wrong, and only after the owner OKs it.
4. **Voice.** Use Fish Audio text to speech with one voice for all six lines, as described in `voice`. Each line is exactly the words given.
5. **Never improvise.** Don't change a prompt, a name or a length. If something can't be made as written, stop and tell the owner.

## Delivering

- **Format: WAV, 44.1 kHz, 16-bit.**
- **Names:** `<name>_1.wav` (a redo is `<name>_2.wav`).
- **One zip per part:** `snowplow-rush-audio.zip` with `sfx/`, `voice/` and `manifest.csv`, then `snowplow-rush-audio-part2.zip` with `sfx/` and `manifest.csv`.
- **manifest.csv:** one row per file, with these columns: `file,type,take,seconds_requested,prompt_used,notes`.
- **Downloading:** to download the takes, convert them and zip them, your workspace needs network access to `*.fish.audio`. Ask the owner to allow it in their Claude settings before you start.
- **Hand-off:** give the zips to the account owner to send to Alex.
