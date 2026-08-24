# Dev Notes

VitePress site publishing notes exported from the posts DB, hosted on GitHub Pages.
Structure follows [omnivore-app/docs.omnivore](https://github.com/omnivore-app/docs.omnivore).

## Regenerate notes from a new CSV export

```bash
python3 scripts/csv_to_posts.py /path/to/posts_export.csv
```

- Rows with `status: draft` or `deleted_at` set are skipped.
- Empty `slug` values are auto-generated from the title.
- Duplicate slugs get a `-2`, `-3`, ... suffix.
- Images referenced by a bare UUID (no real file in the export) are replaced with a
  "missing image" warning block — re-upload those manually under `docs/notes/` and
  fix the link.
- Sidebar entries are regenerated into `docs/.vitepress/sidebar.json`.

## Local dev

```bash
npm install
npm run docs:dev
```

## Build

```bash
npm run docs:build
```

## Deploy

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the site and
publishes `docs/.vitepress/dist` to the `gh-pages` branch via `peaceiris/actions-gh-pages`.

In GitHub: Settings → Pages → Source: Deploy from a branch → `gh-pages` / `/ (root)`
(first appears after the first successful Action run).
