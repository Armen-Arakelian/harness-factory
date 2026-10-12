---
name: sync-agent-memory
description: Checkpoint this project's agent-owned state after significant research, direction changes, user reviews, approved memory changes affecting active work, or an explicit sync or handoff request.
---

# Sync Agent Memory

The project root is three directories above this skill folder. Resolve paths from that root and read the Agent Memory and Research State sections of `rules.md`. Writes are permitted only inside this project's `agent-memory/`; curated memory, instructions and settings retain their own approval boundaries.

1. Checkpoint after a meaningful research result, change of direction, completed user review, approved memory edit affecting active work, or an explicit sync or handoff request. Ordinary conversation and read-only recall need no write. If nothing useful changed, leave files alone. No background worker or reliable pre-compaction hook is supplied.
2. Read Current State and only relevant existing insights or preferences. Reconcile the last snapshot with directly available user instructions and actual work; do not invent missing progress from a compacted summary. Refresh `Updated` using the known checkpoint date/time, then Focus, Progress, Open Questions, Next Step and Relevant Memory. Distinguish a user-requested continuation from an agent-suggested next action. A date records the checkpoint, not guaranteed freshness or the time a thought originated.
3. Keep state compact. Record unresolved questions, blockers and pending decisions without converting unapproved ideas into user beliefs. Pending memory proposals remain unapproved across handoff. Link to conclusions rather than paraphrasing them. Add only significant dated actions/transitions to Research Trail and consolidate older completed repetitive stages only under `rules.md`, preserving chronology and meaningful turns.
4. Update insights or scoped preferences only when useful durable information changed; search for duplicates and preserve basis, scope, date and uncertainty. State-only checkpoints need not touch them. Optional outward links must target existing notes; do not create targets, reverse links, map entries or conclusions.
5. Apply the necessary edits, checking affected content and changed link targets. Read affected files again before writing and respect intervening edits. Report a requested sync briefly; routine checkpoints need no extra checklist. Treat the snapshot as the shared current research direction, not a record of every chat's independent tasks.
