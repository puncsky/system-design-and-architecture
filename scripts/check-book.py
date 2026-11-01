#!/usr/bin/env python3
"""Validate the book's chapter structure: front matter, en/zh-CN parity, and links."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LANGS = ("en", "zh-CN")
# Frontmatter keys that must never reappear in a chapter body (mirrors the site's
# detectOrphanedFrontmatter in tianpan-v4-web).
ORPHAN_FIELDS = (
    "title", "description", "keywords", "tags", "authors", "image", "sidebar_position",
    "sidebar_label", "slug", "draft", "date", "hide_table_of_contents",
)
FORMAL_YOU = "\u60a8"  # 您: the site's Chinese content uses informal 你 only
LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|\bsrc=\"([^\"]+)\"")


def front_matter(text: str) -> dict[str, str] | None:
    """Return the scalar keys of the leading YAML block, or None if absent."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    keys: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return keys
        match = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if match:
            keys[match.group(1)] = match.group(2).strip().strip("\"'")
    return None


def chapters(root: Path, lang: str) -> dict[str, Path]:
    return {p.name: p for p in sorted((root / lang).glob("*.md")) if p.name != "README.md"}


def check_front_matter(root: Path) -> list[str]:
    errors: list[str] = []
    for lang in LANGS:
        for name, path in chapters(root, lang).items():
            keys = front_matter(path.read_text(encoding="utf-8"))
            rel = path.relative_to(root)
            if keys is None:
                errors.append(f"{rel}: missing YAML front matter")
                continue
            if not keys.get("title"):
                errors.append(f"{rel}: missing title")
            stem = name[: -len(".md")]
            for key in ("slug", "id"):
                if keys.get(key) != stem:
                    errors.append(f"{rel}: {key} is {keys.get(key)!r}, expected {stem!r}")
    return errors


def body_after_front_matter(text: str) -> list[str]:
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return []
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[index + 1 :]
    return []


def orphaned_front_matter(text: str) -> list[str]:
    """Front matter keys that appear outside code fences after the leading block."""
    found: list[str] = []
    fences = 0
    pattern = re.compile(r"^(%s):" % "|".join(ORPHAN_FIELDS))
    for line in body_after_front_matter(text):
        stripped = line.strip()
        if stripped.startswith("```"):
            fences += 1
            continue
        if fences % 2 == 0:
            match = pattern.match(stripped)
            if match:
                found.append(match.group(1))
    return found


def check_site_rules(root: Path) -> list[str]:
    """Rules the website's test suite enforces on these chapters after import."""
    errors: list[str] = []
    for lang in LANGS:
        for path in chapters(root, lang).values():
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(root)
            stripped = text.strip()
            if stripped.startswith("```") and stripped.endswith("```"):
                errors.append(f"{rel}: whole file is wrapped in a code fence")
            for field in orphaned_front_matter(text):
                errors.append(f"{rel}: front matter field {field!r} appears in the body")
            if lang == "zh-CN" and FORMAL_YOU in text:
                errors.append(f"{rel}: use informal \u4f60, not formal \u60a8")
    en = chapters(root, "en")
    for name, zh_path in chapters(root, "zh-CN").items():
        en_path = en.get(name)
        if en_path and en_path.read_text(encoding="utf-8") == zh_path.read_text(encoding="utf-8"):
            errors.append(f"zh-CN/{name}: identical to en/{name} (untranslated)")
    return errors


def check_parity(root: Path) -> list[str]:
    en, zh = chapters(root, "en"), chapters(root, "zh-CN")
    errors = [f"zh-CN/{n}: no matching en/ chapter" for n in sorted(set(zh) - set(en))]
    errors += [f"en/{n}: no matching zh-CN/ chapter" for n in sorted(set(en) - set(zh))]
    return errors


# Root-absolute paths (/notes/..., /img/...) belong to the author's website, not this repo.
def local_target(base: Path, target: str) -> Path | None:
    if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith(("#", "/")):
        return None
    return (base / target.split("#", 1)[0].split("?", 1)[0]).resolve()


def check_links(root: Path) -> list[str]:
    """Index and chapter links, and local images, must resolve to real files."""
    pages = [root / "README.md", root / "SUMMARY.md", root / "zh-CN" / "README.md"]
    for lang in LANGS:
        pages += list(chapters(root, lang).values())
    errors: list[str] = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            target = match.group(1) or match.group(2)
            resolved = local_target(page.parent, target)
            if resolved is None or not resolved.name:
                continue
            if not resolved.exists():
                errors.append(f"{page.relative_to(root)}: broken link {target}")
    return errors


def run(root: Path) -> list[str]:
    return check_front_matter(root) + check_parity(root) + check_site_rules(root) + check_links(root)


def main() -> int:
    errors = run(REPO_ROOT)
    for error in errors:
        print(error)
    print(f"{len(errors)} problem(s)" if errors else "book structure ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
