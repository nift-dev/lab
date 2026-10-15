"""Publish regenerated PNG downloads without deleting preserved graph views."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1]
PIN='067ee6ed9667971a0bb41c6f58883100253c687f'
OLD='3225ebcc5d8cd0b3c1d6b09edc84392c0eb4eb7e'
def main():
 for asset in list((R/'public/benchmarks').glob('*/assets/*.png')):
  slug=asset.parents[1].name;url=f'https://raw.githubusercontent.com/nift-experiments/lab-evidence/{PIN}/audits/publication/20261015-v4120-preserved-views/assets/benchmarks/{slug}/assets/{asset.name}'
  p=R/f'content/benchmarks/{slug}/index.html'
  if p.exists():p.write_text(p.read_text().replace(f"@path('public/benchmarks/{slug}/assets/{asset.name}')",url).replace('"assets/'+asset.name+'"','"'+url+'"'))
  asset.unlink()
if __name__=='__main__':main()
