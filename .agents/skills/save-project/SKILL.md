---
name: save-project
description: Commit and push the current project's saved files when the user asks to save or back up the project to Git. Does not create or rewrite research memory.
---

# Save the Project

Resolve this project's root three directories above this skill folder. Run Git from that root, never from another checkout.

For this Factory checkout, before staging or publishing updates, read `../update-factory/SKILL.md` and complete its Publication Check for intended changes and outgoing commits. Verify affected behavior and current user documentation; repair directly related gaps within the authorized scope before continuing. Reuse valid current evidence instead of repeating successful tests. A failed or unavailable material check must be reported rather than presented as passed. This Factory-specific check is not copied into the save-project skills of generated research projects.


1. A user request to save or back up the project to Git authorizes a normal commit and push to its configured remote. Do not run automatically after research or memory writes. Honor narrower requests such as commit-only or selected files.
2. Verify `git rev-parse --show-toplevel` resolves exactly to this project root (a worktree is allowed). If missing, use the local `setup-git` skill; if the root is an ancestor, stop rather than committing another project. Check status, current branch, and `origin` fetch/push URLs. If origin or an upstream targets an unexpected destination, clarify before upload; never replace it silently. Do not expose credentials embedded in URLs.
3. Inspect changed and untracked file names and relevant diffs, including previously staged changes. Honor `.gitignore`; exclude local configuration, credentials, temporary output, and personal Obsidian workspace state. If such a file is already tracked or staged, stop and report it; `.gitignore` does not untrack it. Avoid printing secret contents. Do not force-add ignored files or edit saved memory to make a commit succeed.
4. Stage intended project changes, including authorized deletions. For a whole-project backup, `git add -A -- .` is appropriate only after that inspection. Review staged diff/stat and `git diff --cached --check`. If there are no changes, skip the commit but still check whether existing commits need pushing. Otherwise create a concise English commit message describing the actual change. Missing Git identity must be supplied by the user, not invented.
5. Push the current branch explicitly to origin: `git push -u origin <branch>` (or `git push origin <branch>` with an already verified upstream). Detached HEAD, unresolved conflicts, authentication failures, or a rejected/non-fast-forward push require resolution; do not force push, reset, auto-stash, merge, or rebase as a backup shortcut. A failed push leaves the local commit intact. Permission-limited authentication checks may require execution outside the sandbox; they do not prove credentials are missing.
6. Verify the remote branch hash matches local HEAD (for example `git ls-remote origin refs/heads/<branch>`). Report the commit, branch, destination, and whether remote backup succeeded. A local commit alone is not a GitHub backup. Uncommitted edits appearing during the save remain unsaved; report them.

This workflow saves existing files. It does not authorize new conclusions, memory edits, settings changes, repository visibility changes, or deletion of temporary files. Empty `.gitkeep` files preserve otherwise empty directories in Git.
