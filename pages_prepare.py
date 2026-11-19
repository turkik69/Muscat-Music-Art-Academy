"""Rewrite the generated root-site build for a GitHub Pages project path."""
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

from build import BASE

target = os.getenv("GH_PAGES_BASE", "https://turkik69.github.io/Muscat-Music-Art-Academy").rstrip("/")
parts = urlsplit(target)
if parts.scheme != "https" or not parts.netloc or not parts.path.startswith("/"):
    raise ValueError("GH_PAGES_BASE must be an HTTPS URL with a project path")
prefix = parts.path.rstrip("/")
dist = Path(__file__).parent / "dist"

for page in dist.rglob("*.html"):
    content = page.read_text(encoding="utf-8").replace(BASE, target)
    content = content.replace('href="/', f'href="{prefix}/').replace('src="/', f'src="{prefix}/')
    page.write_text(content, encoding="utf-8")

css = dist / "styles.css"
css.write_text(css.read_text(encoding="utf-8").replace("url('/", f"url('{prefix}/"), encoding="utf-8")
for filename in ("sitemap.xml", "robots.txt"):
    file = dist / filename
    file.write_text(file.read_text(encoding="utf-8").replace(BASE, target), encoding="utf-8")

manifest = dist / "manifest.webmanifest"
data = json.loads(manifest.read_text(encoding="utf-8"))
data["id"] = data["start_url"] = data["scope"] = prefix + "/"
for icon in data["icons"]:
    icon["src"] = prefix + icon["src"]
manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
