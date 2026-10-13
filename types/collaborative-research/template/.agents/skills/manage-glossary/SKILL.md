---
name: manage-glossary
description: Create an optional multilingual glossary on request, maintain it from the current successful information save, or reconcile saved information during an explicitly requested full glossary review. Does not require per-entry approval or edit curated notes.
---

# Manage the Glossary

Resolve the project root three directories above this folder. Read the Glossary section of `rules.md`. Use `python3 .agents/skills/manage-glossary/scripts/glossary.py` for configuration, targeted lookup and writes. Only `glossary.md` is agent-owned by this permission; notes, conclusions and topics keep their approval rules.

## Create on Request

Project generation asks no glossary questions and creates no active glossary. When the user asks to create one, ask only for missing term languages and the explanation language. Reuse explicitly supplied preferences rather than ask again. For example, `create --languages English Russian --explanation-language English`. The first term language anchors deduplication; prefer the research source language when the user has no ordering preference.

The explicit creation request and chosen settings authorize subsequent bounded maintenance without entry previews or Approve. Create an empty glossary; do not scan old research during setup. Configuration lives in its frontmatter. If one exists, preserve it rather than overwrite it. Language changes require the user's request and careful preservation/retranslation of existing rows; do not silently change languages. `disable` stops maintenance on request without deleting terms. `enable` resumes it only on request, preserving its languages and entries. A disabled glossary is not re-enabled automatically.

## Current-Save Maintenance

Run only after `update-memory` successfully saves and verifies substantive content in `nodes/` or `details/`, and only if `config` reports enabled. Select significant terminology from those actual saved files, including the saved details in that operation. Exclude reverse-link-only edits, README changes, rejected or failed saves and unrelated notes. Do not traverse the graph, reread all historical details or scan the whole project. Ordinary messages, recall, conclusions, topic-list changes and agent-memory checkpoints do not trigger this workflow.

Read the configured languages, prepare candidate terms from that bounded material and use `lookup --terms ...` for just their existing equivalents. Upsert new terms or improve relevant definitions in one small batch; skip writing if nothing changed. Keep translations idiomatic and explanations brief. If a translation is uncertain, mark that uncertainty in the meaning or defer the entry rather than invent precision. Context distinguishes genuinely different senses; do not merge homonyms or broaden a scoped definition into a universal claim. Existing terms unrelated to this save stay untouched.

Write candidate JSON in ignored `work/`, then use `merge --entries work/<batch>.json --sources nodes/<saved>.md details/<saved>.md`, passing only the actual source paths for this save. Payload shape:

```json
{"entries":[{"terms":{"English":"Share","Russian":"Акция"},"context":"Equity","meaning":"An ownership interest in a company."}]}
```

Terms must match the configured languages. There are no research-note links, source lists or reverse links in the glossary. The helper reads the glossary and candidate batch, checks supplied paths, and edits only `glossary.md`; it does not extract terms or independently establish approval/scope. The agent supplies language judgment and honors the successful-save boundary. A glossary error does not undo an approved note save; report the partial outcome and do not repeat that curated save.

## Full Review on Request

Only a command such as "Review the glossary across the project" authorizes broad reconciliation. Search saved `nodes/` and `details/` for missing terms, incorrect translations, duplicate senses and outdated definitions. Exclude `work/`, agent memory, instructions and conclusions as factual definition sources. Use saved evidence; new external research needs its own requested scope.

Use `merge --review` with the reviewed source paths. Optional `remove` items identify a term in the first language and its context, for example `{"term":"Share","context":"Equity"}`. Removal/merging must preserve useful meanings; do not discard historical terms merely because they were not mentioned recently. Complete the requested reconciliation without per-entry approval and briefly report material changes and uncertainties. A normal save never initiates this full review.

The glossary is a link-free purple helper node, not a user conclusion or evidence source. Definitions can support terminology recall; substantive answers still use research notes and sources. No background tasks or new node taxonomy are introduced.
