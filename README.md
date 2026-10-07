# Nift Labs

Public experiments, benchmarks, scaling investigations, framework comparisons,
runtime/scripting, languages, FFI, packages, and other Nift research.
Only collections with published content are active. Website reports are the first
collection, not the scope of the entire lab.

## Structure and ownership

- `/`: `content/index.html`, the general Labs homepage.
- `/sites/`: `content/sites/index.html`, the website-experiment catalogue.
- `/sites/<slug>/`: `content/sites/<slug>/index.html`, an experiment report.
- Labs templates: `templates/labs/`; Labs assets: `public/labs/`.
- Independent experiment templates: `templates/sites/<slug>/`.
- Independent experiment assets: `public/sites/<slug>/assets/`.
- Catalogue metadata: `content/data/sites.json`.

The source repository uses `stage`. `public/` is an existing, separate deployment
repository on `main`. Preserve both histories. Static assets are edited directly
in `public/`; generated HTML is built from the source repository. Commit source
changes in the source repository and assets/generated output in `public/`.
No deployment or push is implied by a local build or commit.

## Add a website experiment

1. Choose a stable slug and URL `/sites/<slug>/`.
2. Add `content/sites/<slug>/index.html` and any experiment-owned data under that
   directory. The current entries are reports about large external corpora;
   those thousands of benchmark pages are not vendored into this Labs project.
3. Create independent `template.html` and `head.html` in
   `templates/sites/<slug>/`. Include the head with `@input` and execute `@content`
   exactly once. Do not force experiments through a shared website template.
4. Put CSS, JS, fonts, images, icons, and other assets under
   `public/sites/<slug>/assets/`. Use `@path('public/sites/<slug>/assets/...')`
   for local asset links, and `@path('sites/<slug>/')` for the report page.
   Namespace all assets; do not reuse another experiment's asset directory.
5. Add a minimal tracking entry to `.nift/tracked.json`:

   ```json
   {
     "name": "sites/<slug>/",
     "title": "Descriptive experiment title",
     "template": "templates/sites/<slug>/template.html"
   }
   ```

   Nift derives `content/sites/<slug>/index.html` and
   `public/sites/<slug>/index.html` from the trailing-slash name. Do not track
   static assets unless they need Nift rendering. Run `nift build` immediately
   after changing tracking or config. Keep `.nift/` intact.
6. Add an object to `content/data/sites.json`. Required display fields are
   `name`, `slug`, `page` (the tracked name), `description`, `category`, `status`,
   `upstream_framework`, and `page_count` (the experiment corpus size, not the
   number of Labs report pages). Keep descriptions accurate and counts qualified.
   The homepage and catalogue share `templates/labs/entry.html`.
7. Record `upstream_repo`, the exact 40-character `upstream_commit`, and
   `experiment_repo`. Optional fields may include `date`, capture date, upstream
   build command, benchmark/report links, and measurement scope. Use null for
   genuinely unknown provenance and document why. Cloudflare's SHA is recorded;
   Omarchy's SHA was absent from the supplied report and still needs recovery
   from the experiment's original capture records. Do not substitute current HEAD.
8. Build and validate before committing. No permanent upstream fork is needed for
   provenance: a repository URL and exact commit normally suffice. Store patches
   or use a fork only when comparison changes actually require them.

## Design and methodology

The pages hosted on `lab.nift.dev` / `labs.nift.dev`, including the Labs
homepage, catalogue, and experiment **report pages**, must use dark mode,
regardless of OS preference. No blue belongs in those palettes, including links,
focus rings, charts, gradients, hover states, and browser theme metadata.

This rule does **not** apply to recreated experiment websites maintained in their
own repositories. Those sites may preserve their upstream design language,
support light/dark themes, and use blue. In particular, both Capgo websites should
follow the existing Capgo visual family. The published sibling experiments are
[`capgo`](https://github.com/nift-experiments/capgo), the faithful human+agent migration, and [`capgo-agent`](https://github.com/nift-experiments/capgo-agent),
the agent-native reconstruction with maintained converted HTML. Layouts may differ
where maintainability benefits; different branding is not the experiment goal.
Both prefer HTML/CSS/vanilla JS and allow justified local framework islands for
complex state. Future reports compare build/system and equivalent maintenance
work separately. Their published comparison is `/sites/capgo/`; frozen revisions, benchmark scope and limitations are recorded there.
Do not confuse a Labs report about an experiment with the experiment website.

There is no blanket static-only requirement for experiment websites. Nift can
compose pages and assets while ordinary client/server tooling handles APIs and
runtime features. Downloaded projects should be usable with users' own API
configuration. GitHub Pages can host a static preview, but cannot run backend
features; document the full application's local and deployment requirements.

Labs report designs remain independent: the parent catalogue has a
charcoal/amber notebook identity, Cloudflare a warm orange editorial layout,
and Omarchy a green technical layout.

Use public content corpora to investigate real workloads and implementation
characteristics. Pixel-perfect upstream migration is not the default goal.
Similar independent designs, completely new designs, and Nift-native choices
are welcome. The Cloudflare experiment's extensive parity work is an explicit
experiment constraint, not a requirement for every future entry. Reports must
state measurement boundaries and limitations rather than imply universal rankings.

## Pagination

Nift renders all JSON entries into the catalogue using the shared entry template.
`public/labs/catalogue.js` handles pagination in the browser with eight entries
per page and shareable URLs `/sites/?page=2`, `/sites/?page=3`, etc. It hides cards
outside the selected page, creates previous/next links, and supports browser
back/forward. There is no Nift pagination metadata, `@item`, or `@paginate`.
Pagination controls appear only when there is more than one page. With JavaScript
disabled all entries remain visible. Change `data-page-size` in
`content/sites/index.html` to adjust the page size. Data changes still use Nift's
ordinary JSON/template dependency tracking.

## Build and validation

Run from this directory:

```sh
nift build --all
nift build
nift build /
nift build sites/
nift build sites/cloudflare-docs/
nift build sites/omarchy/
python3 scripts/validate.py
nift status
```

For a fresh-output build without deleting the deployment checkout, copy sources
and static assets into a temporary directory, retaining `.nift/config.json` and
`.nift/tracked.json`, and run `nift build --all` there. Do not remove `.git` or
wipe `public/`. Preview with `python3 -m http.server --directory public`.

Check desktop and mobile rendering, section navigation, assets, metadata, and
pagination when adding entries. Existing report content and measured results
should remain intact when reorganising routes.

Other collections can add `content/<category>/`, `templates/<category>/`, and
`public/<category>/` independently; nothing assumes all future research is a site.

## Benchmark publication

The October benchmark articles have independent templates and palettes in
`templates/benchmarks/` and `public/benchmarks/*/assets/`. Their content and
standalone startup figure are generated from retained raw JSON, not hand-entered
medians. After acquiring the campaign evidence in `content/benchmarks/data/`:

```sh
python3 -m venv .venv-benchmarks
.venv-benchmarks/bin/pip install -r scripts/requirements-benchmarks.txt
.venv-benchmarks/bin/python scripts/render_benchmarks.py
nift build --all
python3 scripts/validate.py
```

The generator rejects non-publishable runs or incorrect samples and checks raw
medians/sample counts against retained summaries. Use each suite's
`scripts/summarize.py` to regenerate every distribution statistic independently.
The plotting library is a publication dependency only, outside all measurements.
Retain historical diagnostics separately; never merge them into official tables.
