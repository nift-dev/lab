const host=document.getElementById('measurements');
const escape=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
fetch(host.dataset.source).then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(d=>{
host.innerHTML=d.sections.map(s=>`<article><h3>${escape(s.t)}</h3><p class="hint">Scroll ↔ to compare runtimes</p><div class="scroll" tabindex="0" role="region" aria-label="Scrollable exact results"><table><caption>${escape(s.c)}</caption><thead><tr><th scope="col">Operation / files</th>${['Nift','Python','Node','Bun','Go'].map(n=>`<th scope="col">${n}</th>`).join('')}</tr></thead><tbody>${s.rows.map(r=>`<tr><th scope="row">${escape(r[0])}</th>${r[1].map(c=>`<td style="--v:${Math.max(0,Math.min(100,Number(c[1])||0))}%">${escape(c[0])}</td>`).join('')}</tr>`).join('')}</tbody></table></div></article>`).join('');
}).catch(()=>{host.textContent='Result tables could not load. Use the source and frozen-evidence links below.'});
