#!/usr/bin/env python3
"""Convert exported posts CSV into Jekyll _posts/_drafts markdown files."""
import csv
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "_posts"
DRAFTS_DIR = REPO_ROOT / "_drafts"


def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "untitled"


def yaml_quote(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_date(created_at):
    # "2026-05-23 19:49:11.184 +0700" -> ("2026-05-23", full string for front matter)
    date_part = created_at.strip().split(" ")[0]
    return date_part


def build_front_matter(row, slug):
    lines = ["---"]
    lines.append(f"title: {yaml_quote(row['title'])}")
    if row.get("excerpt"):
        lines.append(f"description: {yaml_quote(row['excerpt'])}")
    lines.append(f"date: {parse_date(row['created_at'])}")
    if row.get("language"):
        lines.append(f"categories: [{row['language']}]")
    lines.append(f"slug: {slug}")
    lines.append("---")
    return "\n".join(lines)


def convert(csv_path):
    seen_slugs = {}
    published_count = 0
    draft_count = 0

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("deleted_at"):
                continue

            title = row["title"]
            slug = row.get("slug") or slugify(title)

            # de-dupe slugs (e.g. draft + published copy of the same title)
            base_slug = slug
            n = 2
            while slug in seen_slugs:
                slug = f"{base_slug}-{n}"
                n += 1
            seen_slugs[slug] = True

            date = parse_date(row["created_at"])
            front_matter = build_front_matter(row, slug)
            body = front_matter + "\n\n" + row["content"].strip() + "\n"

            if row.get("status") == "draft":
                out_path = DRAFTS_DIR / f"{slug}.md"
                draft_count += 1
            else:
                out_path = POSTS_DIR / f"{date}-{slug}.md"
                published_count += 1

            out_path.write_text(body, encoding="utf-8")
            print(f"wrote {out_path.relative_to(REPO_ROOT)}")

    print(f"\nDone: {published_count} published, {draft_count} draft(s) skipped from build.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <path-to-posts.csv>")
        sys.exit(1)
    POSTS_DIR.mkdir(exist_ok=True)
    DRAFTS_DIR.mkdir(exist_ok=True)
    convert(sys.argv[1])
