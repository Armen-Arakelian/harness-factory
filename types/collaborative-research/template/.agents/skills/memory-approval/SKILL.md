---
name: memory-approval
description: Register an exact research-memory preview, present approval cards by default when visualize is available, and validate one-use approval or cancellation IDs. Used by update-memory, create-conclusion, manage-research-topics and manage-ideas; does not decide what to save.
---

# Memory Approval

Resolve paths from the project root, three directories above this skill folder. The helper is `python3 .agents/skills/memory-approval/scripts/approval.py`; it uses only Python's standard library. Its `apply` command writes the agent-prepared approved content and delegated links under the same project-wide lock used for validation. The local registry is `work/memory-approvals.json`, outside the graph and Git.

## Turn Handling

Every command requires `--session <CHAT_ID>`. Use the host's stable current chat ID when exposed. Otherwise generate a UUID once for this chat and retain it in this chat's context; never use a project name, shared file, another chat's token or a common default. A session ID is routing metadata, not a security credential. If identity is lost after compaction, use a new UUID and fresh preview; do not guess an old session from the registry.

The short rule in project `AGENTS.md` applies before other work on each user turn. An ordinary message expires only this chat's proposals, including clarifications, topic changes and "yes, but…". Only an unambiguous approval/cancellation of the exact displayed preview takes the ID-validation branch. Widget-state notifications alone are never authorization. At fresh chat startup, expire only the current session; after compaction expire the known current session and require a fresh preview. Never expire another chat's records. If classification is uncertain, expire this session and offer a fresh preview. There is no clock-based deadline: a five-minute pause or activity in another chat does not expire a proposal. `created_at` is diagnostic only. Each session has one pending proposal; different sessions can wait independently.

This is agent-driven turn handling, not a background event hook. A stale button can remain visible or send a request. The registry check rejects expired IDs; it cannot discover a user message the agent failed to process. Do not promise automatic visual expiry or filesystem enforcement.

## Register and Present

1. Before preparing the preview, run `snapshot --session <CHAT_ID> --paths <target> ...` and save its JSON result to a uniquely named file in `work/`. Use the returned current text to prepare the exact English substantive text and destinations. Store the preview in another uniquely named `work/` file, never a fixed filename shared by chats, with this shape:

   ```json
   {"kind":"information","title":"Chinese Dragon","changes":[{"path":"nodes/chinese-dragon.md","action":"create","text":"The exact substantive text shown to the user."}]}
   ```

   `kind` is `information`, `conclusion`, `details`, `maintenance`, `topics`, `ideas`, `person` or `batch`; each change has `path`, `action` (`create`, `edit`, `delete`) and `text`. An edit shows exact replacement text with enough context to identify the edit; deletion describes what is removed. A rename is a deletion plus creation, explicitly explained. Preview every substantive change in a batch. Mechanical connections remain delegated to the writing skill. A `topics` preview targets only `research-topics.md`; its changed questions, statuses, related links and remaining questions are part of the approved text.
   An `ideas` preview targets only `ideas.md`; exact entry text and user-selected ratings are approved together.
   Single people saves use `person` (or `maintenance` for mixed maintenance) and target `people/<name>.md`. For creation or editing, include the full substantive note with canonical `contact_status` frontmatter as defined in `rules.md`; its status is part of the approved text. Use `batch` for two or more substantive note changes, including people with information/details; each person creation/edit still requires its complete substantive text and contact status. A single registry ID covers the exact entire package. Present every entry inside one card with one Approve/Cancel pair. An ordinary message revising any entry expires that ID; show the revised package before accepting it. The helper returns all accepted changes together; `apply` serializes writes but does not guarantee transactional multi-file rollback.
