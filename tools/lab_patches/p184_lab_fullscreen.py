# Lab only: the LAB button on the map is drawn in the pop-up pass; keep it at the top of the map on tall screens (p183 moves pop-ups to the middle).
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
a="button('labbtn',W-36,MAP_VY+3,"
assert s.count(a)==1,s.count(a)
s=s.replace(a,"button('labbtn',W-36,MAP_VY+3-UI_OY,")
open(f,'w',encoding='utf-8').write(s)
print('p184 lab: LAB button stays at the top of the map on tall screens')
