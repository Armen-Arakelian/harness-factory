# Project Factory

Create independent projects from self-contained project types. Each type owns its purpose, parameters, template, rules, skills, and settings.

For setup and everyday use, read [the user guide](docs/USER_GUIDE.md). This README also explains the factory architecture and extending it.

## Structure

```text
Project Factory/
    AGENTS.md
    README.md
    .agents/skills/create-project/SKILL.md
    .agents/skills/setup-git/SKILL.md
    .agents/skills/save-project/SKILL.md
    .gitignore
    .factory.example.json
    docs/USER_GUIDE.md
    scripts/init.py
    types/
        collaborative-research/
            README.md
            project.json
            template/
                AGENTS.md
                README.md
                rules.md
                .agents/skills/
                    update-memory/SKILL.md
                    create-conclusion/SKILL.md
                    sync-agent-memory/SKILL.md
                    recall-memory/SKILL.md
                    setup-git/SKILL.md
                    save-project/SKILL.md
                .gitignore
                .obsidian/graph.json
                nodes/
                conclusions/
                details/
                agent-memory/
                    state.md
                    insights.md
                    user.md
                work/
```

The factory skill selects a type and gathers its inputs. The common Python generator reads the type's descriptor, renders its Markdown, and copies its complete template. It contains no research-specific generation logic.

## Available Types

**Collaborative Research** (`collaborative-research`): deep, critical investigation with an AI partner, linked information, personal conclusions, a curated graph controlled by the user, and separate agent working memory. See [the type description](types/collaborative-research/README.md).

## Create a Project

Open this folder in Codex and ask:

> Create a Collaborative Research project named "Urban Trees" about "How urban trees affect summer temperatures" at "../Urban Trees".

Or run from the factory folder:

```bash
python3 scripts/init.py --list-types

python3 scripts/init.py \
  --type collaborative-research \
  --name "Urban Trees" \
  --topic "How urban trees affect summer temperatures" \
  --destination "../Urban Trees"
```

`--name` and `--destination` are common inputs. `--topic` belongs to Collaborative Research. Use `--type collaborative-research --help` to see its inputs.

The destination is the new project folder itself, not its parent, and must be outside Project Factory. Relative paths resolve from the shell's working directory. Existing destinations are refused, including empty folders. Open the generated project according to the selected type's instructions.

## Add a Type

Create `types/<lowercase-hyphenated-id>/` with:

1. `README.md` explaining the purpose, generated contents, and how to use them.
2. `project.json` with `display_name`, `description`, and `parameters` (an empty object if no extra inputs are needed).
3. `template/` containing the complete blank project.

Each parameter declares `help` and an uppercase `token`; all declared parameters are required. For example, `topic` maps to the CLI argument `--topic` and the Markdown placeholder `{{RESEARCH_TOPIC}}`. The common `--name` input maps to `{{PROJECT_NAME}}`. Parameter names and tokens must be unique and must not conflict with common arguments.

The generator discovers type descriptors automatically. Adding a type does not require editing the common generator. Keep rules and local skills inside that type's template; do not add speculative types or a separate shared research policy.

## Generation Guarantees

Python 3's standard library is sufficient. The generator preserves empty directories and copies UTF-8 text files recursively, including hidden skills and configuration. It renders declared placeholders only in Markdown; configuration files are copied unchanged. Binary assets and template symlinks are unsupported. OS `.DS_Store` files are ignored.

Identical inputs and blueprints produce identical contents. Generated projects contain local copies and no dependency on this factory. Blueprint changes affect future projects only; there is no automatic migration of existing projects.

If writing fails after destination creation, partial output may remain. Inspect it before choosing another destination or removing it yourself.

## User Setup and GitHub

Start with [the user guide](docs/USER_GUIDE.md) for a quick overview followed by full setup and usage instructions. [Collaborative Research](types/collaborative-research/README.md) describes the current template and its user workflows.

GitHub backup is optional and separate from generation. Personal owner preferences belong only in ignored `.factory.local.json`; copy `.factory.example.json` and fill in your own account or organization. The example contains no credentials or personal destinations. Ask to connect a project to GitHub, then use `save-project` for requested backups. Generated projects use their own origin and remain independent.

When distributing by Git, personal configuration is excluded by `.gitignore`. When sharing a folder/ZIP manually, exclude `.factory.local.json`, `.git/`, root `.obsidian/`, and temporary `work/` yourself. Include hidden template skills, `.gitignore`, and template graph settings. Empty `.gitkeep` files preserve template folders across Git clones.
