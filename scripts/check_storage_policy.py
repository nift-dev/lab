"""Conservative storage guard for tracked website source/publication, not Git history."""
from pathlib import Path
import subprocess,hashlib,collections
R=Path(__file__).resolve().parents[1]
def files(root):
 return [root/p for p in subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0') if p and (root/p).is_file()]
errors=[];payloads=collections.defaultdict(list);sizes=[]
for p in files(R)+files(R/'public'):
 rel=p.relative_to(R);size=p.stat().st_size;sizes.append(size)
 if any(x in rel.parts for x in ['node_modules','.cache','.venv','build-work','immutable-inputs','incremental-memory-work']):errors.append(f'Build/cache path: {rel}')
 if p.suffix in ['.gz','.zip','.tar','.7z']:errors.append(f'Binary archive: {rel}')
 if p.suffix=='.log' and size>16384:errors.append(f'Verbose log: {rel}')
 if p.suffix=='.json' and size>262144:errors.append(f'Large JSON ({size} bytes): {rel}')
 if size>2097152:errors.append(f'Large individual file ({size} bytes): {rel}')
 if p.suffix=='.json' and size>65536:payloads[hashlib.sha256(p.read_bytes()).hexdigest()].append(str(rel))
 if '/evidence/' in str(rel) or str(rel).startswith('investigation/'):errors.append(f'Canonical evidence in website: {rel}')
for ps in payloads.values():
 if len(ps)>1:errors.append('Duplicate large JSON: '+', '.join(ps))
if sum(sizes)>10485760:errors.append(f'Tracked website over 10 MiB: {sum(sizes)} bytes')
for e in errors:print(e)
print('Tracked website bytes:',sum(sizes),'files:',len(sizes))
raise SystemExit(bool(errors))
