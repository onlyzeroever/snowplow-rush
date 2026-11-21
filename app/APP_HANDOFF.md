# Snowplow Rush: app hand-off (iOS and Android)

For Claude Code on Alex's Mac. Written Nov 21, 2026 by the cloud session that builds the game.
Goal: ship the web game at snowplowrush.app as a free iOS and Android app with real purchases,
rewarded ads, a silent cloud save and a few local reminders. No accounts, no server.

## 1. What exists

- **The game is one file.** `index.html` (about 1 MB, everything inlined) plus `ph/` (PostHog's recorder
  script), `audio/`, `events.json`, icons and `og.png`. It runs in any browser at 180x320 logical pixels,
  scaled up with `image-rendering: pixelated`.
- **Game changes come from the cloud session**, as numbered patches (`tools/patches/`) built into
  `index.html`. Do not edit game code by hand on the Mac; ask for a patch instead, so the two never drift.
  Everything native lives in `app/` (this folder).
- **Branches.** `main` is live (Vercel deploys it to snowplowrush.app), `next` is staging, `lab` is the
  prototype site lab.snowplowrush.app. **The app wraps `app/game/index.html`**: the live game plus the
  app-only patches (p163, p165, p170, p171, p172, p173, p174, p175, p176, p179, p181, p182), rebuilt and committed by the cloud session. Start with
  `app/CC_START.md`.
- **Rules from Alex that apply here:** never spend money or credits without asking; never put keys,
  passwords or tokens in chat or in the repo (Alex types them into the tools himself); prices shown must be
  the real store prices; the privacy wording must never say "no ads"; not Christmas-themed.

## 2. Accounts and ids (Alex)

| What | Value | Notes |
| --- | --- | --- |
| Legal seller (both stores) | Kiln Fire Games Ltd (new company Alex is setting up for the apps; his UGC Program Ltd stays separate) | Organisation accounts in the new company's name, with its own D-U-N-S number and business bank account. Its company number and registered office go in the privacy page and the website footer (UK trading disclosures). The new company must own the game: a short IP assignment from whoever owns it now. |
| Developer name shown under the app | Kiln Fire Games | Apple sets it once, when the first app record is created, and only Apple support can change it later. Confirm the exact spelling with Alex before creating the record. Google's can be changed any time. |
| Apple Developer Program | $99 a year | App Store Connect app record "Snowplow Rush" |
| Apple Small Business Program | 15% instead of 30% | Enrol as soon as the account exists: accept the Paid Apps agreement (with bank and tax), then https://developer.apple.com/app-store/small-business-program/enroll/ . The rate starts 15 days after the end of the Apple fiscal month in which it is approved, so do it weeks before launch. |
| Google Play Console | $25 once | App record "Snowplow Rush". UK/EU/US since Jun 30, 2026: 10% service fee on the first $1M plus a 5% billing fee. |
| Contact addresses | hello@, support@, privacy@kilnfiregames.com | Forwarded to Alex (ImprovMX, free plan: one domain). Use support@ in the store listings, privacy@ in the privacy policy, hello@ for the Apple and Google accounts. |
| Developer website | kilnfiregames.com | A real studio site (Apple rejects sites with minimal content or a parking page): the cloud session builds it once the domain exists. Serves `/app-ads.txt`. | Must serve `/app-ads.txt` with the AppLovin and AdMob lines before ads are approved; the store listing's developer website must be this domain. |
| If the apps ever change company | app transfer | Both stores move apps between developer accounts and keep ratings, reviews and users; keep the bundle id; RevenueCat keeps its app config. On Google Play an app with in-app products is unpublished until it is republished in the new account. |
| Bundle id / package name | `app.snowplowrush` | Same on both stores (reversed domain) |
| RevenueCat | free tier | One project, iOS + Android apps, entitlement `premium` |
| AppLovin MAX + AdMob | free | Rewarded ad unit per platform; AdMob as a network inside MAX |
| Age rating | 4+ (Apple), Everyone (Google) | Not in the Kids category: ads and purchases |

## 3. Game patches this needs (built and tested in the cloud, held from the live site)

