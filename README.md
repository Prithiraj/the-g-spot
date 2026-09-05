# The G Spot.

**Roadside character. Editorial polish.** A custom, photo-led static website design for The G Spot. in Lake Wales, Florida.

**Intended Pages address:** https://prithiraj.github.io/the-g-spot/  
**Release type:** Independent design preview, not an owner-approved official business website.

## Design & documentation

The maintained [17-part design plan](docs/PLAN.md), [research baseline](docs/RESEARCH.md), [photography rights register](docs/IMAGE-RIGHTS.md), and [deployment / launch checklist](docs/LAUNCH.md) are documented in Markdown.

The design pairs oversized roadside-style type with charcoal, warm paper and amber, actual venue photography, an asymmetric gallery and direct Directions/Call actions. No generic template, WebGL scene, fabricated menu, invented rating or recurring event schedule. Three.js was considered and omitted because the real venue imagery is the story.

## Stack

Semantic static HTML, custom CSS and a small progressive-enhancement JavaScript file. No runtime framework or package dependency. A Python build creates responsive WebP/JPEG images, self-hosted licensed font subsets and an original typographic Open Graph image. Chromium/Playwright and axe-core run at build time, not in the public app.

## Build

```sh
python -m pip install -r requirements-dev.txt
python scripts/build.py
python -m http.server 8000 --directory dist
```

The first build requires internet access for source assets. Later builds can use `--offline`. `python scripts/build.py --production` intentionally refuses the uncleared commercial release.

## Deployment

The GitHub Actions workflow builds and tests pushes to `main`, prepares `site-release`, and maintains `gh-pages` once activated. See [LAUNCH.md](docs/LAUNCH.md) for one-time Pages source settings and how to verify deployment. Build/QA results and screenshots are available in the workflow artifact and the published `/verification/` directory after a successful build.

## Honest content & image status

Real frontage, interior and patio photos are used as visibly marked demo/review references. No commercial photo permissions have been verified. Owner-controlled photographer-authorized originals are required before commercial launch. Preview noindex, visible provenance notes and a production build gate remain in place. Exact hours stay “Call for current hours” because public sources conflict. No fake products, testimonials, staff, policy guarantees or live availability.

## Project structure

```text
site/                 Static source and original interface graphics
content/assets.json   Photo provenance and approval state
scripts/build.py      Asset optimization and preview build
scripts/test-site.py  Responsive / accessibility / interaction QA
docs/                 Maintained Markdown plan, evidence, rights and handover
.github/workflows/    Research inspection and verified preview publishing
```
