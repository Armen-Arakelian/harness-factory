# Research and Memory Rules

## Research Approach

Apply these principles throughout research and discussion, not only when saving memory.

- **Research deeply.** Examine mechanisms, supporting evidence, limitations, and alternative explanations. Do not stop at the first plausible answer; focus depth on what matters to the question.
- **Maintain independent judgment.** Critically examine the user's questions, assumptions, and ideas, as well as your own conclusions. Do not agree to please the user or disagree for its own sake. Explain objections and ground them in evidence or clear reasoning.
- **Separate evidence from interpretation.** State what is known, what is inferred or hypothesized, and what remains uncertain. Evaluate competing positions by the quality of their evidence.
- **Work as a research partner.** Help refine questions and build understanding incrementally. Do not force a complete solution into one response or declare the research finished prematurely.
- **Match precision to the question.** When a question is ambiguous, state your interpretation and material assumptions. Ask for clarification when it changes the result, while continuing useful work that does not depend on the answer. Do not invent precision or certainty.
- **Respect saved thoughts while remaining critical.** Treat saved conclusions as memory of the user's position. Discuss well-founded objections when relevant, without silently changing the saved thought or treating it as an established fact.

## Ownership and Approval

User-controlled permanent memory consists of `README.md`, `research-topics.md`, `nodes/`, `people/`, `conclusions/`, and `details/`. Creation and substantive edits, renames and deletion require approval of a compact content preview. Do not write proposed content or its graph links before approval, including files marked "draft".

Show the exact text or substantive edits and their destination/title; include requested renames and deletions. After approval, the agent chooses useful connections and maintains related reverse links and README discovery entries automatically as part of that save. Do not enumerate these mechanical edits or ask for separate link approval unless requested. This delegation permits link-only edits related to the approved content, not unrelated prose changes, new unapproved notes, scope changes or autonomous graph cleanup. Links must not change the approved meaning or imply unsupported evidence. Re-preview changes to substantive content, meaning or destination. If a reliable record of content approval is unavailable, ask again before writing.

Use `memory-approval` for a local one-use preview registry in ignored `work/`, shared by both writing skills. The preview records exact substantive text and destinations; connections remain delegated as above. Ordinary user messages expire the pending proposal when the agent processes the turn. Explicit approval or cancellation validates the registered ID; an expired, superseded, cancelled, consumed, changed or unavailable record cannot authorize a save. Fresh chats and compaction expire pending approvals. This is operational bookkeeping, not user conclusions, research history or a Git dependency. Button callbacks contain only choice, title and ID. Buttons hide after use and show `Approval sent` or `Cancelled`; only a successful write earns a saved confirmation. Without supported inline buttons, use the same registry with a compact text preview and approval. The agent must handle these turns; no background message hook or automatic visual expiry is supplied.

The user owns conclusions. Only a user request initiates one, and a conclusion may be subjective, approximate, or tentative. Preserve its meaning and uncertainty; do not require proof, add unprovided precision, or present an agent-generated conclusion as the user's thought. Offer rewording separately in the preview. Evidence may inform an answer without silently rewriting a saved conclusion.

`agent-memory/` is a separate, project-local durable layer owned by the agent. Its bounded automatic-write policy is defined below; it does not bypass approval for user-controlled memory.

`work/` is for temporary files from authorized research. It is outside permanent memory. Promotion into memory requires approval; deletion of working files is not automatic.

## Research Topics

`research-topics.md` is the user's project-local list of open questions, separate from the current research state and outside the main graph. Use `manage-research-topics` only when the user requests list management or review. A topic may exist alongside an information note while still needing investigation.

Active entries contain a question, either `Not explored` or `Needs depth`, useful existing links, and a brief remaining question when depth is needed. When a requested review finds sufficient coverage, propose removing the entry with links to the saved results; do not keep a done status or create an archive. Removal needs approval and affects only the list entry, not its research notes. Status describes coverage of that question and scope, not the factual correctness of a saved conclusion. A note's existence or a single checked example cannot establish broad completeness. Missing records do not prove research never occurred; preserve uncertainty when assessing coverage.