| Patch | What it gives the app | Status |
| --- | --- | --- |
| p162 | Analytics that keep and retry unsent events (needed on flaky phone networks) | Live (Nov 21) |
| p163 | `IAP`: every price and ad button goes through `window.SRNative`; Restore Purchases in Settings | Lab |
| p165 | Save mirror to the phone, reminder plan, nudge card after the first three-star job | Lab |
| p170 | Launch prices, five gem packs, first gem purchase doubled, honest labels (worked out from the prices on show, so they hold in every store currency) | Lab, app build |
| p171 | Lighter session recording in the apps (section 8) | Lab |
| p172 | Event schedule fetched from the website in the apps | App build |
| p173 | Shop v2: free gift on top, one hero offer (Starter Pack with a real 48-hour countdown, else Premium), one colour per way of paying (green money, purple gems, blue free), "need more gems" jump to the right pack, one layout grid, shop events | Lab, app build |
| p175 | "YOU GOT" card after every purchase; the NEW WILD RIDE reveal for rides bought in the shop | Lab, app build |
| p176 | Real-money values next to gem prices in the garage (outfits, skins, trails) | Lab, app build |
| p179 | Tall phones: a snowy night sky behind the 9:16 game instead of plain bands (for full-screen apps and store screenshots) | Lab, app build |
| p174 | Store prices in the pixel font: £ € ¥ ₩ ₹ ₺ ₪ ₱ are drawn, other currencies are rebuilt from amount + currency (`SAR 18.99`); the shop's TEST MODE line is web only | App build |
| p180 | Title screen without the small print; the anonymous play-data note shows at the top of the map after job 1 (never over a job) | Live (Nov 22) |
| p181 | Snow Bank: a gem jar on the map from the 10th job (+4 gems a job, +1 a star, up to 400); opens for `snow_bank` from 220 | App build |
| p182 | Event Pass for the weekend event on now: flakes x2 (the ones already earned too) and that event's paint for every machine, kept; `event_pass` or 250 gems | App build |
| p161 | Automatic render scale on slow phones | Live |

When Alex OKs them, the cloud session moves them to `main`. The release build (`tools/release.py`, see 9)
then strips the test hooks.

## 4. Project setup

Capacitor 8 (current major). One project in `app/`, web assets copied in by a script, never edited there.

```
app/
  package.json            capacitor 8, plugins below
  capacitor.config.ts     appId app.snowplowrush, appName "Snowplow Rush", webDir "www"
  scripts/copy-web.sh     runs tools/release.py on app/game/index.html into www/index.html, copies ph/, audio/,
                          events.json, icons and og.png from the repo root into www/
  native-bridge.js        defines window.SRNative (section 5), loaded before the game
  ios/  android/          generated by `npx cap add ios|android`
```

- `npm i @capacitor/core @capacitor/cli @capacitor/ios @capacitor/android @capacitor/preferences
  @capacitor/local-notifications @capacitor/app @capacitor/status-bar @capacitor/splash-screen
  @revenuecat/purchases-capacitor` (RevenueCat 12.0.3 or later for Capacitor 8).
- Ads: AppLovin's official plugin is for Cordova (`cordova-plugin-applovin-max`); Capacitor runs Cordova
  plugins. If it does not build with Capacitor 8 and Swift Package Manager, write a small local Capacitor
  plugin around the MAX SDK that does only rewarded ads (load, show, a promise that says rewarded or not).
- Portrait only, full screen, status bar hidden, no zoom (`viewport` already set in the page), dark blue
  splash (`#13306b`) with the logo. App icon from the logo at 1024x1024, no transparency on iOS.
- Screen shapes (Nov 22). The web view fills the whole window on every device; the game fits itself to any
  shape and re-fits on every resize, so do no scaling or letterboxing natively. Build with the iOS 27.1 SDK
  (Xcode 27.1) or later: on iPhone Duo, apps built with older SDKs open as a smaller window in the middle of
  the inner display. Unfold and fold during a job in Xcode 27.1's iPhone Duo simulator: the run must carry on
  without a restart. Today the 9:16 game sits between a snowy sky on tall phones and on the Duo's open screen
  (p179); a full-screen layout for tall phones is waiting for Alex's OK and will come as a patch.
- Load the game from the bundled `www/` (works offline). In the app build the game fetches the weekend-event
  schedule from `https://snowplowrush.app/events.json` (p172; the site allows it with a CORS header), so events
  can be scheduled without an app update.
- `native-bridge.js` must run before the game's script. Add it as the first `<script>` in `www/index.html`
  from `copy-web.sh`.

## 5. The contract: `window.SRNative`

The game calls only these. Everything returns a Promise unless noted. Set `window.SRNative` before the
game's script runs, then call `window.srNativeReady()` once purchases and ads are set up.

