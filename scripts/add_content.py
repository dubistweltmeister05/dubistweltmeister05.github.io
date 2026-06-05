#!/usr/bin/env python3
"""
add_content.py — Add a markdown file to the Jekyll site with proper front matter.

Usage:
    python3 scripts/add_content.py <file.md> [options]

Options:
    --type      Content type: post (default), page, portfolio
    --title     Title for the post/page
    --tags      Comma-separated list of tags (posts only)
    --excerpt   Short excerpt (portfolio only)
    --permalink Custom permalink (pages only)
    --date      Date override as YYYY-MM-DD (posts only, defaults to today)
    --dry-run   Print what would happen without writing any files

Example commands - 
# Blog post (auto-detected or explicit)
python3 scripts/add_content.py ~/my-draft.md --title "My New Post" --tags "embedded,rust"

# Page
python3 scripts/add_content.py ~/notes.md --type page --permalink /notes/

# Portfolio item
python3 scripts/add_content.py ~/project.md --type portfolio --excerpt "A cool project"

# Preview without writing anything
python3 scripts/add_content.py ~/my-draft.md --dry-run

"""

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

# Root of the Jekyll site (the directory containing this script's parent)
SITE_ROOT = Path(__file__).resolve().parent.parent

DEST_DIRS = {
    "post": SITE_ROOT / "_posts",
    "page": SITE_ROOT / "_pages",
    "portfolio": SITE_ROOT / "_portfolio",
}


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Return (front_matter_dict, body) from raw markdown text."""
    import yaml

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if match:
        try:
            fm = yaml.safe_load(match.group(1)) or {}
        except Exception:
            fm = {}
        body = text[match.end():]
    else:
        fm = {}
        body = text
    return fm, body


def build_front_matter(fm: dict) -> str:
    """Serialise a front-matter dict back to YAML fenced block."""
    import yaml

    return "---\n" + yaml.dump(fm, default_flow_style=False, allow_unicode=True) + "---\n"


def slugify(text: str) -> str:
    """Convert a title to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text


def infer_type_from_front_matter(fm: dict) -> str | None:
    collection = fm.get("collection", "")
    layout = fm.get("layout", "")
    if collection == "portfolio" or layout == "single" and "portfolio" in str(fm.get("permalink", "")):
        return "portfolio"
    if fm.get("permalink", "").startswith("/posts/"):
        return "post"
    return None


def build_post(fm: dict, args: argparse.Namespace, slug: str, post_date: date) -> dict:
    fm.setdefault("layout", "single")
    fm["title"] = args.title or fm.get("title") or slug.replace("-", " ").title()
    fm["date"] = post_date.isoformat()
    permalink = f"/posts/{post_date.year}/{post_date.month:02d}/{slug}/"
    fm["permalink"] = fm.get("permalink") or permalink
    if args.tags:
        fm["tags"] = [t.strip() for t in args.tags.split(",")]
    elif "tags" not in fm:
        fm["tags"] = []
    return fm


def build_page(fm: dict, args: argparse.Namespace, slug: str) -> dict:
    fm["title"] = args.title or fm.get("title") or slug.replace("-", " ").title()
    fm.setdefault("permalink", f"/{slug}/")
    if args.permalink:
        fm["permalink"] = args.permalink
    fm.setdefault("author_profile", True)
    return fm


def build_portfolio(fm: dict, args: argparse.Namespace, slug: str) -> dict:
    fm["title"] = args.title or fm.get("title") or slug.replace("-", " ").title()
    fm["collection"] = "portfolio"
    if args.excerpt:
        fm["excerpt"] = args.excerpt
    fm.setdefault("excerpt", fm["title"])
    return fm


def dest_filename(content_type: str, slug: str, post_date: date, suffix: str) -> str:
    if content_type == "post":
        return f"{post_date.isoformat()}-{slug}{suffix}"
    return f"{slug}{suffix}"


def main():
    parser = argparse.ArgumentParser(
        description="Add a markdown file to the Jekyll site with correct front matter."
    )
    parser.add_argument("file", help="Path to the source markdown file")
    parser.add_argument(
        "--type",
        choices=["post", "page", "portfolio"],
        default=None,
        help="Content type (default: auto-detect, fallback to 'post')",
    )
    parser.add_argument("--title", default=None, help="Title override")
    parser.add_argument("--tags", default=None, help="Comma-separated tags (posts)")
    parser.add_argument("--excerpt", default=None, help="Short excerpt (portfolio)")
    parser.add_argument("--permalink", default=None, help="Custom permalink (pages)")
    parser.add_argument(
        "--date",
        default=None,
        help="Date override YYYY-MM-DD (posts, default: today)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without writing files",
    )
    args = parser.parse_args()

    src = Path(args.file).resolve()
    if not src.exists():
        print(f"Error: file not found: {src}", file=sys.stderr)
        sys.exit(1)
    if src.suffix not in (".md", ".markdown"):
        print("Warning: file does not have a .md extension — continuing anyway.")

    raw = src.read_text(encoding="utf-8")
    fm, body = parse_front_matter(raw)

    # Determine content type
    content_type = args.type or infer_type_from_front_matter(fm) or "post"

    # Determine slug from title arg → existing fm title → filename stem
    title_for_slug = args.title or fm.get("title") or src.stem
    slug = slugify(str(title_for_slug))

    # Date (posts only)
    post_date = date.today()
    if args.date:
        try:
            post_date = date.fromisoformat(args.date)
        except ValueError:
            print(f"Error: invalid date format '{args.date}', expected YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
    elif content_type == "post" and fm.get("date"):
        try:
            raw_date = str(fm["date"])
            post_date = date.fromisoformat(raw_date[:10])
        except (ValueError, TypeError):
            pass

    # Build front matter for the chosen type
    if content_type == "post":
        fm = build_post(fm, args, slug, post_date)
    elif content_type == "page":
        fm = build_page(fm, args, slug)
    elif content_type == "portfolio":
        fm = build_portfolio(fm, args, slug)

    new_content = build_front_matter(fm) + "\n" + body.lstrip("\n")

    dest_dir = DEST_DIRS[content_type]
    dest_name = dest_filename(content_type, slug, post_date, src.suffix)
    dest_path = dest_dir / dest_name

    print(f"Content type : {content_type}")
    print(f"Destination  : {dest_path.relative_to(SITE_ROOT)}")
    print()
    print("--- Front matter preview ---")
    print(build_front_matter(fm))
    print("----------------------------")

    if args.dry_run:
        print("[dry-run] No files written.")
        return

    if dest_path.exists():
        answer = input(f"'{dest_path.name}' already exists. Overwrite? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(new_content, encoding="utf-8")
    print(f"Written: {dest_path}")


if __name__ == "__main__":
    main()
