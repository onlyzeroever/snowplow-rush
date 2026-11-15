import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# Test-only hook: draw one map landmark (or a map helper) onto its own canvas, for art review sheets.
a="if(TEST_MODE)window.__AUD="
assert s.count(a)==1
s=s.replace(a,"if(TEST_MODE)window.__LM=(id,w,h)=>{w=w||64;h=h||56;const c=mk(w,h),g=c.getContext('2d');lmArt(g,id,w>>1,h>>1);return c;};\n"+a,1)
open(f,'w',encoding='utf-8').write(s)
