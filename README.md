# Pleasantview Townhome Supply Map

Interactive townhome supply pipeline map for Pleasantview and area, Edmonton.
Same map design and behaviour as the Downtown + Wîhkwêntôwin supply map
(`neilmah12/Downtown-and-area-supply`), retooled for townhome product.

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

## Adding project data

`PROJECTS` currently ships empty, with a commented template row. Add one dict
per townhome project to the `PROJECTS` list in **both** `supply_map_colab.py`
and `build_site.py`:

```python
{"id": 0, "name": "Project Name", "address": "0000 00 Ave NW", "units": 0,
 "status": "Proposed", "year_built": None, "est_completion": None,
 "lat": 53.4825, "lng": -113.5075},
```

- `id` must be the row's index in the list (0, 1, 2, ...) — the sidebar and
  marker selection logic index into `PROJECTS` by `id`.
- `status` must be one of `Stabilized`, `Active`, `Under Construction`,
  `Proposed`. These drive the marker colours and the filter tabs.
- `year_built` shows for built product, `est_completion` for in-progress
  product; set the other to `None`. Neither shows on `Proposed`.

Header stats (stabilized units, active projects, UC units, proposed units)
are computed from `PROJECTS` automatically, so there is nothing to update by
hand when project data changes.

## Map view

The initial view is set in the HTML template in both files:

```js
map.setView([53.4825, -113.5075], 15);
```

Adjust the centre/zoom if the project set extends past Pleasantview.

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
