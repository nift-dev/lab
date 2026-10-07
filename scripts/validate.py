"""Audit generated local links, fragments, assets, metadata, and palette literals."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import colorsys
import re

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
errors = []

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.refs, self.ids, self.meta = path, [], set(), {}
        self.title = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for field in ('href', 'src'):
            if field in attrs:
                self.refs.append(attrs[field])
        if tag == 'meta':
            self.meta[attrs.get('name')] = attrs.get('content')
        if tag == 'title':
            self.title = True

pages = {}
for path in PUBLIC.rglob('*.html'):
    page = Page(path)
    page.feed(path.read_text())
    pages[path.resolve()] = page
    if not page.title or not page.meta.get('viewport'):
        errors.append(f'{path}: missing title or viewport')
    if page.meta.get('color-scheme') != 'dark':
        errors.append(f'{path}: dark color-scheme metadata missing')
    if re.search(r'["\']/(?:cloudflare-docs|omarchy)/', path.read_text()):
        errors.append(f'{path}: stale experiment URL')
    if '@path(' in path.read_text() or '@paginate' in path.read_text():
        errors.append(f'{path}: unresolved template syntax')

references = 0
for path, page in pages.items():
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        references += 1
        target = ((PUBLIC / unquote(url.path.lstrip('/'))) if url.path.startswith('/')
                  else path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target /= 'index.html'
        if not target.exists():
            errors.append(f'{path.relative_to(PUBLIC)}: missing {ref}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{path.relative_to(PUBLIC)}: missing fragment {ref}')

for slug in ('cloudflare-docs', 'omarchy'):
    if (PUBLIC / slug).exists():
        errors.append(f'stale output directory: {slug}')
for route in ('index.html', 'sites/index.html', 'sites/cloudflare-docs/index.html', 'sites/omarchy/index.html', 'sites/capgo/index.html', 'benchmarks/index.html', 'benchmarks/scripting/index.html', 'benchmarks/website-generator/index.html', 'benchmarks/shell/index.html'):
    if not (PUBLIC / route).is_file():
        errors.append(f'missing route: {route}')

for path in PUBLIC.rglob('*.css'):
    css = path.read_text()
    if not css:
        continue
    if 'color-scheme:dark' not in css.replace(' ', ''):
        errors.append(f'{path}: missing dark color scheme')
    if re.search(r'\b(?:blue|navy|cyan|teal|aqua|skyblue|royalblue|dodgerblue)\b', css, re.I):
        errors.append(f'{path}: blue palette keyword')
    colors = re.findall(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', css)
    rgb_values = []
    for value in colors:
        if len(value) == 3:
            value = ''.join(c * 2 for c in value)
        rgb_values.append(tuple(int(value[i:i+2], 16) / 255 for i in (0, 2, 4)))
    for match in re.finditer(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', css):
        rgb_values.append(tuple(int(x) / 255 for x in match.groups()))
    for rgb in rgb_values:
        hue, saturation, _ = colorsys.rgb_to_hsv(*rgb)
        if saturation > .15 and 170 <= hue * 360 <= 260:
            errors.append(f'{path}: blue-family palette color {rgb}')
    for ref in re.findall(r'url\([\"\']?([^\)\"\']+)', css):
        if not urlsplit(ref).scheme and not (path.parent / ref).exists():
            errors.append(f'{path}: missing CSS asset {ref}')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML pages, {references} local references; routes, fragments, metadata, assets, and dark/no-blue CSS palette literals.')
