"""Read-only GitHub verification of every external link in the built AI SDK page."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, quote
from concurrent.futures import ThreadPoolExecutor
import json, subprocess

root=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=set()
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            href=dict(attrs).get('href','')
            if href.startswith('https://github.com/'): self.links.add(href)
parser=Links(); parser.feed((root/'public/sites/ai-sdk/index.html').read_text())
def check(url):
    parts=urlsplit(url).path.strip('/').split('/')
    endpoint='repos/'+parts[0]+'/'+parts[1]
    if len(parts)>2:
        if parts[2]=='blob':
            endpoint+='/contents/'+quote('/'.join(parts[4:]),safe='/')+'?ref='+parts[3]
        elif parts[2]=='tree': endpoint+='/git/commits/'+parts[3]
        else: raise ValueError(url)
    result=subprocess.run(['gh','api',endpoint],capture_output=True,text=True)
    if result.returncode: raise RuntimeError((url,result.stderr[:500]))
    data=json.loads(result.stdout)
    return {'url':url,'verified_api':endpoint,'status':200,'sha':data.get('sha'),'repository':data.get('full_name')}
with ThreadPoolExecutor(max_workers=4) as pool: records=list(pool.map(check,sorted(parser.links)))
assert len(records)>=19
(root/'docs/ai-sdk-link-validation.json').write_text(json.dumps({'scope':'Every external GitHub href in the generated report; read-only API existence verification','links':records},indent=2)+'\n')
print(f'PASS: {len(records)} repository/pinned evidence links verified through GitHub API.')
