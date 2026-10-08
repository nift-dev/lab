# Labs evidence storage

The Labs repository contains website source and compact rendering datasets only.
Canonical benchmark evidence lives in experiment repositories or the dedicated
[nift-experiments/lab-evidence](https://github.com/nift-experiments/lab-evidence)
repository. Large raw outputs, repeated input trees, verbose logs, binary archives,
caches and benchmark history do not belong in the website repository.

The source plus used publication assets should normally remain in single-digit MB;
a zipped source checkout should be a few MB or less. These are guidelines, not a
reason to remove genuine displayed assets or necessary rendering data. Git history
is measured separately and is never rewritten without explicit approval.

content/data/evidence-sources.json records exact canonical commits, paths and SHA256
hashes. Graph summaries carry their canonical source reference. Pages use pinned
GitHub URLs. Normal Nift builds render maintained HTML/templates and local compact
summaries without network access or an evidence checkout. Explicit report-generation
scripts retrieve SHA-verified frozen raw inputs via scripts/evidence_sources.py and
cache them outside Labs under the system temporary directory. Audits produce previews
outside Labs. The evidence repository indexes original relative paths and deduplicates
identical bytes, preserving environment, revisions, scope and sample policy.

Never mutate accepted migration implementations to update Labs evidence. Append a
new identified evidence cohort instead of replacing old measurements. Store only
compact validation receipts in Labs; verification screenshots are temporary unless
actually displayed. Keep generated publication assets only when used by a route.

Run `python3 scripts/check_storage_policy.py` before publication. It checks tracked
source/publication files for large evidence payloads, archives, logs, cache/build
paths and duplicate large JSON; genuine displayed assets have a separate allowance.
Untracked concurrent work is reported but never silently removed or published.
