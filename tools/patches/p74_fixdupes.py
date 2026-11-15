import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# Bug fix: three sprite functions were defined twice, and in JavaScript the later definition silently replaces the
# earlier one everywhere. So the stadium stands, the airport baggage tug and Benny Bear (theme-park chaser) were being
# drawn with the newer props' art (ski grandstand, harbour tugboat, bear statue on a plinth). Rename the newer ones
# and point their props at the new names.
def rename_second(old,new):
    global s
    a=s.index('function '+old+'(');b=s.index('function '+old+'(',a+5)
    s=s[:b]+'function '+new+'('+s[b+len('function '+old+'('):]
    assert s.count('function '+old+'(')==1
rename_second('mascotSprite','mascotStatueSprite')
rename_second('standSprite','grandstandSprite')
rename_second('tugSprite','tugboatSprite')
for a,b in [("mascot:{make:()=>scnSpr('ms',mascotSprite)","mascot:{make:()=>scnSpr('ms',mascotStatueSprite)"),
            ("stand:{arg:80,min:20,max:180,make:a=>standSprite(a)","stand:{arg:80,min:20,max:180,make:a=>grandstandSprite(a)"),
            ("tug:{make:()=>scnSpr('tg',tugSprite)","tug:{make:()=>scnSpr('tg',tugboatSprite)")]:
    assert s.count(a)==1,a
    s=s.replace(a,b)
open(f,'w',encoding='utf-8').write(s)
