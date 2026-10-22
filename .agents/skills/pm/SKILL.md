---
name: pm
description: Arrange the repository's public .pm board for the book — show status, create workstreams, capture inbox notes, promote notes into milestones, add tasks, mark work done, park blocked work, and drop unwanted work. Use only when the user explicitly invokes /pm or asks to update, arrange, or check the .pm board. Do not use for proposing new work (that is pm-brainstorm) or for ordinary chapter edits.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(find:*), Bash(cat:*), Bash(mkdir:*), Bash(git mv:*), Bash(mv:*)
metadata: {"internal": true}
---

# Task: Arrange the `.pm` board

Usage: `/pm [status | new workstream <title> | add <wN> <idea> | promote <wN/NNN> | new milestone <wN> <title> | add-task <wN/mN> <title> | done <wN/mN/tNNN or wN/NNN> | block <target> <reason> | unblock <target> | drop <target> <reason>]`

`/pm` is the **only** skill that writes to `.pm/`. `/pm-brainstorm` proposes; `/pm` materializes; `/loopx` drains. This file is the **canonical** definition of board conventions. Parse the subcommand from `$ARGUMENTS` (default `status`).

## Mission — the editor's lens

The board exists to make *System Design and Architecture* the best open, bilingual (en / zh-CN) system-design book. Sequence work by reader impact, not by what is fun to write. Every milestone names one pillar in `## Source + Goal linkage`:

| Pillar | Meaning |
| --- | --- |
| **B1 — Content quality** | New or improved chapters: correct, current, concrete (numbers, tradeoffs, diagrams), following the 4-step framework in `AGENTS.md`. |
| **B2 — Bilingual parity & consistency** | `en/` and `zh-CN/` mirror each other: filenames, front matter, structure, links, indexes (`README.md`, `SUMMARY.md`, `zh-CN/README.md`). |
| **B3 — Reach & build health** | Discoverability and delivery: tables of contents, cross-links, references, images/diagrams, `make build` health, tianpan.co sync. |

## The `.pm` hierarchy

| Level | Path | Meaning | Effort |
| --- | --- | --- | --- |
| Workstream | `wN/` | a general-purpose worker queue; `README.md` + inbox notes | — |
| Inbox note | `wN/NNN.md` | one idea or **sub-hour** unit of work, plain markdown | ≤ ~1h |
| Milestone | `wN/mN/` | shippable chunk: `README.md` + task files | **> ~1h**, multiple tasks |
| Task | `wN/mN/tNNN.md` | single unit | tens of minutes |

## Rules (enforce every time)

- **The board is public.** No secrets, credentials, or private-repo references. Write for the community.
- **Respect the anti-goals** in `.pm/DO_NOT_DO.md`; refuse conflicting items.
- **Workers are generalists.** A workstream is a queue, not a topic lane.
- **Sizing.** Milestone = > ~1h across more than one task. Smaller → inbox note `wN/NNN.md`, and say why.
- **IDs match paths.** A task's `id: wN/mN/tNNN` equals its location; repair drift rather than copying it.
- **Keep status in sync** in three places: workstream `README.md` checkbox, milestone `README.md` `**Status:**` + `— **DONE**` row marker, task `status:` frontmatter.
- **Completed work exits the open tree.** Done tasks → `wN/mN/done/`; milestones with no open tasks → `wN/done/mN/`; done notes → `wN/done/NNN.md`. Verify old paths are gone before reporting success.
- **Unwanted work leaves with its reason**: `drop` removes files and leaves a one-line tombstone under `## Dropped` in the workstream README; numbers are never reused; work under `done/` is never dropped.
- **Blocked work waits in `blocked/`** (`wN/blocked/mN/`, `wN/blocked/NNN.md`; tasks stay put with `status: blocked`) with the exact blocker and an **Unblock:** condition (and who can clear it).
- **Numbering:** next free zero-padded 3-digit for notes/tasks; next free `wN`/`mN`. Scan `done/`, `blocked/` and `## Dropped` first.
- Use `worker: worker1` unless the workstream README names another.
- **Milestones must be meaningful:** pillar (B1/B2/B3), observable reader outcome, why-now.
- **Book-specific hard rules a milestone must respect:** chapters are added/renamed in **both** languages; filenames/slugs/ids never renumbered; new chapters appear in `README.md`, `SUMMARY.md` and `zh-CN/README.md`; cross-references use `https://tianpan.co/notes/<slug>`.
- **Every milestone ends with standing closing tasks**, appended after implementation tasks:
  1. **Reader surface** — *only when the milestone adds or renames a chapter or changes navigation.* Check `README.md`, `SUMMARY.md`, `zh-CN/README.md` entries, front matter parity, cross-links, image paths (`../images/<file>`). Omit (and say why in Source + Goal linkage) for pure board mechanics.
  2. **Simplify** — tighten prose and diagrams the milestone touched (run `/simplify` if code/scripts changed); behavior/meaning preserving.
  3. **Verification** — run the checks from `AGENTS.md` that apply (front-matter/parity check, link check, `make build` when calibre/gitbook are available) and record what was and wasn't run. No fabricated results.
  4. **Closeout** — last; triggers the milestone move to `wN/done/mN/` via `/pm done` once the definition of done actually holds.
  Each depends on the prior implementation tasks; all count toward `(N tasks)`. `add-task` inserts new work **before** them.

