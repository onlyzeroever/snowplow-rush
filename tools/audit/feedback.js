const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await br.newContext({ viewport: { width: 390, height: 760 } })).newPage(); const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(1000);
  await p.evaluate(() => window.__EV(`(()=>{save.tut=true;state='map';goMap();settingsOpen=true;})()`)); await p.waitForTimeout(500);
  await p.screenshot({ path: '/tmp/fb_settings.png' });
  await p.evaluate(() => window.__EV(`openFeedback('ask8')`)); await p.waitForTimeout(300);
  await p.type('#fbt', 'Love the snow spray! Space bar test works.'); await p.screenshot({ path: '/tmp/fb_box.png' });
  const v = await p.evaluate(() => document.getElementById('fbt').value);
  // in test mode phFeedback refuses to send; check the event shape by calling with TEST_MODE off in a sandboxed copy
  const shape = await p.evaluate(() => window.__EV(`(()=>{let sent=null;const o=phSendForm;phSendForm=(b)=>{sent=b;};const tm=TEST_MODE;try{TEST_MODE=false;}catch(e){}const ok=phFeedback('hello','ask8');phSendForm=o;return {ok,tm,ev:sent&&sent[0].event,props:sent&&Object.keys(sent[0].properties).join(',')};})()`)).catch(e=>'ERR '+e.message);
  await p.click('#fbc'); const gone = await p.evaluate(() => !document.getElementById('fbx'));
  console.log('typed', JSON.stringify(v), 'shape', JSON.stringify(shape), 'closed', gone, 'errors', JSON.stringify(errs)); await br.close(); })();
