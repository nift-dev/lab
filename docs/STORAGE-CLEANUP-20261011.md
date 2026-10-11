# Labs storage cleanup — 2026-10-11

Before: working files excluding Git 382,014,825 bytes; source Git 7,780,822 bytes; publication Git 7,816,141 bytes. Tracked source/publication 9,028,139 bytes. Ignored plotting dependencies (approximately 329 MiB) and public.zip (12,145,221 bytes) caused the apparent growth. Both are preserved outside Labs under ../.lab-tools/. Published chart assets remain intact.

Fifteen audit receipts (163,038 bytes) and original chart inputs containing 382 raw memory samples were preserved byte-for-byte in [canonical evidence](https://github.com/nift-experiments/lab-evidence/tree/c8fe84d/audits/labs-storage-20261011). Compact chart inputs retain the same sample counts, statistics and ranges; raw arrays are removed. No timings, charts or published page bytes changed.

Remote main and stage were inspected. Reachable unique uncompressed blobs total 21,772,147 bytes; the largest is legitimate hero artwork (1,196,950 bytes). Historical small result inputs are not materially responsible for clone size. No history rewrite or force push was warranted. Existing recovery bundles remain untouched.

The storage policy rejects raw evidence directories/formats, JSON audit receipts and embedded raw observation arrays, checks every pointer entry, retains bounded legitimate publication inputs, and tests rejection/acceptance cases. Audit/link scripts now write receipts outside Labs. Plotting instructions use the external tools environment. Build, status and route/asset validation pass; the publication worktree remains byte-identical.
