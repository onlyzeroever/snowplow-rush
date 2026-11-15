import sys; sys.path.insert(0,'/home/claude/art')
from harness import *
SW={'W':'#f6f1e6','C':'#cfc6b2','X':'#3b3442','Z':'#ffffff','p':'#f2a8b8'}
SHEEP=[[
"..KK.KK.KK....",
".KWWKWWKWWK...",
"KWWWWWWWWWWK..",
"KWWCWWWWWWKKK.",
"KWWWWWWWCKXXXK",
"KWCWWWWWWKXZXKK",
"KWWWWWCWWKXXXpK",
".KCWWWWWCKXXXK.",
"..KCCCCCK.KKK..",
"..XX...XX......",
"..XX...XX......"],[
"..KK.KK.KK....",
".KWWKWWKWWK...",
"KWWWWWWWWWWK..",
"KWWCWWWWWWKKK.",
"KWWWWWWWCKXXXK",
"KWCWWWWWWKXZXKK",
"KWWWWWCWWKXXXpK",
".KCWWWWWCKXXXK.",
"..KCCCCCK.KKK..",
"...XX.XX.......",
"...XX.XX......."]]
def skier_rows(col):
    return [
"...KKKK...",
"..KccccK..",
"..KcZcck..",
"..KVVVVK..",
"...KSSK...",
".KKKKKKKK.",
"KccKWWKccK",
"KcKcWWcKcK",
"UXKccccKXU",
"U.KKKKKK.U",
"U.KUKKUK.U",
"U.KUKKUK.U",
"U.KKKKKK.U",
"UKYKKKKYKU",
"..KYKKYK..",
"..KYKKYK..",
"..KYKKYK..",
"..KYKKYK..",
"..KEKKEK..",
"...K..K..."],{'c':col,'k':col,'Y':'#ffc727','E':'#fff1b8','U':'#8793a8'}
BEAR=[
"..............KKKK........",
"..........KKKKWWWWKK......",
"......KKKKWWWWWWWWWWK.....",
"....KKWWWWWWWWWWWWWWWKKK..",
"...KWWWWWWWWWWWWWWWWKWWWK.",
"..KWWCWWWWWWWCWWWWWWKWKWWK",
".KWWWWWWWWWWWWWWWWWWKWWWXK",
".KWWWWWWWCWWWWWWWWWKWWWKK.",
".KWWWWWWWWWWWWWWCWWKWwwK..",
"KKwWWWWWWWWWWWWWWWWWKKK...",
".KwwwwWWWWWWWWWWWwwwK.....",
"..KwwwwwwwwwwwwwwwwK......",
"..KWWWKKWWWK.KWWWKKWWWK...",
"..KWWWK.KWWK.KWWWK.KWWK...",
"..KWWWK.KWWK.KWWWK.KWWK...",
"..KwwwK.KwwK.KwwwK.KwwK...",
"..KXXXK.KXXK.KXXXK.KXXK...",
"..KKKKK.KKKK.KKKKK.KKKK..."]
BEAR1=[r for r in BEAR[:12]]+[
"...KWWWKWWWK.KWWWKWWWK....",
"...KWWWKWWWK.KWWWKWWWK....",
"...KWWWKWWWK.KWWWKWWWK....",
"...KwwwKwwwK.KwwwKwwwK....",
"...KXXXKXXXK.KXXXKXXXK....",
"...KKKKKKKKK.KKKKKKKKK...."]
BW={'w':'#c6d9f3','C':'#dfe7f2','X':'#2a2a36'}
items=[('sheep0',rows(SHEEP[0],SW)),('sheep1',rows(SHEEP[1],SW))]
for c in ['#d8364b','#3f86d6','#9b5fd6']:
    r,e=skier_rows(c); items.append(('skier',rows(r,e)))
items+= [('bear0',rows(BEAR,BW)),('bear1',rows(BEAR1,BW))]
sheet(items,'/home/claude/art/cast3.png',S=9,bg='#eef4fb')
