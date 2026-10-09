# Labs history cleanup — 2026-10-09

Selective history filtering removed migrated evidence, logs, unused screenshots, archives and duplicated AI SDK immutable input backups. Useful website history remains; this was not a squash. The final filter/proof manifests and verified backups are outside Labs at `/home/nick/backups/lab-history-cleanup-20261009-final/`; earlier backups remain at `/home/nick/backups/lab-history-cleanup-20261009/`. Each directory contains `SHA256SUMS` for its bundles.

Source: `2db7de61cc626b24d12799bfbd6704791efbc449` → `7b48678697f12eb92f5976aecb3a137abe8679d4` (38 commits retained).
Publication: `e44551923592b5af914062e27216a09dee16accb` → `1ea031c6331facb57a2fe69907635fab611ea862` (32 commits retained).

Both accepted tree IDs are identical before/after filtering: source `221b4a9e76239f8b7827e1147bb023f1cadcc14e`, publication `959b9ab93160608e51458e1b72d4d3a12ac016e7`. The atomic push used explicit leases for both branches. Fresh GitHub clones passed fsck and tree checks before local reflog expiry and aggressive GC.

Both clean shell worktrees at `/tmp/nift-shell-expanded-20261009/lab-source` and its `public` directory were moved to equivalent rewritten commits (`3de8ddfc93522a0513c23bbf02e3140465e34cbd` and `e893a11a5c2609f52c19797e2df4572b1e832cab`). Their commits were already ancestors of the accepted tips; no cherry-pick was necessary. Both worktree trees are unchanged. Large local smoke inputs already live outside Labs under `/tmp/nift-shell-expanded-20261009/`; none were discarded.

Ordinary ZIP including both Git databases: baseline **41,164,442 bytes**, post-GC **8,542,683 bytes** before this small storage-only closeout. Fresh source/publication clones combined as an ordinary website workspace ZIP: **8,977,683 bytes**. Source Git database fell from approximately 31 MiB to 3.4 MiB; publication from 20 MiB to 3.4 MiB. The final exact ZIP, file-size inventory, all backup hashes, link and viewport receipts are recorded outside the workspace.

Current publication bytes, benchmark values, graph values, conclusions and designs remain unchanged. Storage-only changes add preview/archive guards, this note and an old/new commit map; two compact provenance records now point to equivalent rewritten source commits while retaining the original IDs. Canonical lab-evidence and accepted migration histories were not rewritten.

Full/incremental builds, storage checks, routes/fragments/assets and all 173 GitHub evidence/repository links pass. All 16 live pages are byte-identical to the accepted publication, with 85 live publication links passing. All eight incremental-memory graph panels passed four viewport widths locally and live. Ignored benchmark preview directories are now explicitly rejected by the storage guard.

Keep raw campaign data and workspace ZIPs outside Labs. Do not regenerate or remeasure accepted benchmarks as part of storage maintenance. `history-rewrite-map.json` records original-to-rewritten commit identities; the verified external bundles retain full recoverability.
