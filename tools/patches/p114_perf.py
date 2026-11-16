import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Speed for older phones (Nov 16).
# The snow surface was one canvas the height of the whole job (up to 180x8400). The game draws it every frame and then
# writes the cleared snow into it, and a canvas that has just been drawn from is copied whole before it can be changed:
# ~6 MB per write, several writes per frame, ~1 ms each even for a 2x2 pixel change. It is now cut into 128px tiles,
# changes are tracked per 32px band, and each band is uploaded from a small scratch image into its own tile.
TILE=128
rep("  g.canvas=mk(pw,ph);g.lctx=g.canvas.getContext('2d');g.img=g.lctx.createImageData(pw,ph);",
    "  g.tiles=[];for(let ty=0;ty<ph;ty+=%d){const th=Math.min(%d,ph-ty),c=mk(pw,th);g.tiles.push({c,x:c.getContext('2d'),y0:ty,h:th});}g.lctx=g.tiles[0].x;g.img=g.lctx.createImageData(pw,ph);\n  Object.defineProperty(g,'canvas',{configurable:true,get(){const c=mk(pw,ph),x=c.getContext('2d');for(const t of g.tiles)x.drawImage(t.c,0,t.y0);return c;}}); // whole map, for tools only" % (TILE,TILE))
rep("  for(let cy=0;cy<rows;cy++)for(let cx=0;cx<cols;cx++)paintCell(g,cx,cy);\n  g.lctx.putImageData(g.img,0,0);g.dirty=null;",
    "  for(let cy=0;cy<rows;cy++)for(let cx=0;cx<cols;cx++)paintCell(g,cx,cy);\n  for(const t of g.tiles)t.x.putImageData(g.img,0,-t.y0,0,t.y0,pw,t.h);if(g.dB)g.dB.clear();g.dirty=null;")
rep("  const dr=g.dirty,x0=cx*2,y0=cy*2;\n  if(!dr)g.dirty={x0,y0,x1:x0+2,y1:y0+2};else{if(x0<dr.x0)dr.x0=x0;if(y0<dr.y0)dr.y0=y0;if(x0+2>dr.x1)dr.x1=x0+2;if(y0+2>dr.y1)dr.y1=y0+2;}}",
    "  const x0=cx*2,y0=cy*2,dbi=y0>>5;if(!g.dB)g.dB=new Map();const dr=g.dB.get(dbi);\n  if(!dr)g.dB.set(dbi,{x0,y0,x1:x0+2,y1:y0+2});else{if(x0<dr.x0)dr.x0=x0;if(y0<dr.y0)dr.y0=y0;if(x0+2>dr.x1)dr.x1=x0+2;if(y0+2>dr.y1)dr.y1=y0+2;}g.dirty=1;}")
rep("function flushLevel(g){const d=g.dirty;if(!d)return;g.lctx.putImageData(g.img,0,0,d.x0,d.y0,d.x1-d.x0,d.y1-d.y0);g.dirty=null;}",
    "function flushLevel(g){if(!g.dirty||!g.dB)return;const pw=g.pw,src=g.img.data;if(!g.scr)g.scr=g.lctx.createImageData(pw,32);const sd=g.scr.data;\n  for(const d of g.dB.values()){const t=g.tiles[(d.y0/%d)|0];sd.set(src.subarray(d.y0*pw*4,d.y1*pw*4));t.x.putImageData(g.scr,0,d.y0-t.y0,d.x0,0,d.x1-d.x0,d.y1-d.y0);}g.dB.clear();g.dirty=null;}" % TILE)
rep("  b.drawImage(G.canvas,0,cy,W,VIEW_H,0,cy,W,VIEW_H);",
    "  for(const t of G.tiles){const a=Math.max(cy,t.y0),e=Math.min(cy+VIEW_H,t.y0+t.h);if(e>a)b.drawImage(t.c,0,a-t.y0,W,e-a,0,a,W,e-a);}")

# Forest and rock jobs drew every tree twice a frame (shadow + sprite): 700-900 draws per frame on Snowshoe, Spires,
# Mountain Hut. The trees never move, so they are now baked once per job into 128px layer tiles (one for their shadows,
# one for the trees, in the same back-to-front order as before). Where anything that moves (the plow, hazards, cows,
# neighbours) or a prop is partly behind a tree, that tree is drawn again on top, clipped to that thing's box, so the
# layering is exactly what it was.
rep("g.scenery.push({spr:sp,sx:Math.round(qx-sp.width/2),sy:qy-sp.height+2,base:qy+2});",
    "g.scenery.push({spr:sp,sx:Math.round(qx-sp.width/2),sy:qy-sp.height+2,base:qy+2,wild:1});")
