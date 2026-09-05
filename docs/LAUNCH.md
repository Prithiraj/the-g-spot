# Deployment & commercial launch

## This deployment

An independent website design preview is prepared for https://prithiraj.github.io/the-g-spot/. Do not describe the site as live merely because a branch or workflow exists: verify a successful Pages deployment and a matching HTTP response.

The source of truth is `main`. The build workflow generates optimized assets, runs Chromium/axe checks, stores QA artifacts, and commits only static build output to `site-release`. The existing `.gitignore` and source files are preserved.

Initial Pages setup uses a `gh-pages` branch based on the verified `site-release` commit. In repository Settings → Pages, the publishing source must be **Deploy from a branch → gh-pages → /(root)**. Subsequent successful source builds fast-forward both release branches and request a Pages build. No force pushes and no personal access token in source files. GitHub's normal source-selection administration permission is separate from content write permission.

If the connector cannot activate Pages and no automatic activation occurs, the repository administrator must save that one-time source setting. The prepared app and release branch remain intact. Do not imply activation has occurred until confirmed.

## Local development

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/build.py
python -m http.server 8000 --directory dist
```

Build downloads actual reference photographs and the two open-license typefaces once into `.cache/`. `--offline` uses the cached source assets. The public site never contacts photo aggregators or font providers on page load.

For QA, install Chromium with `python -m playwright install chromium`; download the pinned axe-core bundle to `.cache/axe.min.js` as shown in the workflow; run `python scripts/test-site.py`. QA exercises `/the-g-spot/`, not only a domain root. On hosts with an installed Chromium, set `PLAYWRIGHT_CHROMIUM_EXECUTABLE=/usr/bin/chromium`.

## Commercial readiness — intentionally unresolved

- [ ] Business owner authorizes the official identity and site.
- [ ] Photographer permissions/consents are recorded, or all three reference photos are replaced.
- [ ] Owner confirms hours, current drinks/food offering and any published amenities.
- [ ] Canonical social page, contact destinations and logo treatment are approved.
- [ ] Screen-reader and physical-device tests complete.
- [ ] Final metadata, verified operational JSON-LD and domain are approved.
- [ ] Preview disclosure / noindex changed only after the above approval.
- [ ] Production robots and sitemap configured for the actual hosting/domain arrangement.
- [ ] A responsible person is assigned to maintain business information.

`python scripts/build.py --production` currently fails on purpose. A published preview is not an assertion that this checklist is complete. The current build never claims a full WCAG certification, measured real-user Core Web Vitals, a verified food menu, or commercially licensed review-platform photos.

## Editing content

`site/index.html` contains the actual static content and essential links. `site/assets/styles.css` defines all responsive design tokens/layouts. `site/assets/app.js` adds the optional image viewer, active-anchor indication and clipboard action. `content/assets.json` holds image sources and approval flags. Update `site/credits.html` and the Markdown rights register when sources change. Do not add hours or menu data only to structured data while leaving visible content inconsistent.

## Privacy

No analytics, tracking pixel, map iframe, social-feed widget, newsletter form, cookie banner or account system is installed. Any later addition needs a real operational purpose and an appropriate policy. GitHub hosting may process technical request information under its own policies.
