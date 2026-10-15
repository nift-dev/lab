# Nift + TanStack — publication record

Prepared and approved for publication 2026-10-15. External announcements and outreach remain unauthorized. No benchmark was rerun and no experiment or Nift core source was changed.

Preview: http://127.0.0.1:4174/integrations/tanstack/ ; collection: http://127.0.0.1:4174/integrations/ . Serve with `python3 -m http.server 4174 --bind 127.0.0.1 --directory public` from Labs if needed.

The new Integrations collection has its own metadata/card template and shared navigation entry. Migrations and Benchmarks remain in place; Agora remains a migration. The report uses a charcoal/lime pipeline-board design and ten paired time/tree-RSS plots. It distinguishes the original prototype, integrated Start application, optimized Start control and Nift-first islands. Conditional recommendations and slower scenarios remain prominent.

## Evidence

Canonical experiment revision: `c7469b59ba2ccf519ab85ae83485ed3783545a8f` in `nift-experiments/nift-tanstack`. The renderer verifies source hashes through the evidence index. Only a compact rendering summary is stored in Labs; raw evidence, logs and screenshots remain outside it. All measurements are single observations. Tree RSS and maximum individual-process RSS are labelled separately; JS bodies are uncompressed, and output/server contracts differ.

## Review checks

- Complete Nift build and incremental status; renderer freshness and numerical checks.
- Local HTML/metadata/link validation: 26 HTML documents, 738 references.
- All 15 pinned repository/evidence links resolve.
- Ten zero-origin plots; values checked against canonical inputs.
- Report responsive review at actual widths 1425, 375 and 305 CSS pixels; collection and homepage mobile checks. Wide tables scroll within their own containers.
- Report has one main landmark and one h1, no empty links, native disclosure controls, and no JavaScript dependency. Scoped palette contrast minimum 7.62:1 for checked text/surface combinations; this is not a full accessibility certification.
- Existing report content/assets remain byte-identical. Shared catalogue outputs intentionally gain Integrations navigation; homepage gains category and card.

Recheck with:

```sh
python3 scripts/render_tanstack_integration.py --check
nift build --all
nift build
python3 scripts/validate.py
python3 scripts/check_tanstack_integration_links.py
python3 scripts/check_storage_policy.py
```

Publication approved by the user on 2026-10-15. Release removes draft labels and follows the established source-stage then publication-main push sequence.

## Design/editorial revision

Replaced the hero board with connected static-generation and selective-interaction modules. Nift green, TanStack coral and interface lavender express ownership; modular card shapes and monospace hero give this report its own identity. Removed the underscore. Scoped all full-stack statements to the evaluated implementations: standalone Nift full-stack development was not evaluated, and no general preference is inferred. Ten chart values/scales and evidence pins remain unchanged. Rebuilt, rechecked all 15 evidence links, mobile overflow and text contrast. Publication approved after this revision.
