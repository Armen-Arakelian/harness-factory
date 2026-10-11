---
name: setup-git
description: Connect this independent research project to a private GitHub repository when the user requests GitHub setup or its first backup.
---

# Set Up GitHub Backup

Resolve this project's root three directories above this skill folder. Use the user's explicit `OWNER/REPOSITORY`, or ask for the GitHub owner when missing. This project has no dependency on Factory or its personal configuration. Existing origin identifies its ongoing backup destination.

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
