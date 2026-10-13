---
name: create-conclusion
description: Preview a short user-initiated thought and save it after wording approval, choosing relevant graph links automatically.
---

# Create a User Conclusion

The project root is three directories above this skill folder. Read its `rules.md` and resolve paths from that root.

For each new or revised preview, read `../memory-approval/SKILL.md` before presenting it. With `visualize` available, the initial response must contain the approval card, rather than a text-only question. Do not repeat the preview outside the card. Approval is required by the project rules; this skill implements that existing choice, not an additional permission step.

1. Start from the user's request. Preserve their thought, uncertainty and intent. Clarify if the request could mean information rather than a personal conclusion; never derive a user conclusion from your own research result.
2. Read relevant short information/people notes, existing conclusions and README entries. Select useful existing targets; do not read details unless needed to understand the thought. If a similar conclusion exists, clarify new versus update; requested updates use `update-memory`.
3. Show a compact preview: `conclusions/descriptive-name.md`, a readable title and the exact English thought to save, usually one to three sentences. If reworded, make the alternative clear. Preserve ownership and add scope only when supplied or approved. Do not display generated Connections/Basis sections, reverse-link diffs or README edits unless requested. No proof or detail note is required for a personal thought.
4. Use `../memory-approval/SKILL.md` to register the exact thought and present an orange conclusion card when supported, otherwise a compact text approval. Do not create the conclusion or related links before an accepted ID check. Rejection, silence or an intervening ordinary message means no write. Do not ask twice for content just accepted by the helper; re-preview changes to meaning, wording, scope or destination.
5. After approval, save the thought and automatically add useful connections, the `Conclusion` reverse links in related notes and its README Saved Conclusions entry. Use existing targets or notes approved in the same batch. Explain relationships in saved notes without implying unestablished factual support. Do not create supporting notes, rewrite unrelated content or prune unrelated links. Link choices need no separate approval; disclose them if asked or if they would change the approved meaning.
6. Recheck files before writing. Preserve intervening changes, re-preview substantive conflicts and recompute mechanical links against current files. Verify the approved thought and changed links, then confirm briefly. Never silently merge, replace or strengthen another conclusion.
