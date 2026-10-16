# Harness Factory User Guide

Open Factory in Codex, choose a template, and provide a name, topic and destination. Open the generated project separately and work there. GitHub backup is optional.

The available template is [Collaborative Research](../types/collaborative-research/README.md), with its own guide to research, memory and Obsidian.

## Setup

Clone or download the complete Factory, including hidden files. You need **Codex** and **Python 3**. **Obsidian** is optional for the graph; no community plugins are required. Do not use `template/` as your research project.

From the Factory folder, check:

```bash
python3 --version
python3 scripts/init.py --list-types
```

## Create a Project

Ask Codex:

> Create a Collaborative Research project named "Urban Trees" about "How urban trees affect summer temperatures" at "../Researches/Urban Trees".

Or run from the Factory folder:

```bash
python3 scripts/init.py \
  --type collaborative-research \
  --name "Urban Trees" \
  --topic "How urban trees affect summer temperatures" \
  --destination "../Researches/Urban Trees"
```

The destination is the new folder itself, must not exist, and must be outside Factory. Relative paths start at your shell's working directory. Creation is local and offline; it does not start research or upload anything. If generation fails, inspect any partial folder before retrying.

Open the result in Codex and as an Obsidian vault. Each project is independent; Factory updates apply to future projects only. For managing open research questions, see [Future Research Topics](../types/collaborative-research/README.md#future-research-topics).

## Optional GitHub Setup

Install **Git** and **GitHub CLI (`gh`)**. Configure your commit identity if needed:

```bash
git config --global user.name "Your Name"
git config --global user.email "YOUR-COMMIT-EMAIL"
```

These settings affect all repositories; use local settings if you prefer. Configure SSH using [GitHub's platform-specific guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), and add your **public** key to GitHub. Reuse an existing key rather than overwriting it. Codex uses your computer's Git/SSH access; do not copy private keys or tokens into projects or chat.

Then check SSH and authenticate the CLI:

```bash
ssh -T git@github.com
gh auth login --hostname github.com --git-protocol ssh --web
gh auth status
```

Verify an unfamiliar SSH fingerprint against [GitHub's published fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints). A successful SSH test can return exit code 1 because GitHub provides no shell access. SSH enables pushes; CLI authentication enables repository creation.

### Choose a Default Owner

Use your account or an organization where you can create repositories. From the Factory root:

```bash
cp .factory.example.json .factory.local.json
```

Edit the local copy:

```json
{
  "github_owners": {"collaborative-research": "YOUR-GITHUB-OWNER"},
  "visibility": "private"
}
```

This optional file is ignored by Git and never copied into generated projects. It contains preferences, not credentials; currently only `private` visibility is supported. Without it, specify the owner in your request. Explicit destinations override defaults; existing remotes stay unchanged.

## Connect, Save and Restore

From Factory, ask:

> Connect the Collaborative Research project at "../Researches/Urban Trees" to a private GitHub repository using my configured owner and repository name "urban-trees".

From an independent project, give the destination explicitly:

> Connect this project to a private GitHub repository at OWNER/REPOSITORY.

Setup creates the repository, connects it and performs the first commit/push. Later, say **"Save this project to GitHub."** Backups happen only when requested. A failed push leaves a local commit, not a successful remote backup.

To restore, clone the repository and reopen its folder:

```bash
git clone git@github.com:OWNER/REPOSITORY.git
```

Backups include project instructions, graph settings and saved memory. They exclude temporary `work/` files, credentials and personal Obsidian workspace state; chat history is not backed up. Pending approvals require a fresh preview after restoration. To back up Factory itself, provide its own repository destination separately.

## Update the Factory

Open Factory in Codex and describe the change you want. `update-factory` implements it, checks affected behavior and updates the relevant user documentation. Existing research projects change only when you request a migration. Say **"Save Factory to GitHub"** to upload a task branch and open or update a pull request after readiness checks. Review the PR and ask to merge when ready; saving alone never merges it. The default branch uses PR-only changes, with a generator CI check before merging. For simultaneous tasks, use separate worktrees; separate chats sharing one folder also share its files and checked-out branch. This contribution workflow applies to Factory, not generated projects' backup workflows.

## Share the Factory

Share its Git repository or a clean archive. For archives, exclude `.factory.local.json`, `.git/`, root `.obsidian/` and root `work/`. Keep hidden template files and skills. Recipients configure their own GitHub access and owner preferences.
