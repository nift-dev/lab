"""Measure the Labs working tree separately from Git history; never delete files."""
from pathlib import Path
import hashlib,json,collections,subprocess,zipfile,tempfile
R=Path(__file__).resolve().parents[1]
def audit():
 files=[p for p in R.rglob('*') if p.is_file() and '.git' not in p.relative_to(R).parts]
 sizes={p:p.stat().st_size for p in files}; families=collections.Counter(); duplicates=collections.defaultdict(list)
 for p,n in sizes.items():
  rel=p.relative_to(R);families['/'.join(rel.parts[:3])]+=n
  if n>100000:duplicates[hashlib.sha256(p.read_bytes()).hexdigest()].append(str(rel))
 with tempfile.TemporaryDirectory(prefix='labs-storage-') as tmp:
  z=Path(tmp)/'workspace.zip'
  with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
   for p in files:archive.write(p,p.relative_to(R))
  zipped=z.stat().st_size
 gitdirs={}
 for name,p in [('source',R/'.git'),('publication',R/'public/.git')]:
  gitdirs[name]={'bytes':sum(f.stat().st_size for f in p.rglob('*') if f.is_file()),'objects':subprocess.check_output(['git','count-objects','-vH'],cwd=p.parent,text=True)}
 return {'working_tree_bytes':sum(sizes.values()),'zip_bytes_excluding_git':zipped,'largest_files':[{'path':str(p.relative_to(R)),'bytes':n} for p,n in sorted(sizes.items(),key=lambda x:x[1],reverse=True)[:30]],'families':dict(families.most_common(30)),'duplicate_large_payloads':[{'sha256':h,'paths':ps} for h,ps in duplicates.items() if len(ps)>1],'git':gitdirs}
if __name__=='__main__':
 import sys
 d=audit();(R/'docs'/('storage-'+sys.argv[1]+'.json')).write_text(json.dumps(d,indent=2)+'\n');print({k:d[k] for k in ['working_tree_bytes','zip_bytes_excluding_git','git']})
