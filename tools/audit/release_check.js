// release build: the game runs; ?test=1 / ?review=all / ?event= do nothing; no window hooks; title shows the version
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 360, height: 640 }, hasTouch: true, isMobile: true })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/release_test.html?test=1&review=all&event=blizzard'); await p.waitForTimeout(1500);
  const hooks = await p.evaluate(() => ['__EV', '__SR', '__MONEY', '__UI', '__STEP', '__AUD', '__CAST', '__LM'].filter(k => k in window));
  const u = await p.evaluate(() => document.querySelector('canvas').toDataURL()); fs.writeFileSync('/tmp/audit/release_title.png', Buffer.from(u.split(',')[1], 'base64'));
  await p.touchscreen.tap(180, 420); await p.waitForTimeout(1500);
  const saveKeys = await p.evaluate(() => Object.keys(localStorage));
  console.log(JSON.stringify({ hooks, saveKeys, errs: errs.slice(0, 3) }));
  console.log(hooks.length === 0 && saveKeys.includes('snowplowRush.proto.v2') && !errs.length ? 'ok   release build: no hooks, live save key, no errors' : 'FAIL release build');
  await b.close();
})();
