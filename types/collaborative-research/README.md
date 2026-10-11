# Collaborative Research

A research partnership between the user and an AI assistant, with independent judgment, iterative investigation, a curated graph controlled by the user, and separate project-local agent working memory.

## Quick Start

Use this template for an ongoing investigation where your saved understanding matters across chats. Ask the Factory to create a project with a name, topic, and destination. Open the result in Codex and Obsidian. Discuss and research normally; approve specific notes before saving them, initiate your own conclusions, and request GitHub backups when needed.

For tools, SSH, GitHub, and personal Factory configuration, start with [the Factory user guide](../../docs/USER_GUIDE.md). The complete template instructions follow below.

## Purpose

Explore questions deeply, critically assess assumptions and evidence, and build understanding over time. The agent does not agree merely to please the user or try to finish every problem in one answer. Saved conclusions represent the user's thoughts and remain open to grounded discussion without silent edits.

## Type Contents

- `project.json`: the display name, description, and required `topic` parameter.
- `template/`: the complete independent project, including research rules, local skills, and Obsidian graph settings. Do not open this blueprint as an active research vault.
- `template/rules.md`: the single source for this type's research and memory rules. Edit here to change future projects; there is no factory-wide research standard.

## Generated Project

```text
AGENTS.md
README.md
rules.md
nodes/
conclusions/
details/
agent-memory/
    state.md
    insights.md
    user.md
work/
.agents/skills/
    update-memory/SKILL.md
    create-conclusion/SKILL.md
    sync-agent-memory/SKILL.md
    recall-memory/SKILL.md
    setup-git/SKILL.md
    save-project/SKILL.md
.gitignore
.obsidian/graph.json
```

- `nodes/` contains short information notes with meaningful many-to-many connections and no mandatory entity taxonomy.
- `conclusions/` contains short thoughts initiated only by the user. The agent reads related conclusions before a relevant answer.
- `details/` contains curated deeper explanations, evidence, methods, and limitations, opened when needed.
- `README.md` provides a small memory map and links to saved conclusions.
- `agent-memory/` holds agent-owned state, selective findings and hypotheses, and project-relevant preferences. Automatic milestone updates are limited to this layer; no per-node memory or cross-project sharing is introduced.
- `work/` holds temporary research output, outside permanent memory.

User-controlled permanent memory changes require approval of exact previews, including links and map edits. `update-memory` handles information and requested existing-memory changes; `create-conclusion` captures the user's thought and approved connections. `sync-agent-memory` maintains the separate agent layer under `rules.md`. `recall-memory` retrieves relevant saved information and user conclusions without changing them; it distinguishes the user's important saved understanding from factual certainty. These are agent instructions, not filesystem locks or a background service.

## Create and Open

From the Project Factory root:

```bash
python3 scripts/init.py \
  --type collaborative-research \
  --name "Urban Trees" \
  --topic "How urban trees affect summer temperatures" \
  --destination "../Urban Trees"
```

Open the generated folder in Codex and as a vault in Obsidian. No community plugins or ongoing connection to Project Factory are required. New projects contain no example notes or conclusions.

## Graph

Blue information nodes, orange conclusions, and gray details are defined in `template/.obsidian/graph.json`. The default filter shows only information and conclusions. To include details, use:

```text
path:/^(nodes|conclusions|details)\//
```

Colors do not create fixed spatial regions, and standard graph edges do not show relationship labels written in notes. See [Graph view](https://obsidian.md/help/plugins/graph) and [Search](https://obsidian.md/help/plugins/search).


## Everyday Research

Start with a question, hypothesis, or uncertainty. For example: "Investigate whether tokenized Tesla shares track the ordinary share price, including exceptions and limitations." The assistant should examine evidence deeply, challenge assumptions constructively, distinguish evidence from inference, and refine the question with you. It need not solve a broad research problem in one reply.

Most discussion stays in chat. Large raw research outputs belong in `work/`, not the curated graph. For a reusable result, say "Save this information as a node" or "Save the supporting evidence in details." `update-memory` first presents concrete content and links; approval writes that preview. Declining it leaves curated memory unchanged. The assistant may occasionally suggest information/details worth keeping.

For your own thought, say "Create a conclusion from this: …". `create-conclusion` previews a short formulation, ownership, and links. Your approval saves it under `conclusions/`; the assistant does not initiate its own conclusions. These thoughts have high importance for understanding your view, but may be tentative, overbroad, or wrong. New evidence can be discussed critically. Ask to revise an existing conclusion when your view changes; changes still need an approved preview.

## Recall and Agent Memory

Ask "What did I think about this?" or "Recall our research on this topic." `recall-memory` searches relevant short notes and conclusions, including unlinked conclusions, then follows useful links or opens detailed evidence as needed. It reports saved thoughts faithfully, separates them from factual assessment, and acknowledges when no matching saved record was found.

The assistant may maintain only `agent-memory/` automatically at meaningful milestones. `state.md` contains the current focus, progress, open questions, next step, relevant links, and a short chronological research trail. `insights.md` holds selective agent findings/hypotheses with their basis. `user.md` holds scoped working preferences, distinguishing explicit instructions from inference. These are not your conclusions, and remain local to this project.

Say "Sync agent memory" to refresh this working layer. State stays concise; older repetitive completed trail entries can be combined without merging your conclusions. A fresh chat or compaction should prompt relevant file recall. These workflows are agent instructions, not guaranteed background jobs or access-control locks. Git stores files, not the full chat history.

## Graph and Reading Depth

Notes are flat rather than nested under one concept: a company can link to both Transfer Agent and Service Provider concepts. Relationships are described beside links. Many notes may support one conclusion, and one note may connect to several conclusions. Short nodes link to deeper `details/` notes so the assistant can start with the overview and deepen only when needed.

The graph defaults to blue nodes and orange conclusions. Gray details are hidden until you include them with the filter shown above. Folders supply grouping/color rules, not fixed visual regions. Agent memory and temporary work are outside this main graph.

## GitHub Backup

From Factory, request GitHub setup using your personal configured owner. From the independent project, provide an explicit destination: "Connect this project to a private GitHub repository at OWNER/REPOSITORY." No personal owner is embedded in the blueprint.

After the first setup/backup, say "Save this project to GitHub" to commit and push existing files. The local skills are `setup-git` and `save-project`. Track approved research memory, agent memory, instructions, skills, and graph configuration. Exclude temporary work, credentials, and Obsidian workspace state. Empty `.gitkeep` markers preserve initial folders and are not notes. Saving does not authorize additional memory edits.

Restore by cloning the repository and reopening the folder in Codex and Obsidian. Keep future template upgrades separate from saved research; Factory does not migrate this project automatically.
