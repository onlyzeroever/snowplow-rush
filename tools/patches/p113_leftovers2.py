import sys,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def blob(name):
    i=s.index('const '+name+'=')+len('const '+name+'=');o,e=json.JSONDecoder().raw_decode(s,i);assert json.dumps(o,separators=(',',':'),ensure_ascii=False)==s[i:e];return o,i,e
def put(o,i,e):
    global s;s=s[:i]+json.dumps(o,separators=(',',':'),ensure_ascii=False)+s[e:]
def mv(props,idx,pid,old,new):
    p=props[idx];assert p[0]==pid and p[1:3]==old,(pid,idx,p);p[1],p[2]=new
# Last two jobs over 1%: hay bales and the tub sat in the middle of the maze's dead ends; playground corner oaks.
sub,si,se=blob('SUB_DATA')
pg=sub['playground']['props'];mv(pg,4,'oak',[10,10],[-6,-8]);mv(pg,5,'oak',[148,14],[136,14])
put(sub,si,se)
packs,pi_,pe=blob('AREA_PACKS');jobs={jb['id']:jb for pk in packs for jb in pk['jobs']}
mz=jobs['maze']['data']['props'];mv(mz,1,'hay',[140,1000],[144,974]);mv(mz,2,'hay',[24,780],[24,754]);mv(mz,3,'tub',[144,160],[144,134])
put(packs,pi_,pe)
open(f,'w',encoding='utf-8').write(s)
print('p113 maze + playground pockets')
