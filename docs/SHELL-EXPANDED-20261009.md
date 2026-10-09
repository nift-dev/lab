# Expanded shell campaign: 20261009-v4100-shell-expanded

Nift 4.10.0 development build. This series adds substantial shell work while preserving startup and configuration methodology. It does not establish an overall fastest shell.

## Identity and counts

Nift source `629b1f23afbb5b3be97dac66b6cea1a9d5b3d1fc`; measured suite `fc7c4d93dcd525545f97e302501eb08e1b0f9f7e`. One fresh g6-standard-4 shared-CPU node, us-east, Ubuntu 24.04, 4 vCPU/8 GiB; all measurements serial and pinned to CPU 0. OS caches uncontrolled. Native Make defaults: `make -j2; make install PREFIX=/opt/campaign/tools`, C++17/C99 -O2, no architecture tuning.

293 official jobs, 7,855 measured observations, 711 retained warmups. Existing prepared/fresh matrices: 152 jobs, 6,580 + 456. Added layer: 27 cases, five shells and six GNU baselines, 141 jobs, 1,275 + 255. Heavy 100k cells use 5 measured + 1 warmup; ordinary cells use 10 + 2. No sample or outlier discarded.

## Detected participants

- bash: GNU bash, version 5.2.21(1)-release (x86_64-pc-linux-gnu)
- zsh: zsh 5.9 (x86_64-ubuntu-linux-gnu)
- fish: fish, version 4.9.3
- nu: 0.116.1
- nift: Nift v4.10.0

CPU: AMD EPYC 7642 48-Core Processor. Kernel: 6.8.0-134-generic.
Nift binary SHA-256: `f2117ddafafd3e4c762f66335fc082c96449b3a0f4d1518df7564e908d68b03e`.

## Startup

| Boundary / median ms | bash | zsh | fish | nu | nift |
|---|---:|---:|---:|---:|---:|
| interactive | 1.933 | 2.688 | 18.336 | 16.429 | 1.813 |
| trivial-command | 1.528 | 1.991 | 2.159 | 12.700 | 2.001 |
| external-100 | 84.276 | 97.144 | 70.892 | 93.676 | 94.908 |

## Selected new tasks

| Task / median seconds | bash | zsh | fish | nu | nift | GNU baseline |
|---|---:|---:|---:|---:|---:|---:|
| create-empty-100000 | 3.284670 | 5.108553 | 4.922952 | 3.534623 | 3.605163 | — |
| create-small-100000 | 4.382861 | 6.100811 | 7.089226 | 4.145883 | 15.499080 | — |
| delete-selected-100000 | 2.256578 | 2.043681 | 2.514986 | 6.288551 | 2.631455 | 2.443174 |
| delete-tree-100000 | 2.467874 | 2.271487 | 2.370008 | 6.714993 | 2.549101 | 2.095917 |
| copy-small-10000 | 0.490406 | 0.486558 | 0.487014 | 1.540465 | 1.332920 | 0.484016 |
| rename-selected-10000 | 0.332174 | 0.330292 | 0.333074 | 1.104051 | 1.091107 | 0.328304 |
| concat-small-10000 | 0.099777 | 0.099928 | 0.101869 | 0.508610 | 0.238147 | — |
| traverse-100000 | 0.454618 | 0.456504 | 0.459372 | 0.240810 | 2.881467 | — |
| processes-1000 | 0.790436 | 0.926187 | 0.652459 | 0.760765 | 0.896078 | — |
| pipeline-8 | 0.010820 | 0.012072 | 0.009743 | 0.021385 | 0.011407 | — |
| arithmetic | 0.063952 | 0.025073 | 2.890970 | 0.029281 | 0.017558 | — |
| function-calls | 0.051197 | 0.137919 | 1.282304 | 0.041648 | 0.020609 | — |
| fibonacci-mod | 0.007476 | 0.004192 | 0.137098 | 0.014631 | 0.004000 | — |
| string-transform | 0.034682 | 0.013834 | 0.799833 | 0.044623 | 0.126674 | — |
| log-filter-group | 0.043637 | 0.044445 | 0.043298 | 0.054339 | 0.044164 | — |
| source-tree-report | 0.211124 | 0.211850 | 0.209883 | 0.220630 | 0.209958 | — |
| selected-cleanup | 0.030935 | 0.031656 | 0.031477 | 0.102514 | 0.053292 | — |

