"""Publication-only context for the frozen final shell and scripting series."""
import json
from pathlib import Path
E=Path(__file__).resolve().parents[2]/'nift-benchmarks/lab-evidence'
SERIES='20261015-v4120-final-c14d068';REV='19e390183b9bcb039abe6aa553ad88a2305b49ee'
def link(path,label):return f'<a href="https://github.com/nift-experiments/lab-evidence/blob/{REV}/{path}">{label}</a>'
def recovery(slug,p,table,section,f):
 base=f'campaigns/{SERIES}/recovery-diagnostics/{slug}'
 d=json.loads((E/base/f'recovery-three-way-{slug}/summary.json').read_text());rows=[]
 for r in d['rows']:rows.append([r['case']]+[f(r[v]['median_ms']) for v in ('release','original','final')])
 body=p('Separate same-node diagnostic: exact clean source builds c8d9c266 (previous release), 7f7e487 (original candidate) and c14d068 (final), using the same GCC 13.3 / native Make -O2 configuration, CPU 0, ten measured samples plus two warmups per case/version, six-permutation adjacent ordering and unchanged source/output oracles. All 72 observations passed independent audit; these are not pooled into official peer tables.')
 body+=table(['Case','Release ms','Original candidate ms','Final candidate ms'],rows,'Separate three-version recovery diagnostic; medians, 10 measured samples per cell')
 if slug=='shell':
  body+=p('Calls improved 51.85% from the original candidate; final versus release differed by 0.666 ms (+3.17%), with overlapping ranges. Strings improved 72.10% versus the original and 68.71% versus release, with disjoint ranges and all ten paired final observations faster. These are fixed-specimen gains, not universal language-speed claims.')
 else:
  body+=p('Small/large calls improved 36.56% / 57.69% from the original candidate, with disjoint ranges and every paired final observation faster. Final versus release differed by −0.032 ms / +5.019 ms (−0.67% / +2.59%), with overlapping ranges. This supports substantial recovery to near-release latency, not exact equality or a statistically established residual regression.')
 body+=p(link(base+'/FINDINGS.md','Findings and qualifications')+' · '+link(base+f'/recovery-three-way-{slug}/raw.json','All raw samples and build identities')+' · '+link(base+f'/recovery-three-way-{slug}/independent-audit.json','Independent audit')+'.')
 return section('Separate recovery diagnostic','Same-node checks for the surprising changes.',body,'version-check')
def context(slug,d,p,table,section):
 rows=[[n,(v['version'].splitlines()[0] if isinstance(v,dict) else str(v))] for n,v in d['tools'].items()]
 b=f'benchmarks/{slug}/{SERIES}'
 body=p('Final candidate Nift 4.12.0, exact clean source c14d06835bca515a5281e41da0e40219c2d60ef0; CLI SHA-256 7dd42dcee5ca4a6965f0823c0ae59198282da1eb77e0fcd4cae93a537870a6fb. Native Make -O2, GCC 13.3; dedicated g6-standard-4 (8 GB / four vCPUs), Ubuntu 24.04, timed processes pinned to CPU 0. OS caches are uncontrolled; this is not machine-cold timing. Historical hosts and diagnostic cohorts are never pooled.')
 body+=table(['System','Measured version'],rows,'Detected on this suite’s final measurement host')
 body+=p(link(b+'/candidate-built.json','Exact build identity')+' · '+link(b+'/refresh-readiness.json','Frozen suite and tool pins')+' · '+link(b+'/dpkg-versions.tsv','Actual compiler/package inventory')+'.')
 audit=json.loads((E/b/'independent-audit.json').read_text())
 body+=p(link(b+'/independent-audit.json','Independent complete-count/distribution audit')+' · '+link(b+'/normalized-current-metrics.json','Normalized measurements')+' · '+link(b+'/official-refresh','Complete raw data and retained warmups')+'. No failed or superseded attempt is substituted for this accepted series.')
 return section('Frozen environment','Exact source, tools and boundaries.',body,'machine')+section('Reproduce / scrutinise','All observations are retained.',p(link(b,'Complete accepted series')+'; the frozen suite revision and exact invocation are recorded in its readiness and official controller files. Summaries are independently recomputed from raw observations.'),'reproduce')
def preference(slug,p,section):
 if slug=='shell':
  body=p('For established POSIX shell compatibility I would retain Bash or Zsh; interactive preferences and structured-data workflows can favor Fish or Nushell. For authored Nift-owned automation, agent-maintained mixed projects and workflows needing programmable .f policy plus explicit artifact/input/lifecycle contracts, I would choose Nift. That is a contextual practitioner preference, not a claim of drop-in shell equivalence or universal speed leadership. Direct GNU helper-only baselines are excluded from shell peer rankings because their launch boundary differs.')
 else:
  body=p('For a standalone general-purpose script, especially sustained data/compute work, I would usually choose Python (or a workload-appropriate native/JIT runtime), using the peer rows rather than Nift’s startup cost alone. Inside a Nift-owned project combining templates, files, build policy and tasks, I would choose Nift where the shared runtime and explicit contracts simplify agent maintenance. Human-plus-agent and agent-primary choices depend on those project requirements; the benchmark does not measure authoring error rates or prove that one language is universally best.')
 body+=p('Machine-readable inputs, ownership and dependencies can be useful explicitness rather than redundant ceremony. These qualitative judgements do not turn the harness’s golden-output/fixture checks into automatic product guarantees. Memory remains a separately qualified waited-child high-water measure, not aggregate process-tree usage or a combined performance score.')
 return section('Practitioner judgement / AI-DX','Choose for the actual workflow.',body,'practitioner')
def notice(slug):
 return f"<p>Series <strong>{SERIES}</strong> · Nift <strong>4.12.0 final candidate</strong> · frozen <a href='https://github.com/nift-dev/nift/tree/c14d06835bca515a5281e41da0e40219c2d60ef0'>source revision</a>. Current figures use final audited observations. Earlier reports retain their own dated series; samples are not pooled.</p>"
