# Builds dev.html (the password-protected dev build at /dev) from index.html: same game with window.SR_DEV set.
import sys
src=sys.argv[1] if len(sys.argv)>1 else 'index.html'; out=sys.argv[2] if len(sys.argv)>2 else 'dev.html'
s=open(src,encoding='utf-8').read(); i=s.index('<script')
d=s[:i]+'<script>window.SR_DEV=1</script>'+s[i:]
d=d.replace('<title>','<title>DEV | ',1)
open(out,'w',encoding='utf-8').write(d)
