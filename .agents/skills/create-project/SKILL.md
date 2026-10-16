---
name: create-project
description: Create an independent project from a supported Harness Factory type when the user asks to initialize a new project, including Collaborative Research projects for Codex and Obsidian.
---

# Create a Project

The factory root is three directories above this skill folder. Resolve factory resources from that root, regardless of the current working directory.

1. List available types with `python3 scripts/init.py --list-types` from the factory root. Match the request to a supported type. Research with an AI partner maps to `collaborative-research`. If the request is ambiguous or unsupported, clarify; do not invent a type or silently choose research for unrelated work.
2. Read `types/<type-id>/README.md`, `project.json`, and the template instructions. Determine the name, destination, and required type parameters from the request. Ask only for missing values. The destination is the new folder itself and must be outside the factory.
3. Run the generic generator with the selected type and safely quoted inputs. For the current research type:

   ```bash
   python3 scripts/init.py --type collaborative-research --name "Example Research" --topic "The subject to investigate" --destination "/absolute/path/to/example-research"
   ```

4. If the destination exists, report the conflict and obtain another destination. Never delete or overwrite it to make initialization succeed.
5. Verify the generated files and folders against the selected blueprint and its README. Check that requested values appear in the project README. For Collaborative Research, verify all declared local skills, `rules.md`, graph settings, blank curated memory folders (apart from `.gitkeep`), starter agent-memory files, and `work/`.
6. If the user also requested GitHub setup, use the factory `setup-git` skill after local generation; it resolves personal defaults separately. Do not pass personal config to the generator or copy it to the project. If setup fails, keep the generated project and report what remains.
7. Report the created location and the selected type's opening instructions. Do not start the project's work unless requested.

The generator is the source of truth for creation. Initialization copies the blank blueprint and creates no research memories; no per-note approval is needed for requested initialization. Do not add example memories. Generated projects need no factory installation or ongoing connection.
