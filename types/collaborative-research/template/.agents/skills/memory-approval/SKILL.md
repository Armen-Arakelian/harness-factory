---
name: memory-approval
description: Register an exact research-memory preview, present approval cards by default when visualize is available, and validate one-use approval or cancellation IDs. Used by update-memory, create-conclusion and manage-research-topics; does not decide what to save.
---

# Memory Approval

Resolve paths from the project root, three directories above this skill folder. The helper is `python3 .agents/skills/memory-approval/scripts/approval.py`; it uses only Python's standard library. It never writes curated notes. The local registry is `work/memory-approvals.json`, outside the graph and Git.

## Turn Handling

The short rule in project `AGENTS.md` applies before other work on each user turn. An ordinary message expires a pending proposal, including clarifications, topic changes and "yes, but…". Only an unambiguous approval/cancellation of the exact displayed preview takes the ID-validation branch. Widget-state notifications alone are never authorization. Run `expire` at a new chat or after compaction; do not revive a proposal from summaries, widget state, copied files or backup. If classification is uncertain, expire and offer a fresh preview.

This is agent-driven turn handling, not a background event hook. A stale button can remain visible or send a request. The registry check rejects expired IDs; it cannot discover a user message the agent failed to process. Do not promise automatic visual expiry or filesystem enforcement.

## Register and Present

1. Let the calling writing skill prepare the exact English substantive text and destinations. Store a JSON preview in `work/` with this shape:

   ```json
   {"kind":"information","title":"Chinese Dragon","changes":[{"path":"nodes/chinese-dragon.md","action":"create","text":"The exact substantive text shown to the user."}]}
   ```

   `kind` is `information`, `conclusion`, `details`, `maintenance`, `topics` or `person`; each change has `path`, `action` (`create`, `edit`, `delete`) and `text`. An edit shows exact replacement text with enough context to identify the edit; deletion describes what is removed. A rename is a deletion plus creation, explicitly explained. Preview every substantive change in a batch. Mechanical connections remain delegated to the writing skill. A `topics` preview targets only `research-topics.md`; its changed questions, statuses, related links and remaining questions are part of the approved text.
   People saves use `person` (or `maintenance` for mixed maintenance) and target `people/<name>.md`. For creation or editing, include the full substantive note with canonical `contact_status` frontmatter as defined in `rules.md`; its status is part of the approved text. A `person` batch may include supporting approved details.
2. Run `create --preview work/<preview>.json`. It creates a unique ID, replaces any older proposal, and records immutable preview content with a checksum. There is one active proposal per project; concurrent chats should coordinate rather than share pending approvals.
3. Choose the presentation before responding. If `visualize` is listed in the current skills, read its complete SKILL.md and render the card by default, including on the first preview and every revision. Do not assume the message bridge is unavailable without rendering: the card feature-detects `window.openai.sendFollowUpMessage` at runtime. Follow the visualization skill's current rendering instructions. Run `render --id <ID> --output <new-absolute-authorized-visualization-path>` to generate the fragment from `assets/card.html`, then present it using the supported inline mechanism. The output path must be writable and visible to this conversation. Never require users to install a plugin or start a web server just to approve.
4. Use text only when the visualization capability is absent, the user explicitly requests text, or a concrete rendering failure prevents the card. Then show the compact text preview and ask for `Approve ID: <ID>` or `Cancel ID: <ID>`. If the card renders but the message bridge is unavailable, it hides the buttons and shows a text fallback. Rendering failure uses the same registered ID and exact preview; no save is implied.

Keep the response to a short lead-in such as "Save this conclusion?" plus the card. The card already contains the title, destination and exact text: do not repeat them in prose, add a second text approval question, narrate the registry procedure or list connections. Keep factual objections brief and separate from the user's thought. Do not praise an unsupported formulation as correct. Explain a real blocking error when necessary; do not add unsolicited technical explanations. The preview choice is the approval already required by the project rules, not another approval layer.

Information is blue, people green and conclusions orange; details have a gray label. Buttons highlight on hover, hide on use, and show `Approval sent` or `Cancelled`. `Approval sent` means the request was sent, not accepted or saved. The callback contains only the user's choice, title and ID, never workflow instructions or the whole preview. Cancel also sends its short choice so the agent can close the registry entry.

## Validate and Finish

- On an approval, run `approve --id <ID>` before any curated edit. Only exit code 0 with `status: accepted` authorizes applying the returned exact preview. It consumes the ID once, under a local lock. Missing/corrupt registry, unknown, superseded, expired, cancelled, consumed or changed previews are rejected. Never bypass a failure or reconstruct authorization from the chat.
- A plain "yes" can refer to the pending ID only when it is the immediate, unambiguous answer to this exact preview in the same chat. It must still pass the helper. Do not apply a broader "remember this" request as approval.
- On cancellation, run `cancel --id <ID>`. Rejection or silence never authorizes writing. An ordinary message instead uses `expire` before continuing the conversation. Checking or closing the registry creates no research checkpoint by itself.
- After acceptance, the calling skill rechecks affected files, applies only the approved substantive changes and related mechanical links, and verifies them. If substantive conflicts or a failed write require another attempt, issue a fresh preview and ID; do not reopen a consumed entry. A process crash may leave a lock; stop and explain rather than bypass it.
- Confirm only actual outcomes, briefly: "Saved", "Cancelled", or "This preview expired; a new preview is needed." Report a failed or partial write honestly. Do not claim memory was saved just because a button was pressed.
