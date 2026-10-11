# Collaborative Research Project Instructions

This is an independent research project. Keep saved content in English.
Read `rules.md` for research principles and memory conventions, and `README.md` for the topic and entry points.
Apply the research approach in `rules.md` throughout research and discussion, not only when saving memory.

## Reading

- Start with the README map, the compact `agent-memory/state.md`, and relevant short notes in `nodes/`. Agent memory belongs to this project only.
- Before answering about a topic, retrieve its relevant notes in `conclusions/`, including useful unlinked conclusions. They are high-priority memory of the user's evolving understanding, including tentative or mistaken thoughts. Assess their factual scope and evidence independently; discuss material objections without editing saved wording.
- Use `.agents/skills/recall-memory/SKILL.md` for recall requests, research depending on prior work, and relevant memory retrieval after a fresh session or compaction. Search beyond the map and links, and report the user's saved thought faithfully. Recall itself is read-only; unrelated simple replies need no memory workflow.
- Open linked `details/` notes only when the question needs depth, evidence, or verification. Do not bulk-load the vault or `work/` into context.
- Consult relevant entries in `agent-memory/insights.md` and applicable preferences in `agent-memory/user.md` on demand. Keep agent hypotheses distinct from evidence and the user's saved thoughts. Recheck time-sensitive claims.
- After context compaction or a fresh session, return to the map, agent state, and relevant saved conclusions rather than relying only on the conversation summary.

## Writing

- User-controlled permanent memory is `README.md`, `nodes/`, `conclusions/`, and `details/`, including their links. Never create, edit, rename, or delete any of it without approval of a concrete preview.
- Research requests and phrases such as "remember this" trigger a preview; they do not bypass approval. If the user already approved that exact preview, apply it without asking again.
- Use `.agents/skills/update-memory/SKILL.md` for information notes, details, and maintenance of existing memory. Use `.agents/skills/create-conclusion/SKILL.md` when the user initiates a new conclusion.
- Only the user initiates conclusions. Do not propose conclusions of your own or automatically extract them from research.
- You may occasionally suggest saving a significant reusable result in `nodes/` or `details/`. Keep the suggestion short; do not append task lists or proposals to every answer.
- Use `.agents/skills/sync-agent-memory/SKILL.md` after meaningful research milestones or a user request to sync. You may update only `agent-memory/` without a per-entry preview under the bounded policy in `rules.md`. This permission does not extend to user-controlled memory, instructions, skills, settings, other projects, or machine-wide memory.
- Authorized research may produce temporary files in `work/`. They are not permanent memory; do not promote them without approval. Do not automatically delete them.
- Keep nodes flat, links meaningful, and folder names unchanged. `.obsidian/graph.json` defines graph colors; do not change settings or instructions incidentally during memory operations.
- For ordinary discussion, answer directly. Load a writing skill only when needed and verify only affected files after an approved write.

## GitHub Backup

- Use `.agents/skills/setup-git/SKILL.md` for requested first-time GitHub setup and `.agents/skills/save-project/SKILL.md` for requested commit/push backups.
- This project's Git remote is its backup destination. No factory configuration or organization is embedded here. Do not auto-push after research or memory updates.
- Saving existing files to Git does not authorize changes to user-controlled memory. `.gitignore` excludes temporary `work/` contents and machine-specific files; track the graph configuration and both memory layers.
