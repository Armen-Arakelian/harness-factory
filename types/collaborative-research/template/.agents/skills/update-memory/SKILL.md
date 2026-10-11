---
name: update-memory
description: Preview and apply user-approved changes to this research project's information notes, detail notes, map, and existing memory. New user conclusions use create-conclusion; agent-owned working notes use sync-agent-memory instead.
---

# Update Research Memory

The project root is three directories above this skill folder. Read its `rules.md` when using this workflow. Resolve project paths from that root.

1. Identify the requested change and read only relevant existing notes and map entries. Search for duplicates and existing connections. For rename or deletion, search incoming links. The user must explicitly initiate any change to an existing conclusion; never add conclusion maintenance to a routine information update.
2. Choose `nodes/` for short information or `details/` for a curated deeper explanation. Keep notes flat and follow the note shapes and link conventions in `rules.md`.
3. Show a compact preview in chat: paths, proposed new text or exact changes, connection labels, and any README or reverse-link changes. Include deletions explicitly. Do not write to user-controlled permanent memory yet. Temporary preview files, if useful, belong in `work/`.
4. Ask the user to approve the concrete batch. An instruction to save information starts this workflow; it does not skip the preview. Apply a previously approved identical preview without asking twice. A rejection or silence means no write. Show a revised preview if the user requests changes.
5. After approval, ensure affected files still match what the preview was based on. If they changed, show an updated preview rather than overwriting intervening work. Apply only approved changes.
6. Verify affected paths and changed link targets, then briefly report what was saved. Do not rewrite unrelated notes, settings, or instructions.

When offering a save suggestion during research, propose only information notes or details, and only when a significant reusable result warrants it. Never suggest creating a user conclusion or add a proposal after every answer.
