---
name: setup-git
description: Connect the factory or a generated project to a private GitHub repository when requested, using local owner preferences for supported project types.
---

# Set Up GitHub Backup

Resolve the factory root three directories above this skill folder. Identify the target folder and, for generated projects, its supported type. Creation and GitHub setup are separate operations; do not upload a project merely because the user requested local generation.

For generated projects, read `.factory.local.json` from the factory root only when GitHub setup needs defaults. Its schema is documented in `docs/USER_GUIDE.md`. Resolve the owner from `github_owners[<type-id>]`; `visibility` must be `private`. Missing config/owner means ask for the destination; never use the example's placeholder or assume the authenticated account. Invalid JSON or unsupported visibility means report the configuration error. Keep this personal config in the factory, excluded from Git; never copy it into templates or projects. Never store credentials here.

For the factory itself, ask for or use an explicitly supplied destination. Research owner preferences do not apply to the factory. Once a project has origin, that remote is the ongoing destination; changing factory defaults does not migrate it.

Read the generated project's own `setup-git` and `save-project` skills when present. Pass the resolved target explicitly; generated projects do not read factory configuration. For the factory, use the local `save-project` skill.

## Connect the Project

- Run commands from the target project root. Check whether Git already exists: `git rev-parse --show-toplevel`. An ancestor checkout is not this project's repository; stop and explain rather than modifying it. If the root already matches, inspect existing remotes and staged state. Never overwrite a remote, reuse a conflicting GitHub repository, or change visibility silently. For a new local repository, use `git init -b main` after checking `.gitignore` exists and excludes machine-specific files and temporary output.
- Check `gh auth status` and Git identity (`git var GIT_AUTHOR_IDENT`). The user completes login/key setup and supplies missing identity; never read or copy private keys/tokens into project files. Sandbox/keychain/network failures may need permitted execution outside the sandbox before diagnosing invalid credentials.
- Resolve the exact `OWNER/REPOSITORY` destination from the request/configuration. Use a lowercase hyphenated repository slug based on the project name, explaining the resulting destination briefly. Clarify only missing or conflicting values. Explicit user destinations take precedence. This workflow creates private repositories; public publishing requires a separate explicit request and workflow.
- Check repository existence with `gh repo view OWNER/REPOSITORY --json nameWithOwner,isPrivate,sshUrl`. Only a clear not-found response permits creation; authentication, permission, and network failures are not evidence of availability. If the repository exists and is not already the verified origin, clarify instead of attaching or overwriting it.
- Create the empty remote and link it, without uploading files yet:

  ```bash
  gh repo create OWNER/REPOSITORY --private --source . --remote origin
  ```

  Ensure origin uses `git@github.com:OWNER/REPOSITORY.git` (set it to this URL only for the origin just created), and verify remote ownership/privacy via `gh repo view`. Report partial success if remote creation succeeded but linking failed; do not delete/recreate or blindly retry.
- Finish the first commit and push using the target's `save-project` skill. A request to connect a project to GitHub includes its initial backup; do not ask again for the same already-authorized destination. Inspect files before upload under that skill. Report the repository URL and actual push status.

No auto-push, force push, repository deletion, or organization creation. Do not edit research memory during setup. Local generation remains usable if GitHub setup is unavailable; report the local project separately from remote backup.
