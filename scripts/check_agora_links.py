#!/usr/bin/env python3
"""Read-only Agora draft links; pending evidence is not falsely marked live."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json,urllib.request
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--require-published',action='store_true');a=p.parse_args()
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=set()
 def handle_starttag(self,tag,attrs):
  url=dict(attrs).get('href','')
  if tag=='a' and url.startswith('https://github.com/'):self.urls.add(url)
h=Links();h.feed((R/'public/sites/agora/index.html').read_text())
for url in sorted(h.urls):
 if '/nift-experiments/lab-evidence/' in url and not a.require_published:
  print('PENDING PUBLICATION:',url);continue
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Nift-Labs-link-check'}),timeout=20) as response:
  assert response.status==200,url;response.read(128);print('PASS:',url)
print('Link checks complete; no deployment. Use --require-published after approved evidence release.')