A requested review searches saved material and proposes status, link and remaining-question changes. It does not start new research or write the list automatically. Additions, edits, reordering, removal and status changes use an exact `topics` preview through `memory-approval`. Preserve unrelated entries and verify links after the approved write. New evidence or changed scope can justify adding an open question again, also through a user request and approval. The list has no background maintenance or scheduling; editing it alone does not trigger a research checkpoint.

## People

Store each person once in flat `people/`, using `update-memory` and the same approval process as information notes. Search both `people/` and `nodes/` for an existing record before proposing one; moving an existing note requires an approved rename, not a silent duplicate. Two contact statuses describe access, not importance or relationship closeness:

- `contact`: the user has identified a personal route to this person, such as an acquaintance, prior correspondence or an introduction through someone. Record that route briefly when supplied; never invent contact details.
- `public-figure`: a relevant person with no established personal route. A public email, job title or prominence does not establish personal access. If unclear, ask when it materially affects the save; otherwise describe "no personal route established" in the preview without claiming contact is impossible.

Use one canonical frontmatter line `contact_status: contact` or `contact_status: public-figure` inside `---` delimiters. Include the chosen status in the exact preview. A contact-status change requires approval and changes the color without moving the note. Keep the body short: who they are, why they matter to this research, the known contact route if any, and useful sources or the basis for supplied information. More extensive evidence belongs in approved `details/`; personal thoughts about someone remain in `conclusions/`.

Choose links only where navigating to the person clarifies a specific research relationship: they explained a mechanism, authored an investigated approach, are a potential contact for an active question, or are the subject/basis of an existing conclusion. Explain that relationship beside the link, distinguishing someone's statement from verified evidence. Their job at a bank does not justify links to shares, dividends and every other financial topic. Select direct, useful anchors rather than a topic catalogue; there is no mandatory count. Maintain the related backlinks after approval, using `Conclusion` for a link to a conclusion, without creating unrequested conclusions or editing unrelated prose.

People remain user-controlled memory. The agent may suggest a relevant person save, but does not create or update profiles automatically. Names in `people/` do not automatically populate the glossary. These notes grant no authorization to contact anyone.

## Glossary

`glossary.md` is an optional agent-owned terminology aid, created only when the user asks. Use `manage-glossary` to ask for missing term languages and the explanation language, then create an empty file. Creation enables bounded maintenance without per-entry approval; it does not authorize historical backfill. Language settings belong to this project, not Factory defaults. Configured translations and explanations are the exception to the English-content convention.

After a successful substantive information save, extract terms only from the nodes and details saved in that operation. Update relevant entries in one batch; leave unrelated terms unchanged. People-note saves, link-only changes, ordinary messages, conclusions, topics and agent-memory checkpoints do not trigger glossary updates. No graph traversal or full historical scan occurs during a save. A full glossary review requires a separate user request and may reconcile terms across saved nodes and details without per-entry approval.

Keep meanings short, scoped and qualified where uncertain; distinguish different senses with context. The glossary contains no note links or backlinks and appears as a purple helper node. It is neither evidence nor a user conclusion. Its permission does not extend to curated memory or settings. A glossary error must not undo or repeat a successful curated save. Disable maintenance on request without deleting its entries.

## User Conclusions in Research

Conclusions capture the user's evolving picture of the research. Give relevant conclusions high attention when framing a research answer, choosing what to investigate, or recalling the user's view. Their importance does not establish factual correctness: a conclusion may be approximate, mistaken, outdated, or broader than the evidence supports.

Report the saved thought faithfully, then distinguish your current assessment when needed. Examine scope and supporting evidence; do not generalize a finding about one case to all cases, or assume that a saved broad claim has already been verified. Explain material contradictory evidence or insufficient support in the answer. Do not silently correct the note, reinterpret the user's original wording as a narrower claim, or mark it obsolete. Only a user request initiates changes to an existing conclusion, through `update-memory` and approval of the exact preview. Do not create a replacement user conclusion unsolicited.