| Member | Called when | Must do |
| --- | --- | --- |
| `platform` (string) | every analytics event | `'ios'` or `'android'` |
| `buy(productId)` | a price button is tapped | Purchase through RevenueCat. Resolve `{ok:true}` when the store confirms; `{ok:false, reason:'cancelled'\|'pending'\|'error'}` otherwise. The game grants the item only on `ok`. |
| `owned()` | at launch, silently | Resolve the list of non-consumable product ids the player owns (RevenueCat `getCustomerInfo`, no sign-in prompt). |
| `restore()` | Restore Purchases in Settings | RevenueCat `restorePurchases`, then resolve the owned list. |
| `prices()` | at launch | Resolve `{productId: {price, amount, currency}}`: RevenueCat's `priceString`, `price` and `currencyCode` (a plain localised string per product also works). These replace the US test prices everywhere in the game. The game redraws each price in its pixel font (p174) and works out every value label from these prices. |
| `showAd(placement)` | an ad button is tapped | Show a MAX rewarded ad. Resolve `{ok:true}` only if the reward callback fired; `{ok:false, reason:'no_fill'\|'closed'\|'error'}` otherwise. The game suspends its own audio while it waits. |
| `storeSave(key, json)` (sync) | after saves, at most every 5 s, and when the app goes to the background | Keep the latest JSON in `@capacitor/preferences` and, on iOS, in iCloud key-value storage (`NSUbiquitousKeyValueStore`, small local plugin). |
| `window.SRNativeSave` (object, not a function) | read once at launch | `{key: json}` with the saved game, set at document start so the game finds it when the browser storage is empty (reinstall, new phone). On iOS a `WKUserScript` at document start; on Android `WebViewCompat.addDocumentStartJavaScript`. |
| `network` (string, or a function returning one, sync) | before a session recording starts | `'wifi'`, `'cellular'` or `'none'`, kept current by the app (`@capacitor/network`). Anything else counts as not Wi-Fi. |
| `recordOK()` (sync) | before a session recording starts | `false` when the player said no to analytics in the consent flow (section 7); otherwise `true`. |
| `askReminders()` | the player says yes on the game's own nudge card | Ask for notification permission; resolve `true` if granted. Never ask before this. |
| `scheduleReminders(list)` (sync) | every time the game goes to the background | Cancel all pending reminders and schedule this list: `[{id, at (ms), title, body}]`. Send at most one a day: drop any that fall within 20 hours of another, keep the earliest. No reminders between 21:00 and 09:00 local: move them to 09:00. |

Placements (`showAd`): `continue` (+15 s when time runs out near a star), `double_coins` (x2 coins after a
job), `free_gems` (5 gems, 3 a day), `shed_double` (x2 helper-shed coins). Premium players never see ads;
the game handles that.

## 6. Products (create these in both stores, then in RevenueCat)

