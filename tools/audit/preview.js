// the app preview page: boots as a new player, ?fresh wipes only its own save, analytics say 'lab'
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => {
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await br.newContext({ viewport: { width: 393, height: 852 } }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  const sent = []; await p.route(/posthog|\/i\/v0|\/e\/|batch|capture/, r => { try { sent.push(r.request().postData() || ''); } catch (e) {} r.fulfill({ status: 200, body: '{}' }); });
  await p.goto('http://127.0.0.1:8766/app_preview.html'); await p.waitForTimeout(1200);
  const st = await p.evaluate(() => [document.title, Object.keys(localStorage).join(',')]);
  await p.evaluate(() => { localStorage.setItem('snowplowRush.proto.v2', 'LABSAVE'); });
  const box = await p.locator('canvas:not(#bg)').boundingBox(); await p.mouse.click(box.x + box.width / 2, box.y + box.height * 0.8); await p.waitForTimeout(900);
  await p.goto('http://127.0.0.1:8766/app_preview.html?test=1'); await p.waitForTimeout(1200);
  const b2 = await p.locator('canvas:not(#bg)').boundingBox(); await p.mouse.click(b2.x + b2.width / 2, b2.y + b2.height * 0.8); await p.waitForTimeout(900);
  const play = await p.evaluate(() => window.__EV('(persist(),state)')); const keys = await p.evaluate(() => Object.keys(localStorage).join(','));
  await p.goto('http://127.0.0.1:8766/app_preview.html?fresh'); await p.waitForTimeout(1200);
  const after = await p.evaluate(() => [location.search, localStorage.getItem('snowplowRush.proto.v2'), Object.keys(localStorage).filter(k => k.indexOf('appPreview') >= 0).join(',')]);
  const html = require('fs').readFileSync('/home/claude/proto/app_preview.html', 'utf8'); const live = (html.match(/'review':'live'|register\(\{build:'live'/g) || []).length, lab = (html.match(/build:DEV_MODE\?'dev':'lab'|register\(\{build:'lab'/g) || []).length;
  console.log(JSON.stringify({ st, play, keys, after, live, lab }), 'errors', errs.slice(0, 2));
  console.log(st[0].startsWith('APP PREVIEW') && play === 'play' && /snowplowRush\.appPreview\.test/.test(keys) && !/snowplowRush\.test/.test(keys) && after[0] === '' && after[1] === 'LABSAVE' && live === 0 && lab === 3 && errs.length === 0 ? 'ALL OK' : 'FAILS'); await br.close();
})();
