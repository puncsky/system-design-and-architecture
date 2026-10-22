---
name: pm-brainstorm
description: Propose milestones and tasks for the repository's public .pm board — decompose a topic through the editor's reader-impact lens, size and gate the work, and emit a text-only proposal for /pm to materialize. Use only when the user explicitly invokes /pm-brainstorm or asks to brainstorm, plan, or break down book roadmap work. Not for writing board files (that is pm) or ordinary chapter edits.
allowed-tools: Read, Bash(ls:*), Bash(find:*), Bash(cat:*), Bash(grep:*), Bash(git fetch:*), Bash(git pull:*), Bash(git status:*)
metadata: {"internal": true}
---

# Task: Propose milestones and tasks

Usage: `/pm-brainstorm <topic or goal to break down>`

The **divergent** half of the pair: think a topic through, **propose** work, hand materialization to `/pm`. It writes **nothing**. Conventions (pillars B1/B2/B3, hierarchy, sizing, closing tasks, templates) live in [`../pm/SKILL.md`](../pm/SKILL.md) — read and apply them; do not restate or diverge.

**Minimum proposal size:** at least **5 distinct, actionable top-level candidates** (milestones and/or inbox notes) that pass scope, anti-goal, dedup, sizing and quality rules. Don't pad or artificially split.

## Steps

1. **Load canon and anti-goals.** Read `.agents/skills/pm/SKILL.md` and `.pm/DO_NOT_DO.md`. Reject conflicting candidates explicitly.
2. **Sync if safe.** `git fetch origin`, `git status`; fast-forward only when behind and clean. Never block on a dirty/diverged tree.
3. **Load context.** Read the board (`find .pm -name README.md`, loose notes, `done/` and `blocked/`) so proposals fit and don't duplicate shipped work. Ground truth for the book is the repo itself: `README.md`, `SUMMARY.md`, `zh-CN/README.md`, the relevant `en/` chapters, `drafts/`, and `awesome-system-design.md`. Check that a candidate chapter doesn't already exist (`ls en | grep`, `grep -il`), and what the `en`/`zh-CN` parity gap actually is (`diff <(ls en) <(ls zh-CN)`).
4. **Apply the editor's lens.** For each candidate answer: **Pillar** (B1/B2/B3, else out); **Reader** (interview candidate, practicing engineer, translator/contributor); **Friction removed** (what they can now learn/find/trust); **Signal** (site traffic, GitHub stars/issues, reader feedback, build passing). Prefer compounding assets (fixing a template, parity tooling, a TOC) over one-off prose; prefer fixing wrong/outdated content over adding more.
5. **Discuss & decompose.** Pressure-test scope, surface dependencies/risks; break into tasks with estimates and `depends_on`.
6. **Size and gate** by `/pm`'s rules. Undersized → inbox note. Fails the gate → "not meaningful" with a better-scoped alternative.
7. **Emit text only.** Full detail first: target queue and why, each milestone (task table, definition of done, source, pillar, outcome, why-now) or inbox note, in proposed priority order. Implementation tasks only — `/pm` appends closing tasks; flag whether you expect Reader surface to apply.
8. **End with exactly two blocks, nothing after:**
   1. **"Summary (priority order)"** — `N. <title> (wN, ~size) — one-line outcome`.
   2. The exact `/pm` invocations (`/pm new milestone w1 <title>`, `/pm add w1 <idea>`, `/pm promote w1/NNN`).

## Topic

$ARGUMENTS
