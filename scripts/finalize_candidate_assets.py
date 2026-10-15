"""Keep historical figures and PNG downloads immutable without duplicate site payloads."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1]
PIN='eeb3afe865e38f37e0bf78572ed22dcd816b3657'
OLD='3225ebcc5d8cd0b3c1d6b09edc84392c0eb4eb7e'
def main():
 for folder in (R/'content/benchmarks').glob('*/series/*'):
  if not folder.is_dir():continue
  slug=folder.parents[1].name;series=folder.name;assets=R/f'public/benchmarks/{slug}/series/{series}/assets'
  docs=list(folder.glob('*.html'));template=R/f'templates/benchmarks/{slug}/series-{series}.html'
  if template.exists():docs.append(template)
  for asset in list(assets.glob('*')):
   if asset.suffix not in ['.svg','.png']:continue
   url=f'https://raw.githubusercontent.com/nift-dev/lab/{OLD}/benchmarks/{slug}/assets/{asset.name}'
   for p in docs:
    t=p.read_text();t=t.replace(f"@path('public/benchmarks/{slug}/series/{series}/assets/{asset.name}')",url).replace(f"@path('public/benchmarks/{slug}/assets/{asset.name}')",url).replace(f'public/benchmarks/{slug}/series/{series}/assets/{asset.name}',url).replace('"assets/'+asset.name+'"','"'+url+'"').replace("'assets/"+asset.name+"'","'"+url+"'")
    p.write_text(t)
   asset.unlink()
 for asset in list((R/'public/benchmarks').glob('*/assets/*.png')):
  slug=asset.parents[1].name;url=f'https://raw.githubusercontent.com/nift-experiments/lab-evidence/{PIN}/audits/publication/20261015-v4120/assets/benchmarks/{slug}/assets/{asset.name}'
  p=R/f'content/benchmarks/{slug}/index.html'
  if p.exists():p.write_text(p.read_text().replace(f"@path('public/benchmarks/{slug}/assets/{asset.name}')",url).replace('"assets/'+asset.name+'"','"'+url+'"'))
  asset.unlink()
if __name__=='__main__':main()