2. Run `create --session <CHAT_ID> --preview work/<unique-preview>.json --basis work/<unique-snapshot>.json`. It rejects targets changed since the snapshot, creates a unique ID, supersedes only this chat's older proposals, and records the exact preview checksum and target hashes. Version 1 records have no chat ownership or baseline: they are preserved as legacy data but never authorize a save; present a fresh preview after upgrade.
3. Choose the presentation before responding. If `visualize` is listed in the current skills, read its complete SKILL.md and render the card by default, including on the first preview and every revision. Do not assume the message bridge is unavailable without rendering: the card feature-detects `window.openai.sendFollowUpMessage` at runtime. Follow the visualization skill's current rendering instructions. Run `render --session <CHAT_ID> --id <ID> --output <new-absolute-authorized-visualization-path>` to generate the fragment from `assets/card.html`, then present it using the supported inline mechanism. The output path must be writable and visible to this conversation. Never require users to install a plugin or start a web server just to approve.
4. Use text only when the visualization capability is absent, the user explicitly requests text, or a concrete rendering failure prevents the card. Then show the compact text preview and ask for `Approve ID: <ID>` or `Cancel ID: <ID>`. If the card renders but the message bridge is unavailable, it hides the buttons and shows a text fallback. Rendering failure uses the same registered ID and exact preview; no save is implied.

Keep the response to a short lead-in such as "Save this conclusion?" plus the card. The card already contains the title, destination and exact text: do not repeat them in prose, add a second text approval question, narrate the registry procedure or list connections. Keep factual objections brief and separate from the user's thought. Do not praise an unsupported formulation as correct. Explain a real blocking error when necessary; do not add unsolicited technical explanations. The preview choice is the approval already required by the project rules, not another approval layer.

Information is blue, people green and conclusions orange; details have a gray label and ideas a purple label. Buttons highlight on hover, hide on use, and show `Approval sent` or `Cancelled`. `Approval sent` means the request was sent, not accepted or saved. The callback contains only the user's choice, title and ID, never workflow instructions or the whole preview. Cancel also sends its short choice so the agent can close the registry entry.

## Validate and Finish

- On an approval, run `approve --session <CHAT_ID> --id <ID>` before any curated edit. Only exit code 0 with `status: accepted` authorizes the returned exact preview. It consumes approval once under a local lock and checks targets against their preview baselines. Unknown IDs, another chat's IDs, changed targets/previews, and superseded, expired, cancelled or already consumed records are rejected. Never bypass a failure or reconstruct authorization from chat.
- A plain "yes" can refer to the pending ID only as the immediate, unambiguous reply to this exact preview in the same chat. It must still pass the helper. A broader "remember this" request is not approval.
- On cancellation, run `cancel --session <CHAT_ID> --id <ID>`. Ordinary messages use `expire --session <CHAT_ID>`. Neither affects other chats or creates a research checkpoint.
- After acceptance, use `snapshot --session <CHAT_ID> --paths ...` for all substantive targets and every related mechanical link/map file to be written. Prepare a uniquely named JSON manifest in `work/`:

  ```json
  {"writes":[{"path":"nodes/chinese-dragon.md","expected_sha256":null,"text":"# Chinese Dragon\n\nThe exact approved substantive text.\n"}]}
  ```

  Each entry contains the full final file text (or `null` to delete) and the latest snapshot's `sha256` (`null` only when absent). Include every approved substantive destination exactly once. Additional files may contain only delegated related link/map changes; the helper checks paths and versions, while the agent remains responsible for exact approved meaning, faithful edits, and permitted links. Never use this manifest for unrelated prose, settings, glossary or agent-memory changes.
- Run `apply --session <CHAT_ID> --id <ID> --manifest work/<unique-manifest>.json`. Do not write curated files directly with shell/editor tools. The helper checks all expected hashes and the original substantive baselines before its first write and holds the project lock through all writes, including README and backlinks. Another helper save cannot interleave. External editors and agents running old instructions do not honor this lock; do not claim filesystem-wide enforcement.
- If only a mechanical file changed, reread it and rebuild the manifest with current links and hashes, then retry `apply` using the same consumed ID: no write began on a preflight rejection. If a substantive target changed, require a fresh preview and ID. Any change to approved text, destination or meaning requires a fresh preview too. Do not update the original baseline to bypass a conflict.
- `apply` is one-use after a successful write. It records `applying`, written paths, then `applied` or `failed`. A partial failure or interrupted write must never be retried blindly: inspect actual files and offer a fresh preview for remaining work. There is no multi-file rollback. A crash can leave a lock; stop and explain rather than removing/bypassing it automatically.
- Verify affected saved files and links, then confirm only actual outcomes: "Saved", "Cancelled", or "This preview expired; a new preview is needed." A button click or accepted approval alone does not mean saved.
