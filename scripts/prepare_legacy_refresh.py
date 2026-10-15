"""Pin final suite inputs; historical reports are evidence-only."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];E=R.parent/'nift-benchmarks/lab-evidence'
REV='19e390183b9bcb039abe6aa553ad88a2305b49ee';SERIES='20261015-v4120-final-c14d068'
def prepare():
 index=R/'content/data/evidence-sources.json';d=json.loads(index.read_text())
 for slug in ('shell','scripting'):
  base=E/'benchmarks'/slug/SERIES
  files=list((base/'official-refresh').glob('*.json'))+[base/name for name in ('independent-audit.json','candidate-built.json','refresh-readiness.json','normalized-current-metrics.json','dpkg-versions.tsv','compiler.txt')]
  for path in files:
   if not path.exists():continue
   name=path.name
   for key in [f'content/benchmarks/data/history/{SERIES}/{slug}/{name}',f'public/benchmarks/{slug}/evidence/{SERIES}/{name}']:
    d['files'][key]={'repo':'nift-experiments/lab-evidence','commit':REV,'path':str(path.relative_to(E)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 index.write_text(json.dumps(d,indent=2)+'\n')
if __name__=='__main__':prepare()
