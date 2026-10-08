# Labs evidence repository split — closed

Canonical datasets: https://github.com/nift-experiments/lab-evidence/tree/6250bc46604ad82713644cfb2a8bb46850573340
Final remotely verified evidence/audit head: https://github.com/nift-experiments/lab-evidence/tree/26419361d87ff10611c1b35874145b4d273fa9ed
Canonical file classification, hashes and provenance: indexes/classification-before.json and indexes/labs-paths.json in that repository. This classification preceded any removal.

The split removed 1,635 verified tracked payload/screenshot files from Labs; compact graph summaries remain. Benchmarks/histories/environment/numeric receipts/audits are canonical in lab-evidence. Forty-two matching migration snapshots refer directly to accepted experiment evidence at exact commits, avoiding duplication. Unpacked superseded diagnostic numeric files remain with explicit exclusion labels; disposable logs and binary bundles do not migrate. Duplicate source/public files are stored once with indexed aliases. Large input copies remain excluded. No accepted migration implementation, Nift core, timing, conclusion, graph value, scope or design changed.

| Measurement (Git excluded unless stated) | Before | After |
|---|---:|---:|
| Whole workspace bytes, including unrelated untracked work | 68,676,333 | 15,336,703 |
| Whole workspace ZIP bytes | 14,149,073 | 2,426,712 |
| Tracked source + publication bytes | 57,171,979 | 3,627,331 |
| Tracked website ZIP bytes | not captured | 1,458,397 |

Tracked source is about 1.63 MB; tracked publication about 2.00 MB. The whole checkout still contains an unrelated untracked 11,340,196-byte shell-preview dataset, deliberately preserved and not committed/deployed. Concurrent shell source/template/style changes remain untouched except independently staged evidence URL integration. The working-tree/ZIP snapshot precedes the small closeout receipts/CI file; precise measurement definitions and all largest remaining files/directories are in canonical audits/storage/20261009-repository-split/.

Evidence repo: 23,641,259 bytes excluding Git. Family sizes: {"README.md": 2118, "audits": 765554, "benchmarks": 18895375, "indexes": 1399511, "supplemental": 2578701}. Benchmark history is the largest family, about 18.9 MB; supplemental AI SDK about 2.58 MB. No identical remaining canonical payloads above 16 KiB were found. The 1,309 original pushed files and all subsequent audit additions were verified through a fresh remote clone and SHA256 manifests before closeout.

Source split 8fa5d9b; absolute-archive link correction 3992ffd. Publication split 16a98a9; final deployment d31805853016412022f64748480fc72b51eedb61, GitHub Pages built. All 15 live HTML pages exactly match committed bytes; all non-URL bytes preserve the accepted publication. All 76 same-origin publication links pass, including archived routes/assets; every live pinned evidence link belongs to the verified external/remote-hash set. Eight affected pages pass four responsive widths (32 views), graph bars visible with numeric labels, no page errors/overflow. Temporal/AI SDK/website-generator inspected manually. A discovered legacy absolute archive evidence URL gap was corrected; same-origin absolute URLs are now validated locally too. Full/incremental builds and Nift status pass. Explicit report regeneration reproduces accepted headline/sample/hash/parity gates from pinned raw inputs outside Labs and does not recreate local evidence payloads.

Storage guard and source CI: scripts/check_storage_policy.py and .github/workflows/storage-policy.yml. Normal Nift builds use only local website content/compact summaries and need no network/evidence checkout. See EVIDENCE-STORAGE.md.

Historical Git objects remain reachable. Measured source/publication Git databases total about 38.1 MB. Old-only unique objects have an estimated 29,251,306 independently zlib-compressed bytes (about 29 MB); actual reclaim depends on Git delta packing, shared refs and retained branches. A separate approved history rewrite could reduce clone/archive history size, but no rewrite/prune was performed. Do not rewrite without explicit human approval. Current website HEAD is small; history cleanup is a separate decision.
