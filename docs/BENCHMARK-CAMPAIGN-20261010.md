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

