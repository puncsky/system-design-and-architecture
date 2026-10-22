---
name: dont-code-but-answer
description: Answer a question about the book, its chapters, or system design/architecture without editing any file. Use when the user invokes /dont-code-but-answer or says "don't code, just answer", "explain only", or "no changes, just tell me".
allowed-tools: Read, Bash(ls:*), Bash(find:*), Bash(grep:*), Bash(git log:*), Bash(git show:*), Bash(git status:*), WebSearch, WebFetch
metadata: {"internal": true}
---

# Task: Answer, don't change anything

Usage: `/dont-code-but-answer <question>`

The user wants an **answer**, not a diff. Treat the session as read-only.

## Rules

1. **No writes.** Do not Write/Edit files, run formatters, `git add/commit/push`, install packages, or start servers. If a Bash command could mutate state, do not run it.
2. **Ground the answer.** If the question touches this repo, read the relevant chapter(s) in `en/` (and `zh-CN/` if asked) and `AGENTS.md` first; cite as `file_path:line`. Do not answer from memory about what the book says. For general system-design questions, answer from knowledge and say so; use web search only if freshness matters.
3. **Answer first, briefly.** Lead with the direct answer, then the key reasoning, tradeoffs and numbers. Recommend one option rather than surveying all. Use a short Mermaid sketch only if a picture clearly beats prose (see the `mermaid` skill; skip its render step since nothing may be written to disk).
4. **Don't expand scope.** Don't propose or start implementation. If the answer reveals work worth doing, end with one line: "If you want this changed, say so and I'll do it" — or suggest `/pm add <wN> <idea>`.
5. **Be honest about uncertainty** — say what you verified in the repo versus what is general knowledge.

## Question

$ARGUMENTS
