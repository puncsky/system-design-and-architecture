#!/usr/bin/env python3
"""Unit tests for scripts/check-book.py, run against throwaway book trees."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("check_book", Path(__file__).with_name("check-book.py"))
check_book = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_book)


def chapter(slug: str, body: str = "text\n", id_: str | None = None) -> str:
    return f"---\nslug: {slug}\nid: {id_ or slug}\ntitle: \"T\"\n---\n\n{body}"


def zh_chapter(slug: str, body: str = "文本\n") -> str:
    return f"---\nslug: {slug}\nid: {slug}\ntitle: \"标题\"\n---\n\n{body}"


def make_book(root: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


class CheckBookTest(unittest.TestCase):
    def run_checks(self, files: dict[str, str]) -> list[str]:
        base = {"README.md": "# Book\n", "SUMMARY.md": "# Summary\n", "zh-CN/README.md": "# 中文\n"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_book(root, {**base, **files})
            return check_book.run(root)

    def test_clean_book_has_no_problems(self) -> None:
        files = {"en/1-a.md": chapter("1-a"), "zh-CN/1-a.md": zh_chapter("1-a")}
        self.assertEqual(self.run_checks(files), [])

    def test_slug_must_match_filename(self) -> None:
        files = {"en/1-a.md": chapter("1-b", id_="1-a"), "zh-CN/1-a.md": zh_chapter("1-a")}
        self.assertEqual(self.run_checks(files), ["en/1-a.md: slug is '1-b', expected '1-a'"])

    def test_id_must_match_filename(self) -> None:
        files = {"en/1-a.md": chapter("1-a", id_="x"), "zh-CN/1-a.md": zh_chapter("1-a")}
        self.assertEqual(self.run_checks(files), ["en/1-a.md: id is 'x', expected '1-a'"])

    def test_missing_front_matter_is_reported(self) -> None:
        files = {"en/1-a.md": "no front matter\n", "zh-CN/1-a.md": zh_chapter("1-a")}
        self.assertEqual(self.run_checks(files), ["en/1-a.md: missing YAML front matter"])

    def test_chapter_missing_in_one_language(self) -> None:
        files = {"en/1-a.md": chapter("1-a"), "zh-CN/2-b.md": zh_chapter("2-b")}
        self.assertEqual(
            self.run_checks(files),
            ["zh-CN/2-b.md: no matching en/ chapter", "en/1-a.md: no matching zh-CN/ chapter"],
        )

    def test_broken_summary_link(self) -> None:
        files = {"SUMMARY.md": "* [Gone](./en/9-gone.md)\n"}
        self.assertEqual(self.run_checks(files), ["SUMMARY.md: broken link ./en/9-gone.md"])

    def test_external_anchor_and_site_absolute_links_are_ignored(self) -> None:
        body = "[a](https://example.com/x) [b](#top) [c](/notes/1-a) ![d](/img/x.png)\n"
        files = {"en/1-a.md": chapter("1-a", body), "zh-CN/1-a.md": zh_chapter("1-a")}
        self.assertEqual(self.run_checks(files), [])

    def test_local_image_must_exist(self) -> None:
        files = {
            "en/1-a.md": chapter("1-a", "![x](../images/p.png)\n"),
            "zh-CN/1-a.md": zh_chapter("1-a", "![x](../images/q.png)\n"),
            "images/p.png": "",
        }
        self.assertEqual(self.run_checks(files), ["zh-CN/1-a.md: broken link ../images/q.png"])

    def test_html_img_src_is_checked(self) -> None:
        files = {"README.md": '<img src="./images/none.png" />\n'}
        self.assertEqual(self.run_checks(files), ["README.md: broken link ./images/none.png"])

    def test_title_is_required(self) -> None:
        no_title = "---\nslug: 1-a\nid: 1-a\n---\n\ntext\n"
        files = {"en/1-a.md": no_title, "zh-CN/1-a.md": zh_chapter("1-a")}
        self.assertEqual(self.run_checks(files), ["en/1-a.md: missing title"])

    def test_formal_you_is_rejected_in_zh_only(self) -> None:
        files = {"en/1-a.md": chapter("1-a", "您\n"), "zh-CN/1-a.md": zh_chapter("1-a", "您好\n")}
        self.assertEqual(self.run_checks(files), ["zh-CN/1-a.md: use informal \u4f60, not formal \u60a8"])

    def test_untranslated_zh_copy_is_rejected(self) -> None:
        files = {"en/1-a.md": chapter("1-a"), "zh-CN/1-a.md": chapter("1-a")}
        self.assertEqual(self.run_checks(files), ["zh-CN/1-a.md: identical to en/1-a.md (untranslated)"])

    def test_code_fence_wrapped_file_is_rejected(self) -> None:
        wrapped = "```markdown\n" + chapter("1-a") + "```\n"
        files = {"en/1-a.md": wrapped, "zh-CN/1-a.md": zh_chapter("1-a")}
        self.assertIn("en/1-a.md: whole file is wrapped in a code fence", self.run_checks(files))

    def test_orphaned_front_matter_in_body(self) -> None:
        files = {"en/1-a.md": chapter("1-a", "tags: [x]\n"), "zh-CN/1-a.md": zh_chapter("1-a")}
        self.assertEqual(self.run_checks(files), ["en/1-a.md: front matter field 'tags' appears in the body"])

    def test_front_matter_key_inside_code_fence_is_fine(self) -> None:
        body = "```yaml\ntitle: x\n```\n"
        files = {"en/1-a.md": chapter("1-a", body), "zh-CN/1-a.md": zh_chapter("1-a", body + "译\n")}
        self.assertEqual(self.run_checks(files), [])


if __name__ == "__main__":
    unittest.main()
