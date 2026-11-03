# Portfolio CSS Structure

HTML owns document structure and meaning. All presentation belongs in external CSS.

**HTML requirements**
- No `<style>` elements.
- No `style=""` attributes.
- Keep the document limited to semantic markup, classes, and stylesheet links.

## Stylesheet entry points

Each page loads its original page stylesheet:

| Document | Stylesheets |
| --- | --- |
| `index.html` | `pages/index.css`, then `pages/index-layout.css` |
| `outputs.html` | `pages/outputs.css` |
| Project overview | Its matching `pages/StellaName.css` |
| Technical review | Its matching `pages/StellaName-Technical.css` |

Do not add a separate `css/main.css` link to a page stylesheet that already imports it.

## Shared CSS

- `tokens.css` contains the shared design tokens.
- `components.css` contains reusable presentation utilities.
- `pages/page-system.css` contains shared project-page and gallery styling.
- `design-overrides.css` contains the established visual refinements used by the page stylesheets.
- `main.css` imports the shared tokens, components, and page system.

The page-level stylesheets import the shared foundation they need. `index-layout.css` is loaded after `index.css` to control the homepage layout.

## Change rules

- Put shared rules in the existing shared stylesheets.
- Put project-specific rules in that project's stylesheet.
- Keep page-specific markup changes separate from visual styling.
- Preserve the established appearance. A CSS extraction or maintenance pass should not redesign the page.
- Before committing, confirm every local stylesheet link and CSS import resolves, and verify that every HTML page contains no style block or style attribute.
