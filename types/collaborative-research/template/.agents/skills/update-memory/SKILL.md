---
name: update-memory
description: Preview and save user-approved information or requested existing-memory changes, maintaining related graph links automatically. New conclusions use create-conclusion; agent working notes use sync-agent-memory.
---

# Update Research Memory

The project root is three directories above this skill folder. Read its `rules.md` and resolve paths from that root.

For each new or revised preview, read `../memory-approval/SKILL.md` before presenting it. With `visualize` available, the initial response must contain the approval card, rather than a text-only question. Do not repeat the preview outside the card. Approval is required by the project rules; this skill implements that existing choice, not an additional permission step.

1. Identify the requested change and read relevant existing notes/map entries. Search for duplicates. The user must initiate changes to existing conclusions; never add conclusion maintenance to an information save. For rename or deletion, inspect incoming links.
2. Choose `nodes/` for short information or `details/` for deeper curated explanation. Follow note shapes and keep substantive content separate from connection sections.
3. Show a short preview: the destination/title and exact information to save, or the substantive edits to an existing note. State requested renames/deletions explicitly. Do not enumerate connections, reverse-link files or README link edits unless the user asks. If a batch contains substantive changes to multiple notes, preview each. Temporary previews may go in `work/`; do not write curated memory yet.
4. Use `../memory-approval/SKILL.md` to register this exact preview and present buttons when supported, otherwise a concise text approval. A save request starts the preview, not the write. Only an accepted ID check authorizes the returned content; rejection, silence or an intervening ordinary message means no write. Re-preview changes to meaning, wording, scope or destination. Do not ask again for content just accepted by the helper.
5. After approval, save that content and choose relevant connections under `rules.md`. Maintain necessary reverse links and README discovery entries automatically as part of this save. Use existing targets or notes whose content was approved in the same batch. These mechanical edits require no separate link approval; they must not change unrelated prose, create unapproved notes, invent evidence or prune unrelated connections. Show link details only on request or when a relationship would change the approved meaning.
6. Recheck affected files before applying edits and preserve intervening work. Re-preview substantive conflicts; recompute link-only edits against the latest files without overwriting content. Verify the saved text and changed links, then give a brief confirmation. Do not modify settings or instructions incidentally.

Occasionally suggest saving significant reusable information or details; never initiate a user conclusion or append save proposals to every reply.
