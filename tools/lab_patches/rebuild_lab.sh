set -e
# prototype build: everything rebuild6.sh does, then the lab patches, into lab6.html (never shipped to main)
cd /home/claude/proto && cp game5.html gamelab.html && python3 /home/claude/scripts/patches/p1_levels.py gamelab.html >/dev/null && python3 /home/claude/scripts/patches/p2_map.py gamelab.html >/dev/null
for f in $(ls /home/claude/scripts/patches/p*_*.py | sed -E 's#.*/p([0-9]+)_.*#\1 &#' | sort -n | awk '$1>=3{print $2}'); do python3 "$f" gamelab.html >/dev/null; done
for f in $(ls /home/claude/scripts/lab_patches/p*_*.py | sort); do python3 "$f" gamelab.html; done
python3 /home/claude/scripts/build.py gamelab.html /home/claude/ref/logo_crop.png lab6.html
