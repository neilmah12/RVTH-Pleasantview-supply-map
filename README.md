# Existing Townhome Supply Map — River Valley & Pleasantview

Interactive map of **existing** townhome supply across Edmonton, built to
support a comparison study between two subject sites: **River Valley
Townhomes** (4210 102 Ave NW, 216 units) and **Pleasantview Townhomes**
(4905 107 St NW, 216 units). Same map design/build pipeline as the Downtown +
Wîhkwêntôwin supply map (`neilmah12/Downtown-and-area-supply`), retooled for
existing-stock comps instead of an upcoming-supply pipeline.

## Files

- `supply_map_colab.py` — Colab-editable source. Edit `PROJECTS`, run the
  cell, and it writes a standalone HTML file you can download for manual use
  (deck screenshots, email attachments).
- `build_site.py` — same generator, kept in sync with `supply_map_colab.py`,
  but writes to `public/index.html` for the Firebase Hosting deploy step
  instead of a Colab download. **This is the file the live site is actually
  built from** — if you edit project data, update both files (or copy
  `supply_map_colab.py`'s `PROJECTS` over into `build_site.py`).
- `public/` — generated at build time by `build_site.py`. Not committed
  (gitignored); GitHub Actions regenerates it on every push to `main`.

## What's on the map

131 existing townhome properties (Edmonton-wide CoStar inventory, deduped and
geocoded), including the two subject sites. Two header chips ("River Valley
Townhomes" / "Pleasantview Townhomes") pan/zoom straight to each subject site
and open its detail card — built for quick presentation.

Every property card has an **include/exclude checkbox** for narrowing the
comp set down by hand (e.g. by proximity, product type, condition) — state is
saved in the browser's local storage so it survives a page reload. Each
comp's sidebar/detail card also shows straight-line distance (km) to the
nearer of the two subject sites, and the list can be sorted by distance,
units, name, or year built.

**Export to Excel** (header button) downloads the full 131-property table —
including your current include/exclude picks and each comp's distance to
both subject sites — as an `.xlsx` file, so you can keep working the
shortlist outside the map.

## Adding / editing project data

Add or edit one dict per property in the `PROJECTS` list in **both**
`supply_map_colab.py` and `build_site.py`:

```python
{"id": 0, "name": "Project Name", "address": "0000 00 Ave NW", "units": 0,
 "year_built": None, "subdivision": None, "lat": 53.4825, "lng": -113.5075,
 "subject": False},
```

- `id` must be the row's index in the list (0, 1, 2, ...) — the sidebar and
  marker selection logic index into `PROJECTS` by `id`.
- `subject: True` marks River Valley Townhomes / Pleasantview Townhomes —
  it drives the navy marker colour, the header quick-jump chips, and the
  "SUBJECT SITE" tag. Leave `False` for comps.
- `year_built` / `subdivision` may be `None` if unknown.

Header stats (properties, total units, included, included units) are
computed client-side from `PROJECTS` + the include/exclude state, so nothing
needs to be updated by hand when project data changes.

## Map view

The map fits its bounds to every property in `PROJECTS` on load — no fixed
centre/zoom to maintain. If you trim `PROJECTS` down to a tighter comp set
later, the initial view will automatically tighten with it.

## One-time Firebase setup

1. Create a Firebase project in the [Firebase console](https://console.firebase.google.com)
   with Hosting enabled.
2. Project Settings → Service Accounts → generate a new private key (downloads
   a JSON file).
3. In this repo: Settings → Secrets and variables → Actions → New repository
   secret, named `FIREBASE_RVTH_PLEASANTVIEW`, value = the full JSON file
   contents.
4. `.firebaserc` and `.github/workflows/firebase-deploy.yml` are currently set
   to the `rvth-pleasantview-supply` Firebase project ID. If your Firebase
   project ID differs, update it in both files.
5. Push to `main` — the workflow builds and deploys automatically.
