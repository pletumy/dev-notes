#!/usr/bin/env python3
"""Convert exported posts CSV into VitePress markdown pages under docs/notes/."""
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = REPO_ROOT / "docs" / "notes"
SIDEBAR_PATH = REPO_ROOT / "docs" / ".vitepress" / "sidebar.json"


def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "untitled"


def yaml_quote(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_date(created_at):
    return created_at.strip().split(" ")[0]


UUID_IMAGE_RE = re.compile(
    r"!\[([^\]]*)\]\(([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\)"
)


def strip_missing_images(content, missing_images):
    def replace(match):
        alt = match.group(1) or "ảnh"
        missing_images.append(alt)
        return f"> ⚠️ Ảnh thiếu: **{alt}** (không có trong dữ liệu export, cần upload lại thủ công)"

    return UUID_IMAGE_RE.sub(replace, content)


def build_front_matter(row):
    lines = ["---"]
    lines.append(f"title: {yaml_quote(row['title'])}")
    if row.get("excerpt"):
        lines.append(f"description: {yaml_quote(row['excerpt'])}")
    lines.append(f"date: {parse_date(row['created_at'])}")
    lines.append("---")
    return "\n".join(lines)


def convert(csv_path):
    seen_slugs = {}
    sidebar_items = []
    published_count = 0
    draft_count = 0

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("deleted_at"):
                continue
            if row.get("status") == "draft":
                draft_count += 1
                continue

            title = row["title"]
            slug = row.get("slug") or slugify(title)

            base_slug = slug
            n = 2
            while slug in seen_slugs:
                slug = f"{base_slug}-{n}"
                n += 1
            seen_slugs[slug] = True

            missing_images = []
            content = strip_missing_images(row["content"].strip(), missing_images)
            if missing_images:
                print(f"  ! {slug}: {len(missing_images)} missing image(s)")

            front_matter = build_front_matter(row)
            body = front_matter + "\n\n" + content + "\n"

            out_path = NOTES_DIR / f"{slug}.md"
            out_path.write_text(body, encoding="utf-8")
            sidebar_items.append({"text": title, "link": f"/notes/{slug}"})
            published_count += 1
            print(f"wrote {out_path.relative_to(REPO_ROOT)}")

    sidebar_items.sort(key=lambda x: x["text"])

    other_sections = []
    if SIDEBAR_PATH.exists():
        existing = json.loads(SIDEBAR_PATH.read_text(encoding="utf-8"))
        other_sections = [section for section in existing if section.get("text") != "Notes"]

    sidebar = [{"text": "Notes", "items": sidebar_items}] + other_sections
    SIDEBAR_PATH.write_text(
        json.dumps(sidebar, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {SIDEBAR_PATH.relative_to(REPO_ROOT)}")
    print(f"\nDone: {published_count} published, {draft_count} draft(s) skipped.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <path-to-posts.csv>")
        sys.exit(1)
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    SIDEBAR_PATH.parent.mkdir(parents=True, exist_ok=True)
    convert(sys.argv[1])
