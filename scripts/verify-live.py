"""Verify GitHub Pages is actually serving this exact revision and its assets."""
from __future__ import annotations
import json, os, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path
BASE=os.environ.get('SITE_URL','https://prithiraj.github.io/the-g-spot/').rstrip('/')+'/'
EXPECTED=os.environ.get('EXPECTED_SHA',os.environ.get('GITHUB_SHA',''))
checks=[]
def get(path):
    url=BASE+path+'?verify='+str(time.time_ns())
    req=urllib.request.Request(url,headers={'User-Agent':'The-G-Spot-deployment-check'})
    with urllib.request.urlopen(req,timeout=25) as response:
        return response.status,response.read()
try:
    for attempt in range(12):
        try:
            status,data=get('revision.json')
            revision=json.loads(data)['commit']
            if status==200 and revision==EXPECTED: break
        except Exception as error:
            revision=str(error)
        if attempt==11: raise RuntimeError('Live revision did not match: '+revision)
        time.sleep(10)
    checks.append({'path':'revision.json','status':200,'commit':revision,'matches_expected':True})
    for path in ['', 'credits.html','assets/styles.css','assets/app.js','assets/images/frontage-800.webp','assets/images/interior-1200.webp','assets/images/patio-800.webp','assets/fonts/barlow-condensed.woff2','assets/fonts/source-sans.woff2','assets/social-card.png','documentation/PLAN.md','verification/REPORT.md']:
        status,data=get(path)
        if status!=200 or not data: raise RuntimeError('Missing live asset: '+path)
        if path=='':
            html=data.decode('utf-8')
            assert 'A LITTLE' in html and 'tel:+18639494243' in html and 'noindex' in html and '3825 N Scenic Hwy' in html
        checks.append({'path':path or '/','status':status,'bytes':len(data)})
    result={'success':True,'site_url':BASE,'commit':revision,'verified_at':datetime.now(timezone.utc).isoformat(),'checks':checks}
except Exception as error:
    result={'success':False,'site_url':BASE,'expected_commit':EXPECTED,'error':str(error),'checks':checks}
Path('live-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if not result['success']: raise SystemExit('Live deployment verification failed.')