## Subcommands

### `status` (default)
Read the tree (skip `done/`) and `.pm/DO_NOT_DO.md`. Per open workstream print milestones with `**Status:**`, next actionable task, open notes, and everything under `blocked/` with its condition. Validate and flag: anti-goal conflicts, missing `## Source + Goal linkage`/pillar, vague DoD, completed items still in open tree, blocked items lacking **Unblock:**. Touch no files.

### `new workstream <title>`
Create next `wN/README.md` from the template. Title must be a generic queue.

### `add <wN> <idea…>`
Create next inbox note `wN/NNN.md` (terse markdown, no frontmatter).

### `promote <wN/NNN>` / `new milestone <wN> <title>`
Apply sizing first. > ~1h and multi-task → create `wN/mN/` with `README.md` + `tNNN.md` files + standing closing tasks, add `- [ ] **mN** — … (N tasks) ← from <source>` to the workstream README. Otherwise keep as an inbox note and explain.

### `add-task <wN/mN> <title>`
Create next `tNNN.md`, add its table row before the closing tasks, update their `depends_on`, fix `(N tasks)`.

### `done <target>`
1. Set `status: done` (add `## Closed by triage` with evidence if the work landed elsewhere).
2. Mark the row `— **DONE**`, update `**Status:**`.
3. Move to `wN/mN/done/tNNN.md`.
4. If no open tasks remain, move the milestone to `wN/done/mN/` and check `- [x]`.
5. Verify exit condition. Inbox notes: append `---` + `**Resolved <YYYY-MM-DD>** — <what changed>, shipped in `<SHA>``, move to `wN/done/NNN.md`.

### `block <target> <reason>` / `unblock <target>`
Block: refuse without a reason; write `## Blocked` (blocker, **Unblock:**, owner, partial work shipped); move per the rules; keep the `- [ ]` line, retarget its link, append `— **blocked:** …`. Unblock: verify the condition actually holds, move back, replace the Blocked section with a one-line history, restore links.

### `drop <target> <reason>`
Refuse without a reason or for anything under `done/`. Delete the files (task: also fix table, `depends_on`, counts, add a `## Dropped` line in the milestone README), add `- ~~**mN**~~ — <title> — dropped <YYYY-MM-DD>: <reason>` under `## Dropped` in the workstream README. Propose (don't write) a `DO_NOT_DO.md` entry if the reason generalizes.

`DRY_RUN=1` in arguments → show intended moves, mutate nothing.

## Templates

### Workstream `README.md`
```markdown
# wN — <generic worker-queue title> (<worker>)

**Worker:** <worker> — general-purpose worker; takes the next highest-impact milestone across B1/B2/B3.

## Milestones

- [ ] **mN** — <title> (<N> tasks) ← from <source>
```

### Milestone `README.md`
```markdown
# wN · mN — <name>

**Worker:** <worker> **Goal:** <what shipping achieves> **Status:** todo

## Tasks (in order)

| id   | title   | est | depends_on |
| ---- | ------- | --- | ---------- |
| t001 | <title> | 30m | —          |

## Definition of done

<observable, testable end state>

## Source + Goal linkage

- **Source:** <note / brainstorm / issue>
- **Goal linkage:** <B1/B2/B3 and how>
- **Expected outcome:** <what a reader can now do/find>
- **Why now:** <dependency / risk / sequence>
```

### Task `tNNN.md`
```markdown
---
id: wN/mN/tNNN
title: <title>
worker: <worker>
status: todo
estimate: 30m
depends_on: [wN/mN/tMMM]
---

## Objective
## Context
## Steps
## Files
## Acceptance criteria
- [ ] <testable check>
## Out of scope
```

## Arguments

$ARGUMENTS
