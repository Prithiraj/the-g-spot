# The G Spot. — approved design & implementation plan

**Direction:** Roadside character. Editorial polish.  
**Approval:** The requester approved implementation and publication in `Prithiraj/the-g-spot` after reviewing the 17-part plan.  
**Primary actions:** Get Directions; Call the Bar.  
**Research:** September 2026.  
**Release status:** Independent design preview, not an owner-approved official site. Photography and operating-detail approval are outstanding.

This is the maintained implementation edition of the approved Markdown plan. The original research plan was delivered in the conversation as `the-g-spot-website-design-plan.md`.

## 1. Evidence baseline

The G Spot. is a bar at **3825 N Scenic Hwy, Lake Wales, FL 33898**. The corroborated phone is **(863) 949-4243**. The associated Facebook page is `Gspotlakewales`. Public visitor accounts describe motorcycles/biker character, a wooden bar and memorabilia, pool, a jukebox and a patio. The three inspected venue photographs visually support the exterior, interior and patio identity.

Hours conflict between public listings, so the site says **Call for current hours**. No verified current menu or prices were supplied. No numeric review badge, recurring event schedule, payment/parking/access policy or formal owner story is invented. The mixed Florida/South Carolina menu aggregator is excluded. See [RESEARCH.md](RESEARCH.md).

## 2. Audience

Local regulars needing fast contact information; motorcycle riders and small adult social groups checking atmosphere; Maps visitors needing immediate identity and arrival clarity. These are design hypotheses, not measured demographics. The name is always contextualized by Lake Wales and the bar's actual address.

## 3. Conversion goals

Directions is the leading action in the header, hero, location panel, closing section and mobile quick-action bar. Call is the supporting action. Use the full address in Google Maps directions, the exact supplied place CID for Maps/reviews, and `tel:+18639494243`. Facebook updates and Google reviews are secondary outbound links. No bookings, orders, email capture or tracking without an actual service and approval.

## 4. Creative direction

Warm roadside/editorial rather than an upscale cocktail-bar template: oversized condensed type, charcoal backgrounds, cream paper sections, amber accents, a real frontage photograph and three authentic venue images. Strong section rhythm; purposeful rules and small wayfinding labels. Custom type treatment is a proposal, not a confirmed official logo. No fictional heritage date, stock motorcycles, generated premises, velvet ropes or theme-park biker styling.

The nearby official sites for Cherry Pocket and The Crooked Bass illustrate the value of clear visit information, but this preview does not copy their restaurant menus, events or destination breadth.

## 5. Color system

| Token | Hex | Use |
|---|---|---|
| Roadside charcoal | `#181916` | Header, hero, gallery, footer |
| Warm paper | `#F4EAD7` | Light sections and light-on-dark text |
| Amber | `#D9A441` | Calls to action and restrained highlights |
| Deep panel | `#242722` | Dark surfaces |
| Muted stone | `#B9BAAE` | Secondary dark-surface text |
| Cypress panel | `#252C25` | Decorative address/wayfinding panel |

Dark text is used on amber buttons. Contrast and focus states are tested, not assumed from the palette.

## 6. Typography

Barlow Condensed ExtraBold for headlines and the proposed wordmark. Source Sans 3 for body, controls and contact information. A small Georgia italic contrast creates editorial emphasis without an additional downloaded font. The two open-license families are downloaded during the build, subsetted to Latin/required symbols, and self-hosted with SIL OFL notices. Headings wrap and scale responsively.

## 7. Image strategy

Three real photographs: blue frontage with motorcycles, wooden bar/memorabilia, and the patio. No synthetic or unrelated venue photo. Hero prioritizes the exterior to make the place recognizable. Responsive WebP plus JPEG alternatives and explicit dimensions are generated at build time. The interior is cropped to concentrate on the bar rather than ceiling décor; no scene details are fabricated. Photographer permissions are unverified. See [IMAGE-RIGHTS.md](IMAGE-RIGHTS.md).

## 8. Information architecture

Single homepage: hero → introduction/three experience themes → real-photo gallery → Google reviews link → Facebook updates → location/contact/hours → final directions CTA → footer. A dedicated credits/notes page explains provenance and preview status. Unverified menu, food, team/history and event sections are omitted entirely.

## 9. Section-by-section layout

