# Official shell and scripting campaign: 20261010-v4100

Nift 4.10.0 development build (development build). This campaign preserves methodology, sample treatment, correctness oracles and evidence conventions; it does not establish a universal shell or language winner.

## Frozen measurement identity

- Nift: `2eaec7d70e9ce2e698d0ba23a605fb9cf85317ff`
- Shell suite: `48a4a8e3e1f3e1ccf2c61fc7f8a7fd3a490ab4a1`
- Scripting suite: `6f5b0e3d7c977fca25758c6e2dd2189b67d209ea`
- Shell series: 20261010-v4100-shell-expanded · Scripting series: 20261010-v4100
- Labs source: `36c1dcbad0acb88c4a82e08f3ca65500ff3c6a63` · Labs deployment: `8d0cc21d029958dd2e6c66d507730c2c570e039e`

Both suites use fresh, separate g6-standard-4 shared-CPU Linodes in us-east, Ubuntu 24.04, 8 GiB and four vCPUs. All measurements pin CPU 0. OS caches are uncontrolled. Native `make -j2` and `make install PREFIX=/opt/campaign/tools` use identical defaults on both nodes.

## Shell node
CPU: AMD EPYC 7542 32-Core Processor. Kernel: 6.8.0-134-generic.
Nift binary SHA-256: `e7cb28d6150c797acbb52a618faff3cf981281b9ea4e91a8c478062242f0c3a2`.

Participants:
- bash: GNU bash, version 5.2.21(1)-release (x86_64-pc-linux-gnu)
- zsh: zsh 5.9 (x86_64-ubuntu-linux-gnu)
- fish: fish, version 4.9.3
- nu: 0.116.1
- nift: Nift v4.10.0

## Scripting node
CPU: AMD EPYC 7542 32-Core Processor. Kernel: 6.8.0-134-generic.
Nift binary SHA-256: `e7cb28d6150c797acbb52a618faff3cf981281b9ea4e91a8c478062242f0c3a2`.

Participants:
- nift: Nift v4.10.0
- python: Python 3.12.3
- ruby: ruby 3.2.3 (2024-01-18 revision 52bb2ac0a6) [x86_64-linux-gnu]
- lua54: Lua 5.4.6  Copyright (C) 1994-2023 Lua.org, PUC-Rio
- luajit: LuaJIT 2.1.1703358377 -- Copyright (C) 2005-2023 Mike Pall. https://luajit.org/
- node: v24.21.0
- bash: GNU bash, version 5.2.21(1)-release (x86_64-pc-linux-gnu)

## Validation

Shell: 293 official jobs, 7855 measured observations, 711 warmups. Scripting: 188 official jobs, 1880 measured observations, 376 warmups. All correctness oracles passed; summaries independently recomputed exactly; clean checkouts; CPU 0 affinity; no sample discarded.

## Method and counts

Shell retains startup/configuration matrices (prepared and fresh-HOME) plus the expanded workload layer (filesystem create/delete/copy/move/concat/traverse, process and pipeline scaling, algorithm-heavy and practical/mixed workloads). Scripting retains the established families: no-op, output, loops, function calls, array/string/hash scan, frequency count, sliding window, sort/index, map/set, Fibonacci, BFS, JSON parse/transform/traverse and filesystem traversal, with participant rotation and exact golden oracles.

## Comparison with previous series

Cross-node differences combine Nift version, virtual hardware, runtime/package state and shared-CPU noise. No cross-node percentage is presented as a version speedup; observations of substantial movement are reviewed in `comparison.json` only for correctness/attribution limits. Where a same-node diagnostic implies a change in Nift itself, it will be labelled distinctly.

## Publication and lifecycle

Result commits, canonical `lab-evidence` commit, Labs source/deployment, live verification, teardown and credential cleanup are recorded in publication and lifecycle evidence. Nodes remain until raw evidence is copied, canonical repos are pushed, Labs is pushed and live byte verification passes. Only the two campaign nodes are deleted; independent authenticated API 404 and CLI absence are required.


## Verified publication and teardown

- shell_results: `86388ac7d43da8409b4f1525c97a427d476a1c05`
- scripting_results: `1a43c3d24822b8c1c69352c2cee44b71845321ba`
- canonical_evidence: `3dce3d984ba4ea9034add57dd664bb5033434baf`
- labs_source: `0bf636ffd77ec7c0231ec5958f3b00baba2de610`
- labs_deployment: `3eab4013d8ede1f40bbd0d398104335b25aa0829`

- nift-shell-20261010-v4100: CLI absence and independent authenticated HTTP 404, verified 2026-10-09T22:22:47.409434+00:00.
- nift-scripting-20261010-v4100: CLI absence and independent authenticated HTTP 404, verified 2026-10-09T22:22:49.969444+00:00.

## Real-browser viewport certification

Final live pages (`/benchmarks/shell/`, `/benchmarks/scripting/`, `/benchmarks/`) were validated in a real rendered-browser session (Playwright headless Chromium) at 1440, 390 and 320 px. All nine page/width combinations passed: no page-level horizontal overflow; tables scroll within their own keyboard-focusable `.table-scroll`/`.chart-scroll` regions; shell aligned-chart columns share exact column alignment; all three original shell graph assets load and render (startup distributions, prepared RC, external work); new workload charts and tables do not clip; scripting tables retain the compact accessible dash treatment; no broken image assets; no clipped/overlapping text; in-page anchor navigation works. The shell RC section remains one prepared table, one fresh-HOME table and one collapsed login matrix. Receipt: `docs/browser-viewport-validation-20261010.json`; full per-width records and screenshots remain in the campaign workspace (temporary, per storage policy).

Only change found and fixed during this pass: the benchmarks landing paragraph (this campaign's content edit) did not wrap the frozen 40-character commit SHA at 320px because backticks in the raw HTML were literal; the token is now a wrappable `<code>` and the landing has no overflow at any width.

## Shell graph design parity

`scripts/plot_startup.py` and `scripts/report_presentation.py` (the generators of the three pre-existing graphs) are byte-identical to the expanded-campaign base; only measurement inputs changed. The three SVG assets retain the exact `viewBox`, `defs`/clip-path structure, graph type, axes, legend arrangement and surrounding figure/table presentation. SVG/PNG bytes differ because the measured values changed; design/component parity is retained.

## Evidence-storage note (scripting duplication)

`nift-experiments/lab-evidence` is the canonical data store and the Labs site links only to pinned canonical evidence. `docs/EVIDENCE-STORAGE.md` permits raw campaign evidence in "experiment repositories or the dedicated lab-evidence repository". The scripting-benchmark repository retains its own per-campaign evidence directories by its long-standing convention (20261007, 20261008-v480, 20261009-v490 were all stored there), so `campaign-20261010-v4100` keeps a full copy there, with the identical bytes pinned in lab-evidence. The shell-benchmark repository moved to canonical-only linking for the expanded series per its immediate prior convention, so its v4.10 entry is a README link to canonical evidence. This intentional difference follows each suite's own established convention; no measured evidence is duplicated into Labs and no storage policy is violated. No git history was rewritten.
