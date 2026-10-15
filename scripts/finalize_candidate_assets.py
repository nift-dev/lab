"""Publish current PNG downloads without duplicate site payloads."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1]
PIN='b895146073c16a7bb785a866206216c9cbbc3065'
OLD='3225ebcc5d8cd0b3c1d6b09edc84392c0eb4eb7e'
def main():
 for asset in list((R/'public/benchmarks').glob('*/assets/*.png')):
  slug=asset.parents[1].name;url=f'https://raw.githubusercontent.com/nift-experiments/lab-evidence/{PIN}/audits/publication/20261015-v4120-current-only/assets/benchmarks/{slug}/assets/{asset.name}'
  p=R/f'content/benchmarks/{slug}/index.html'
  if p.exists():p.write_text(p.read_text().replace(f"@path('public/benchmarks/{slug}/assets/{asset.name}')",url).replace('"assets/'+asset.name+'"','"'+url+'"'))
  asset.unlink()
 # A current-results report must not keep unreferenced old graph files deployed.
 for folder in (R/'public/benchmarks').glob('*/assets'):
  source=R/f'content/benchmarks/{folder.parent.name}/index.html'
  if not source.exists():continue
  text=source.read_text()
  for asset in folder.iterdir():
   if asset.suffix in ('.svg','.png') and asset.name!='favicon.svg' and asset.name not in text:
    asset.unlink()
if __name__=='__main__':main()
