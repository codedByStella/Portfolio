# Portfolio CSS Architecture

The HTML documents load one shared stylesheet entry point followed by one page stylesheet.

## Load order

`main.css` is the only shared entry point. It imports the shared layers in this order:

1. `tokens.css` — design tokens: colors, typography, and shared values.
2. `base.css` — global reset and element-level defaults.
3. `components.css` — reusable presentation utilities and component variants.
4. `layout.css` — shared page layout, spacing, and responsive composition.
5. `pages/page-system.css` — shared page-family layouts for project overviews, technical reviews, and the evidence gallery.

Each HTML page then loads its own stylesheet from `pages/`.

## Page stylesheets

Page stylesheets contain only page-specific composition and presentation. They must not import `main.css`, tokens, or shared layers. Shared CSS is loaded once by the HTML document.

## Hard separation-of-concerns rule

**HTML must contain zero CSS.** This is a release requirement, not a preference:

- No `<style>` elements.
- No `style` attributes, including dynamically meaningful presentation values.
- No CSS embedded in HTML comments, scripts, SVG markup, or data attributes as a styling workaround.
- All presentation must be expressed through external stylesheets and semantic classes. Use IDs only when an element genuinely needs a unique identifier, such as an in-page anchor or script hook.
- If a page needs a unique visual treatment, add a page-scoped class and define it in that page's stylesheet. Do not put the rule back into HTML.

This rule applies to every HTML document in the repository, including future pages.

## Conventions

- Keep colors, typography, and recurring dimensions in custom properties.
- Put global resets and element defaults in `base.css`, not in individual pages.
- Put reusable patterns and explicit variants in `components.css`.
- Put shared page-family layout and responsive behavior in the shared layout layers.
- Keep one-off page presentation in that page's stylesheet.
- Do not add inline presentation styles to HTML; create a semantic class and define it in the appropriate stylesheet.
- Avoid duplicating shared rules in page stylesheets. Extend a shared component with a modifier when a real variant is needed.
- Preserve the established visual system when changing structure. Refactoring should not silently redesign a page.
- Keep responsive behavior and reduced-motion handling alongside the component or layout they affect.

## Adding a page

1. Add the shared `css/main.css` link in the document head.
2. Add exactly one page stylesheet link after it.
3. Add page-specific rules under `css/pages/`.
4. Promote a rule into a shared layer only when it is genuinely reused.
