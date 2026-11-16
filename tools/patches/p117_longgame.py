import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Long-game decisions Alex said yes to (Nov 16 audit).
# 1. Ice Palace opens at 20 North stars (was 24): in the sim North replays drop from 36 to 21.
rep('"bossStars":{"icepalace":24}','"bossStars":{"icepalace":20}')
# 2. A New Winter opens at 60 stars short of every star (300 of 360 in winter 1), so the hardest North 3-stars aren't required.
WINTER_SLACK=60
rep("function starsNeeded(){let n=0;for(let i=0;i<NL;i++)if((LEVELS[i].winter||1)<=winterNo())n+=3;return n;}",
    "const WINTER_SLACK=%d;   // stars you can skip before a New Winter opens\n"
    "function starsNeeded(){let n=0;for(let i=0;i<NL;i++)if((LEVELS[i].winter||1)<=winterNo())n+=3;return Math.max(3,n-WINTER_SLACK);}"%WINTER_SLACK)
rep("text(b,'3-STAR EVERY JOB, THEN',W/2,206,","text(b,'EARN '+need+' STARS, THEN',W/2,206,")
rep("text(b,'3-STAR EVERY JOB TO UNLOCK',W/2,y,","text(b,'EARN '+need+' STARS TO UNLOCK',W/2,y,")
# 5. Helpers work up to 6 h while you're away (was 2 h), 12 h with Premium (was 6 h): an evening player who comes back
# the next evening gets about 1.2 runs of coins instead of 0.4 (sim, idle.py).
rep("premium:{price:'$4.99',was:'$7.99',coinRuns:25,shedS:21600}","premium:{price:'$4.99',was:'$7.99',coinRuns:25,shedS:43200}")
rep("const OFFLINE_CAP_BASE=7200, OFFLINE_RATE=0.5;","const OFFLINE_CAP_BASE=21600, OFFLINE_RATE=0.5;")
rep("'COIN PACK + 3x HELPER SHED'","'COIN PACK + 12H HELPER SHED'")
# Combo analytics, so the bump rule can be tuned on real play: best combo, coin-weighted average multiplier,
# and how many x1.2+ combos ended from a bump vs from slowing down (the 0.75 s fade).
rep("if(got>0){const coins=got*cellVal*comboMult;","if(got>0){const coins=got*cellVal*comboMult;run.cW=(run.cW||0)+got*comboMult;run.cG=(run.cG||0)+got;")
rep("if(run.combo<COMBO_MAX){run.combo++;","if(run.combo<COMBO_MAX){run.combo++;if(run.combo>(run.cBest||0))run.cBest=run.combo;")
rep("shake=0.25*red;run.combo=0;run.comboProg=0;run.hits++;","shake=0.25*red;if(run.combo>=2)run.cBonk=(run.cBonk||0)+1;run.combo=0;run.comboProg=0;run.hits++;")
rep("if(run.comboT<=0&&run.combo>0){if(run.combo>=2)sfx('cend');","if(run.comboT<=0&&run.combo>0){if(run.combo>=2){sfx('cend');run.cFade=(run.cFade||0)+1;}")
rep("track('job_end',Object.assign(phJob(),{pct:Math.round(R2.pct),",
    "track('job_end',Object.assign(phJob(),{combo_best:+(1+0.1*(run.cBest||0)).toFixed(1),combo_avg:run.cG?+(run.cW/run.cG).toFixed(2):1,combo_bonks:run.cBonk||0,combo_fades:run.cFade||0,pct:Math.round(R2.pct),")
# 6. Bots: link-preview and deployment-screenshot browsers (headless Chrome, 1280x800, UTC) were counted as players.
# Like posthog-js does by default, don't send anything from automated browsers or known bot user agents.
rep("function phOn(){return !TEST_MODE&&!save.noTrack&&typeof fetch==='function';}",
    "const PH_BOT=(()=>{try{return !!navigator.webdriver||/headless|googlebot|bingbot|twitterbot|slackbot|discordbot|telegrambot|linkedinbot|applebot|duckduckbot|yandexbot|petalbot|semrushbot|ahrefsbot|baiduspider|crawl|spider|slurp|facebookexternalhit|embedly|skypeuripreview|vercel|screenshot|lighthouse|pagespeed|prerender|phantomjs|puppeteer|playwright/i.test(navigator.userAgent||'');}catch(e){return false;}})();\n"
    "function phOn(){return !TEST_MODE&&!PH_BOT&&!save.noTrack&&typeof fetch==='function';}")
open(f,'w',encoding='utf-8').write(s)
print('p117 long game: ice palace 20, winter at -%d stars, idle 6h/12h, combo analytics, bot filter'%WINTER_SLACK)
