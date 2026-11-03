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