rep("function drawPlay(){",
r"""function bakeWild(g){const key=LOOK+'|'+SHD+'|'+lkShadow()+'|'+lkOutline();if(g.wbk===key)return;
  if(!g.wlist){g.wlist=g.scenery.filter(o=>o.wild).sort((a,c)=>a.base-c.base);g.scenery=g.scenery.filter(o=>!o.wild);g.wb=new Map();
    for(const o of g.wlist){for(let k=(o.sy-1)>>5;k<=(o.sy+o.spr.height)>>5;k++){let a=g.wb.get(k);if(!a)g.wb.set(k,a=[]);a.push(o);}}}
  g.wbk=key;g.wsh=null;g.wtr=null;if(!g.wlist.length)return;const TH=128;
  const put=(L,img,x,y,al)=>{const a=Math.max(0,y),e=Math.min(g.ph,y+img.height);for(let ty=Math.floor(a/TH);ty*TH<e;ty++){let t=L.get(ty);
    if(!t){const h=Math.min(TH,g.ph-ty*TH),c=mk(g.pw,h);t={c,x:c.getContext('2d'),y0:ty*TH,h};L.set(ty,t);}t.x.globalAlpha=al;t.x.drawImage(img,x,y-t.y0);t.x.globalAlpha=1;}};
  if(lkShadow()){const sp=SHD_P[SHD]||SHD_P.thin;g.wsh=new Map();for(const o of g.wlist)put(g.wsh,shadowOf(o.spr),o.sx+sp[0],o.sy+sp[1],sp[2]);}
  g.wtr=new Map();for(const o of g.wlist){if(lkOutline())put(g.wtr,outlineOf(o.spr),o.sx-1,o.sy-1,1);put(g.wtr,bright(o.spr),o.sx,o.sy,1);}}
function drawWildLayer(L,cy){if(!L)return;for(let ty=Math.floor(Math.max(0,cy)/128);ty*128<cy+VIEW_H;ty++){const t=L.get(ty);if(!t)continue;
  const a=Math.max(cy,t.y0),e=Math.min(cy+VIEW_H,t.y0+t.h);if(e>a)b.drawImage(t.c,0,a-t.y0,W,e-a,0,a,W,e-a);}}
function wildOcc(x,y,w,h,base,ents){const g=G;if(!g.wb)return;x=Math.round(x);y=Math.round(y);w=Math.round(w);h=Math.round(h);const seen=new Set();
  for(let k=y>>5;k<=(y+h)>>5;k++){const a=g.wb.get(k);if(!a)continue;for(const o of a){if(o.base<=base||seen.has(o))continue;
    if(o.sx-1>=x+w||o.sx+o.spr.width+1<=x||o.sy-1>=y+h||o.sy+o.spr.height+1<=y)continue;seen.add(o);
    ents.push({base:o.base,draw:()=>{b.save();b.beginPath();b.rect(x,y,w,h);b.clip();if(lkOutline())b.drawImage(outlineOf(o.spr),o.sx-1,o.sy-1);b.drawImage(bright(o.spr),o.sx,o.sy);b.restore();}});}}}
function drawPlay(){""")
rep("  const top=cy-60,bot=cy+VIEW_H+60;","  const top=cy-60,bot=cy+VIEW_H+60;bakeWild(G);")
rep("if(lkShadow()){const sp=SHD_P[SHD]||SHD_P.thin;b.save();b.globalAlpha=sp[2];\n    for(const o of G.obstacles)",
    "if(lkShadow()){const sp=SHD_P[SHD]||SHD_P.thin;b.save();drawWildLayer(G.wsh,cy);b.globalAlpha=sp[2];\n    for(const o of G.obstacles)")
rep("  for(const o of G.obstacles)if(o.sy+o.spr.height>top&&o.sy<bot)ents.push({base:o.base,draw:()=>{if(lkOutline()||(LOOK==='e'&&smallOb(o)))b.drawImage(outlineOf(o.spr),o.sx-1,o.sy-1);b.drawImage(bright(o.spr),o.sx,o.sy);}});",
    "  for(const o of G.obstacles)if(o.sy+o.spr.height>top&&o.sy<bot){ents.push({base:o.base,draw:()=>{if(lkOutline()||(LOOK==='e'&&smallOb(o)))b.drawImage(outlineOf(o.spr),o.sx-1,o.sy-1);b.drawImage(bright(o.spr),o.sx,o.sy);}});wildOcc(o.sx-1,o.sy-1,o.spr.width+2,o.spr.height+2,o.base,ents);}")
rep("  for(const o of G.scenery)if(o.sy+o.spr.height>top&&o.sy<bot)ents.push({base:o.base,draw:()=>{if(lkOutline())b.drawImage(outlineOf(o.spr),o.sx-1,o.sy-1);b.drawImage(bright(o.spr),o.sx,o.sy);}});",
    "  for(const o of G.scenery)if(o.sy+o.spr.height>top&&o.sy<bot){ents.push({base:o.base,draw:()=>{if(lkOutline())b.drawImage(outlineOf(o.spr),o.sx-1,o.sy-1);b.drawImage(bright(o.spr),o.sx,o.sy);}});wildOcc(o.sx-1,o.sy-1,o.spr.width+2,o.spr.height+2,o.base,ents);}")
rep("  ents.sort((a,c)=>a.base-c.base);for(const e of ents)e.draw();",
    "  if(G.wb){for(const hz of G.hazards){if(hz.kind!=='skier'&&(hz.y+40<top||hz.y-40>bot))continue;wildOcc(hz.x-16,hz.y+hz.h-56,hz.w+32,64,hz.y+hz.h,ents);}\n    for(const cw of G.cows)if(cw.y>top&&cw.y<bot)wildOcc(cw.x-12,cw.y-18-(cw.z||0),24,24+(cw.z||0),cw.y+3,ents);\n    for(const nb of G.neighbours)if(nb.y>top&&nb.y<bot)wildOcc(nb.x-10,nb.y-30,20,32,nb.y+1,ents);\n    wildOcc(P.x-52,fp.y-40,104,fp.h+80,fp.y+fp.h,ents);}\n  drawWildLayer(G.wtr,cy);\n  ents.sort((a,c)=>a.base-c.base);for(const e of ents)e.draw();")

open(f,'w',encoding='utf-8').write(s)
print('p114 perf: tiled snow surface, baked forest layers')
