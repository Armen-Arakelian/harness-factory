# Harness Factory

This project creates independent projects from self-contained type blueprints.

- Use `.agents/skills/create-project/SKILL.md` when asked to create a project. Run `scripts/init.py` rather than constructing generated projects manually.
- Keep each type's description, parameters, template, rules, local skills, and settings under `types/<type-id>/`. Keep only type-independent creation logic at the factory root.
- The current type is `collaborative-research` (Collaborative Research): deep, critical research with an AI partner and user-controlled permanent memory.
- Read the selected type's `README.md` before creation. Never silently substitute another type for an unsupported request.
- Keep generated projects independent and outside the factory directory. Copy local resources; do not create links back to the factory.
- Keep saved project content and factory files in English. Extend only for concrete needs; avoid speculative types, plugins, taxonomies, or configuration layers.
- Blueprint changes affect future projects. Update existing projects only when requested.
- Factory development is separate from generated research memory. Memory preview-and-approval rules govern saved research content inside generated projects.

## Developing Factory

- Use `.agents/skills/update-factory/SKILL.md` for changes to Factory or its blueprints, and its publication check before saving Factory updates to GitHub.
- Recover a fresh task from the current request, files and Git diff. Keep changes scoped, preserve unrelated work, and verify affected behavior in disposable generated projects outside Factory.
- When user-facing behavior changes, update its primary description: root README for overview, User Guide for shared setup, type README for template usage, generated README for everyday project use. Keep implementation details in agent instructions; replace outdated text and link rather than repeat.
- Internal changes without behavior changes need no new user prose. Reuse current test evidence or run the missing checks; do not assume validation from an old chat or commit message.
- Do not auto-migrate working projects, add personal configuration to blueprints, or publish without a user request. State material limitations and incomplete checks honestly.

## GitHub Backup

- Use `.agents/skills/setup-git/SKILL.md` when asked to connect the factory or a generated project to GitHub. Use `.agents/skills/save-project/SKILL.md` to save this factory to its configured remote.
- Read `.factory.local.json` only for personal GitHub defaults during setup. It is ignored by Git and must never be copied into generated projects or distribution archives. `.factory.example.json` is the portable schema example, not active configuration.
- GitHub organization/account choices and credentials are deployment preferences, not project-type standards. Keep the generator deterministic and offline. Creating a project locally does not authorize GitHub upload.
- User onboarding is in `docs/USER_GUIDE.md`; each type's README explains its own use. Existing projects retain their own remotes and are not migrated when defaults change.
