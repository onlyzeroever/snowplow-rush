// Sprite census: every sprite the game can draw in a job (SPR table, constants, frame sets, chasers, hazards' own sprites, pickups).
// node tools/audit/spritecensus.js  -> /tmp/va/allspr.json ; then python3 tools/audit/spritecensus_sheet.py -> /tmp/va/allspr_N.png (labelled, 4x)
// Map props/buildings: tools/audit/visaudit.js renders every map; /tmp/va/census.js style census lives in the worklog notes.
// every sprite the game can draw in a job: SPR table, *_FR frame sets, chasers, hazards' own sprites, kid/skins sample, pickups
const { chromium } = require('/opt/npm-tools/node_modules/playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await (await b.newContext()).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://127.0.0.1:8765/index6.html?test=1');await p.waitForTimeout(900);
const r=await p.evaluate(()=>window.__EV(`(()=>{const out=[];const seen=new Set();const add=(name,c,grp)=>{if(!c||!c.getContext||!c.width)return;if(seen.has(c))return;seen.add(c);out.push({name,grp,w:c.width,h:c.height,u:c.toDataURL()});};
 for(const k in SPR){const v=SPR[k];if(Array.isArray(v))v.forEach((c,i)=>add('SPR.'+k+'['+i+']',c,'SPR'));else add('SPR.'+k,v,'SPR');}
 const tops={CART,CARTL,CONE,BARREL,TIRES,HAY,BUS};for(const k in tops)add(k,tops[k],'const');
 for(const k of ['COW','COWL'])try{add(k,eval(k),'const');}catch(e){}
 for(const k of ['GHOST_FR','GULL_FR','PENG_FR','SHEEP_FR','SKIER_FR','BUMPER_FR','FORK_FR'])try{const a=eval(k);(Array.isArray(a)?a:[]).forEach((c,i)=>{if(Array.isArray(c))c.forEach((cc,j)=>add(k+'['+i+']['+j+']',cc,'frames'));else add(k+'['+i+']',c,'frames');});}catch(e){}
 for(const k in CHASERS){const C=CHASERS[k];for(const f in C){const v=C[f];if(v&&v.getContext)add('CHASER.'+k+'.'+f,v,'chaser');else if(Array.isArray(v))v.forEach((c,i)=>{if(c&&c.getContext)add('CHASER.'+k+'.'+f+'['+i+']',c,'chaser');});}}
 // hazards with own sprites across all jobs
 for(let i=0;i<LEVELS.length;i++){let g;try{g=buildLevel(i);}catch(e){continue;}for(const h of g.hazards){if(h.spr)add('HZ.'+h.kind+(h.horse?'.horse':h.peng?'.peng':h.gull?'.gull':''),h.spr,'hazard');}}
 try{add('partIcon',partIcon(),'pickup');add('driveIcon',driveIcon(),'pickup');}catch(e){}
 return JSON.stringify(out);})()`));
const o=JSON.parse(r);fs.mkdirSync('/tmp/va',{recursive:true});fs.writeFileSync('/tmp/va/allspr.json',JSON.stringify(o));
const g={};for(const x of o)g[x.grp]=(g[x.grp]||0)+1;console.log(o.length,g,errs.slice(0,3));await b.close();})();
