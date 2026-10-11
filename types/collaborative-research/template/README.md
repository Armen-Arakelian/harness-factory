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
- `conclusions/`: short thoughts and conclusions initiated by the user.
- `details/`: curated deeper explanations and supporting evidence.
- `agent-memory/`: project-local agent state, findings, and working preferences, excluded from the main graph. The agent updates this separate layer at meaningful milestones.
- `work/`: temporary research files, excluded from the main graph.

Changes to user-controlled memory require a concrete preview and approval, including changes to this map. Ask to "save this information" or "create a conclusion from this thought" to start the appropriate local skill.

Ask "what did I think about this?" or "recall our research on this topic" to use `recall-memory`. It searches short notes and relevant conclusions, follows useful links, and opens deeper evidence when needed. Your conclusions are priority context for your evolving understanding; the agent may critically discuss their scope and correctness, while changes still require your request and approval.

Ask to "sync agent memory" to refresh the agent's working notes. These notes do not become your conclusions or curated information without the normal approval workflow. Automatic updates follow `rules.md`; they are instructions for the agent, not a background service or filesystem lock.

The default graph shows information notes in blue and conclusions in orange. Details are assigned gray but hidden by default. To include them, change the graph's search filter to:

```text
path:/^(nodes|conclusions|details)\//
```

Colors distinguish folders; they do not create separate spatial regions. Relationship labels are written in notes, not displayed as edge labels in the standard graph.

## GitHub Backup

GitHub is optional. Ask "Connect this project to a private GitHub repository at OWNER/REPOSITORY" for first-time setup. Git, GitHub CLI authentication, and working SSH access must be configured on this computer. The local skills guide setup and the first commit/push; no Factory installation is needed.

After setup, ask "Save this project to GitHub" to commit and push existing files to its origin. Only a successful push is a remote backup. There is no automatic upload. Rules, skills, graph settings, and both memory layers are tracked; `work/` output, personal workspace state, and credentials are excluded. Empty `.gitkeep` files preserve the initial folders and are not memory entries.

Restore with `git clone git@github.com:OWNER/REPOSITORY.git`, then open the cloned folder in Codex and Obsidian. Create `work/` if missing; its contents are not restored from Git. GitHub stores project files and commit history, not Codex chat history, credentials, or native machine memory.
