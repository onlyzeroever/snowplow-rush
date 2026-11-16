import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Balance audit (Nov 16). Airport is the first job you can only enter with the Super Plow, and it is twice the size of
# the City jobs before it (179k cells vs ~95k) in 85 s with 40/65/85% stars. In the economy sim a player who has just
# bought the Super Plow needed 5 tries for the first star (first-visit difficulty 1.61; the rest of the City is ~1.0),
# the worst spike in the game, right after the big purchase that should feel like a power-up.
# Now 105 s and 35/60/85% like City Hall after it: first star on the first try, 3 stars still a real goal.
rep("id:'airport', name:'AIRPORT',      area:'city',   h:4000,time:85,value:6,   stars:[40,65,85],",
    "id:'airport', name:'AIRPORT',      area:'city',   h:4000,time:105,value:6,  stars:[35,60,85],")
open(f,'w',encoding='utf-8').write(s)
print('p116 balance: airport')
