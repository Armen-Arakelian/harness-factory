# Collaborative Research Project Instructions

This is an independent research project. Keep saved content in English, except the explicitly configured glossary languages.
## Entering the Project

Read `rules.md` before project work, unless its current contents are already loaded. Use README's Topic and Memory Map and the compact `agent-memory/state.md` for orientation; the Reading section below guides further retrieval. Apply the research approach throughout discussion, not only saves. README is an additional entry route; `CLAUDE.md` and `GEMINI.md` only import this file. Do not recursively reread entry files or preload all skills.

Follow the instruction and conflict policy in `rules.md`. At the first relevant project task, establish access to its actual files and needed tools from the available environment; an attachment is not proof of a writable vault. If an instruction or required tool is unavailable, name the limitation and continue useful read-only work. Local skills can be read by their paths even when the application does not auto-discover them. Before a memory write, the selected workflow and Python approval helper must be available; otherwise offer a proposal without saving or claiming registry validation. Inline cards require the supported message bridge; use the existing text fallback when unavailable. No startup transcript, checkpoint or repeated capability checklist is required.

## Pending Approval Turns

Before other work on a user turn, if `work/memory-approvals.json` exists, handle any pending preview through `python3 .agents/skills/memory-approval/scripts/approval.py`. For an ordinary message (including clarification), run `expire`. For an unambiguous approval/cancellation, read `.agents/skills/memory-approval/SKILL.md` and validate its ID with `approve`/`cancel`; widget-state updates alone never count. At a fresh chat or after compaction, expire pending previews even if the first message contains an old approval. If unsure, expire rather than save. Only an accepted helper result permits the writing skill to apply its returned preview. This small local bookkeeping step is separate from research memory and creates no state checkpoint or user-facing checklist. There is no automatic message event hook or guarantee of visual button expiry.

## Reading

- Start with the README map, the compact `agent-memory/state.md`, and relevant short notes in `nodes/` and `people/`. Agent memory belongs to this project only.
- Before answering about a topic, retrieve its relevant notes in `conclusions/`, including useful unlinked conclusions. They are high-priority memory of the user's evolving understanding, including tentative or mistaken thoughts. Assess their factual scope and evidence independently; discuss material objections without editing saved wording.
- Use `.agents/skills/recall-memory/SKILL.md` for recall requests, research depending on prior work, and relevant memory retrieval after a fresh session or compaction. Search beyond the map and links, and report the user's saved thought faithfully. Recall itself is read-only; unrelated simple replies need no memory workflow.
- Use `.agents/skills/review-conclusions/SKILL.md` for a requested review of all conclusions or a specified subset. Search relevant information, people and details beyond their links; report only grounded concerns or an honest clean/insufficient-evidence result. The review is read-only and creates no agent-memory checkpoint.
- Recall saved views from relevant short notes first. For evidence checks, locate useful detail sections and read their qualifications; expand for gaps or conflicts without a fixed file count or graph depth. Do not bulk-load the vault or `work/` into context.
- Consult relevant entries in `agent-memory/insights.md` and applicable preferences in `agent-memory/user.md` on demand. Keep agent hypotheses distinct from evidence and the user's saved thoughts. Recheck time-sensitive claims.
- After context compaction or a fresh session, return to the map, compact agent state and relevant saved conclusions. Reconcile the recorded next step with the current request and available artifacts rather than relying only on a conversation summary or stale state.

## Writing

- For every new or revised save preview, use `memory-approval` immediately. When `visualize` is available in the current skills, read it and present the approval card in the first preview response; do not default to a text question or wait for the user to request a button. The card itself checks the message bridge. Use text only if the capability is absent, the user requests text, or rendering actually fails. Earlier text-only replies do not establish that buttons are unsupported.

- User-controlled permanent memory is `README.md`, `research-topics.md`, `nodes/`, `people/`, `conclusions/`, and `details/`. Preview substantive content, destinations and requested renames/deletions before saving. After content approval, choose useful connections and maintain related reverse links/map entries automatically within that save; do not enumerate mechanical link edits unless asked. Unrelated content and graph cleanup remain outside that approval.
- Research requests and phrases such as "remember this" trigger a preview; they do not bypass approval. Use `memory-approval` to register and validate previews, with buttons when supported and text fallback otherwise. An immediately accepted identical preview needs no second approval; old chat approvals do not bypass the registry.
- Use `.agents/skills/update-memory/SKILL.md` for information notes, people, details, and maintenance of existing memory. Use `.agents/skills/create-conclusion/SKILL.md` when the user initiates a new conclusion.
- Use `.agents/skills/manage-research-topics/SKILL.md` when the user asks to show, add, revise or review future research topics. Changes to `research-topics.md` require a requested preview and accepted approval; never maintain it automatically after research or conclusion saves. Topic-list maintenance alone creates no research checkpoint.
- Use `.agents/skills/manage-glossary/SKILL.md` when asked to create or review the optional glossary, or after a successful substantive information save if it is enabled. Only `glossary.md` may be maintained under this separate permission; follow its current-save scope and configured languages.
- Store people in flat `people/` notes with an approved `contact_status` of `contact` or `public-figure`. Never infer personal access from fame, employment or a public email. Choose links for specific research relevance, not all topics associated with their employer; follow the People section in `rules.md`.
- Only the user initiates conclusions. Do not propose conclusions of your own or automatically extract them from research.
- You may occasionally suggest saving a significant reusable result in `nodes/` or `details/`. Keep the suggestion short; do not append task lists or proposals to every answer.
- Use `.agents/skills/sync-agent-memory/SKILL.md` after meaningful research results, direction changes, completed user reviews, approved memory edits affecting active work, or an explicit sync or handoff request. Ordinary discussion and read-only recall need no checkpoint. You may update only `agent-memory/` without a per-entry preview under the bounded policy in `rules.md`. This agent-memory permission does not extend to other files; the optional glossary has its own narrow policy below in `rules.md`. User-controlled memory, instructions, skills, settings, other projects and machine-wide memory remain outside both automatic-write permissions.
- Authorized research may produce temporary files in `work/`. They are not permanent memory; do not promote them without approval. Do not automatically delete them.
- Keep nodes flat, links meaningful, and folder names unchanged. `.obsidian/graph.json` defines graph colors; do not change settings or instructions incidentally during memory operations.
- For ordinary discussion, answer directly. Load a writing skill only when needed and verify only affected files after an approved write.

## Project Modules

Use `.agents/skills/add-module/SKILL.md` when the user describes a new reusable project capability, external integration or extension, even without saying "module". If a local module would help, briefly propose it before the normal design review and plan. Prefer existing skills for supported workflows; do not turn one-off tasks into modules or append suggestions to ordinary replies. Assess its design and likely context overhead without running it or testing it. Agree on a concise implementation plan before installation. Keep module instructions in their local skill folder; add only a short trigger/path here. Load them only for the relevant task. Module setup does not bypass existing memory approval or authorize installing external software, contacting people or background jobs beyond the agreed scope.

## GitHub Backup

- Use `.agents/skills/setup-git/SKILL.md` for requested first-time GitHub setup and `.agents/skills/save-project/SKILL.md` for requested commit/push backups.
- This project's Git remote is its backup destination. No factory configuration or organization is embedded here. Do not auto-push after research or memory updates.
- Saving existing files to Git does not authorize changes to user-controlled memory. `.gitignore` excludes temporary `work/` contents and machine-specific files; track the graph configuration and both memory layers.
