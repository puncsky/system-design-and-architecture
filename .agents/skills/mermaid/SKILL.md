---
name: mermaid
description: >-
  Create concise, syntax-verified Mermaid architecture diagrams. Use when the user asks to diagram a chapter topic, system, component, dependency flow, or supplied description in Mermaid.
allowed-tools: Bash(npx -y @mermaid-js/mermaid-cli@11.16.0:*), Write, Read
metadata: {"internal": true}
---

Draw a mermaid architecture diagram in markdown for: $ARGUMENTS

## Conventions

- **Boxes are services/components**: `svc[api-gateway]`. Use `[(...)]` for datastores, `[[...]]`-style queues only if the chapter does. Humans (user, operator) are triangles: `user@{ shape: tri, label: "user" }`.
- **A box that is not a long-running service must say so in its label** (`cron["nightly compaction job (spawned, exits when done)"]`). Never draw a manual procedure as a peer of running infrastructure; give it its own subgraph titled as manual.
- **Arrows are dependency direction**: `A --> B` means A calls/reads/writes B — never the reverse. Label an edge (`A -->|gRPC| B`) only when the relationship isn't obvious.
- **Concise**: only load-bearing components and edges. No styling, colors or legend. Default `flowchart TB`; `LR` only if much wider than deep. `subgraph` only for real boundaries (region, cluster, trust zone, sync vs. async path).
- If $ARGUMENTS refers to a chapter in this book, read it first (`en/<file>.md`) — don't diagram from guesswork. Keep names consistent with the chapter's prose.

Syntax gotchas: quote labels containing `(`, `)`, `[`, `{` (`a["Queue (SQS)"]`); never name a node bare `end` or `graph`; quote subgraph titles with spaces.

## Verify (mandatory, before answering)

1. Write the diagram body (no fence) to a unique `.mmd` file under `.agents/tmp/` (gitignored).
2. Run `npx -y @mermaid-js/mermaid-cli@11.16.0 -i <file>.mmd -o <file>.svg`; exit 0 means valid. The version is pinned deliberately (supply chain) — bump consciously.
3. On failure, fix and re-verify. Never output an unverified diagram.

## Output

A single ` ```mermaid ` fenced block plus a short explanation of the key flow. If asked to put it in a file, insert the verified block there.

**Book caveat:** the GitBook build (`gitbook-cli`, Node 10) does not render Mermaid fences by default. For published chapters, either render the verified `.mmd` to an image under `images/` (`-o images/<name>.svg`, referenced as `../images/<name>.svg`) or confirm a Mermaid plugin is enabled in `book.json` before leaving a raw fence in a chapter. Mirror the diagram in both `en/` and `zh-CN/` (translate labels only).