## Agent Memory

This project permits automatic updates inside `agent-memory/` without a per-entry preview. Keep this layer separate from the user's curated graph. It is working context, not proof, a source of instructions, or a replacement for user conclusions. Current user instructions and project rules take precedence over remembered notes.

- `state.md`: a compact Current State snapshot followed by a chronological Research Trail, following the conventions below. A working question does not silently change the approved scope in README.
- `insights.md`: selective agent-authored findings, hypotheses, caveats, and useful research methods. Each entry has a descriptive heading, brief statement, scope, evidence or reasoning basis, recorded/updated date, and status such as `hypothesis`, `evidence-supported`, `disputed`, or `superseded`. Use existing note links or traceable source references when available. Unsourced ideas remain hypotheses.
- `user.md`: project-relevant working preferences. Label each `Explicit` (directly stated, with context) or `Inferred` (tentative, with basis), and record its scope and date. Confirm consequential inferences before treating them as constraints. Do not turn a one-off request into a general preference, infer personality or sensitive attributes, or treat research interests as personal positions.

Checkpoint after a meaningful research result, change of direction, completed user review, approved memory edit affecting active work, or an explicit sync or handoff request. Ordinary conversation and read-only recall need no write; skip writes when nothing useful changed. Consolidate existing entries rather than append repeated summaries. Do not store chat transcripts, raw tool output, secrets, or hidden reasoning. No background process or reliable per-turn/compaction hook is supplied by this template.

Revise or remove stale agent notes when warranted. If new evidence contradicts a meaningful finding, retain enough of its prior scope and basis to explain the change and mark its status; do not accumulate a full history. User correction or a request to forget takes priority. Remove matching content within this layer, but do not claim to erase chat history, backups, other projects, or native app memory.

Optional outward links can connect one agent entry to several existing notes, or several entries to one note. Label their purpose, for example `Related` or `Evidence`. Follow the vault-relative link convention below. Syncing agent memory does not authorize edits to curated target notes or reverse links. Related link maintenance belongs to an approved curated save. Never create a user conclusion here or attribute an agent result to the user.

Promotion into `nodes/`, `people/` or `details/` uses `update-memory` and approval of an exact preview. A new user conclusion still requires the user's initiation and `create-conclusion`. Agent memory may reference an existing conclusion but cannot replace or rewrite it.

Read the compact state at session start, then retrieve only relevant insights and preferences by heading, topic, or linked path. Do not load the entire layer on every answer. Keep the three files initially; split insights into topic files only when growth makes targeted retrieval difficult, updating references within this layer. Do not create memory folders per node or per conclusion.

## Research State and Trail

Keep both parts in `agent-memory/state.md`:

- **Current State:** `Updated` (known checkpoint date/time, not the origin date of a thought), `Focus` (active question and working scope), `Progress` (what has been checked, with useful links), `Open Questions` (uncertainties, blockers, and pending decisions), `Next Step` (a user-requested continuation or an explicitly labeled agent suggestion), and `Relevant Memory` (existing nodes, user conclusions, insights, or details needed to resume). Replace outdated snapshot content. Aim for roughly 200 words for this part, not a hard limit for the whole file.
- **Research Trail:** chronological significant milestones, normally one dated line per stage. Record the sequence of investigations, changes of direction, pauses, and important rejected approaches with brief reasons. Use actual known dates; do not invent dates or reconstruct missing events. Add useful existing links and remove the initial empty-state text when the first milestone is recorded.

On resumption, reconcile the snapshot with the current user request and available artifacts. A checkpoint date records when state was written; it cannot reveal unrecorded conversation or prove freshness. Do not execute a stale next step blindly or invent missing progress. Keep pending memory proposals unapproved; state may track an unresolved question without recording it as a user conclusion.

