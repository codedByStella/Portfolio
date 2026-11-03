#!/usr/bin/env python3
"""Static security regression checks for the codedByStella portfolio."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CSP_MARKER = "default-src 'self'"
YOUTUBE_HOST = "www.youtube-nocookie.com"
SECRET_PATTERN = (
    r"(?i)(AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}"
    r"|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|sk_live_[0-9A-Za-z]{24,}"
    r"|-----BEGIN (?:RSA|EC|OPENSSH|DSA) PRIVATE KEY-----"
    r"|(?:api[_-]?key|client[_-]?secret|access[_-]?token|password)\\s*[:=]\\s*['\"][^'\"]{12,}['\"])"
)

class AuditParser(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.errors = []
        self.csp = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "content-security-policy":
            self.csp = CSP_MARKER in attrs.get("content", "")
        for key, value in attrs.items():
            if key.lower().startswith("on"):
                self.errors.append(f"inline event handler: {key}")
            if key.lower() in {"href", "src", "action", "formaction"} and value:
                if value.strip().lower().startswith("javascript:"):
                    self.errors.append(f"javascript URL in {key}")
        if tag == "script" and not attrs.get("src"):
            self.errors.append("inline script element")
        if tag == "style":
            self.errors.append("inline style element")
        if tag == "iframe":
            src = attrs.get("src", "")
            host = urlparse(src).hostname or ""
            if host.endswith("youtube.com") and host != YOUTUBE_HOST:
                self.errors.append(f"YouTube iframe must use {YOUTUBE_HOST}")
            if host == YOUTUBE_HOST:
                allowed = set(attrs.get("allow", "").lower().replace(";", " ").split())
                if not allowed.issubset({"encrypted-media", "picture-in-picture", "fullscreen"}):
                    self.errors.append("YouTube iframe has excessive permissions")
                if attrs.get("loading") != "lazy":
                    self.errors.append("YouTube iframe must lazy-load")
                if attrs.get("referrerpolicy") != "strict-origin-when-cross-origin":
                    self.errors.append("YouTube iframe must set a restrictive referrer policy")
        if tag == "a" and attrs.get("target", "").lower() == "_blank":
            rel = set(attrs.get("rel", "").lower().split())
            if "noopener" not in rel:
                self.errors.append("target=_blank link missing noopener noreferrer")

def scan_history():
    result = subprocess.run(
        ["git", "log", "--all", "--format=%H", "-G", SECRET_PATTERN, "--name-only", "--", "."],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        return ["Could not scan Git history; ensure checkout fetch-depth is 0"]
    matches = []
    for line in result.stdout.splitlines():
        value = line.strip()
        if not value or re.fullmatch(r"[0-9a-f]{40,64}", value):
            continue
        matches.append(value)
    return sorted(set(matches))

def main():
    failures = []
    pages = sorted(ROOT.glob("*.html"))
    if not pages:
        failures.append("No root HTML pages found")
    for path in pages:
        parser = AuditParser(path)
        try:
            parser.feed(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{path.name}: parse error: {exc}")
            continue
        if not parser.csp:
            parser.errors.append("missing restrictive CSP meta policy")
        failures.extend(f"{path.name}: {err}" for err in parser.errors)
    history_matches = scan_history()
    if history_matches:
        failures.append("Potential secret-like changes found in Git history (paths only): " + ", ".join(history_matches))
    if failures:
        print("\n".join(failures))
        return 1
    print(f"Security checks passed for {len(pages)} HTML pages.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
