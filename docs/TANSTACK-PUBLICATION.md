# TanStack.com — bounded migration phase publication

Published route: https://lab.nift.dev/sites/tanstack/

Disposition: **migration unsuccessful / poor architectural fit; rewrite planned**. The rewrite is not started. This is a useful negative result about retained application architecture, not a blanket judgement about Nift or TanStack. No new measurements, implementation changes or Nift core changes belong to this publication pass.

Frozen authored repository: `7af3af0141e09248dacfc11f722c495abadd96a4`.
Frozen agent repository and canonical evidence: `8bd68069410f984a5949e7fa0e629b6084c1caee`.
Pinned upstream application: `862ccc3d191818320c3e6d217542883f80cb907a`.

`content/data/evidence-sources.json` pins hashes/paths for T12 raw samples, summaries, components, reproduction and both rejection receipts, plus the separate T10 summary. The generator acquires and SHA-verifies these in an external temporary cache. Only the compact summary, maintained HTML and actual displayed assets enter Labs. Normal Nift builds need no network, renderer or experiment checkout.

Run `python3 scripts/render_tanstack.py`, `nift build --all`, `nift build`, `python3 scripts/validate.py`, `python3 scripts/check_tanstack_links.py`, `python3 scripts/check_storage_policy.py`, and `nift status`.

The generator recomputes all T12 medians/ranges from 80 raw rows. The preserved T10 225 observations remain historical; native ready-input refresh and complete Nift publication are distinct scopes. The broader T11 replacement 225-row campaign is pending, not relabeled complete. T12 A/B are two agent-source engine variants, not authored/rendered models. Browser and backend compilation costs remain included when required. Maximum individual-process RSS and nominal 50ms sampled tree RSS remain separate, and the incremental graph uses a linear zero-origin 0–5,000 MiB scale with text values. Whole-page/session and article/HTML-authority failures are explicit rejected branches, never successful timed migrations. Approximate phase memory attribution is not an allocator diagnosis.

Design is page-local: charcoal/amber/copper boundary map, terminated fork traces, measured tradeoff rails and a separate planned rewrite state. No other report assets/templates are reused. Public design does not imply TanStack endorsement. The homepage/catalogue keep their shared family identity.

Local browser checks at 1440, 768, 390 and 320 pixels verify no document overflow, dark mode, status/benchmark text, 14 evidence links and anchor navigation. Hero/status, architecture diagrams, branch traces and measurement layouts were manually inspected. A mobile hidden-line-break word-spacing defect was fixed before publication. Wide numeric tables scroll inside focusable regions with warm focus rings; key measurements remain visible as text. Screenshots and audit previews live outside Labs, under `/tmp`, and are not published assets.

Fresh-output regeneration rebuilt all 14 tracked report/index pages and reproduced all 80 maintained publication files exactly; static archives remain maintained assets. See tanstack-fresh-build.json, tanstack-viewport-validation.json and tanstack-link-validation.json. The central incremental-memory audit includes this new report without regenerating historical cohorts.

Source branch is `stage`; the separate deployment checkout uses `main`. Commit/push both normally; never rewrite history. After deployment verify the live page, generated asset bytes and catalogue links. Keep both experiment repositories clean and at the pinned T12 checkpoints. The planned rewrite needs a future explicit work phase, not this publication.
