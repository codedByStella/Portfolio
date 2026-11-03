#!/usr/bin/env python3
"""Validate the portfolio's HTML/CSS separation contract."""

from pathlib import Path
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
REFERENCED_CSS = set()


def local_path(url: str, base: Path) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = parsed.path.lstrip("/")
    return (base / path).resolve()


def check_css_balance(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    depth = 0
    index = 0
    quote = None
    while index < len(source):
        char = source[index]
        if quote:
            if char == "\\\\":
                index += 1
            elif char == quote:
                quote = None
        elif source.startswith("/*", index):
            end = source.find("*/", index + 2)
            if end == -1:
                ERRORS.append(f"{path.relative_to(ROOT)}: unclosed CSS comment")
                return
            index = end + 1
        elif char in ("'", '"'):
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                ERRORS.append(f"{path.relative_to(ROOT)}: unexpected closing brace")
                return
        index += 1

    if quote:
        ERRORS.append(f"{path.relative_to(ROOT)}: unclosed CSS string")
    if depth:
        ERRORS.append(f"{path.relative_to(ROOT)}: unbalanced CSS braces ({depth})")


html_files = sorted(ROOT.rglob("*.html"))
css_files = sorted((ROOT / "css").rglob("*.css"))

for html_path in html_files:
    source = html_path.read_text(encoding="utf-8")
    relative = html_path.relative_to(ROOT)

    if re.search(r"<\\s*style\\b", source, re.IGNORECASE):
        ERRORS.append(f"{relative}: inline <style> block found")
    if re.search(r"\\sstyle\\s*=", source, re.IGNORECASE):
        ERRORS.append(f"{relative}: inline style attribute found")

    body = re.search(r"<body\\b[^>]*>", source, re.IGNORECASE)
    body_tag = body.group(0) if body else ""
    classes_match = re.search(r'\\bclass=["\']([^"\']*)["\']', body_tag, re.IGNORECASE)
    classes = set(classes_match.group(1).split()) if classes_match else set()

    links = re.findall(r"<link\\b[^>]*>", source, re.IGNORECASE)
    local_stylesheets = set()
    for link in links:
        rel = re.search(r'\\brel=["\']([^"\']*)["\']', link, re.IGNORECASE)
        href = re.search(r'\\bhref=["\']([^"\']*)["\']', link, re.IGNORECASE)
        if not rel or "stylesheet" not in rel.group(1).lower().split() or not href:
            continue
        resolved = local_path(href.group(1), ROOT)
        if resolved is None:
            continue
        if not resolved.is_file():
            ERRORS.append(f"{relative}: stylesheet not found: {href.group(1)}")
            continue
        local_stylesheets.add(resolved)
        REFERENCED_CSS.add(resolved)

    main_css = (ROOT / "css" / "main.css").resolve()
    if main_css not in local_stylesheets:
        ERRORS.append(f"{relative}: css/main.css is not linked")

    required = {
        "page--home": {"css/pages/index.css", "css/pages/index-layout.css"},
        "page--overview": {"css/pages/overview.css"},
        "page--technical": {"css/pages/technical.css"},
        "page--gallery": {"css/pages/outputs.css"},
    }
    for page_class, stylesheets in required.items():
        if page_class in classes:
            for stylesheet in stylesheets:
                if (ROOT / stylesheet).resolve() not in local_stylesheets:
                    ERRORS.append(f"{relative}: {page_class} page must load {stylesheet}")

for css_path in css_files:
    check_css_balance(css_path)
    source = css_path.read_text(encoding="utf-8")
    for import_url in re.findall(r'@import\\s+(?:url\\()?["\']([^"\']+)["\']\\)?\\s*;', source, re.IGNORECASE):
        resolved = local_path(import_url, css_path.parent)
        if resolved is None:
            continue
        if not resolved.is_file():
            ERRORS.append(f"{css_path.relative_to(ROOT)}: imported stylesheet not found: {import_url}")
        else:
            REFERENCED_CSS.add(resolved)

orphaned = [path for path in css_files if path.resolve() not in REFERENCED_CSS]
for path in orphaned:
    ERRORS.append(f"{path.relative_to(ROOT)}: stylesheet is not linked or imported")

if ERRORS:
    print("CSS separation checks failed:")
    for error in ERRORS:
        print(f" - {error}")
    sys.exit(1)

print(
    f"CSS separation checks passed: {len(html_files)} HTML documents, "
    f"{len(css_files)} CSS files, no inline CSS, no missing/orphaned stylesheets."
)
