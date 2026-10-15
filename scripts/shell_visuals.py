"""Charts and numeric rows share one table, one column order and one source vector."""
import html,math
esc=lambda x:html.escape(str(x))
COLORS={'bash':'#ed85dc','zsh':'#cab9d8','fish':'#f09583','nu':'#c392ff','nift':'#59f58a','external-baseline':'#f5cb79'}
LABELS={'bash':'Bash','zsh':'Zsh','fish':'Fish','nu':'Nushell','nift':'Nift','external-baseline':'GNU baseline'}
def fmt(v):return f'{v:,.3f}' if v<100 else f'{v:,.1f}'
def aligned_chart(names,rows,caption,unit='ms',distribution=None):
 """rows: [(metric, {participant: numeric value})]. Geometry uses exact values.

A graphical row sits in the SAME columns as its numeric rows. No independent
image width, legend order, layout padding or participant order can drift.
 """
 values=rows[0][1];ceiling=max((distribution[n]['max_ms'] if distribution else values[n]) for n in names if n in values)*1.08
 top=f'<div class="table-scroll aligned-chart" role="region" tabindex="0" aria-label="{esc(caption)}"><table><caption>{esc(caption)} · common linear axis: 0–{fmt(ceiling)} {esc(unit)}</caption><thead><tr><th scope="col">Measurement</th>'+''.join(f'<th scope="col" class="num"><span style="color:{COLORS[n]}">{LABELS[n]}</span></th>' for n in names)+'</tr></thead><tbody>'
 charts='<tr class="chart-row"><th scope="row">'+('Min–max range<br>● median · ◆ p95<br>× p99' if distribution else 'Median elapsed time')+f'<small>0–{fmt(ceiling)} {esc(unit)}</small></th>'
 for n in names:
  if n not in values:charts+='<td><span aria-label="Outside scope">—</span></td>';continue
  def y(v):return 108-100*v/ceiling
  grid=''.join(f'<line x1="0" x2="100" y1="{k}" y2="{k}" stroke="#49314d"/>' for k in (8,58,108))
  if distribution:
   d=distribution[n];marks=f'<line x1="50" x2="50" y1="{y(d["min_ms"])}" y2="{y(d["max_ms"])}" stroke="{COLORS[n]}" stroke-width="3"/>'
   marks+=f'<circle cx="50" cy="{y(d["median_ms"])}" r="4" fill="{COLORS[n]}"/><path d="M50,{y(d["p95_ms"])-4} l4,4 l-4,4 l-4,-4 Z" fill="#f4edf6"/><text x="50" y="{y(d["p99_ms"])+4}" fill="#f4edf6" text-anchor="middle" font-size="13">×</text>'
  else:marks=f'<rect x="28" y="{y(values[n])}" width="44" height="{108-y(values[n])}" fill="{COLORS[n]}"/>'
  charts+=f'<td><svg viewBox="0 0 100 118" role="img" aria-label="{esc(LABELS[n])}: {fmt(values[n])} {esc(unit)}">{grid}{marks}</svg></td>'
 charts+='</tr>'
 numeric=''.join('<tr><th scope="row">'+esc(label)+' '+esc(unit)+'</th>'+''.join('<td class="num">'+(fmt(vals[n]) if n in vals else '<span aria-label="Outside scope" title="Outside scope">—</span>')+'</td>' for n in names)+'</tr>' for label,vals in rows)
 return top+charts+numeric+'</tbody></table></div>'

