import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:80])
    s=s.replace(a,b)
# Bug audit fixes (Nov 15)
# 1. Theme-park ghosts: the generic 'ped' branch caught them first, so they were drawn as a solid, still sheet.
rep("else if(hz.kind==='ped')ents.push({base:hz.y+hz.h,draw:()=>b.drawImage(hz.spr,hx-2,hy-9+(Math.floor(hz.t*6)%2))});",
    "else if(hz.kind==='ped'&&!hz.ghost)ents.push({base:hz.y+hz.h,draw:()=>b.drawImage(hz.spr,hx-2,hy-9+(Math.floor(hz.t*6)%2))});")

# 2. Save hardening: a damaged or hand-edited save could crash every frame (machine number out of range),
#    turn coins into text, or stop the save loading. Clean every field after loading.
rep("}catch(e){}save.tv=2;}","}catch(e){}save.tv=2;sanitizeSave();}\nfunction sanitizeSave(){const num=(v,d)=>(typeof v==='number'&&isFinite(v))?v:d,obj=v=>v&&typeof v==='object'&&!Array.isArray(v);\n  save.coins=Math.max(0,num(save.coins,0));save.gems=Math.max(0,Math.floor(num(save.gems,0)));save.winters=Math.max(0,Math.floor(num(save.winters,0)));\n  save.tool=Math.max(0,Math.min(TOOLS.length-1,Math.floor(num(save.tool,0))));if(save.use!=null){const u=Math.floor(num(save.use,-1));save.use=(u<0||u>save.tool)?null:u;}\n  if(save.gold!=null&&!(num(save.gold,-1)>=-1&&save.gold<TOOLS.length))save.gold=-1;\n  for(const k of ['stars','best','fails']){const src=Array.isArray(save[k])?save[k]:[],a=Array(NL).fill(0);for(let i=0;i<NL&&i<src.length;i++)a[i]=Math.max(0,num(src[i],0));save[k]=a;}\n  for(let i=0;i<NL;i++)save.stars[i]=Math.min(3,Math.floor(save.stars[i]));\n  for(const k of ['ach','stats','hats','outfits','skin','skins','trails','treasures','tolls','story','parts','rideSeen'])if(save[k]!=null&&!obj(save[k]))save[k]={};\n  if(!obj(save.lv))save.lv={};for(const k of ['speed','size','value','bumper','helpers'])save.lv[k]=Math.max(0,Math.min(k in UPG?upMax(k):99,Math.floor(num(save.lv[k],0))));\n  if(save.mlv!=null){if(!obj(save.mlv))save.mlv={};for(const t in save.mlv){const m=save.mlv[t];if(!obj(m)){delete save.mlv[t];continue;}for(const k of MACHINE_UPG)m[k]=Math.max(0,Math.min(upMax(k),Math.floor(num(m[k],0))));}}\n  if(save.parts)for(const t in save.parts)save.parts[t]=Math.max(0,Math.min(3,Math.floor(num(save.parts[t],0))));}")

# 3. Title screen: the kid and his shovel pushed past the right edge at the end of the loading bar. The bar now stops
#    so the shovel's snow ends 20px from the right, matching the bar's 20px start on the left.
rep("const prog=(tNow*18)%140;","const prog=(tNow*18)%120;")
open(f,'w',encoding='utf-8').write(s)
