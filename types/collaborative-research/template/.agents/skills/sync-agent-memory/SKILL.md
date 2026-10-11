---
name: sync-agent-memory
description: Update this research project's agent-owned state, findings, and working preferences after meaningful research progress, user corrections, or a request to sync memory. Curated notes and user conclusions use their approval workflows instead.
---

# Sync Agent Memory

The project root is three directories above this skill folder. Read its `rules.md`, especially Agent Memory, and resolve paths from that root. This workflow permits writes only inside the project's `agent-memory/`; it does not grant access to other projects or machine-wide memory.

1. Identify what changed since the last meaningful checkpoint. Read the compact state and only relevant existing insights or preferences; search for duplicates. Use reliable research results and directly available user statements, not invented context from a compacted summary. If nothing useful changed, do not write.
2. Refresh the Current State fields in `state.md` and add only significant chronological milestones to its Research Trail, following Research State and Trail in `rules.md`. When needed, consolidate older completed consecutive stages automatically, preserving chronology, important turns, rejected approaches and reasons, and useful links. Keep recent stages and unresolved issues distinct; skip consolidation if it would lose context. Link to user conclusions rather than restating or merging them. Merge significant agent findings into `insights.md`, preserving scope, basis, date, and uncertainty. Record only useful project preferences in `user.md`, labeled Explicit or Inferred. Apply the content boundaries and correction/forgetting rules in `rules.md`.
3. Use optional outward links to existing notes where they help retrieval. Do not create targets, reverse links, map entries, or user conclusions. Promotion to curated memory follows its preview-and-approval workflow separately.
4. Apply only the necessary agent-memory edits without a per-entry approval. Check affected content and changed link targets. Avoid unrelated rewrites and respect intervening edits. Briefly report a sync when the user requested it; routine checkpoints need no extra checklist or save proposal.

This skill is an in-session workflow. It installs no background worker and does not guarantee a write after every turn or before compaction.
