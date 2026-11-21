// the review links as a tester opens them (no test hooks): first screen of each, on a phone-sized browser
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => {
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const links = [['fresh', 'app_preview.html?fresh'], ['play', 'app_preview.html'], ['starter', 'app_preview.html?review=all&starter'], ['bank', 'app_preview.html?review=all&bank'], ['bank2', 'app_preview.html?review=all&bank2'], ['event', 'app_preview.html?review=all&event=blizzard'], ['labrev', 'lab6.html?review=all']];
  const errs = [];
  for (const [n, u] of links) {
    const ctx = await br.newContext({ viewport: { width: 393, height: 760 }, isMobile: true, hasTouch: true }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(n + ': ' + e.message));
    await p.goto('http://127.0.0.1:8766/' + u); await p.waitForTimeout(1500);
    // tap through the title (bottom half) to reach the map
    const box = await p.locator('#c').boundingBox(); await p.mouse.click(box.x + box.width / 2, box.y + box.height * 0.75); await p.waitForTimeout(1800);
    await p.screenshot({ path: `/tmp/audit/links_${n}.png` }); console.log(n, p.url().replace('http://127.0.0.1:8766/', ''));
    await ctx.close();
  }
  console.log('errors', errs.slice(0, 4)); await br.close();
})();
