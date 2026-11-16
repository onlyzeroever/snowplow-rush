import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:80],s.count(a));s=s.replace(a,b_)
# Reach mask, more accurate (Nov 16): players steer diagonally, so a plow facing up/down can still edge sideways
# (and one facing left/right can edge up/down). The flood fill now lets either facing step in all four directions
# wherever its footprint fits; turning still needs room for both facings. Less snow is wrongly written off.
rep("    const a=o?(x>0?k-1:-1):(y>0?k-nx:-1),c=o?(x+2<=PW?k+1:-1):(k+nx<N?k+nx:-1);\n    if(a>=0&&!seen[a*2+o]){seen[a*2+o]=1;if(fits(a,o))q[qt++]=a*2+o;}if(c>=0&&!seen[c*2+o]){seen[c*2+o]=1;if(fits(c,o))q[qt++]=c*2+o;}}",
    "    for(const n2 of [x>0?k-1:-1,x+2<=PW?k+1:-1,y>0?k-nx:-1,k+nx<N?k+nx:-1]){if(n2<0||seen[n2*2+o])continue;seen[n2*2+o]=1;if(fits(n2,o))q[qt++]=n2*2+o;}}")
open(f,'w',encoding='utf-8').write(s)
print('p108 reach mask: diagonal steering')