def workload_sections(data,section,p,table):
 jobs={j['id']:j for j in data['jobs']};names=('bash','zsh','fish','nu','nift');out=''
 out+=section('Measurement boundaries','Different architectures. Equivalent tasks.',p('Runtime-native cases execute shell arithmetic, functions and strings. Orchestration cases coordinate the same absolute GNU executables. End-to-end filesystem cases allow each shell’s normal APIs: Bash/Zsh/Fish use batching/redirection; Nushell and Nift use native operations. Direct GNU xargs baselines exclude shell launch. These are user-task comparisons, not five equivalent filesystem engines. Added tasks run as bare, non-interactive invocations: elapsed time includes launch and program work, while fixture setup and complete validation remain outside timing.'),'boundaries')
 out+=section('100,000 targets + 20,000 keepers','Selected files. Nothing else.', '<div class="fixture-diagram" role="img" aria-label="Interspersed target and keeper files share one directory or 100 mixed directories">'+''.join('<span class="'+('keeper' if i%6==0 else 'target')+'">'+('KEEP' if i%6==0 else 'TARGET')+'</span>' for i in range(12))+'</div>'+p('Deterministic target and keeper names are interleaved. Flat cases share one directory; the tree variant distributes both sets over 100 directories. Removing a target-only parent or the entire workspace fails validation. Selected deletion reads an exact manifest; batching avoids ARG_MAX. Nift/Nushell have native selected deletion; Bash/Zsh/Fish have no native deletion result, and their end-to-end GNU rm results remain visible.')+p('Empty creation measures inode creation; small creation writes 128 bytes per target. Nift’s file save uses temporary-file replacement, while other implementations have different write paths. We disclose that extra atomic-save work rather than claiming equivalent internals. All target bytes, all keeper bytes, keeper mode/mtime/inode, counts and unexpected files are checked outside timing.'),'selected-files')
 out+=p('Native selected-delete subset: the Nift and Nushell observations use their runtime filesystem APIs. Traditional shells have no native deletion primitive; their end-to-end timings below use batched GNU rm. The native subset reuses those exact checked observations, rather than timing an artificial second implementation.')
 out+=table(['Native deletion','Bash','Zsh','Fish','Nushell s','Nift s'],[[label,'Outside scope','Outside scope','Outside scope',fmt(jobs[case+'/nu']['summary']['median_ms']/1000),fmt(jobs[case+'/nift']['summary']['median_ms']/1000)] for label,case in [('100k flat','delete-selected-100000'),('100k tree','delete-tree-100000')]],'Runtime-native selected deletion subset; identical samples to the end-to-end cases')
 categories=[('filesystem','Filesystem operations'),('processes','Process scaling: 1 → 10 → 100 → 1,000'),('pipelines','Pipeline scaling: 2 → 4 → 8 stages'),('text','Text and Unix workflows'),('algorithms','Substantial logic in the shell'),('real-world','Mixed workflows')]
 for category,title in categories:
  body=p('LOCAL SMOKE PREVIEW: one correctness-test observation per participant; not official performance results.') if data.get('smoke') else ''
  if category=='filesystem':
   for prefix in ('create-empty','delete-selected'):
    defs=[c for c in data['definitions'] if c['id'].startswith(prefix+'-')]
    keys=list(names)+(['external-baseline'] if prefix=='delete-selected' else [])
    body+=aligned_scaling(keys,[(str(c['count']),{n:jobs[c['id']+'/'+n]['summary']['median_ms']/1000 for n in keys}) for c in defs],prefix+' · file-count scaling')
  if category in ('processes','pipelines'):
   defs=[c for c in data['definitions'] if c['category']==category]
   series=[(str(c['count']),{n:jobs[c['id']+'/'+n]['summary']['median_ms']/1000 for n in names}) for c in defs]
   body+=aligned_scaling(names,series,title)
  for c in data['definitions']:
   if c['category']!=category:continue
   keys=list(names)+(['external-baseline'] if c['id']+'/external-baseline' in jobs else [])
   values={n:jobs[c['id']+'/'+n]['summary']['median_ms']/1000 for n in keys};body+=f'<h3>{esc(c["id"])}</h3>'+('<p class="muted">Local correctness-smoke values; not official benchmark results.</p>' if data.get('smoke') else '')
   body+=('' if category in ('processes','pipelines') or c['id'].startswith(('create-empty-','delete-selected-')) else aligned_chart(keys,[('Median',values),('p95',{n:jobs[c['id']+'/'+n]['summary']['p95_ms']/1000 for n in keys})],f'{c["classification"]}; '+('LOCAL SMOKE ONLY: 1 test observation, no warmups' if data.get('smoke') else f'{c["samples"]} measured samples + {c["warmups"]} warmups per participant'),'s'))
   body+='<details><summary>Implementations, invocations, tails and correctness</summary>'
   if category in ('processes','pipelines') or c['id'].startswith(('create-empty-','delete-selected-')):
    body+=table(['Distribution · seconds',*[LABELS[n] for n in keys]],[[metric,*[fmt(jobs[c['id']+'/'+n]['summary'][field]/1000) for n in keys]] for metric,field in [('p95','p95_ms'),('Minimum','min_ms'),('Maximum','max_ms')]],c['id']+' retained tails; no outliers removed')
   body+=table(['System','Implementation'],[[LABELS[n],jobs[c['id']+'/'+n]['implementation']] for n in keys],c['id']+' implementation boundaries')
   for n in keys:
    j=jobs[c['id']+'/'+n];body+=f'<h4>{LABELS[n]}</h4><pre>{esc(j.get("source") or " ".join(j["command"]))}</pre>'
   body+=p('Every observation passed its output and filesystem oracle. Reconstructed fixture setup and verification are outside elapsed time. Exact source, manifest and oracle hashes, commands, samples, waited-child high-water RSS and validation records are preserved in shell-workloads.json.')+'</details>'
  if category=='text':body+=p('This log filter/group workload uses the same grep → awk → sort → uniq engines in all shells. Its timings include orchestration and utility work; it does not compare five native text engines.')
  if category=='algorithms':body+=p('Four bounded native scripting cases cover arithmetic, calls, iterative modular Fibonacci and string transforms. Fish uses its builtin math/test/string operations; builtin pipelines and command substitutions still incur shell machinery. No deliberately pathological recursion or unsupported map API is forced onto a participant.')
  if category=='real-world':body+=p('The common Unix report groups a synthetic .py/.cc/.md tree plus keepers by extension, counting files, bytes and lines. Cleanup deletes its exact temporary-file manifest, preserves keepers, moves 200 outputs into a report directory and writes a verified summary. These combine filesystem APIs and orchestration rather than pretending to isolate an interpreter.')
  out+=section(category,title,body,category)
 return out

