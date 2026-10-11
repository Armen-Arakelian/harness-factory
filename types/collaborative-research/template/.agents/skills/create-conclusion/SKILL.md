---
name: create-conclusion
description: Preview and save a short personal thought or conclusion only when the user asks to remember it as their conclusion, with approval of its wording and connections before writing.
---

# Create a User Conclusion

The project root is three directories above this skill folder. Read its `rules.md` when using this workflow. Resolve project paths from that root.

1. Start only from a user request. Capture the user's thought, preserving uncertainty and intent. If it is unclear whether they want information saved or a personal conclusion, clarify before choosing. Do not infer a new conclusion from the agent's research result or suggest one unsolicited.
2. Read relevant short notes, existing conclusions, and README entries. Propose links to existing notes or other explicitly requested notes in the same batch. Do not open detail notes unless necessary to understand the requested thought.
3. Preview in chat:
   - Destination: `conclusions/descriptive-name.md`.
   - The user's original thought and exact English text to save. If rephrased, make the alternative explicit so it can be accepted or rejected. Usually keep the thought to one to three sentences; do not add unsupported scope or numerical precision.
   - All connections and their labels. Include the conclusion's links back to relevant information notes, a `Conclusion` link in each source note, and the README Saved Conclusions entry. Show exact changes to every affected file.
   - Optional basis links only when available and relevant. No proof or detail note is required for a personal thought.
4. Ask whether this exact batch should be saved. Do not create the conclusion, source links, or map entry before approval. Revise the preview if requested. If the exact preview was already approved, proceed without asking again.
5. Before writing, check affected files have not changed since the preview. If they have, show a revised preview. Save only the approved batch and verify its text and links. Report the saved conclusion briefly.

If a similar conclusion already exists, show it and clarify whether the user wants another thought or an update. Use `update-memory` for a requested update; never silently merge, replace, or strengthen an existing conclusion.
