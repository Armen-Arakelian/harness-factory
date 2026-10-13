---
name: manage-research-topics
description: Show, add, revise or review research-topics.md when the user asks. Propose evidence-based coverage statuses and save list changes only through memory-approval. Does not maintain the list automatically or create research notes.
---

# Manage Research Topics

Resolve the project root three directories above this skill folder. `research-topics.md` is the user's durable list of open research questions, outside the main graph. Read its current content and the Research Topics section of `rules.md`.

## Show or Change

Showing the list is read-only. For additions, revisions, reordering or removal, act only on the user's request. Preserve their question and scope; suggest a clearer formulation only as a preview. Search the list for overlapping questions before creating duplicates. Do not add topics just because they appeared in conversation or research. For an added question, use available context and a targeted search of existing notes to propose its initial coverage status under the review criteria below; do not default to Not explored when related work already exists.

Use a compact entry:

```markdown
### Do tokenized shares track ordinary share prices?

- **Status:** Needs depth
- **Related:** [[nodes/tokenized-shares|Tokenized Shares]]
- **Remaining:** Tesla was checked; other issuers and trading-hour differences remain unexamined.
```

Active entries use only `Not explored` or `Needs depth`. `Sufficient for now` is a review assessment, not a stored done status: propose removing that entry after approval, citing where its answer remains saved. `Related` is optional when no saved material exists; never invent a link. For `Needs depth`, include a short `Remaining` explanation; identify the unknown if the gap is not yet clear. These are coverage statuses, not truth or confidence scores.

## Review on Request

Read candidate notes relevant to each requested question. Search titles, aliases, content and conclusions, including unlinked ones; inspect evidence and limitations in details as needed. Review only the requested entries, or the whole list when that is requested. Reviewing the list checks saved research; it does not authorize new web research or new notes.

- `Not explored`: no research has started, as established by available context or the user. Failure to find a note alone does not prove nothing was studied; report missing evidence and keep an existing status when coverage cannot be established.
- `Needs depth`: an existing note, partial investigation or limited result touches the question but leaves material gaps. A concept description is not a complete answer. State what remains and link useful existing material.
- Sufficient coverage for removal: saved results adequately answer the recorded question within its scope, including relevant qualifications and unresolved limits. A result about one example does not settle a question about all examples. A user's conclusion is useful context, not proof of coverage.

When coverage is sufficient, show the question proposed for removal and links to the relevant saved results. Keep it in the list until approval. Do not create a completed-topic section or archive. New evidence or expanded scope can justify a user-requested, approved addition of the question again with `Needs depth`. Do not reopen topics unsolicited or automatically mark them complete after a research answer, checkpoint or conclusion save. If the user specifies a status unsupported by the records, explain the limitation briefly and preserve the user's final approved choice without presenting it as verified completeness.

## Preview and Save

For any list change, use `../memory-approval/SKILL.md`. Register `kind: topics`, with changes targeting only `research-topics.md` (`action: edit`, or `create` if the file is missing). Preview exact changed entries, statuses, related links and remaining questions; describe proposed or requested removals explicitly, including the exact question and links showing where the answer is saved. Removal changes only the list entry, never its linked research notes. Keep unchanged entries out of the preview. A review request authorizes assessment and a proposal, not writing.

Present the shared approval card when supported, otherwise its text fallback. Only an accepted ID check authorizes applying that returned proposal. An intervening ordinary message expires it. Recheck the list before writing, preserve unrelated entries and re-preview substantive conflicts. Remove the initial empty-state sentence when the first approved entry is added. Verify changed text, allowed statuses and link targets, then confirm briefly.

The save affects only this list. Do not create or modify nodes, conclusions, details, README map entries or agent memory to support it. A topic-list edit alone is not a research checkpoint; a separately requested change of active research direction can use the normal state workflow. No scheduling, automatic reviews or cross-project topic lists are introduced.
