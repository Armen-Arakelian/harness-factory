# Project Factory

Create independent Codex projects from reusable templates. Each project contains its own instructions, skills and settings; it can be moved or shared without the Factory.

The current template is [Collaborative Research](types/collaborative-research/README.md): deep research with an AI partner, user-approved memory and an Obsidian graph.

## Start

Open the Factory folder in Codex and ask:

> Create a Collaborative Research project named "Urban Trees" about "How urban trees affect summer temperatures" at "../Researches/Urban Trees".

Open the generated folder as a separate Codex project and, optionally, an Obsidian vault. The destination must be new and outside the Factory. Python 3 is required; no additional Python packages are needed.

For setup, terminal commands and optional GitHub backup, read the [user guide](docs/USER_GUIDE.md).

## Structure

```text
AGENTS.md          Factory instructions for Codex
.agents/skills/    Project creation and GitHub workflows
scripts/init.py    Offline project generator
types/             Self-contained project blueprints
docs/USER_GUIDE.md  Setup and usage
```

## Add a Template

Create `types/<lowercase-hyphenated-id>/` with:

- `README.md`: purpose and usage.
- `project.json`: `display_name`, `description` and `parameters`.
- `template/`: the complete blank project, including its rules and skills.

Use [the current descriptor](types/collaborative-research/project.json) as an example. Each extra parameter declares `help` and an uppercase `token`; all are required. For example, `topic` becomes `--topic` and replaces `{{RESEARCH_TOPIC}}` in Markdown. `--name` replaces `{{PROJECT_NAME}}`.

The generator discovers types automatically and copies hidden files and empty directories. Templates use UTF-8 text; binary files and symlinks are unsupported. Identical inputs and templates produce identical content.

Template updates affect new projects only. Existing projects need an explicit update; their saved research is not replaced automatically.
