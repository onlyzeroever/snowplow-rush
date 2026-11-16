const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const [id,ti]=process.argv.slice(2);
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await (await b.newContext({viewport:{width:390,height:844}})).newPage();
 await p.goto('http://127.0.0.1:8765/'+(process.env.PAGE||'index6.html')+'?test=1');await p.waitForTimeout(800);
 const r=await p.evaluate(([id,ti])=>{const R=window.__SR,EV=window.__EV;window.__HOLD=true;R.save.tut=true;R.save.tool=12;R.save.use=+ti;R.startLevel(R.LEVELS.findIndex(l=>l.id===id));window.__STEP(60,1/30,1);if(R.run)R.run.moved=true;
  const P=R.P,G=R.G;const proto=CanvasRenderingContext2D.prototype,od=proto.drawImage,op=proto.putImageData,of=proto.fillRect;let n=0,area=0,pn=0,parea=0,fn=0;const big={};
  proto.drawImage=function(im,...a){n++;let w,h;if(a.length>=8){w=a[6];h=a[7];}else if(a.length>=4){w=a[2];h=a[3];}else{w=im.width;h=im.height;}area+=Math.abs(w*h);const k=im.width+'x'+im.height;big[k]=(big[k]||0)+1;return od.call(this,im,...a);};
  proto.putImageData=function(d,x,y,dx,dy,dw,dh){pn++;parea+=(dw!=null?dw*dh:d.width*d.height);return op.apply(this,arguments);};proto.fillRect=function(){fn++;return of.apply(this,arguments);};
  const F=60;for(let k=0;k<F;k++){P.y=Math.max(30,G.ph*(1-(k%6)/6)-40);window.__STEP(1,1/30,0);}
  proto.drawImage=od;proto.putImageData=op;proto.fillRect=of;
  return {draws:n/F,areaK:Math.round(area/F/1000),puts:pn/F,putAreaK:Math.round(parea/F/1000),fills:fn/F,top:Object.entries(big).sort((a,b)=>b[1]-a[1]).slice(0,12).map(([k,v])=>k+':'+(v/F).toFixed(1)),ph:G.ph};},[id,ti]);
 console.log(id,JSON.stringify(r));await b.close();})();
