# Collaborative Research

A template for ongoing research with an AI partner and an Obsidian graph. The assistant examines evidence, challenges assumptions and helps build understanding over time. You choose what enters your permanent memory.

## Start

Ask Factory to create a project with a name, topic and destination, then open its folder in Codex and Obsidian. For installation, project creation commands and GitHub setup, see the [Factory user guide](../../docs/USER_GUIDE.md). No community Obsidian plugins are required.

Start with a question, for example:

> Investigate whether tokenized Tesla shares track the ordinary share price, including exceptions and limitations.

Broad questions can develop across several conversations; the assistant should distinguish evidence, interpretation and uncertainty.

## What Gets Saved

| Location | Purpose |
|---|---|
| `nodes/` | Short information notes connected by meaningful links. |
| `people/` | Relevant people, with or without a known personal contact route. |
| `conclusions/` | Your short thoughts and conclusions, initiated by you. |
| `details/` | Deeper explanations, evidence and limitations. |
| `research-topics.md` | Your future questions, coverage statuses and links to existing research. |
| `README.md` | Entry points and links to saved conclusions. |
| `agent-memory/` | The assistant's working context, kept separate from your graph. |
| `work/` | Temporary research output, outside permanent memory. |

Notes stay flat and can have many-to-many connections. The assistant starts with relevant short notes and opens deeper material when needed.

## Save and Approve

Ask **"Save this information as a node"**, **"Save the supporting evidence in details"**, or **"Create a conclusion from this: …"**.

You receive a compact preview with the exact text and destination. Supported clients show a blue information card or orange conclusion card with **Approve** and **Cancel**; other clients use text approval. After approval, the assistant saves the content and chooses related links automatically. Ask to see the links if you want to review them.

Buttons disappear after use. **Approval sent** means the request was sent; the assistant confirms saving separately. Another ordinary message expires the proposal when the agent processes it. Old buttons may remain visible, but expired IDs are rejected. New chats, compaction and restoration require a fresh preview. There is one active proposal per project.

Your conclusions matter as records of your understanding, but may be tentative or wrong. The assistant may challenge them with evidence and must not silently rewrite them. Ask to revise a conclusion when your view changes; revisions need approval too. The assistant may suggest information worth saving, but does not invent conclusions on your behalf.

## Future Research Topics

Say **"Add these topics to our research list"** or **"Review the research topics list."** Open questions are **Not explored** or **Needs depth**, with links and remaining gaps. On a requested review, sufficiently answered questions are proposed for removal; their results stay in the research notes. Every change needs approval. There are no automatic additions, reviews or completed-topic archives.

## People

Ask **"Save this person: …"** to preview who they are, why they matter and their contact status. **Contact** means a known personal route; **Public figure** means none is established, regardless of prominence. Profiles and status changes require approval. The assistant chooses links to specific research contributions or thoughts, not every topic connected to their employer. One flat `people/` folder holds both statuses.

The graph uses muted light green (`#91B89A`) for contacts and darker green (`#5B8A70`) for public figures. These shades suit a dark graph; the light shade has weaker contrast on a white background.

## Optional Glossary

Ask **"Create a glossary"** and choose term languages and an explanation language. It starts empty, then updates automatically from each successfully saved information note and its saved details, without entry approvals. Say **"Review the glossary across the project"** to include earlier research or reconcile terms; full reviews are never automatic. Ask to disable it to pause maintenance.

The glossary is a purple, link-free helper node. It is optional and has no language defaults imposed during project creation.

## Recall and Continue

Ask **"What did I think about this?"** or **"Recall our research on this topic."** The assistant searches relevant notes and conclusions, including unlinked ones, and separates your saved view from its current assessment.

Agent memory has three files: `state.md` for the current question, progress, next step and brief research trail; `insights.md` for agent findings and hypotheses; `user.md` for scoped working preferences. The assistant updates these at meaningful milestones. Say **"Sync agent memory"** to request a checkpoint.

Fresh sessions should recover context from these files. These workflows depend on the agent following instructions; they are not background jobs or filesystem locks. Unsaved chat content is not guaranteed to survive compaction.

## View the Graph

The default graph shows **blue information nodes** and **orange conclusions**. **Gray details** are hidden; to include them, use this graph search filter:

```text
path:/^(nodes|people|conclusions|details)\// OR path:"glossary.md"
```

For a focused view, open a note's local graph at depth 1 and expand as needed. Colors identify folders, not separate spatial regions; relationship descriptions appear in notes rather than on graph edges. Agent memory and temporary output stay outside the main graph.

## Backup and Reference

GitHub is optional. After connecting a repository, say **"Save this project to GitHub."** Restore by cloning and reopening it; temporary files and chat history are not included. See the [backup instructions](../../docs/USER_GUIDE.md#connect-save-and-restore).

The blueprint lives in `template/`. Its [rules](template/rules.md), [agent instructions](template/AGENTS.md) and [local skills](template/.agents/skills/) define the workflow. Edit the blueprint to change future projects; existing research projects require an explicit update.
