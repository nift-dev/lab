"""Conservative storage guard for tracked website source/publication, not Git history.

Canonical evidence pointers (content/data/evidence-sources.json) are an index/manifest,
not raw benchmark payloads; they receive a bounded allowance above the ordinary JSON cap.
Ordinary large JSON, raw benchmark payloads, archives and build/cache paths stay rejected.
"""
from pathlib import Path
import subprocess,hashlib,collections,json,sys
R=Path(__file__).resolve().parents[1]
JSON_LIMIT=262144
EVIDENCE_LIMIT=1048576
EVIDENCE_INDEX=Path('content/data/evidence-sources.json')
EXPECTED_FIELDS={'repo','commit','path','sha256','origin_sha256','transformation'}

def files(root):
 return [root/p for p in subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0') if p and (root/p).is_file()]

def file_errors(rel,size):
 out=[]
 if any(x in rel.parts for x in ['node_modules','.cache','.venv','build-work','immutable-inputs','incremental-memory-work','preview','raw-output','benchmark-output']):out.append(f'Build/cache path: {rel}')
 if rel.suffix in ['.gz','.zip','.tar','.7z']:out.append(f'Binary archive: {rel}')
 if rel.suffix=='.log' and size>16384:out.append(f'Verbose log: {rel}')
 limit=EVIDENCE_LIMIT if rel==EVIDENCE_INDEX else JSON_LIMIT
 if rel.suffix=='.json' and size>limit:out.append(f'Large JSON ({size} bytes): {rel}')
 if size>2097152:out.append(f'Large individual file ({size} bytes): {rel}')
 return out

def evidence_index_errors(root):
 p=root/EVIDENCE_INDEX
 if not p.exists():return []
 try:d=json.loads(p.read_text())
 except Exception as e:return [f'Evidence index parse error: {e}']
 out=[]
 if set(d)!= {'evidence_repo','evidence_commit','files'}:
  out.append('Evidence index unexpected top-level keys: '+','.join(sorted(set(d)-{'evidence_repo','evidence_commit','files'} or set(d))))
 for field in ('evidence_repo','evidence_commit'):
  if not isinstance(d.get(field),str) or not d.get(field):out.append(f'Evidence index {field} missing/invalid')
 f=d.get('files')
 if not isinstance(f,dict):out.append('Evidence index files is not an object');return out
 for key,item in list(f.items())[:400]:
  if not isinstance(item,dict):out.append('Evidence index entry is not an object: '+str(key));continue
  extra=set(item)-EXPECTED_FIELDS
  if extra:out.append('Evidence index entry has unexpected fields: '+str(key)+' '+','.join(sorted(extra)));continue
  for k,v in item.items():
   if not isinstance(v,str):out.append('Evidence index non-string field: '+str(key))
   elif len(v)>4096:out.append('Evidence index oversized field value: '+str(key))
   elif v.lstrip().startswith('[') or v.lstrip().startswith('{'):
    out.append('Evidence index value looks like embedded payload: '+str(key))
 return out

def self_test():
 errs=file_errors(Path('x/large.json'),JSON_LIMIT+1);assert not errs or any('Large JSON' in e for e in errs)
 errs=file_errors(EVIDENCE_INDEX,JSON_LIMIT+1);assert not any('Large JSON' in e for e in errs),'evidence index within cap must be accepted'
 errs=file_errors(EVIDENCE_INDEX,EVIDENCE_LIMIT+1);assert any('Large JSON' in e for e in errs),'evidence index over cap must be rejected'
 from unittest.mock import patch
 import tempfile
 with tempfile.TemporaryDirectory() as td:
  root=Path(td);idx=root/EVIDENCE_INDEX;idx.parent.mkdir(parents=True)
  idx.write_text(json.dumps({'evidence_repo':'r','evidence_commit':'c'*40,'files':{'pub/f':{'repo':'r','commit':'c'*40,'path':'a/b','sha256':'h'*64,'origin_sha256':'h'*64}}}))
  assert not evidence_index_errors(root)
  idx.write_text(json.dumps({'wrong':1}));assert evidence_index_errors(root)
  idx.write_text(json.dumps({'evidence_repo':'r','evidence_commit':'c'*40,'files':{'pub/f':{'repo':'r','commit':'c'*40,'path':'a/b','sha256':'h'*64,'origin_sha256':'h'*64,'raw':[1,2,3]}}}))
  assert evidence_index_errors(root)
  bad={'repo':'r','commit':'c'*40,'path':'a/b','sha256':'h'*64,'origin_sha256':'h'*64,'note': '[{' + 'x'*5000}
  idx.write_text(json.dumps({'evidence_repo':'r','evidence_commit':'c'*40,'files':{'pub/f':bad}}))
  assert evidence_index_errors(root)
 print('SELF-TEST PASS')

def main():
 if '--self-test' in sys.argv:
  self_test();raise SystemExit(0)
 errors=[];payloads=collections.defaultdict(list);sizes=[]
 for archive in R.glob('*.zip'):
  errors.append(f'Workspace archive must live outside Labs: {archive.name}')
 for directory in (R/'public/benchmarks').rglob('*'):
  if directory.is_dir() and directory.name in ['preview','raw-output','benchmark-output'] and any(directory.iterdir()):
   errors.append(f'Benchmark working output must live outside Labs: {directory.relative_to(R)}')
 published=files(R/'public') if (R/'public/.git').exists() else []
 for p in files(R)+published:
  rel=p.relative_to(R);size=p.stat().st_size;sizes.append(size);errors+=file_errors(rel,size)
  if p.suffix=='.json' and size>65536:payloads[hashlib.sha256(p.read_bytes()).hexdigest()].append(str(rel))
  if '/evidence/' in str(rel) or str(rel).startswith('investigation/'):errors.append(f'Canonical evidence in website: {rel}')
 errors+=evidence_index_errors(R)
 for ps in payloads.values():
  if len(ps)>1:errors.append('Duplicate large JSON: '+', '.join(ps))
 if sum(sizes)>10485760:errors.append(f'Tracked website over 10 MiB: {sum(sizes)} bytes')
 for e in errors:print(e)
 print('Tracked website bytes:',sum(sizes),'files:',len(sizes))
 raise SystemExit(bool(errors))

if __name__=='__main__':main()