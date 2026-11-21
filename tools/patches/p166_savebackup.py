# Audit Nov 21 (bugs and tech, item 5): the save lived in one browser storage key; if it ever failed to load (a write
# cut off by a crash or a full disk), the game silently started over and the next save overwrote what was left.
# Now a second copy (key + '.bak') is written at most once a minute, and the game starts from it when the main copy is
# missing or unreadable. Reset progress clears the copy too. Works with p165 (apps: main copy, then the phone's copy,
# then the backup).
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
A="let s=JSON.parse(localStorage.getItem(SAVE_KEY)||'null');"
B="let s=JSON.parse(localStorage.getItem(SAVE_KEY)||(window.SRNativeSave&&window.SRNativeSave[SAVE_KEY])||'null');"
NEW=("let s=null;try{s=JSON.parse(localStorage.getItem(SAVE_KEY)||'null');}catch(e){s=null;}"
     "if((!s||typeof s!=='object')&&window.SRNativeSave&&window.SRNativeSave[SAVE_KEY]){try{s=JSON.parse(window.SRNativeSave[SAVE_KEY]);}catch(e){s=null;}}"
     "if(!s||typeof s!=='object'){try{s=JSON.parse(localStorage.getItem(SAVE_KEY+'.bak')||'null');if(s)window.__saveFromBak=1;}catch(e){s=null;}}")
if s.count(B)==1: rep(B,NEW)
else: rep(A,NEW)
rep("function persist(){if(window.__noPersist)return;try{save.last=Date.now();localStorage.setItem(SAVE_KEY,JSON.stringify(save));}catch(e){}}",
    "function persist(){if(window.__noPersist)return;try{save.last=Date.now();const j=JSON.stringify(save);localStorage.setItem(SAVE_KEY,j);"
    "if(Date.now()-(window.__bakT||0)>60000){localStorage.setItem(SAVE_KEY+'.bak',j);window.__bakT=Date.now();}}catch(e){}}")
rep("function resetSave(){Object.assign(save,{", "function resetSave(){try{localStorage.removeItem(SAVE_KEY+'.bak');}catch(e){}window.__bakT=0;Object.assign(save,{")
open(f,'w',encoding='utf-8').write(s)
print('p166 save backup: a second copy once a minute, used when the main save is missing or unreadable')