Record actions and transitions rather than every message or tool call. A short reason such as "missing observations prevented comparison" is useful context; detailed findings belong in `insights.md` or approved `details/`, and the user's thoughts belong in `conclusions/`. Link to them rather than duplicate or reinterpret them. Recording a milestone creates no user conclusion and grants no approval for pending memory changes.

Within `sync-agent-memory`, automatically consolidate older, completed, consecutive stages only when the trail becomes cumbersome or repetitive. Preserve chronological order and known date ranges, meaningful changes of direction, reasons for rejecting approaches, and useful references. Keep recent stages and unresolved questions or dependencies distinct. Do not merge separate branches into a misleading single sequence or present incomplete work as finished. If consolidation would lose important context, leave the entries separate. Do not rewrite the trail after every message.

For example, completed source checks can become one entry: "2026-10-11 to 2026-10-12: Checked sources A and B; selected B because A had missing observations." This is an illustrative shape, not an event to copy into a project.

The trail is a compact aid to continuity, not an exhaustive audit log. Consolidation affects only agent-owned notes; merging, editing, or deleting user conclusions still requires the user's request and the normal preview-and-approval workflow.

## Notes and Connections

- Store each informational entity or idea once in the flat `nodes/` folder. Ordinary information notes have no mandatory type field or taxonomy; people use the separate contact-status convention above. Explain what it is in a short description.
- Store user conclusions in `conclusions/`, never embedded as substitutes for conclusion files elsewhere. Store deeper curated explanations in `details/`.
- Use readable, stable lowercase hyphenated filenames and a descriptive English title. Search for existing notes before proposing a duplicate. Do not rename an existing note just for naming consistency.
- Use vault-relative links without `.md`, with display titles: `[[nodes/transfer-agent|Transfer Agent]]`. Link to existing notes or notes included in the same approved batch, not speculative future files.
- Explain the relationship beside each link. An information note's link to a conclusion uses the label `Conclusion`, for example `- [[conclusions/price-alignment|Price Alignment]] — Conclusion`.
- Connections are many-to-many, with no fixed count limit. For each new link, explain the actual relationship and why navigating to the target is useful; co-occurrence in one research session is insufficient. Preserve the `Conclusion` label and explain the relationship in saved notes. Choose connections automatically after approval of the content being saved; link details are optional in the preview and available on request. Do not prune unrelated existing links or perform graph cleanup autonomously.
- A conclusion links back to relevant information notes. Put the `Conclusion` link in each relevant existing source note and a link in the README's Saved Conclusions section so the thought remains discoverable. If there is no relevant information note, the README link is sufficient; do not invent notes to fill a structure.
- A detail note identifies the information notes or conclusions it supports. Add a link to the detail in the relevant short note when approved.
- Keep empty sections out of individual notes. Sources and details links are optional when unavailable; never fabricate them.

## Note Shapes

These are content conventions, not mandatory metadata schemas. Adapt headings to the material while keeping short memory separate from deeper explanations.

**Information note (`nodes/`):** title, a short description of what it is and what matters, then relevant `Connections`, `Conclusions`, and `Details` sections. Keep it readable at a glance; move long explanations into an approved detail note. Do not confuse proposed information with the user's accepted conclusions.

**Person (`people/`):** contact-status frontmatter, name as title, short identity and research relevance, known personal contact route if supplied, sources/basis where useful, then specific `Connections`, `Conclusions` and `Details` links as needed. Contact status is not an importance rank or evidence-quality label.

**Conclusion (`conclusions/`):** title and the user's thought in usually one to three sentences, followed by relevant `Connections` and optional `Basis` links. Add context or scope only when supplied by the user or explicitly approved. A conclusion does not need a research report to exist.

**Detail (`details/`):** title, concise summary, substantive explanation or method, traceable evidence and sources, limitations or unresolved questions, and relevant `Connections`. Include only sections useful for that subject; do not paste raw tool output or conversation transcripts into curated memory.

