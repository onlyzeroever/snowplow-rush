#!/usr/bin/env python3
"""Release build for the iOS and Android apps (Section 4 of the launch plan, Nov 21).

    python3 tools/release.py index.html www/index.html [--version 1.0.0]

Takes the live web build and writes a copy for the app stores with every test and review hook turned off:
  - ?test=1, ?review=..., the dev panel (window.SR_DEV), the look-test mode and ?event= previews do nothing;
  - window.__MONEY, window.__SR, window.__EV, window.__UI, window.__STEP, window.__AUD, window.__CAST and
    window.__LM are no longer created (anyone with a debugger could otherwise grant Premium or start any job);
  - the title shows "V<version>" instead of "PLAYTEST V0.8.0", and analytics report that version;
  - the page description no longer says "playtest build".
It refuses to write the file if any hook is still there, or if the input is not the shape it expects
(a game update that renames one of these lines makes this script stop rather than ship a hook).
"""
import re
import sys

REPLACEMENTS = [
    # mode flags: every query-string switch off
    ("const TEST_MODE=/[?&]test=1/.test(location.search),REVIEW_MODE=/[?&]review=(1|all|themepark|ski|pass|north)/.test(location.search);",
     "const TEST_MODE=false,REVIEW_MODE=false;"),
    ("const RV=(location.search.match(/[?&]review=(themepark|ski|pass|north)/)||[])[1]||null;", "const RV=null;"),
    ("const DEV_MODE=!!window.SR_DEV;", "const DEV_MODE=false;"),
    ("const LOOKTEST=!!window.__LOOKTEST;", "const LOOKTEST=false;"),
    ("const q=new URLSearchParams(location.search).get('event');", "const q=null;"),
    # hooks that exist on every page load: keep the objects (nothing inside the game reads them) but don't publish them
    ("window.__MONEY={", "const __MONEY_OFF={"),
    ("window.__SR={", "const __SR_OFF={"),
]
# hooks that are only made in test mode: make sure they can never be made
GUARDED = ["window.__EV=", "window.__UI=", "window.__STEP=", "window.__AUD=", "window.__CAST=", "window.__LM="]
FORBIDDEN = ["window.__MONEY", "window.__SR=", "window.SR_DEV", "/[?&]test=1/", "review=(1|all"]


def build(src, version):
    s = src
    for a, b in REPLACEMENTS:
        n = s.count(a)
        if n != 1:
            raise SystemExit(f"release: expected one '{a[:60]}...', found {n}; update tools/release.py")
        s = s.replace(a, b)
    for h in GUARDED:
        n = s.count("if(TEST_MODE)" + h)
        if n != 1:
            raise SystemExit(f"release: expected '{h}' behind if(TEST_MODE) once, found {n}")
        s = s.replace("if(TEST_MODE)" + h, "if(false)window.__off_" + h[len("window.__"):])
    for v in ("PLAYTEST V0.8.0'",):
        if s.count(v) != 1:
            raise SystemExit("release: title version label not found")
        s = s.replace(v, "V" + version.upper() + "'")
    s = s.replace("v:'0.8.0'", "v:'" + version + "'")
    s = s.replace(" - playtest build, plays in your browser.", ".")
    bad = [f for f in FORBIDDEN if f in s] + [h for h in GUARDED if re.search(r"(?<!if\(false\))" + re.escape(h), s)]
    if bad:
        raise SystemExit("release: hooks still present: " + ", ".join(bad))
    return s


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    version = "1.0.0"
    if "--version" in sys.argv:
        version = sys.argv[sys.argv.index("--version") + 1]
        args = [a for a in args if a != version]
    if len(args) != 2:
        raise SystemExit(__doc__)
    src = open(args[0], encoding="utf-8").read()
    out = build(src, version)
    open(args[1], "w", encoding="utf-8").write(out)
    print(f"release build {version}: {args[1]} ({len(out) // 1024} KB), test and review hooks off")


if __name__ == "__main__":
    main()
