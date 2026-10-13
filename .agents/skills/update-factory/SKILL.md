---
name: update-factory
description: Develop Project Factory or a project-type blueprint, verify affected behavior and keep concise user documentation current. Also checks publication readiness before the Factory save-project workflow. Does not migrate existing projects or publish without a user request.
---

# Update Project Factory

Resolve the Factory root three directories above this skill folder. Read its `AGENTS.md`. This workflow lives only in Factory; generated research projects use their own skills.

## Develop

1. Establish the requested behavior and inspect the current files and Git diff, including staged and untracked changes. Preserve unrelated edits. In a fresh chat, recover the task from available files and the user request rather than assuming earlier test results or intentions. Clarify only material ambiguity; routine implementation choices do not need extra approval.
2. Place type-independent creation logic and Factory workflows at the root. Keep a type's parameters, rules, skills, settings and blank files in `types/<id>/`. Read the affected type's README and relevant template instructions. Factory maintenance is not a research-memory operation; do not run a generated project's memory-approval workflow to edit its blueprint.
3. Make the smallest complete change. Keep the generator offline, deterministic and standard-library-only; keep generated projects self-contained. Do not embed personal GitHub owners, credentials, absolute machine paths, runtime approval records or actual research content. Do not migrate live projects unless the user explicitly requests it, and preserve their research and settings during authorized migrations.
4. Verify the affected behavior in a disposable generated project outside Factory. Use `python3 .agents/skills/update-factory/scripts/check_factory.py` for generation changes, or add `--type <id>` for a type-specific change. Exercise the changed workflow where relevant: a generation smoke check does not prove skill behavior, approval logic, UI interaction or research quality. Use narrowly scoped scenarios instead of rerunning every unrelated test. Documentation-only changes need link, example and consistency checks, not a full behavioral suite. Repeat successful tests only for new changes, failures or unresolved concerns. Label simulations and untested limitations honestly.
5. Review documentation as described below. Confirm affected links, examples, commands and generated instructions still agree. Prepare a short summary of what changed, how it was checked and material limitations. Leave unfinished work recognizable in files or a brief ignored `work/` handoff when useful; do not depend on this chat being retained.

## Documentation Review

Update user documentation when behavior, setup, inputs, outputs or a supported workflow changes. Internal refactors and behavior-preserving fixes need no new prose; explain that judgment briefly in the completion summary when relevant.

- Root `README.md`: purpose, quick start and architecture/extension overview.
- `docs/USER_GUIDE.md`: shared setup, creation, backup and sharing steps.
- `types/<id>/README.md`: that template's user-facing behavior and examples.
- `types/<id>/template/README.md`: the generated project's entry points and everyday use; preserve replacement tokens.
- `AGENTS.md`, rules and skills: operational details for the agent, not material to copy into a user guide.

Give each fact one primary home; use links elsewhere. Replace outdated wording rather than append another explanation. Describe what the user does and what happens, with a short example when useful. Keep necessary setup and honest limitations, remove repetitions, and avoid implementation narration or exhaustive file inventories. Do not add a large changelog or blanket word limit. A longer section needs a concrete user need.

## Publication Check

The root `save-project` skill uses this section before committing or pushing Factory changes. Inspect the intended diff and any outgoing commits, not only the working tree. For each affected area, establish that relevant checks passed and user-facing documentation matches the resulting behavior. Existing valid evidence can be reused; when it is absent or stale, perform the appropriate checks. A clean working tree or a "tested" commit message is not evidence by itself.

Fix directly related code or documentation gaps within the authorized update before publication. Do not alter unrelated work, create research memory or expand the feature. If a material check cannot be completed, describe the limitation and do not claim readiness; clarify unresolved scope before uploading. After readiness is established, return to `save-project` for its staging, commit, push and remote verification steps. Publication still requires the user's request; updating Factory alone does not authorize upload.