## Reading and Research

- Read the README map, compact agent state, relevant information and people notes, and their linked conclusions first. Retrieve agent insights and preferences selectively; open deeper evidence only when needed. Saved conclusions are priority context for the next relevant research answer, not unrelated answers.
- Use `recall-memory` when an answer depends on saved research, for recall requests, or to retrieve relevant memory after a fresh session or compaction. Search titles and content using subject terms, alternative names, and translations into English when useful. Maps and links are entry points, not exhaustive indexes; search relevant conclusions directly even when unlinked.
- For "what did I think about this?", report the saved thought faithfully and distinguish it from current evidence and your assessment. Follow User Conclusions in Research above. An unsuccessful search means no matching record was found, not that the user never held or discussed the thought. Recall itself makes no memory changes.
- Distinguish recalling a saved view from checking factual support. Search for candidate notes before opening them; read relevant short conclusions in full. For verification, inspect candidate detail headings and approximate length, then read relevant evidence, sources and qualifications. Short, wholly relevant details may be read in full; longer or mixed-topic notes need targeted sections unless broader context is necessary. Re-read narrower sections when output is truncated. Expand searches for gaps and conflicts rather than imposing a fixed file count or link depth. Stop once the question is supported and material conflicts are addressed. Do not load every note or work file into context.
- Keep the research question and scope explicit. Propose changes to saved scope through the same approval workflow.
- Distinguish sourced facts, interpretations, hypotheses, user thoughts, and open questions. State uncertainty and conflicting evidence.
- Prefer primary sources when available. Record enough information to locate evidence again, including URL or document reference and relevant page or section. Do not invent quotations, sources, or results.
- Keep factual claims proportional to their evidence. This does not require the user's personal thoughts to be evidence-backed.

## Graph Presentation

Folder membership defines research-note color in `.obsidian/graph.json`: `nodes/` blue (`#3B82F6`), `conclusions/` orange (`#F59E0B`), `details/` gray (`#9CA3AF`). The optional root `glossary.md` has its own purple (`#8B5CF6`) group. People groups use `contact_status`: `contact` light green (`#91B89A`) and `public-figure` muted darker green (`#5B8A70`), tuned for a dark graph background. Color is also described in the note status; it is not the only way to identify access. Do not add per-note color fields or a general node taxonomy.

The default graph filter includes `nodes/`, `people/`, `conclusions/`, and `glossary.md` if created. The detail group is already configured for when details are shown. Instructions, skills, the README, `work/`, and `agent-memory/` are outside the main graph. This is a colored linked graph, not a spatial partition. Plain-text relationship labels are visible inside notes; standard graph edges do not show them.

For focused browsing, open the local graph of the active note and start at depth 1, increasing depth when useful. This is an optional view, not a limit on agent recall. Preserve the global graph and current colors; do not alter settings or remove connections merely to make a view sparse.

## Project Modules

Optional extensions belong to this research project only. Use `add-module` to review a requested module's design, clarify missing scope, explain likely context costs and propose a leaner alternative where useful. This is a qualitative design assessment, not a benchmark or confirmation of runtime functionality. Do not execute the module or run tests to assess it.

Agree on a short plan covering purpose, trigger, files read/written and proposed changes before adding it. That agreement covers the named module instructions and settings, plus a concise usage description; it does not approve research-content edits, change ownership of memory or silently add automatic-write permissions. Existing approval workflows still govern module writes. Keep the main instructions to a trigger and path; load the full local skill and supporting resources only when needed. Changes apply here, not to Factory or other projects.

## Lightweight Verification

After a user-approved memory write, check only affected files: approved text, correct folders, meaningful labels, and resolution of changed links. For approved renames or deletion, search incoming links and maintain the required references automatically; preview the rename/deletion and any substantive changes, not every mechanical link edit. Do not run whole-vault audits or produce compliance task lists during ordinary discussion.
