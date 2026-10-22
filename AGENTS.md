# AGENTS.md

Guidance for AI coding agents (Codex, Claude Code, etc.) working in this repository.

## What this repo is

The source of the book *System Design and Architecture* (2nd Edition, work in progress) by Tian Pan. It is a pure Markdown content repo built with GitBook — there is no application code, test suite, or linter.

## Commands

```sh
make install   # nvm use v10 && npm install gitbook-cli -g  (gitbook-cli needs Node 10)
make dev       # gitbook serve — local preview
make build     # PDF/EPUB/MOBI into ./_book/ (needs calibre's ebook-convert)
```

`_book/` and `*.pdf` are gitignored.

## Structure

- `en/` and `zh-CN/` — one Markdown file per chapter. The two directories mirror each other with **identical filenames** (zh-CN additionally has its own `README.md` index). When adding or renaming a chapter, do it in both languages.
- `README.md` — the English landing page and table of contents (product-icon table for "System Design in Practice", bullet lists for "Theories" and "Interview prep"). Links use `./en/<file>.md`.
- `SUMMARY.md` — GitBook's navigation; controls what appears in the built book. It only links `en/` files and is maintained separately from `README.md`, so a new chapter must be added to both.
- `zh-CN/README.md` — Chinese index; links are relative within `zh-CN/` (no `./zh-CN/` prefix).
- `drafts/` — unpublished notes, not linked from SUMMARY.
- `awesome-system-design.md` — external resource list.

## Chapter conventions

- Filenames are `<number>-<slug>.md` (or older `YYYY-MM-DD-<slug>.md`). The number is a stable ID shared with the author's site `https://tianpan.co/notes/<slug>`; don't renumber existing files.
- Every chapter starts with YAML front matter; keep `slug` and `id` equal to the filename without `.md`, and keep them identical between `en/` and `zh-CN/` (only `title` and `tags` are translated, e.g. `[system design]` → `[系统设计]`):

  ```yaml
  ---
  slug: 120-designing-uber
  id: 120-designing-uber
  title: "Designing Uber"
  date: 2019-01-03 18:39
  comments: true
  tags: [system design]
  references:
     - https://...
  ---
  ```

- Cross-references between chapters inside chapter bodies use absolute URLs `https://tianpan.co/notes/<slug>` (recent commits converted bare relative slugs to this form), not relative paths.
- Images are mostly hosted externally (`res.cloudinary.com`). Local images go in `images/` at the repo root and are referenced from chapters as `../images/<file>`, so the same path works from `en/` and `zh-CN/`.
- Design chapters generally follow the book's 4-step framework: clarify requirements → high-level design → component deep dive → wrap-up/bottlenecks.

## Agent skills and the `.pm` board

Development workflows live in `.agents/skills/<name>/SKILL.md` (read by Codex); Claude Code reads the same files through the relative symlink `.claude/skills -> ../.agents/skills`. Edit the canonical files and keep the link relative. Ported from the `beancount-io` repo and adapted to this book.

| Skill | Purpose |
| ----- | ------- |
| `pm` | Maintain the public `.pm/` board (pillars B1 content quality, B2 bilingual parity, B3 reach/build health); the only writer of `.pm/`. |
| `pm-brainstorm` | Propose milestones/tasks as text for `/pm` to materialize. |
| `loopx` | Drain a workstream (`/loopx w1`): triage, write, ship, close, block, or drop each item. |
| `ship` | Rebase, commit, and push. |
| `mermaid` | Draw and syntax-check Mermaid diagrams (`npx @mermaid-js/mermaid-cli`); GitBook needs a rendered image or plugin. |
| `dont-code-but-answer` | Read-only Q&A: answer without editing files. |

Board hard constraints are in `.pm/DO_NOT_DO.md`. Scratch files go in `.agents/tmp/` (gitignored).
