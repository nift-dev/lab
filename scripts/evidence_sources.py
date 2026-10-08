"""Pinned evidence access for explicit report regeneration, never normal Nift builds.

Only compact rendering datasets live in Labs. Frozen raw data is SHA-checked in
canonical repositories and cached outside the checkout when a generator needs it.
"""
from pathlib import Path
import json,hashlib,urllib.request,re,shutil,tempfile
R=Path(__file__).resolve().parents[1]
INDEX=R/'content/data/evidence-sources.json'
def sources():return json.loads(INDEX.read_text())
def url(item):return f'https://github.com/{item["repo"]}/blob/{item["commit"]}/{item["path"]}'
def canonical_url(path):
 d=sources();key=str(path).replace('\\','/');key=key.removeprefix(str(R)+'/')
 return url(d['files'][key]) if key in d['files'] else None
def canonicalize_links(text):
 return re.sub(r"@(?:path|pathto)\((['\"])(public/[^'\"]+)\1\)",lambda m:canonical_url(m[2]) or m[0],text)
def data_root(prefix):
 """Materialize exact frozen maintenance inputs outside Labs, with verified hashes."""
 d=sources();cache=Path(tempfile.gettempdir())/('nift-labs-evidence-'+d['evidence_commit'])/prefix
 cache.mkdir(parents=True,exist_ok=True)
 for key,x in d['files'].items():
  if not key.startswith(prefix.rstrip('/')+'/'):continue
  destination=cache/key[len(prefix)+1:]
  if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest()==x['sha256']:continue
  local=R.parent/(('nift-experiments/lab-evidence' if x['repo']=='nift-experiments/lab-evidence' else x['repo']))/x['path']
  if local.exists() and hashlib.sha256(local.read_bytes()).hexdigest()==x['sha256']:b=local.read_bytes()
  else:b=urllib.request.urlopen(f'https://raw.githubusercontent.com/{x["repo"]}/{x["commit"]}/{x["path"]}',timeout=60).read()
  assert hashlib.sha256(b).hexdigest()==x['sha256'],key
  destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(b)
 localroot=R/prefix
 if localroot.exists():
  for p in localroot.rglob('*'):
   if p.is_file() and str(p.relative_to(R)) not in d['files']:
    dest=cache/p.relative_to(localroot);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 return cache