- **Header:** Proposed typographic identity, three visible anchor links, directions button. No JavaScript-dependent navigation.
- **Hero:** “A little offbeat. Right on Scenic.” Strong left-aligned poster type beside the actual frontage, direct actions and address; static scenic stamp.
- **Introduction:** Cream editorial section with atmosphere copy, glass/pool/patio icons and three restrained columns. A note identifies amenities as visitor-reported pending current confirmation.
- **Gallery:** Asymmetric three-image grid, captioned and source-linked; accessible progressive lightbox. Native image links work without JavaScript.
- **Social proof:** Link to the exact Google place, not a copied rating or fabricated review.
- **Updates:** Amber transition section linking to the associated Facebook page, with no invented calendar.
- **Visit:** Address, phone, call-for-hours state and directions. Highway-inspired address illustration is labeled decorative, not a real navigable map.
- **Close/footer:** Oversized final invitation and repeated visit/contact links. Visible independent-preview disclosure and credits.

## 10. Three.js / animation

Three.js is deliberately not used: it adds no useful business information to the photography-led experience. No WebGL, autoplay media, parallax, scroll hijacking or continuous motion. Refinement comes from short hover/focus transitions and optional smooth anchor scrolling. Reduced-motion preferences remove all decorative transitions and smooth scrolling. Content is never hidden waiting for JavaScript.

## 11. Responsive behavior

Mobile-first, verified from 320 px to 1920 px. Mobile hero copy and photograph stack; tablet gallery becomes a wide image plus two smaller images; desktop uses an asymmetric editorial grid. Mobile Directions/Call bar reserves safe-area and document space. Header anchors stay visible. No fragile fixed-height text containers.

## 12. Accessibility

Semantic HTML, one descriptive H1, skip link, named navigation, useful image alt text, keyboard-accessible native links/buttons and visible focus. Native modal dialog has Escape/arrow controls and focus restoration. Reduced-motion, forced-colors and print styles exist. Automated axe checks and manual browser interaction checks supplement—but do not constitute—a full WCAG 2.2 AA certification or screen-reader audit.

## 13. Performance

Static HTML/CSS/minimal JS. Zero runtime package dependencies or third-party embed requests. Prioritized responsive hero; lazy below-fold photography; self-hosted subset fonts; dimensions prevent image layout shifts. Targets: mobile hero under 200 KB, first-party compressed JS under 35 KB. Field LCP ≤2.5 s, INP ≤200 ms and CLS ≤0.1 remain post-launch goals, not claimed measurements.

## 14. SEO / local discovery

Descriptive title, meta description, canonical Pages URL, original typographic social card and appropriately limited JSON-LD. The preview `WebPage` is about a `BarOrPub`; it is not declared the business's official URL. Name/address/phone/geo are consistent. No unconfirmed hours, ratings, prices or menu structured data. Preview `noindex,nofollow` remains until formal commercial sign-off. A project-subpath robots file does not control the host root; HTML noindex is the important safeguard.

## 15. Rights / licensing

No photograph is claimed to be commercially licensed. All three are marked reference-only in the asset manifest, visible gallery note, hero source link, dedicated credits page and documentation. The published artifact is an **independent design preview**, not the commercial release envisioned by the original launch acceptance criterion. This preview/commercial distinction is an explicit implementation limitation, not a claim that credit grants permission. A commercial build is blocked; obtain owner-controlled, photographer-authorized assets before commercial launch. Original graphics and licensed fonts are handled separately.

## 16. Implementation sequence

1. Read the existing repository and approved plan; preserve original starter files.
2. Inspect real venue photographs and document evidence/rights.
3. Build semantic static source, custom visual system and progressive enhancements.
4. Generate responsive assets and self-hosted fonts; enforce commercial-clearance gate.
5. Run browser/axe/subpath/no-JS/reduced-motion/mobile checks and inspect screenshots.
6. Commit maintained Markdown documentation; prepare verified static release branch.
7. Publish the preview on GitHub Pages and verify actual deployment status.
8. Report any activation or commercial-approval blocker precisely.

## 17. Acceptance criteria

Recognizable actual business imagery; accurate contact destinations; obvious mobile actions; no fabricated operational content; working gallery and source notes; zero horizontal overflow at tested widths; no broken asset links; no uncaught JS errors; no serious automated accessibility failures; functional no-JS fallback; production gate blocks uncleared release; deployment status evidenced by GitHub workflow and live response. Physical-device, screen-reader, owner sign-off and field-performance checks remain explicit handover items.

## Maintenance

See [LAUNCH.md](LAUNCH.md) for deployment and commercial-readiness steps, [RESEARCH.md](RESEARCH.md) for evidence, and [IMAGE-RIGHTS.md](IMAGE-RIGHTS.md) for photography provenance. The website is intentionally small enough to edit without introducing a CMS.
