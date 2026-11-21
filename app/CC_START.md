# Start here: building the Snowplow Rush apps

For Claude Code on Alex's Mac. Read this, then `APP_HANDOFF.md` (the full spec). Written Nov 21, 2026 by the
cloud session that builds the game.

## What to paste into Claude Code to begin

> Read app/CC_START.md and app/APP_HANDOFF.md in this repo. Do Phase 1, then Phase 2. Stop and ask me before
> anything that costs money, before creating anything in App Store Connect or Play Console, and before
> anything that needs my passwords or keys (I type those in myself). Keep your decisions in app/NOTES.md.

## The game you wrap

- **`app/game/index.html`** is the app build of the game: the live game plus the app-only patches (store and ads
  bridge, save mirror and reminders, launch prices, lighter session recording, event schedule from the website, store prices in the pixel font).
  The cloud session rebuilds and commits it; never edit it on the Mac. Ask for a patch instead.
- `copy-web.sh` runs `python3 tools/release.py app/game/index.html www/index.html` (test hooks off), then copies
  `ph/`, `audio/`, `events.json`, the icons and `og.png` from the repo root into `www/`.
- The game talks to the phone only through `window.SRNative` (APP_HANDOFF.md section 5). Everything native goes
  behind that contract.

## Phase 1: the shell (no store accounts needed)

1. Mac: the current Xcode with an iOS simulator, Android Studio with an SDK and an emulator, Node LTS. An iPhone
   and an Android phone for device tests. A free Apple ID in Xcode is enough to run on a phone for now.
2. Capacitor 8 project in `app/` (section 4 of the hand-off): app id `app.snowplowrush`, name "Snowplow Rush",
   portrait only, full screen, status bar hidden, dark blue splash `#13306b`.
3. `copy-web.sh` and a `native-bridge.js` that loads before the game's script and defines `window.SRNative` with
   `platform`, `storeSave`, `window.SRNativeSave`, `network`, `recordOK`, `askReminders`, `scheduleReminders`;
   `buy`, `owned`, `restore`, `prices` and `showAd` as stubs that resolve `{ok:false, reason:'error'}` for now.

Done when: the game boots offline on an iPhone simulator, an Android emulator and both phones; a weekend event
listed on https://snowplowrush.app/events.json shows in the app; quitting and reopening keeps the save; a
reinstall brings the save back (iCloud key-value store on iOS); a reminder fires after the nudge card's "yes".

## Phase 2: purchases and ads against test stores (still no accounts)

1. RevenueCat Capacitor SDK wired to `buy`, `owned`, `restore`, `prices` (section 5). `prices()` gives
   `{productId: {price, amount, currency}}` from `priceString`, `price` and `currencyCode`.
2. An Xcode StoreKit configuration file with every product in section 6 (ids, types, prices), so purchases,
   cancels, failures and restores work in the simulator without App Store Connect.
3. AppLovin MAX rewarded ads behind `showAd` in test mode (section 7), including "no fill".

Done when: every price button in the shop shows a store price, a purchase grants its item only after the store
says yes, a cancelled purchase grants nothing, Restore Purchases brings back Premium, the Starter Pack outfit and
any Wild Rides, and an ad that fails hands the reward button back.

## Phase 3: real accounts (when Alex says they exist)

The apps are published by **Kiln Fire Games Ltd** (Alex's new company); developer name **Kiln Fire Games**
(confirm the spelling with Alex before the first App Store Connect app record: Apple sets it once).
Products in both stores and RevenueCat (section 6), MAX + AdMob units, consent flow and App Tracking Transparency
(section 7), `/app-ads.txt` on the developer website, Apple Small Business Program (section 2).

## Phase 4: test builds and submission

TestFlight for Alex and Lloyd, Google Play internal testing, then the checklist in section 10.

## Ground rules

- Never spend money or start a paid plan without asking Alex. Never put keys, passwords or tokens in chat or the
  repo. Prices shown must come from the stores. The privacy wording must never say "no ads".
- Game changes only come from the cloud session, as patches (the cloud session runs the game's test suite).
- Ask Alex about: anything that costs money, store listings and screenshots, submitting for review. Decide the
  rest yourself (plugins, project layout, build settings) and note it in `app/NOTES.md`.
