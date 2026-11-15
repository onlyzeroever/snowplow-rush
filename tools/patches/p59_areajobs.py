import sys,json,os
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# ---------------------------------------------------------------------------------------------
# AREA JOB PACKS: every area after the Suburbs is a data pack written by /home/claude/levels/<area>.py
# (jobs, map positions, landmarks, road shapes, relinks, boss star gates, the area's story card).
# Packs are appended after the existing jobs so old saves keep their star slots.
# ---------------------------------------------------------------------------------------------
PACKS=[]
for a in ['farm','city','themepark','harbour','ski','pass','north']:
    p='/home/claude/levels/'+a+'.json'
    if os.path.exists(p):
        P=json.load(open(p));P['area']=a;PACKS.append(P)
JS=json.dumps(PACKS,separators=(',',':'))
rep("for(const L of LEVELS){const D2=SUB_DATA[L.id];if(!D2)continue;L.data=D2;for(const k of ['h','time','value','stars','presents'])if(D2[k]!=null)L[k]=D2[k];}",
    "for(const L of LEVELS){const D2=SUB_DATA[L.id];if(!D2)continue;L.data=D2;for(const k of ['h','time','value','stars','presents'])if(D2[k]!=null)L[k]=D2[k];}\n"
    "const AREA_PACKS="+JS+";\n"
    "for(const A of AREA_PACKS){for(const J of A.jobs)LEVELS.push(Object.assign({mx:0,my:0},J));for(const id in (A.relink||{})){const L=LEVELS.find(L2=>L2.id===id);if(L)L.from=A.relink[id];}}")
rep("for(const L of LEVELS){const p=MAPPOS[L.id];if(p){L.mx=p[0];L.my=p[1];}}\nfunction mapEdgesOld()",
    "for(const A of AREA_PACKS){Object.assign(MAPPOS,A.mappos||{});Object.assign(LANDMARK,A.landmark||{});Object.assign(EDGE_VIA,A.edgevia||{});}\n"
    "for(const L of LEVELS){const p=MAPPOS[L.id];if(p){L.mx=p[0];L.my=p[1];}}\nfunction mapEdgesOld()")
rep("const BOSS_STARS={blockparty:25};","const BOSS_STARS=Object.assign({blockparty:25},...AREA_PACKS.map(A=>A.bossStars||{}));")
rep("const STORY={","const STORY_EXTRA=Object.fromEntries(AREA_PACKS.filter(A=>A.story).map(A=>[A.area,A.story]));\nconst STORY={")
rep("function jobLockReason(i){","Object.assign(STORY,STORY_EXTRA);\nfunction jobLockReason(i){")
rep("for(const ar of ['suburbs','farm','city']){if(save.story[ar])continue;","for(const ar of AREA_SEQ){if(save.story[ar]||!STORY[ar])continue;")
open(f,'w',encoding='utf-8').write(s);print('p59 ok',len(PACKS),'packs')
