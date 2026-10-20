---
name: manage-ideas
description: Show, add, revise, rate or remove user ideas in the single ideas.md list on request, using exact preview approval. Does not automatically collect ideas, decide ratings or create informational notes.
---

# Manage Ideas

Resolve the project root three directories above this skill folder. Read the Ideas section of `rules.md`. All entries live in root `ideas.md`; an idea is a possibility, not a fact, user conclusion or research-coverage status.

## Read or Prepare

Showing or finding ideas is read-only. Search headings and bounded relevant passages; read the whole list only when the request needs it. For a requested change, inspect the affected entries and nearby context, deduplicate overlapping ideas and preserve unrelated entries. Update the same idea in place when appropriate; do not create a new file or keep copies for successive ratings. The agent may briefly suggest saving a useful idea, but writes only after the user requests it and approves the preview. No automatic harvesting, rating or review after messages or research.

Use a short descriptive heading, the user's rating and a few sentences capturing what is proposed and why it matters. Preserve the user's meaning without inventing implementation plans, evidence or certainty. Useful depth stays in existing linked notes rather than a long entry. For example, this shape is illustrative, not an idea to insert:

```markdown
### Compare a mechanism across markets

- **Status:** Promising

Compare how the same mechanism works in two markets to identify which differences matter for this research.
```

Use exactly `Tentative`, `Promising` or `💥 Cannon` for the stored status. Map an unambiguous user rating, including "пушка", to the matching label; if the rating is missing or unclear, ask rather than silently choosing one. A rating belongs to the user and is not evidence quality, correctness or completion. A requested reassessment may discuss tradeoffs, but cannot change ratings without approval.

Select only useful links to existing information, people, conclusions or details. Use vault-relative wikilinks with display titles and brief relationship text. Keep links out of the compact preview unless requested or needed to preserve its meaning; they are delegated under the normal connection policy. Do not invent supporting notes or link everything mentioned. Outward links from the idea list suffice: do not add reverse links, README entries or edit linked content as a side effect. Link to an individual idea with `[[ideas#Its heading|Its heading]]` when such a reference is independently requested; no separate idea files or mandatory IDs are needed.

## Preview and Save

Read `../memory-approval/SKILL.md`. Register `kind: ideas` with one change targeting only `ideas.md`: `edit` normally, or `create` if the list is missing. Several idea-entry changes fit in that one file preview and one approval. Preview each exact new/revised heading, rating and description, with enough context to identify an edit; state removals and reordering explicitly. Do not preview the entire unchanged list. A review or save request starts a proposal, not a write.

Present the shared purple Ideas card by default when supported, otherwise the normal text fallback. Only an accepted ID check authorizes the returned proposal; revisions and intervening ordinary messages expire it. Recheck the file before applying the exact approved edits, preserve unrelated entries and re-preview substantive conflicts. Remove the initial empty-state sentence when the first approved entry is added; restore it if the last entry is removed. Keep the three-status legend. Verify the saved text, user-selected ratings and changed link targets; confirm only actual outcomes.

This operation changes only `ideas.md` and its approval bookkeeping. It does not create information, people, details or conclusions, run the glossary hook, update agent state merely because the list changed, or modify graph settings. Promotion of an idea into other memory needs the corresponding separately requested approval workflow; an idea rating never changes automatically when research progresses.
