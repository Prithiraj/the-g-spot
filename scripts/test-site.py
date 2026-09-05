"""Browser QA for the generated site at the actual GitHub Pages subpath.
python scripts/test-site.py
Optional PLAYWRIGHT_CHROMIUM_EXECUTABLE lets local QA use an installed Chromium.
"""
from __future__ import annotations
import functools, gzip, http.server, json, os, re, subprocess, tempfile, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'qa'; OUT.mkdir(exist_ok=True)
results=[]; failures=[]
def check(name, okay, details=''):
    results.append({'test':name,'passed':bool(okay),'details':details})
    if not okay: failures.append(name)
    print(('PASS' if okay else 'FAIL') + ': ' + name + (' — ' + str(details) if details else ''))
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
with tempfile.TemporaryDirectory() as tmp:
    (Path(tmp)/'the-g-spot').symlink_to(ROOT/'dist', target_is_directory=True)
    handler=functools.partial(QuietHandler,directory=tmp)
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f'http://127.0.0.1:{server.server_port}/the-g-spot/'
    with sync_playwright() as p:
        opts={'headless':True,'args':['--no-sandbox']}
        if os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE'): opts['executable_path']=os.environ['PLAYWRIGHT_CHROMIUM_EXECUTABLE']
        browser=p.chromium.launch(**opts)
        page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
        errors=[]; bad=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
        page.goto(url,wait_until='networkidle'); page.evaluate('document.fonts.ready')
        check('One descriptive H1',page.locator('h1').count()==1 and 'The G Spot.' in page.locator('h1').inner_text())
        check('Preview noindex disclosure', 'noindex' in page.locator('meta[name="robots"]').get_attribute('content') and page.locator('.preview-note').is_visible())
        schema=json.loads(page.locator('script[type="application/ld+json"]').text_content())
        business=next(v for v in schema['@graph'] if v['@type']=='BarOrPub')
        check('Accurate minimal business schema',business['telephone']=='+18639494243' and 'openingHours' not in business and 'aggregateRating' not in business)
        check('Directions target exact address',all('3825' in x for x in page.locator('a[href*="maps/dir"]').evaluate_all('(els)=>els.map(x=>x.href)')))
        check('Phone links match confirmed number',all(x=='tel:+18639494243' for x in page.locator('a[href^="tel:"]').evaluate_all('(els)=>els.map(x=>x.getAttribute("href"))')))
        check('No third-party embeds or runtime scripts',page.locator('iframe').count()==0 and page.locator('script[src^="http"]').count()==0)
        for w in [320,360,390,600,768,1024,1440,1920]:
            page.set_viewport_size({'width':w,'height':900})
            page.goto(url,wait_until='networkidle');page.evaluate('document.fonts.ready')
            overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
            check(f'{w}px has no horizontal overflow',not overflow)
            page.locator('#gallery').scroll_into_view_if_needed();page.wait_for_timeout(100)
            page.locator('#visit').scroll_into_view_if_needed();page.wait_for_timeout(100)
            image_errors=page.locator('main img').evaluate_all('(els)=>els.filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)')
            check(f'{w}px venue photos load',len(image_errors)==0,str(image_errors) if image_errors else '')
            page.evaluate('window.scrollTo({top:0,behavior:"instant"})');page.wait_for_timeout(100)
            if w in [390,768,1440]:
                page.screenshot(path=str(OUT/f'homepage-{w}.png'),full_page=True)
                page.screenshot(path=str(OUT/f'hero-{w}.png'))
        page.set_viewport_size({'width':390,'height':844}); page.goto(url,wait_until='networkidle')
        check('Mobile quick actions visible',page.locator('.mobile-actions').is_visible())
        first=page.locator('.gallery-trigger').first
        first.click();check('Gallery opens native dialog',page.locator('#lightbox').evaluate('(d)=>d.open'))
        check('Close control receives focus',page.locator('.lightbox-close').evaluate('(e)=>e===document.activeElement'))
        page.keyboard.press('ArrowRight');check('Gallery keyboard next',page.locator('#lightbox-count').inner_text()=='02 / 03')
        page.keyboard.press('ArrowLeft');check('Gallery keyboard previous',page.locator('#lightbox-count').inner_text()=='01 / 03')
        page.keyboard.press('Escape');check('Escape closes gallery and restores focus',not page.locator('#lightbox').evaluate('(d)=>d.open') and first.evaluate('(e)=>e===document.activeElement'))
        page.goto(url,wait_until='networkidle');page.keyboard.press('Tab')
        check('Skip link is first keyboard stop',page.locator('.skip-link').evaluate('(e)=>e===document.activeElement'))
        page.keyboard.press('Enter');check('Skip link reaches main',page.url.endswith('#main'))
        page.emulate_media(reduced_motion='reduce')
        check('Reduced motion disables smooth scrolling',page.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto')
        page.emulate_media(reduced_motion='no-preference')
        # Verify reflow with enlarged text without assuming automated audit equals full WCAG conformance.
        page.set_viewport_size({'width':390,'height':844});page.goto(url,wait_until='networkidle')
        page.add_style_tag(content='body{font-size:200% !important}')
        check('Enlarged base text does not cause page overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
        axe=ROOT/'.cache/axe.min.js'
        for w in [390,1440]:
            page.set_viewport_size({'width':w,'height':1000});page.goto(url,wait_until='networkidle')
            if axe.exists():
                page.add_script_tag(path=str(axe))
                audit=page.evaluate('''async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}})''')
                (OUT/f'axe-{w}.json').write_text(json.dumps(audit,indent=2))
                check(f'{w}px automated accessibility audit',not audit['violations'],', '.join(v['id'] for v in audit['violations']))
            else: check(f'{w}px automated accessibility audit available',False,'axe-core not downloaded')
        page.goto(url+'credits.html',wait_until='networkidle');check('Source/rights page loads at Pages subpath',page.locator('h1').count()==1 and page.locator('#photography').is_visible())
        check('No missing local resources',not bad,str(bad))
        check('No browser JavaScript errors',not errors,str(errors))
        page.close()
        context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
        nojs=context.new_page();nojs.goto(url,wait_until='networkidle')
        check('No-JS headline and contact work',nojs.locator('h1').is_visible() and nojs.locator('a[href="tel:+18639494243"]').count()>0)
        check('No-JS gallery has real image links',all(x.endswith('.jpg') for x in nojs.locator('.gallery-trigger').evaluate_all('(els)=>els.map(x=>x.href)')))
        check('No-JS hides unavailable clipboard control',not nojs.locator('.copy-address').is_visible())
        context.close();browser.close()
    server.shutdown()
js=(ROOT/'dist/assets/app.js').read_bytes()
check('First-party JS below 35 KB compressed',len(gzip.compress(js))<35000,f'{len(gzip.compress(js))} bytes gzip')
hero=(ROOT/'dist/assets/images/frontage-800.webp').stat().st_size
check('Mobile hero below 200 KB',hero<200000,f'{hero} bytes')
production=subprocess.run(['python',str(ROOT/'scripts/build.py'),'--production'],capture_output=True,text=True)
check('Uncleared commercial build is blocked',production.returncode!=0 and 'blocked' in (production.stderr+production.stdout).lower())
(OUT/'results.json').write_text(json.dumps(results,indent=2))
lines=['# Verification report','','Automated Chromium checks of this build. These results are not a blanket WCAG conformance claim or field Core Web Vitals measurement.','','| Check | Result | Details |','|---|---|---|']
for r in results: lines.append(f'| {r["test"]} | {"PASS" if r["passed"] else "FAIL"} | {str(r["details"]).replace("|","/")} |')
lines += ['','## Remaining human / field checks','','- Owner approval of current operations and photo licensing remains outstanding.','- Test on physical iOS/Safari and Android devices and with screen-reader software before commercial launch.','- Field LCP, INP and CLS require real traffic; none is claimed here.','- Validate live directions and telephone handling on an actual device; browser tests validate link targets, not an answered call.']
(OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
print(f'\n{len(results)-len(failures)}/{len(results)} checks passed.')
if failures: raise SystemExit('Failed checks: '+', '.join(failures))
