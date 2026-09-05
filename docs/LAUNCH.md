# Deployment & commercial launch

## GitHub Pages deployment

**URL:** https://prithiraj.github.io/the-g-spot/  
**Hosting:** GitHub Pages, published by the repository's custom GitHub Actions workflow.  
**Release type:** Independent noindex website design preview.

The source of truth is `main`. Pages was already enabled when inspected. The workflow builds responsive images and licensed font subsets, checks the app in Chromium/axe, uploads the verified static artifact with `actions/upload-pages-artifact`, and publishes it using `actions/deploy-pages` in the `github-pages` environment. No release-branch duplication, personal access token, secret in source code, or force push is needed.

A separate `verify-live` job checks the public URL, its exact committed revision, three venue images, scripts, fonts, sharing image and documentation. **A successful build alone is not a deployment confirmation.** Require both deploy and verify-live to pass. The live response evidence is stored as the `live-deployment-verification` artifact; the generated browser checks report is served at `/verification/REPORT.md`.

For future hosting setup, Settings → Pages → Build and deployment → Source must be **GitHub Actions**. No custom domain is configured by this implementation. The initial branch-based fallback plan was replaced after confirming this repository already had Pages enabled.

## Local development

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/build.py
python -m http.server 8000 --directory dist
```

The build downloads the actual reference photographs and two open-license typefaces once into `.cache/`. `--offline` uses cached source assets. Public visitors never contact photo aggregators or font providers on page load.

For QA, install Chromium with `python -m playwright install chromium`; download the pinned axe-core bundle to `.cache/axe.min.js` as shown in the workflow; run `python scripts/test-site.py`. Tests exercise `/the-g-spot/`, not only a domain root. On hosts with an installed Chromium, set `PLAYWRIGHT_CHROMIUM_EXECUTABLE=/usr/bin/chromium`.

## Commercial readiness — outstanding

- [ ] Business owner authorizes the official identity and site.
- [ ] Photographer permissions/consents are recorded, or all three reference photos are replaced.
- [ ] Owner confirms hours, current drinks/food offering and any published amenities.
- [ ] Canonical social page, contact destinations and logo treatment are approved.
- [ ] Screen-reader and physical-device tests complete.
- [ ] Final metadata, verified operational JSON-LD and domain are approved.
- [ ] Preview disclosure / noindex changed only after the above approval.
- [ ] Production robots and sitemap configured for the actual hosting/domain arrangement.
- [ ] A responsible person is assigned to maintain business information.

`python scripts/build.py --production` currently fails on purpose. A published preview does not mean this checklist is complete. The current build does not claim full WCAG certification, measured real-user Core Web Vitals, a verified food menu, or commercially licensed review-platform photos.

## Editing content

`site/index.html` contains the actual static content and essential links. `site/assets/styles.css` defines the responsive design tokens and layouts. The small touch-target/sticky-focus refinements are in the homepage head. `site/assets/app.js` adds the optional image viewer, active-anchor indication and clipboard action. `content/assets.json` holds image sources and approval flags. Update `site/credits.html` and the Markdown rights register when sources change. Do not add hours or menu data only to structured data while visible content remains inconsistent.

## Privacy

No analytics, tracking pixel, map iframe, social-feed widget, newsletter form, cookie banner or account system is installed. Any later addition needs a real operational purpose and an appropriate policy. GitHub hosting may process technical request information under its own policies.
