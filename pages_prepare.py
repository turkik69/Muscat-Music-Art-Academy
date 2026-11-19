"""Build branch-published GitHub Pages files at the repository root.

Usage: GH_PAGES_BASE=https://example.com/Muscat-Music-Art-Academy python3 pages_prepare.py
"""
import json
import os
import shutil
from pathlib import Path
from urllib.parse import urlsplit

from build import BASE  # also regenerates the private review build in dist/

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
TARGET = os.getenv('GH_PAGES_BASE', 'https://byyassmin.com/Muscat-Music-Art-Academy').rstrip('/')
parts = urlsplit(TARGET)
if parts.scheme != 'https' or not parts.netloc or not parts.path.startswith('/'):
    raise ValueError('GH_PAGES_BASE must be an HTTPS URL with a project path')
PREFIX = parts.path.rstrip('/')

for source in DIST.rglob('*'):
    if not source.is_file():
        continue
    relative = source.relative_to(DIST)
    dest = ROOT / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix == '.html':
        content = source.read_text(encoding='utf-8').replace(BASE, TARGET)
        content = content.replace('href="/', f'href="{PREFIX}/').replace('src="/', f'src="{PREFIX}/')
        dest.write_text(content, encoding='utf-8')
    elif relative.as_posix() == 'styles.css':
        dest.write_text(source.read_text(encoding='utf-8').replace("url('/", f"url('{PREFIX}/"), encoding='utf-8')
    elif relative.as_posix() in ('sitemap.xml', 'robots.txt'):
        dest.write_text(source.read_text(encoding='utf-8').replace(BASE, TARGET), encoding='utf-8')
    elif relative.as_posix() == 'manifest.webmanifest':
        data = json.loads(source.read_text(encoding='utf-8'))
        data['id'] = data['start_url'] = data['scope'] = PREFIX + '/'
        for icon in data['icons']:
            icon['src'] = PREFIX + icon['src']
        dest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    else:
        shutil.copy2(source, dest)
