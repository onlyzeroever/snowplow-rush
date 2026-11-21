# Audit Nov 21: the fun question was asked twice in a row. A player whose 5th job lands on a later day than their
# first visit answered "how fun is it so far?" and got "how fun is it, now you're back?" straight after (Alex and
# Lloyd both did on Nov 20: job5 + day2 ratings 1-2 s apart). The "back again" question now waits for a later day
# than the first answer.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("if(save.funAsk1&&!save.funAsk2&&save.day0!==today)return 'day2';",
    "if(save.funAsk1&&!save.funAsk2&&save.day0!==today&&(save.funAsk1Day||'')!==today)return 'day2';")
rep("const done=(score)=>{save[ask==='day2'?'funAsk2':'funAsk1']=true;",
    "const done=(score)=>{save[ask==='day2'?'funAsk2':'funAsk1']=true;if(ask!=='day2')save.funAsk1Day=new Date().toDateString();")
open(f,'w',encoding='utf-8').write(s)
print('p160 fun question: the "back again" ask waits for a later day than the first answer')
