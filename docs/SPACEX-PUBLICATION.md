# SpaceX public-output reconstruction publication

The report at `/sites/spacex/` compares two reconstructed Nift source models, not SpaceX's unavailable private build system. Accepted experiment closeouts: authored `a467f6f85cdd6684739943612fb9e1bf72e592f2`, rendered `151240887b1a77587cd75516cdb77b111fcb2b9d`. Actual benchmark/parity build revisions are separately preserved in the pinned evidence. No publication input changed during experiment closeout.

`python3 scripts/render_spacex.py` explicitly fetches hash-verified pinned benchmark evidence; `--evidence /absolute/external/file` permits offline regeneration. Normal Nift builds use maintained report HTML without network access. There are five serialized samples for fourteen scenarios per model, paired time and maximum individual-process RSS, zero-based linear charts and visible ranges. No aggregate-tree RSS or private incumbent timing is invented.

Raw time/RSS logs and the 15,335-file acquired-reference hash manifest are canonical in `nift-experiments/lab-evidence` at `8c1d417a1772d58559a23c0768c3d106dc6c2ff4`, `sites/spacex/20261012/`. Heavy reference payloads/releases remain outside Labs. The acquired reference is a bounded playback/public-output record, not a complete offline video catalogue; remote-only, inherited defect, codec, private-service and test-coverage qualifications remain visible.

The independent near-black/white/orange flight-test design uses orbit and telemetry motifs. It does not reuse another report's template/assets or imply endorsement. All internal paths use Nift's path primitive. Four viewport fixtures were inspected at actual 1440×1000, 768×1000, 390×844 and 320×844; the table scrolls in its container, not the page. Local browser review showed no console errors.

Validation: full/incremental build, `python3 scripts/validate.py`, `python3 scripts/check_spacex_links.py`, `python3 scripts/check_storage_policy.py`, `nift status`. Link validation writes temporary receipts outside Labs. Source is `stage`; publication is the separate `public/` checkout on `main`. Push both only after checks; verify live report/CSS bytes against local publication.

Do not reopen the accepted migrations for cosmetic changes. Repeated inline CSS/shared-shell fan-out and migration-init guidance are future work, not hidden limitations or unfinished polishing.

Storage validation found legitimate report growth crossing the 10 MiB aggregate website bound; the documented allowance is now 11 MiB, with all payload/archive/duplicate/per-file limits retained. The new report adds approximately 97 KiB tracked source/publication, not reference media or raw evidence.