## Correctness and boundaries

All complete cloud smoke, RC-state certifications, eight workload tests and three supervisor tests passed. Every official output and filesystem oracle passed. All distribution fields were independently recomputed exactly; the added raw file passed JSON Schema validation. Frozen definitions, job identities, sample/warmup counts, affinity and binary hashes were checked. Fixture manifests, content recipes, implementation sources, exact commands, every observation and strict validation records are retained.

100k fixtures contain 100k selected targets and 20k interspersed keepers. Tree variants mix both in every directory. Removing a whole parent cannot pass. Every target byte/absence, keeper byte/mode/mtime/inode, complete inventory and copy/concat/source-integrity postcondition is checked outside elapsed timing. Selected cleanup additionally moves 200 outputs and writes a checked summary.

Native arithmetic/calls/Fibonacci/string cases compare bounded shell-code work. GNU log and source-report pipelines share the same external engines in all shells. Filesystem end-to-end tasks permit Nift/Nu native APIs versus traditional redirection/batched GNU utilities. Nift atomic saving performs temporary-file replacement. Direct GNU xargs baselines exclude shell launch but include utility work. These architectural differences are explicit, and the baseline is not subtracted. Uncontrolled caches, shared CPU scheduling and different internal semantics limit attribution. RSS is Linux waited-child high-water memory, not simultaneous aggregate tree memory.

The most informative additions are exact 100k selected deletion with keeper preservation, native algorithm cases and 1/10/100/1000 process scaling. Creation/copy/deletion increasingly expose filesystem/kernel throughput; common log/source-report cases expose Unix utility work plus orchestration. No one result should be treated as an overall shell-quality score. Giant-argv capability tests, parallel jobs, personal dotfiles and large streaming copies remain outside this bounded extension.

## Publication and lifecycle

Result evidence is pushed before Labs. The original 4.9 raw series remains immutable and its original report/figures are archived. The three pre-existing graphs retain their exact original Git implementations, axes, legend styles and surrounding graph/table blocks; unchanged-data PNGs were verified byte-identical before substituting fresh official values. Only genuinely new workload graphs use shared graphical/numeric table columns and numeric vectors. Local desktop/390/320, keyboard scrolling, route/fragment/assets, private-material and historical hash checks precede publication. Changed live bytes and historical evidence are checked before deleting only the campaign node. CLI absence and independent authenticated API HTTP 404 are required; temporary SSH/config/connection state is then removed. The final lifecycle records provide timestamps and publication commits.

## Verified publication and teardown

Results evidence commit: `92c241f74a6208155ba5158707fd7a4317773090`. Labs source: `c15584f5b1ccb2ca86ee1b9a9a607f075025c05b`. Deployment: `e31233ab40910fec6dd6a96d725de29434c228c6`. All 18 changed public files matched live bytes before teardown; historical raw evidence and graph assets remained byte-identical; separately committed archived-page href relocations were documented and verified. Desktop, 390px, 320px, keyboard scrolling and chart/header/value alignment passed.

Only `nift-shell-20261009-expanded` was deleted. CLI absence and independent authenticated API HTTP 404 were verified at 2026-10-09T00:47:49.127571+00:00. Temporary SSH private/public keys, known-host state, node connection metadata, CLI config and private error logs were removed. Post-cleanup private-material scan passed. Final lifecycle commits append these records without changing any raw measured observations or prior series.
