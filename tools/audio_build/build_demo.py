import numpy as np, scipy.io.wavfile as w, scipy.signal as sg, subprocess
SR=44100; V='/home/claude/vsco/'; F='/home/claude/fish_in/b1/'; O='/home/claude/audio_build/'
def load(p):
    sr,x=w.read(p); x=x.astype(np.float64)
    if x.dtype!=np.float64 or np.abs(x).max()>2: x=x/32768.0
    if x.ndim==1: x=np.stack([x,x],1)
    assert sr==SR; return x
def norm(x,db=-1.0): return x/np.abs(x).max()*10**(db/20)
def shift(x,semi):
    if semi==0: return x
    n=int(round(len(x)/2**(semi/12))); return sg.resample(x,n,axis=0)
def fade(x,fin=0.003,fout=0.05):
    x=x.copy(); a=int(fin*SR); b=int(fout*SR)
    if a: x[:a]*=np.linspace(0,1,a)[:,None]
    if b: x[-b:]*=np.linspace(1,0,b)[:,None]**2
    return x
def trim_onset(x,rel_db=-30,pre=0.004):
    m=np.abs(x).max(1); th=m.max()*10**(rel_db/20); i=np.argmax(m>th); return x[max(0,i-int(pre*SR)):]
def place(buf,x,t,gain=1.0,pan=0.0):
    i=int(t*SR); n=min(len(x),len(buf)-i)
    L=np.cos((pan+1)*np.pi/4); R=np.sin((pan+1)*np.pi/4)
    buf[i:i+n,0]+=x[:n,0]*gain*L*1.414; buf[i:i+n,1]+=x[:n,1]*gain*R*1.414
# glockenspiel notes (file -> sounding pitch): C5f=C6, G5f=G6, C6f=C7, G6f=G7, C7f=C8
G={}
for f,(name) in {'C5':'C6','G5':'G6','C6':'C7','G6':'G7','C7':'C8'}.items():
    G[name]=trim_onset(load(V+f'Percussion/Glock/glock_medium_{f}.wav'),-40,0.002)
def note(n):
    src={'D6':('C6',2),'F#6':('G6',-1),'A6':('G6',2),'D7':('C7',2),'F#7':('G7',-1),'A7':('G7',2),'D8':('C8',2)}[n]
    return norm(shift(G[src[0]],src[1]),-3)
NS={n:note(n) for n in ['D6','F#6','A6','D7','F#7','A7','D8']}
def chord(buf,t,notes,g=0.5,spread=0.3):
    for k,n in enumerate(notes): place(buf,NS[n],t+k*0.004,g,(-spread+2*spread*k/max(1,len(notes)-1)))
def write(name,x):
    x=norm(x,-1.0); w.write(O+name+'.wav',SR,(x*32767).astype(np.int16))
# --- pow (Fish), cleaned: trim the front gap, keep the thump, fade the tail
pw=trim_onset(load(F+'raw_pow.wav'),-24); pw=fade(pw[:int(0.42*SR)],0.002,0.15); write('pow',pw)
# --- treasure, built: rising D major arpeggio into a sparkling chord
tr=np.zeros((int(1.7*SR),2))
for k,n in enumerate(['D6','F#6','A6','D7','F#7','A7']): place(tr,NS[n],k*0.065,0.35+0.08*k,-0.35+0.14*k)
chord(tr,0.43,['D7','F#7','A7','D8'],0.55); write('treasure',fade(tr,0,0.35))
# --- newmachine, hybrid: Fish's engine start + revs, then a glockenspiel unlock flourish
en=load(F+'raw_newmachine.wav')[:int(1.0*SR)]; en=fade(en,0.002,0.35)
nm=np.zeros((int(2.1*SR),2)); place(nm,en,0,0.9)
for k,n in enumerate(['D6','A6','D7','F#7','A7']): place(nm,NS[n],0.62+k*0.08,0.4+0.06*k,-0.3+0.15*k)
chord(nm,1.06,['D6','D7','F#7','A7','D8'],0.55); write('newmachine',fade(nm,0,0.4))
# --- sweep, built: a swelling snowy whoosh (filtered noise) rising into a quick glockenspiel run
rng=np.random.default_rng(7); L=int(0.75*SR); nz=rng.standard_normal((L,2))
t=np.arange(L)/SR; out=np.zeros_like(nz); blk=512
for i in range(0,L,blk):
    fc=350+2800*(i/L)**1.6; b,a=sg.butter(2,[fc*0.55/(SR/2),min(0.95,fc*1.8/(SR/2))],'band')
    out[i:i+blk]=sg.lfilter(b,a,nz[max(0,i-2048):i+blk],axis=0)[-min(blk,L-i):]
envw=np.sin(np.pi*np.clip(t/0.75,0,1))**1.5; out*=envw[:,None]
sw=np.zeros((int(1.5*SR),2)); place(sw,norm(out,-6),0,0.8)
for k,n in enumerate(['A6','D7','F#7','A7','D8']): place(sw,NS[n],0.38+k*0.045,0.3+0.05*k,0.4-0.2*k)
write('sweep',fade(sw,0,0.4))
# --- reel: current vs Fish (pow), Fish vs built (sweep, treasure, newmachine)
def mp3in(p):
    subprocess.run(['ffmpeg','-v','error','-y','-i',p,'-ar','44100','-ac','2','/tmp/_r.wav']); return load('/tmp/_r.wav')
seq=[(mp3in('/home/claude/snowplow-rush/audio/bump.mp3'),0.8),(pw,1.8),
     (load(F+'raw_sweep.wav'),0.8),(load(O+'sweep.wav'),1.8),
     (load(F+'raw_treasure.wav'),0.8),(load(O+'treasure.wav'),1.8),
     (load(F+'raw_newmachine.wav'),0.8),(load(O+'newmachine.wav'),0.5)]
parts=[]
for x,gap in seq: parts+= [norm(x,-1.5), np.zeros((int(gap*SR),2))]
reel=np.concatenate(parts); w.write(O+'reel.wav',SR,(reel*32767).astype(np.int16))
subprocess.run(['ffmpeg','-v','error','-y','-i',O+'reel.wav','-b:a','192k',O+'snowplow-sound-test-1.mp3'])
print('reel',len(reel)/SR,'s')
