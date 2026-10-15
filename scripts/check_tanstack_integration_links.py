#!/usr/bin/env python3
"""Read-only validation of the new report's pinned repository/evidence links."""
from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
import urllib.request
R=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=set()
 def handle_starttag(self,tag,attrs):
  u=dict(attrs).get('href','')
  if tag=='a' and u.startswith('https://github.com/'):self.urls.add(u)
h=Links();h.feed((R/'public/integrations/tanstack/index.html').read_text())
def check(u):
 with urllib.request.urlopen(urllib.request.Request(u,method='HEAD',headers={'User-Agent':'Nift-Labs-local-review'}),timeout=30) as r:
  assert r.status==200,(u,r.status)
 return u
with ThreadPoolExecutor(max_workers=4) as pool:
 for u in pool.map(check,sorted(h.urls)):print('PASS',u,flush=True)
print(f'{len(h.urls)} repository/evidence links verified. Read-only; no deployment.')
