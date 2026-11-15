# usage: python3 retime.py area [ids,comma]  -> sets each job's time so d (ref tool lv0) matches its target, rebuilds
import json, subprocess, sys, os
area = sys.argv[1]; only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
REF = {'suburbs': 2, 'farm': 3, 'city': 5, 'themepark': 5, 'harbour': 5, 'ski': 5, 'pass': 5, 'north': 5}
base = json.load(open('/home/claude/levels/baseline_stats.json'))
tgt = json.load(open('/home/claude/levels/targets.json')) if os.path.exists('/home/claude/levels/targets.json') else {}
ref = int(os.environ.get('REF', REF[area]))
out = subprocess.run(['node', '/home/claude/scripts/jobstat.js', area], capture_output=True, text=True, env=dict(os.environ, TOOLS=str(ref)), cwd='/home/claude/proto', timeout=900).stdout
S = json.loads(out.strip().splitlines()[-1])
tf = '/home/claude/levels/%s.json.times.json' % area
T = json.load(open(tf)) if os.path.exists(tf) else {}
for id, e in S.items():
    if only and id not in only: continue
    if id not in base: continue
    dt = tgt.get(id, base[id]['d']); t3 = e['tools'][str(ref)]['t3']
    T[id] = max(20, round(t3 / dt)); print(id, 'd target %.2f  t3 %.1f  time %d -> %d' % (dt, t3, e['time'], T[id]))
json.dump(T, open(tf, 'w'))
subprocess.run(['python3', '/home/claude/levels/%s.py' % area], cwd='/home/claude/levels', check=True, capture_output=True)
subprocess.run(['bash', '/home/claude/scripts/rebuild6.sh'], check=True, capture_output=True)