Ids are fixed in the game (`IAP.ids` in p163, the gem ladder in p170). Prices approved by Alex on
Nov 21 (price doc: https://claude.ai/artifact/HAVajemhRomSd4CxGXcbHS). UK and euro stores: the same numbers
in pounds and euros (£0.99, €0.99 and so on), set by hand per storefront. Every claim in the shop (pack bonus %,
BEST VALUE, what a coin bag's gems cost in money, the Wild Ride Pass saving) is worked out on the phone from the
store's own prices and rounded down; a claim the prices can't support is simply not shown.

| Product id | Type | Price (USD tier) | Gives | Restorable |
| --- | --- | --- | --- | --- |
| `premium` | Non-consumable | $6.99 | x2 coins forever, rewards without ads, Gold Paint, 12 h helper shed, 25 runs of coins on purchase | Yes (not the coins) |
| `starter_pack` | Non-consumable | $0.99 | 150 gems, 10 runs of coins, Explorer outfit; offered once, for 48 hours | Yes (outfit only) |
| `gems_60` | Consumable | $0.99 | 60 gems | No |
| `gems_135` | Consumable | $1.99 | 135 gems | No |
| `gems_365` | Consumable | $4.99 | 365 gems | No |
| `gems_800` | Consumable | $9.99 | 800 gems | No |
| `gems_1850` | Consumable | $19.99 | 1,850 gems | No |
| `ride_monster` | Non-consumable | $1.99 | Monster Truck Wild Ride | Yes |
| `ride_jet` | Non-consumable | $1.99 | Jet Sled Wild Ride | Yes |
| `ride_mech` | Non-consumable | $2.99 | Mech Wild Ride | Yes |
| `ride_dragon` | Non-consumable | $2.99 | Dragon Wild Ride | Yes |
| `ride_ufo` | Non-consumable | $3.99 | UFO Wild Ride | Yes |
| `wild_ride_pass` | Non-consumable | $7.99 | All five Wild Rides as they unlock | Yes |

The first gem pack a player buys gives double gems: the game does that, no extra product.
In the app build since Nov 22 (p181, p182; Alex said yes on Nov 21): create these two with the others.

| Product id | Type | Price (USD tier) | Gives | Restorable |
| --- | --- | --- | --- | --- |
| `snow_bank` | Consumable | $2.99 | The gems saved in the Snow Bank (220 to 400); the jar starts again | No |
| `event_pass` | Consumable | $2.99 | Event Pass for the weekend event on now (one per event; 250 gems is the other way to get it) | No (the paint it gives is in the save, which the phone mirrors) |

RevenueCat: one entitlement `premium` attached to `premium`; the rest are read from the customer's
non-subscription purchases. Use StoreKit 2. Test with Sandbox testers (Apple) and license testers (Google).

## 7. Ads and consent

- AppLovin MAX with AdMob as a mediated network. Rewarded ads only; no banners, no interstitials.
- Consent: turn on MAX's Terms and Privacy Policy flow. It shows Google's consent form to players in the
  EU and UK and Apple's App Tracking Transparency prompt on iOS, with the privacy policy URL
  (https://snowplowrush.app/privacy, Alex reviews it first).
- iOS `Info.plist`: `NSUserTrackingUsageDescription` ("Lets ads in Snowplow Rush be more relevant to you."),
  the `SKAdNetworkItems` list from AppLovin's docs, `GADApplicationIdentifier` for AdMob.
- Android: AdMob app id in the manifest; `com.google.android.gms.permission.AD_ID`.

## 8. Analytics in the app

The game's own PostHog code works inside the app unchanged (with p162 it survives bad connections).
`platform` tells PostHog which app an event came from. Session recording in the apps (decided Nov 21,
p171): 1 in 4 new installs, first visit only, up to 10 minutes, 1 frame a second, only on Wi-Fi
(`SRNative.network`), never when `SRNative.recordOK()` is false; it must be in the consent text. Still to
decide before launch: whether `iap_test` events become `purchase` events with the price (a small patch).

## 9. Release build

`python3 tools/release.py index.html www/index.html` (written by the cloud session) removes
`window.__MONEY`, `window.__SR`, `window.__EV` and the other test hooks, turns off `?test`, `?review`,
`?lab`, `?event` previews and the dev panel, and checks that none are left. `copy-web.sh` runs it.

## 10. Store submission checklist

- [ ] Accounts open; bundle id `app.snowplowrush` registered on both stores
- [ ] Apple Small Business Program enrolled (weeks before launch); Paid Apps agreement, bank and tax done
- [ ] Developer name "Kiln Fire Games" confirmed with Alex before the first app record
- [ ] `/app-ads.txt` live on the developer website listed in both stores
- [ ] Products from 6 created in both stores and in RevenueCat; prices confirmed by Alex
- [ ] MAX rewarded units created; AdMob linked inside MAX; consent flow on
- [ ] `www/` built with `tools/release.py`; game boots offline; Restore Purchases works in Sandbox
- [ ] A purchase, a cancelled purchase, a restore, an ad with no fill, a reinstall (save comes back)
- [ ] The shop on a UK and a euro Sandbox account: £ and € prices drawn, no TEST MODE line, labels sensible
- [ ] Reminders: card after the first three-star job; at most one a day; none at night
- [ ] Privacy policy live at https://snowplowrush.app/privacy (after Alex's review)
- [ ] Apple privacy label, Google data safety form, age rating: answers in the store doc
- [ ] Screenshots: iPhone 6.9" (1320x2868) and 6.5" (1242x2688); iPad only if iPad is supported; Android
      phone 1080x1920 or larger; feature graphic 1024x500 for Google Play
- [ ] TestFlight build to Alex and Lloyd; Google Play internal testing track
- [ ] Export compliance: the app only uses standard HTTPS, so it qualifies for the exemption

## 11. What to ask Alex, what not to

Ask before: anything that costs money, the final prices, turning on session recording in the apps,
the store text and screenshots, submitting for review. Don't ask about: plugin choices, project layout,
build settings, test devices; decide and note it in `app/NOTES.md`.
