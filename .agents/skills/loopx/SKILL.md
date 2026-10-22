---
name: loopx
description: Autonomously drain a `.pm` workstream item by item — triage every pending milestone, task, and inbox note, then implement and ship it, close it as already done, block it with an unblock condition, or delete it as invalid, and keep going until nothing actionable remains. Use when the user explicitly invokes /loopx or asks to loop, drain, or work through a whole workstream's backlog (e.g. `/loopx w1`). Sequential, not interval-based; not for timed polls, a single task, or ordinary edits.
metadata: {"internal": true}
---

# Task: Drain a `.pm` workstream item by item

Usage: `/loopx <wN>`

Repeatedly pick the next **actionable pending item** in workstream `<wN>` (a pending milestone, a pending task in a live milestone, or an open inbox note), **triage** it, act, `/ship` it, and continue until nothing actionable remains. Every item ends in exactly one place: implemented and shipped, closed as already done, moved to `blocked/` with an unblock condition, or deleted as invalid. Composes `/pm` (only writer to `.pm/`), your own writing work, and `/ship`. If you can name the next pick, keep looping — don't pause for a checkpoint or ask the user to re-run.

A pending item is a claim that the work is still wanted and undone. Boards go stale; never start on the strength of a checkbox alone.

If `$ARGUMENTS` is empty, **STOP** and ask which workstream.

## Preconditions (once)

1. `git branch --show-current` is `main`; else STOP and ask.
2. `git status` — pre-existing uncommitted changes you didn't make (other than ignorable `.DS_Store`) must not ride along; surface and ask.
3. `.pm/<wN>/README.md` exists; else STOP.
4. Read `.pm/DO_NOT_DO.md`; a conflict is a delete reason.

(There is no stop-hook guard in this repo; the Exit rules below are the only enforcement.)

## The loop

### 1. Pick
List `.pm/<wN>/m*/`, `*.md`, `done/`, `blocked/`. Checkbox and disk must agree; if not, trust task files and repair via `/pm`. Order: (1) lowest-numbered actionable pending milestone, its tasks in `depends_on` order; (2) lowest-numbered open inbox note; (3) a blocked item whose unblock condition now verifiably holds (`/pm unblock`). Honor `depends_on`; scan all later items before concluding none are actionable. Announce the pick. Nothing actionable → **Exit**.

### 2. Triage (before writing)
Read the item fully. Establish what is true on `main` with evidence: `git log` and grep the cited paths, check whether the chapter/file already exists in `en/` and `zh-CN/`, run the DoD checks. Announce outcome + evidence:

| Outcome | When | Action |
| --- | --- | --- |
| **Work on it** | still wanted, acceptance not yet true | one-line plan → step 3 |
| **Close as already done** | acceptance already holds (incl. both languages, indexes, checks) | `/pm done`; ship board move alone: `chore(pm): close <target> — already satisfied by <SHA>` |
| **Block it** | wanted but can't proceed: needs author/user decision, missing source material, unavailable tooling (e.g. no calibre for PDF build), unverifiable claim | `/pm block <target> <reason>` with **Unblock:**; ship alone: `chore(pm): block <target> — …` |
| **Delete as invalid** | conflicts with `DO_NOT_DO.md`, superseded/duplicate, or targets removed content | `/pm drop <target> <reason>`; ship alone: `chore(pm): drop <target> — …` |

User-routed/approved items you merely doubt are **blocked**, never deleted. Closing tasks (Reader surface, Simplify, Verification) are real work.

### 3. Implement
Do the writing/editing following `AGENTS.md`:
- Both languages: `en/` and `zh-CN/` change together; identical filenames; `slug`/`id` equal filename; only `title`/`tags` translated; never renumber.
- New chapter → also `README.md`, `SUMMARY.md`, `zh-CN/README.md`.
- Cross-refs use `https://tianpan.co/notes/<slug>`; local images in `images/` as `../images/<file>`; diagrams via the `mermaid` skill.
- Checks before shipping: front-matter/parity check (`diff <(ls en) <(ls zh-CN)`, slug==filename), no broken relative links, `make build` when gitbook/calibre exist (otherwise say it was not run).
- Don't fabricate facts, numbers, or references; verify or cite.
- Keep board in sync with `/pm done <target>` per finished item — never hand-edit board state.

### 4. Ship
Invoke `/ship` for this item (content + `.pm/` moves together, or board move alone). One board outcome per ship; never batch items. Never ship red — run checks as their own command and read the result before committing.

### 5. Continue
Re-scan immediately and pick again. Between items write one sentence: what shipped and what's next. Long queue / long session / several ships is **not** an exit.

## Handling a block
Report item, blocker, and unblock; don't stop while independent work remains. Preserve partial work (stash or branch) — don't ship half-work. Block individual tasks in place when only some are stuck; block the milestone when all open tasks are. Skip dependents of blocked work automatically. Don't retry an unchanged blocker.

## Exit
Only when: **Done** (nothing pending), **Blocked** (all remaining items blocked or depend on blocked work), or **Hard stop** (user interrupt/runtime limit/lost push access). Final report: shipped items with SHAs, closed-with-evidence, blocked-with-conditions-and-owners, deleted-with-reasons (and any proposed `DO_NOT_DO.md` entry), and for a hard stop the next actionable pick.

## Guardrails
- Triage before writing; every item ends somewhere; one outcome per ship.
- `/pm` owns `.pm/`. Doubt is a block, not a delete.
- The board is public: no secrets or private references anywhere, including commit messages.
- Stay in `<wN>`. Report honestly: skipped checks, partial work, closes-by-triage.

## Arguments

$ARGUMENTS
