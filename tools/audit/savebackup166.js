// p166: a backup copy of the save is written, and the game starts from it when the main save is unreadable
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const page = process.argv[2] || 'index6.html';
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/' + page + '?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c).then(JSON.parse);
  const k = await EV(`(()=>{save.coins=777777;save.tut=true;window.__bakT=0;persist();return JSON.stringify(SAVE_KEY);})()`);
  const bak = await p.evaluate(k => { const j = JSON.parse(localStorage.getItem(k + '.bak') || 'null'); return j && j.coins; }, k);
  ok('a save also writes the backup copy', bak === 777777, { key: k, bak });
  await EV(`(()=>{save.coins=888888;persist();return '1';})()`);
  const bak2 = await p.evaluate(k => JSON.parse(localStorage.getItem(k + '.bak')).coins, k);
  ok('the backup is written at most once a minute', bak2 === 777777, bak2);
  await p.evaluate(k => { window.__noPersist = true; localStorage.setItem(k, '{"coins":12,"broken'); }, k);
  await p.reload(); await p.waitForTimeout(900);
  const after = await EV(`JSON.stringify({coins:save.coins,fromBak:!!window.__saveFromBak})`);
  ok('an unreadable save comes back from the backup instead of starting over', after.coins === 777777 && after.fromBak, after);
  await EV(`(()=>{resetSave();return '1';})()`);
  const gone = await p.evaluate(k => localStorage.getItem(k + '.bak'), k);
  ok('Reset progress clears the backup too', gone === null || JSON.parse(gone).coins === 0, gone && gone.slice(0, 40));
  ok('no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
