import sys
p=sys.argv[1];s=open(p).read()
a="text(b,'PROTOTYPE V0.5',W/2,300,"
assert s.count(a)==1
s=s.replace(a,"text(b,'PROTOTYPE V0.6.3',W/2,300,")
open(p,'w').write(s);print('p7 ok')
