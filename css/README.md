# Portfolio CSS Architecture

HTML is structure and meaning only. **Zero CSS is permitted in HTML.** This is a release requirement:

- No `<style>` elements.
- No `style` attributes.
- No CSS embedded in HTML comments, scripts, or data attributes.
- No SVG presentation attributes such as `fill`, `stroke`, or `opacity`; keep SVG geometry and accessibility attributes in markup, but move presentation into CSS.
- Presentation belongs in external stylesheets and semantic classes.
- Use page-scoped classes for page-specific visual treatments; use IDs only for genuine unique targets such as in-page anchors or script hooks.

## Stylesheet layers

Every document loads `css/main.css` once. It is the shared entry point and imports:

1. `tokens.css` — design tokens and CSS custom properties.
2. `base.css` — global reset and element defaults.
3. `components.css` — reusable component variants and utilities.
4. `layout.css` — shared layout primitives and global composition.
5. `pages/page-system.css` — shared project-page and gallery systems.

Page-family stylesheets are loaded after the shared entry point, only by documents that use them:

| Page family | Stylesheet | Responsibility |
| --- | --- | --- |
| Homepage | `pages/index.css`, `pages/index-layout.css` | Homepage-specific composition |
| Project overview | `pages/overview.css` | Shared project overview foundation and responsive layout |
| Technical review | `pages/technical.css` | Shared technical documentation foundation |
| Evidence gallery | `pages/outputs.css` | Gallery-specific presentation |

Each project page then loads its own stylesheet after its family stylesheet. These files contain only genuine project-specific variations and components.

## Page identity

Each document's `body` declares semantic scope classes:

- `page--home`
- `page--overview`
- `page--technical`
- `page--gallery`
- `project--{name}` for project identity

Shared page-family rules use these explicit classes. Do not infer page identity from DOM contents with structural selectors such as `:has()`.

## Conventions

- Keep colors, typography, and recurring dimensions in custom properties.
- Put global resets and element defaults in `base.css`, never in page stylesheets.
- Put reusable patterns and explicit variants in `components.css`.
- Keep shared page-family structure in its family stylesheet.
- Keep unique page composition in the relevant page stylesheet.
- Avoid duplicating selectors or using later overrides to patch earlier declarations.
- Prefer semantic classes and low-specificity selectors over broad element selectors or deeply nested selectors.
- Keep responsive and reduced-motion behavior beside the component or page family it affects.
- Preserve the established visual system; refactoring must not silently redesign a page.
- Keep the cascade ordered from tokens and base rules through shared components, layout, page-family rules, and finally page-specific rules.
- Use the existing page-family breakpoints as the shared responsive baseline; add a different breakpoint only when a component's actual layout requires it.

## Adding a page

1. Add `css/main.css` in the document head.
2. Add the appropriate page-family stylesheet.
3. Add one project stylesheet if the page needs unique presentation.
4. Add the correct page and project scope classes to `body`.
5. Keep all presentation in external CSS and verify the zero-CSS-in-HTML rule.
6. Run `python scripts/check-css-separation.py` before committing.