def aligned_scaling(names,rows,caption,unit='s'):
 ceiling=max(v for _,vals in rows for v in vals.values())*1.08
 out=f'<div class="table-scroll aligned-chart" role="region" tabindex="0" aria-label="{esc(caption)}"><table><caption>{esc(caption)} · shared zero-based axis: 0–{fmt(ceiling)} {esc(unit)}</caption><thead><tr><th scope="col">Task size</th>'+''.join(f'<th scope="col" class="num"><span style="color:{COLORS[n]}">{LABELS[n]}</span></th>' for n in names)+'</tr></thead><tbody><tr class="chart-row"><th scope="row">Elapsed time vs size<small>Logarithmic task-size axis;<br>lines connect measured points.</small></th>'
 for n in names:
  pts=[(10+80*i/(len(rows)-1),108-100*vals[n]/ceiling) for i,(_,vals) in enumerate(rows)]
  svg=''.join(f'<line x1="0" x2="100" y1="{k}" y2="{k}" stroke="#49314d"/>' for k in (8,58,108))
  svg+='<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{COLORS[n]}" stroke-width="2"/>'
  for index,((x,y),(size,vals)) in enumerate(zip(pts,rows)):
   anchor='start' if index==0 else 'end' if index==len(rows)-1 else 'middle'
   svg+=f'<circle cx="{x}" cy="{y}" r="3" fill="{COLORS[n]}"><title>{esc(size)}: {fmt(vals[n])} {unit}</title></circle><text x="{x}" y="119" text-anchor="{anchor}" fill="#f4edf6" font-size="7">{esc(size)}</text>'
  out+=f'<td><svg viewBox="0 0 100 125" role="img" aria-label="{LABELS[n]} scaling at the sizes below">{svg}</svg></td>'
 out+='</tr>'
 for size,vals in rows:out+=f'<tr><th scope="row">{esc(size)}</th>'+''.join(f'<td class="num">{fmt(vals[n])}</td>' for n in names)+'</tr>'
 return out+'</tbody></table></div>'
