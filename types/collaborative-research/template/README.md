# {{PROJECT_NAME}}

## Topic

{{RESEARCH_TOPIC}}

## Research Question

To be defined with the user.

## Memory Map

No entries saved yet. Add only approved entry points into the research, not a catalogue of every file.

## Saved Conclusions

No conclusions saved yet. Add a short link here when the user approves a new conclusion.

## Working with This Project

Open this folder in Codex and as a vault in Obsidian. No community plugins or connection to the Project Factory are required.

- `nodes/`: short information notes, without mandatory entity types.
- `people/`: short profiles, light green for a known personal contact route and darker green otherwise.
- `conclusions/`: short thoughts and conclusions initiated by the user.
- `details/`: curated deeper explanations and supporting evidence.
- `agent-memory/`: project-local agent state, findings, and working preferences, excluded from the main graph. The agent updates this separate layer at meaningful milestones.
- `research-topics.md`: your future questions, coverage statuses and links to existing research; changes require your request and approval.
- `work/`: temporary research files, excluded from the main graph.

Saving or changing substantive memory requires approval of a compact preview showing the text and destination. After approval, the assistant chooses useful connections and maintains related reverse links and map entries automatically; ask to see the links if you want to review them. Unrelated content changes and graph cleanup still require a separate request and approval. Ask to "save this information" or "create a conclusion from this thought" to start the appropriate local skill.

When supported, a compact blue information card or orange conclusion card offers **Approve** and **Cancel**. A click sends only a short choice, title and ID. Buttons disappear after use; **Approval sent** is a request, and the assistant confirms **Saved** only after the write succeeds. If you send another ordinary message first, the agent expires the old proposal in a local registry; clicking it later cannot pass that registry check. Ask for a new preview to return to it. Old buttons can remain visually active because there is no automatic new-message hook. New chats and compaction also require a fresh preview. In clients without buttons, approve the text preview with its ID instead. No additional dependency or Git setup is needed.

Ask "Add these topics to our research list" or "Review the research topics list" to use `manage-research-topics`. Open questions are **Not explored** or **Needs depth**, with useful links and remaining gaps. A requested review can propose removing answered questions; results stay in the research notes. Every list change requires approval, with no automatic reviews.

Ask **"Save this person: …"** to preview a short profile and its contact status. A known personal route is **Contact** (light green); otherwise **Public figure** (darker green). The assistant selects a few useful research anchors by relevance, not every topic associated with the person. Profile and status changes require approval. These colors are intended for a dark graph.

Ask **"Create a glossary"** and choose term languages and an explanation language. It starts empty, then updates automatically from each successfully saved information note and its saved details, without entry approvals. Say **"Review the glossary across the project"** to include earlier research or reconcile terms; full reviews are never automatic. Ask to disable it to pause maintenance.

Ask "what did I think about this?" or "recall our research on this topic" to use `recall-memory`. It finds candidate short notes and conclusions first. Recalling your saved view may need no details; checking factual support opens relevant evidence sections and expands when gaps or conflicts require it. Your conclusions are priority context for your evolving understanding; the agent may critically discuss their scope and correctness, while changes still require your request and approval.

Ask to "sync agent memory" to refresh the agent's working notes. These notes do not become your conclusions or curated information without the normal approval workflow. Checkpoints record the update date and significant results, changes of direction, reviews, pending questions and the next step. On resumption, the agent checks that the recorded next step still fits your request. Automatic updates follow `rules.md`; they are instructions for the agent, not a background service or filesystem lock.

The default graph shows information notes in blue and conclusions in orange. An enabled glossary appears as a purple helper node without research-note connections. Details are assigned gray but hidden by default. To include them, change the graph's search filter to:

```text
path:/^(nodes|people|conclusions|details)\// OR path:"glossary.md"
```

Colors distinguish folders; they do not create separate spatial regions. Relationship labels are written in notes, not displayed as edge labels in the standard graph.

For a focused view, open a note such as an entry point from the Memory Map, run **Open local graph**, and start with depth **1** in the local graph filter settings. Increase depth to explore farther. The global graph remains available; this display choice does not limit the assistant's memory search.

## Project-Specific Modules

Describe a new capability or external connection you want in this project; the assistant can suggest a module without that keyword. You can also say **"Add a module for …"**. Existing workflows and one-off tasks need no new module. The assistant reviews when it loads instructions, what it reads and stores, and how often it updates data. If the design may inflate context, it explains why and suggests a smaller alternative. You agree on a short plan before the module is added to this project. The review does not run the module, perform tests or certify that it works. Existing memory approval rules remain in force.

## GitHub Backup

GitHub is optional. Ask "Connect this project to a private GitHub repository at OWNER/REPOSITORY" for first-time setup. Git, GitHub CLI authentication, and working SSH access must be configured on this computer. The local skills guide setup and the first commit/push; no Factory installation is needed.

After setup, ask "Save this project to GitHub" to commit and push existing files to its origin. Only a successful push is a remote backup. There is no automatic upload. Rules, skills, graph settings, and both memory layers are tracked; `work/` output, personal workspace state, and credentials are excluded. Empty `.gitkeep` files preserve the initial folders and are not memory entries.

Restore with `git clone git@github.com:OWNER/REPOSITORY.git`, then open the cloned folder in Codex and Obsidian. Create `work/` if missing; its contents are not restored from Git. GitHub stores project files and commit history, not Codex chat history, credentials, or native machine memory.
