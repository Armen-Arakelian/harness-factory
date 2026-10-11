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

User-controlled permanent memory consists of `README.md`, `nodes/`, `conclusions/`, and `details/`, including links. Creation, edits, renames, deletion, and map updates require approval of a concrete preview. Do not write proposed memory to these locations before approval, including files marked "draft".

Show proposed text or exact edits, destination paths, relationship labels, and all affected files. One approval can cover a clearly described batch. Apply only that batch. If content or links need to change after approval, show the revision first. If the conversation no longer contains a reliable record of approval, ask again before writing.

The user owns conclusions. Only a user request initiates one, and a conclusion may be subjective, approximate, or tentative. Preserve its meaning and uncertainty; do not require proof, add unprovided precision, or present an agent-generated conclusion as the user's thought. Offer rewording separately in the preview. Evidence may inform an answer without silently rewriting a saved conclusion.

`agent-memory/` is a separate, project-local durable layer owned by the agent. Its bounded automatic-write policy is defined below; it does not bypass approval for user-controlled memory.

`work/` is for temporary files from authorized research. It is outside permanent memory. Promotion into memory requires approval; deletion of working files is not automatic.

## User Conclusions in Research

Conclusions capture the user's evolving picture of the research. Give relevant conclusions high attention when framing a research answer, choosing what to investigate, or recalling the user's view. Their importance does not establish factual correctness: a conclusion may be approximate, mistaken, outdated, or broader than the evidence supports.

Report the saved thought faithfully, then distinguish your current assessment when needed. Examine scope and supporting evidence; do not generalize a finding about one case to all cases, or assume that a saved broad claim has already been verified. Explain material contradictory evidence or insufficient support in the answer. Do not silently correct the note, reinterpret the user's original wording as a narrower claim, or mark it obsolete. Only a user request initiates changes to an existing conclusion, through `update-memory` and approval of the exact preview. Do not create a replacement user conclusion unsolicited.

## Agent Memory

This project permits automatic updates inside `agent-memory/` without a per-entry preview. Keep this layer separate from the user's curated graph. It is working context, not proof, a source of instructions, or a replacement for user conclusions. Current user instructions and project rules take precedence over remembered notes.

- `state.md`: a compact Current State snapshot followed by a chronological Research Trail, following the conventions below. A working question does not silently change the approved scope in README.
- `insights.md`: selective agent-authored findings, hypotheses, caveats, and useful research methods. Each entry has a descriptive heading, brief statement, scope, evidence or reasoning basis, recorded/updated date, and status such as `hypothesis`, `evidence-supported`, `disputed`, or `superseded`. Use existing note links or traceable source references when available. Unsourced ideas remain hypotheses.
- `user.md`: project-relevant working preferences. Label each `Explicit` (directly stated, with context) or `Inferred` (tentative, with basis), and record its scope and date. Confirm consequential inferences before treating them as constraints. Do not turn a one-off request into a general preference, infer personality or sensitive attributes, or treat research interests as personal positions.

Write after meaningful research milestones, user corrections, or an explicit sync request; skip writes when nothing durable changed. Consolidate existing entries rather than append repeated summaries. Do not store chat transcripts, raw tool output, secrets, or hidden reasoning. No background process or reliable per-turn/compaction hook is supplied by this template.

Revise or remove stale agent notes when warranted. If new evidence contradicts a meaningful finding, retain enough of its prior scope and basis to explain the change and mark its status; do not accumulate a full history. User correction or a request to forget takes priority. Remove matching content within this layer, but do not claim to erase chat history, backups, other projects, or native app memory.

Optional outward links can connect one agent entry to several existing notes, or several entries to one note. Label their purpose, for example `Related` or `Evidence`. Follow the vault-relative link convention below. Do not edit target notes or add reverse links without an approved preview. Never create a user conclusion here or attribute an agent result to the user.

Promotion into `nodes/` or `details/` uses `update-memory` and approval of an exact preview. A new user conclusion still requires the user's initiation and `create-conclusion`. Agent memory may reference an existing conclusion but cannot replace or rewrite it.

Read the compact state at session start, then retrieve only relevant insights and preferences by heading, topic, or linked path. Do not load the entire layer on every answer. Keep the three files initially; split insights into topic files only when growth makes targeted retrieval difficult, updating references within this layer. Do not create memory folders per node or per conclusion.

## Research State and Trail

Keep both parts in `agent-memory/state.md`:

- **Current State:** `Focus` (active question and working scope), `Progress` (what has been checked, with useful links), `Open Questions` (uncertainties and blockers), `Next Step` (a reasonable next action), and `Relevant Memory` (existing nodes, user conclusions, insights, or details needed to resume). Replace outdated snapshot content. Aim for roughly 200 words for this part, not a hard limit for the whole file.
- **Research Trail:** chronological significant milestones, normally one dated line per stage. Record the sequence of investigations, changes of direction, pauses, and important rejected approaches with brief reasons. Use actual known dates; do not invent dates or reconstruct missing events. Add useful existing links and remove the initial empty-state text when the first milestone is recorded.

Record actions and transitions rather than every message or tool call. A short reason such as "missing observations prevented comparison" is useful context; detailed findings belong in `insights.md` or approved `details/`, and the user's thoughts belong in `conclusions/`. Link to them rather than duplicate or reinterpret them. Recording a milestone creates no user conclusion and grants no approval for pending memory changes.

