# Sim v10 / ladder3 (Nov 17, 2026): real combos, Mk II, Front Loader + Icebreaker

Combo per machine from live job_end data (43 runs, 5 players): early machines x2.2-2.5, Plow Truck x1.56,
Super Plow x1.8; later machines assumed x1.7. Mk II bought as soon as speed and width are maxed. 6 seeds each, rides off.

| Ladder | Winter 1 | North runs (replays) | Machines bought at run |
|---|---|---|---|
| Today (8 machines) | 331 runs, 8.3 h | 88 (17) | super 58, snowcat 118, rotary 161, Mk II 240; Rotary->end 170 runs |
| + Front Loader 2.5M + Icebreaker 180M | 290 runs, 7.2 h | 47 (9) | super 58, loader 88, snowcat 118, rotary 161, Mk II 240, icebreaker 272 |
| same, combos x0.85 | 338 runs | 53 (13) | loader 99, snowcat 132, rotary 184, icebreaker 321 |
| same, combos x1.15 | 258 runs | 41 (7) | loader 78, snowcat 105, rotary 144, icebreaker 239 |

Chosen: FRONT LOADER 48 wide, speed 84, x7.5 coins, 2.5M (caps speed 1.062, width 1.10; upgrades priced off the Snowcat).
Super Plow caps now point at the Loader (speed 1.101, width 1.14, upBase from 2.5M). Snowcat and Rotary caps and upgrade
prices unchanged (Rotary keeps 1.15/1.25 and upBase from 72M). ICEBREAKER 62 wide, speed 132, x18 coins, 180M.
Day one: Super->Loader +9% clearing, +15% coins/cell; Loader->Snowcat -14% / +27%; Snowcat->Rotary -10% / +42% (as today);
Rotary->Icebreaker +14% / +33%.

Findings:
- Real combos make every machine land about one area earlier than designed. Raising Snowcat/Rotary prices to pull them back
  lengthens the pre-Rotary gaps (41-86 runs) because areas slow down too, so existing prices stay.
- The long stretch is Rotary -> end (170 runs), not Super -> Snowcat (60). Wild Rides drop in exactly that stretch, Mk II
  lands at ~240, the Icebreaker at ~272. A +25% Icebreaker finished the North 10 runs after purchase, so it's +14%.
- With real combos and Mk II the North wall is mostly gone (17 replays in 88 runs, 9 in 47 with the Icebreaker).
- The old index-based ride missions break with an extra base machine (rides after the Icebreaker, weaker than it):
  Wild Rides must be a separate collection that scales with the best machine (task 77) before the Icebreaker ships.

## Update Nov 18: Super Plow kept as it is, wider Loader (shipped in p126)
The first version pointed the Super Plow's upgrade caps at the Loader, which made a maxed Super Plow ~15% weaker for
players who already had it. Instead: Super Plow caps 1.15/1.30 and upgrade prices exactly as today; FRONT LOADER 52 wide,
speed 80, x7.5, caps speed 1.08 / width 1.06, 2.5M, same body size as the Super Plow (hw 12, so it reaches the same snow).
ladder3_keepsuper_wide.py: winter 1 299 runs (~7.5 h), loader at run 98 with the Super Plow at about level 5: clearing
+0%, coins/cell +15%; Loader -> Snowcat -15% / +27%; North 47 runs, 9 replays. Combos x0.85: 344 runs.
