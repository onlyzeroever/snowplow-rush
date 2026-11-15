# desktop: keyboard hint on the first job, no stuck keys when the window loses focus, arrows/space don't scroll the page
import sys
p=sys.argv[1];s=open(p).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)
rep("text(b,'TO PUSH THE SNOW',W/2,VIEW_Y+VIEW_H-88,'#ffd23f',{align:'center'});}",
    "text(b,'TO PUSH THE SNOW',W/2,VIEW_Y+VIEW_H-88,'#ffd23f',{align:'center'});if(!('ontouchstart' in window)&&!navigator.maxTouchPoints)text(b,'OR USE ARROW KEYS / WASD',W/2,VIEW_Y+VIEW_H-76,'#9fd8ff',{align:'center'});}")
rep("window.addEventListener('keydown',e=>{keys[e.key]=true;",
    "window.addEventListener('blur',()=>{for(const k in keys)keys[k]=false;});\nwindow.addEventListener('keydown',e=>{keys[e.key]=true;if(state==='play'&&['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key))e.preventDefault();")
open(p,'w').write(s);print('p5 ok')
