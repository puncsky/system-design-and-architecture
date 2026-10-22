---
name: ship
description: Ship pending changes on main by pulling with rebase, committing intentionally, and pushing to origin. Use only when the user explicitly invokes /ship or asks to ship or publish the current main branch.
allowed-tools: Bash(git status:*), Bash(git pull:*), Bash(git fetch:*), Bash(git diff:*), Bash(git show:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git branch:*), Bash(git rev-parse:*), Bash(git rebase:*)
metadata: {"internal": true}
---

# Task: Ship the current main branch

Usage: `/ship [optional commit message context...]`

Bring the local `main` up to date, commit any pending work, and push to `origin/main`. (This repo's default branch may be `master` upstream; ship whatever branch `origin` tracks as the working branch — verify with `git rev-parse --abbrev-ref @{u}`.)

## Session-aware mode

If you made the pending changes earlier in this conversation, you already know what changed and why:

- Skip the diff stat calls in Step 2. Run only `git status` as a sanity check.
- In Step 4, stage exactly the files you edited this session by name and write the commit message from session knowledge.
- If `git status` shows files you did not touch (e.g. `.DS_Store`), leave them unstaged; inspect anything else before staging.

## Step 1 — Verify branch

`git branch --show-current`. If it is not the branch `origin` tracks for shipping (`main`), **STOP** and ask whether to switch or abort.

## Step 2 — Inspect state

`git status`; for unfamiliar changes also `git diff --stat` and `git diff --cached --stat`. If the tree is clean, skip Step 4 but still pull and push.

## Step 3 — Pull latest with rebase

`git pull --rebase origin <branch>`. Resolve conflicts proactively: inspect both sides (`git show :2:<path>`, `git show :3:<path>`), keep both sides' intent, remove markers, stage by path, `git rebase --continue`. For chapter pairs, resolve `en/` and `zh-CN/` consistently. Escalate only when competing resolutions would change meaning and the right one cannot be inferred.

## Step 4 — Stage and commit

Stage only relevant files explicitly by path. Write a Conventional Commits message (`docs(en): …`, `docs(zh-CN): …`, `chore(pm): …`, `chore(skills): …`). Honor `$ARGUMENTS` as context. End the message with the attribution line the harness specifies, if any.

Before committing book content, run the book checks in `AGENTS.md` (front matter / bilingual parity / link checks) when they apply.

## Step 5 — Push

`git push origin <branch>`. If rejected as non-fast-forward, redo Step 3 and retry. Never force-push.

## Step 6 — Report

Print the shipped HEAD SHA and subject, e.g. `Shipped: a1b2c3d docs(en): add chapter on …`.

## Optional User Context

$ARGUMENTS
