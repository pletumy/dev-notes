# Learning Notes

Jekyll site publishing notes exported from the posts DB, hosted on GitHub Pages.

## Regenerate posts from a new CSV export

```bash
python3 scripts/csv_to_posts.py /path/to/posts_export.csv
```

- Rows with `status: draft` go to `_drafts/` (excluded from the build).
- Rows with `deleted_at` set are skipped entirely.
- Empty `slug` values are auto-generated from the title.
- Duplicate slugs get a `-2`, `-3`, ... suffix.

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

## Deploy

Settings → Pages → Build and deployment → Source: Deploy from a branch → `main` / `/ (root)`.
