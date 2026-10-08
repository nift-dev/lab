"""Audit external GitHub hrefs across every published report, read-only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,quote
from concurrent.futures import ThreadPoolExecutor
import subprocess,json
R=Path(__file__).resolve().parents[1];ledger=json.loads((R/'investigation/incremental-memory-audit.json').read_text());links=set()
class P(HTMLParser):
 def handle_starttag(self,t,a):
  h=dict(a).get('href','')
  if t=='a' and h.startswith('https://github.com/'):links.add(h)
for report in ledger['reports']:
 p=R/'public'/urlsplit(report['report_url']).path.lstrip('/')/'index.html';parser=P();parser.feed(p.read_text())
def check(u):
 parts=urlsplit(u).path.strip('/').split('/');ep='repos/'+parts[0]+'/'+parts[1]
 if len(parts)>2 and parts[2] in ['tree','blob']:
  ep+=('/contents/'+quote('/'.join(parts[4:]),safe='/')+'?ref='+quote(parts[3],safe='')) if len(parts)>4 else '/commits/'+quote(parts[3],safe='')
 elif len(parts)>2:raise ValueError(u)
 p=subprocess.run(['gh','api',ep],capture_output=True,text=True)
 if p.returncode:return {'url':u,'endpoint':ep,'valid':False,'error':p.stderr[:250]}
 d=json.loads(p.stdout);return {'url':u,'endpoint':ep,'valid':True,'sha':d.get('sha') if isinstance(d,dict) else None}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(check,sorted(links)))
(R/'docs/incremental-memory-external-link-validation.json').write_text(json.dumps(results,indent=2)+'\n')
bad=[r for r in results if not r['valid']];print('Verified',len(results),'external repository/evidence references; failures',len(bad));assert not bad,bad