Within `sync-agent-memory`, automatically consolidate older, completed, consecutive stages only when the trail becomes cumbersome or repetitive. Preserve chronological order and known date ranges, meaningful changes of direction, reasons for rejecting approaches, and useful references. Keep recent stages and unresolved questions or dependencies distinct. Do not merge separate branches into a misleading single sequence or present incomplete work as finished. If consolidation would lose important context, leave the entries separate. Do not rewrite the trail after every message.

For example, completed source checks can become one entry: "2026-10-11 to 2026-10-12: Checked sources A and B; selected B because A had missing observations." This is an illustrative shape, not an event to copy into a project.

The trail is a compact aid to continuity, not an exhaustive audit log. Consolidation affects only agent-owned notes; merging, editing, or deleting user conclusions still requires the user's request and the normal preview-and-approval workflow.

## Notes and Connections

- Store each informational entity or idea once in the flat `nodes/` folder. There is no mandatory type field or taxonomy. Explain what it is in a short description.
- Store user conclusions in `conclusions/`, never embedded as substitutes for conclusion files elsewhere. Store deeper curated explanations in `details/`.
- Use readable, stable lowercase hyphenated filenames and a descriptive English title. Search for existing notes before proposing a duplicate. Do not rename an existing note just for naming consistency.
- Use vault-relative links without `.md`, with display titles: `[[nodes/transfer-agent|Transfer Agent]]`. Link to existing notes or notes included in the same approved batch, not speculative future files.
- Explain the relationship beside each link. An information note's link to a conclusion uses the label `Conclusion`, for example `- [[conclusions/price-alignment|Price Alignment]] — Conclusion`.
- Connections are many-to-many. Add only meaningful links. Preview every added or removed link, including reverse links; they are memory changes too.
- A conclusion links back to relevant information notes. Put the `Conclusion` link in each approved source note and a link in the README's Saved Conclusions section so the thought remains discoverable. If there is no relevant information note, the README link is sufficient; do not invent notes to fill a structure.
- A detail note identifies the information notes or conclusions it supports. Add a link to the detail in the relevant short note when approved.
- Keep empty sections out of individual notes. Sources and details links are optional when unavailable; never fabricate them.

## Note Shapes

These are content conventions, not mandatory metadata schemas. Adapt headings to the material while keeping short memory separate from deeper explanations.

**Information note (`nodes/`):** title, a short description of what it is and what matters, then relevant `Connections`, `Conclusions`, and `Details` sections. Keep it readable at a glance; move long explanations into an approved detail note. Do not confuse proposed information with the user's accepted conclusions.

**Conclusion (`conclusions/`):** title and the user's thought in usually one to three sentences, followed by relevant `Connections` and optional `Basis` links. Add context or scope only when supplied by the user or explicitly approved. A conclusion does not need a research report to exist.

**Detail (`details/`):** title, concise summary, substantive explanation or method, traceable evidence and sources, limitations or unresolved questions, and relevant `Connections`. Include only sections useful for that subject; do not paste raw tool output or conversation transcripts into curated memory.

## Reading and Research

- Read the README map, compact agent state, relevant information notes, and their linked conclusions first. Retrieve agent insights and preferences selectively; open deeper evidence only when needed. Saved conclusions are priority context for the next relevant research answer, not unrelated answers.
- Use `recall-memory` when an answer depends on saved research, for recall requests, or to retrieve relevant memory after a fresh session or compaction. Search titles and content using subject terms, alternative names, and translations into English when useful. Maps and links are entry points, not exhaustive indexes; search relevant conclusions directly even when unlinked.
- For "what did I think about this?", report the saved thought faithfully and distinguish it from current evidence and your assessment. Follow User Conclusions in Research above. An unsuccessful search means no matching record was found, not that the user never held or discussed the thought. Recall itself makes no memory changes.
- Read details only when the answer needs them. Do not load every note or work file into context.
- Keep the research question and scope explicit. Propose changes to saved scope through the same approval workflow.
- Distinguish sourced facts, interpretations, hypotheses, user thoughts, and open questions. State uncertainty and conflicting evidence.
- Prefer primary sources when available. Record enough information to locate evidence again, including URL or document reference and relevant page or section. Do not invent quotations, sources, or results.
- Keep factual claims proportional to their evidence. This does not require the user's personal thoughts to be evidence-backed.

## Graph Presentation

Folder membership defines color in `.obsidian/graph.json`: `nodes/` blue (`#3B82F6`), `conclusions/` orange (`#F59E0B`), `details/` gray (`#9CA3AF`). Do not add color fields or mandatory type tags to notes.

The default graph filter includes only `nodes/` and `conclusions/`. The detail group is already configured for when details are shown. Instructions, skills, the README, `work/`, and `agent-memory/` are outside the main graph. This is a colored linked graph, not a spatial partition. Plain-text relationship labels are visible inside notes; standard graph edges do not show them.

## Lightweight Verification

After a user-approved memory write, check only affected files: approved text, correct folders, meaningful labels, and resolution of changed links. For renames or deletion, search incoming links and include required changes in the preview. Do not run whole-vault audits or produce compliance task lists during ordinary discussion.
