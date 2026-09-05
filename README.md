# The G Spot.

**Roadside character. Editorial polish.** A custom, photo-led static website design for The G Spot. in Lake Wales, Florida.

**GitHub Pages:** https://prithiraj.github.io/the-g-spot/  
**Release type:** Independent design preview, not an owner-approved official business website.  
**Deployment evidence:** Require the `deploy` and `verify-live` jobs to pass in [the publishing workflow](https://github.com/Prithiraj/the-g-spot/actions/workflows/pages.yml).

## Design & documentation

The maintained [17-part design plan](docs/PLAN.md), [research baseline](docs/RESEARCH.md), [photography rights register](docs/IMAGE-RIGHTS.md), and [deployment / launch checklist](docs/LAUNCH.md) are documented in Markdown.

The design pairs oversized roadside-style type with charcoal, warm paper and amber, actual venue photography, an asymmetric gallery and direct Directions/Call actions. No generic template, WebGL scene, fabricated menu, invented rating or recurring event schedule. Three.js was considered and omitted because real venue imagery is the story.

## Stack

Semantic static HTML, custom CSS and a small progressive-enhancement JavaScript file. No runtime framework or package dependency. A Python build creates responsive WebP/JPEG images, self-hosted licensed font subsets and an original typographic Open Graph image. Chromium/Playwright and axe-core run at build time, not in the public app.

## Build

```sh
python -m pip install -r requirements-dev.txt
python scripts/build.py
python -m http.server 8000 --directory dist
```

The first build requires internet access for source assets. Later builds can use `--offline`. `python scripts/build.py --production` intentionally refuses the uncleared commercial release.

## Deployment & verification

Pushes to `main` build and test the app, publish the static artifact through GitHub's official Pages actions, and verify the live revision and assets. This repository already has Pages enabled. See [LAUNCH.md](docs/LAUNCH.md) for setup and verification details. No separate release branch or third-party hosting account is required.

Build results and screenshots are available in the workflow artifact. The browser-check report is published at `/verification/REPORT.md`; a separate artifact records live HTTP checks. The first browser run caught small mobile footer links; those targets were enlarged before release.

## Honest content & image status

Real frontage, interior and patio photos are visibly marked demo/review references. Commercial photo permissions have not been verified. Owner-controlled photographer-authorized originals are required before commercial launch. Preview noindex, visible provenance notes and a production build gate remain in place. Exact hours stay “Call for current hours” because public sources conflict. No fake products, testimonials, staff, policy guarantees or live availability.

## Project structure

```text
site/                  Static source and original interface graphics
content/assets.json    Photo provenance and approval state
scripts/build.py       Asset optimization and preview build
scripts/test-site.py   Responsive / accessibility / interaction QA
scripts/verify-live.py Deployed-revision and public-asset checks
docs/                  Markdown plan, evidence, rights and handover
.github/workflows/     Research inspection and verified Pages publishing
```
