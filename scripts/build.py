"""Build the static preview, optimized venue photography and self-hosted fonts.
Usage: python scripts/build.py [--offline] [--production]
Original images are cached outside the public output. Production is clearance-gated.
"""
from __future__ import annotations
import argparse, hashlib, io, json, shutil, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from fontTools import subset
from fontTools.ttLib import TTFont
ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / '.cache'
DIST = ROOT / 'dist'
MAX_DOWNLOAD = 16 * 1024 * 1024

def acquire(url: str, target: Path, offline: bool) -> Path:
    if target.exists() and target.stat().st_size:
        return target
    if offline:
        raise RuntimeError(f'Offline build needs cached asset: {target.name}')
    target.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (The-G-Spot-design-preview)'})
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if not data or len(data) > MAX_DOWNLOAD:
        raise ValueError(f'Unexpected asset size: {target.name}')
    target.write_bytes(data)
    return target

def make_font(source: Path, target: Path) -> None:
    options = subset.Options()
    options.flavor = 'woff2'
    font = TTFont(source)
    sub = subset.Subsetter(options=options)
    sub.populate(unicodes=list(range(0x20, 0x250)) + list(range(0x1e00, 0x1f00)) + list(range(0x2000, 0x2070)) + list(range(0x2190, 0x2200)))
    sub.subset(font)
    font.flavor = 'woff2'
    font.save(target)

def build() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--production', action='store_true')
    args = parser.parse_args()
    config = json.loads((ROOT / 'content/assets.json').read_text())
    if args.production:
        required = ('photography_cleared', 'operations_confirmed', 'official_site_authorized')
        missing = [key for key in required if not config.get(key)]
        if missing or any('unverified' in image.get('rights', '').lower() for image in config['photos']):
            raise SystemExit('Commercial launch blocked. Resolve documented approvals: ' + ', '.join(missing))
        raise SystemExit('Approvals recorded. Complete the production checklist in docs/LAUNCH.md and explicitly update preview metadata before enabling a production build.')
    if DIST.exists(): shutil.rmtree(DIST)
    shutil.copytree(ROOT / 'site', DIST)
    images = DIST / 'assets/images'; images.mkdir(parents=True, exist_ok=True)
    fonts = DIST / 'assets/fonts'; fonts.mkdir(parents=True, exist_ok=True)
    manifest = {'mode':'independent-preview', 'photos':[], 'fonts':[]}
    for item in config['photos']:
        path = acquire(item['url'], CACHE / 'photos' / (item['id'] + '.jpg'), args.offline)
        with Image.open(path) as source:
            image = ImageOps.exif_transpose(source).convert('RGB')
        if image.width < 700 or image.height < 500:
            raise ValueError(f'Unexpectedly small source: {item["id"]}')
        crop = round(image.height * item.get('crop_top', 0))
        if crop: image = image.crop((0, crop, image.width, image.height))
        for bucket in (480, 800, 1200, 1600):
            width = min(bucket, image.width)
            resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
            resized.save(images / f'{item["id"]}-{bucket}.webp', quality=79, method=6)
            resized.save(images / f'{item["id"]}-{bucket}.jpg', quality=84, optimize=True, progressive=True)
        manifest['photos'].append({**item,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rendered_dimensions':image.size})
    raw = 'https://raw.githubusercontent.com/google/fonts/main/ofl/'
    font_specs = [
        ('barlow-condensed','barlowcondensed/BarlowCondensed-ExtraBold.ttf','barlowcondensed/OFL.txt'),
        ('source-sans','sourcesans3/SourceSans3%5Bwght%5D.ttf','sourcesans3/OFL.txt'),
    ]
    font_sources = {}
    for name, font_url, license_url in font_specs:
        source = acquire(raw + font_url, CACHE / 'fonts' / (name + '.ttf'), args.offline)
        license_file = acquire(raw + license_url, CACHE / 'fonts' / (name + '-OFL.txt'), args.offline)
        make_font(source, fonts / (name + '.woff2'))
        shutil.copy(license_file, fonts / (name + '-OFL.txt'))
        manifest['fonts'].append({'id':name,'source':raw+font_url,'license':'SIL Open Font License 1.1','sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
        font_sources[name] = source
    # Original typographic sharing image: no uncleared venue photography in metadata.
    card = Image.new('RGB',(1200,630),'#181916'); d=ImageDraw.Draw(card)
    display = lambda size: ImageFont.truetype(str(font_sources['barlow-condensed']), size)
    body = lambda size: ImageFont.truetype(str(font_sources['source-sans']), size)
    d.rectangle((45,40,1155,590),outline='#5d594d',width=1)
    d.text((80,66),'THE G SPOT.',font=display(45),fill='#f4ead7')
    d.text((80,151),'A LITTLE OFFBEAT.',font=display(105),fill='#f4ead7')
    d.text((80,266),'RIGHT ON SCENIC.',font=display(105),fill='#d9a441')
    d.line((83,414,1115,414),fill='#5d594d',width=1)
    d.text((83,444),'3825 N SCENIC HWY  /  LAKE WALES, FLORIDA',font=body(23),fill='#f4ead7')
    d.text((83,529),'INDEPENDENT WEBSITE DESIGN PREVIEW',font=body(17),fill='#b9baae')
    card.save(DIST / 'assets/social-card.png',optimize=True)
    (DIST / 'build-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    # Include only publicly appropriate maintenance notes, not research downloads.
    if (ROOT / 'docs').exists(): shutil.copytree(ROOT / 'docs', DIST / 'documentation')
    total=sum(p.stat().st_size for p in DIST.rglob('*') if p.is_file())
    print(f'Built {DIST.name}: {total/1024:.0f} KB total, including all responsive alternatives. Zero runtime package dependencies.')
    print('This is a noindex design preview. Commercial clearance remains blocked.')

if __name__ == '__main__': build()
