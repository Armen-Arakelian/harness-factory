# Project Factory User Guide

## Short Version

Project Factory creates independent projects from reusable templates. Open the Factory in Codex, choose a template, and give it a project name, topic, and destination. The generated folder contains its own instructions and skills; it can be moved or used without the Factory.

The current template is **Collaborative Research**: deep research with an AI partner, short linked notes in Obsidian, user-owned conclusions, and separate agent working memory. [Read its user guide](../types/collaborative-research/README.md).

GitHub backup is optional. Set your personal GitHub owner in an ignored local configuration file, ask to connect a project, and later say "Save this project to GitHub." Each project has its own private repository. Credentials remain on your computer.

## Full Setup

### 1. Get the Factory and Tools

Clone or copy the complete Factory folder, including hidden `.agents/` and template `.obsidian/` folders. Place it separately from generated projects, for example alongside a `Researches/` folder. Open the Factory as a project in Codex. Do not conduct research inside the blank `template/` folder.

- Python 3 is needed for generation; no Python packages are required.
- Codex runs the local instructions and skills.
- Obsidian is optional for viewing the research graph; no community plugins are required.
- Git and GitHub CLI (`gh`) are needed only for GitHub backup. Install them from their official distributions or your normal package manager.

From the Factory folder, verify:

```bash
python3 --version
python3 scripts/init.py --list-types
```

### 2. Configure Git and GitHub (Optional)

Set your commit identity if it is not already configured. Replace these placeholders with your own values; you may use your GitHub-provided noreply email. Global settings apply to all repositories on this computer; use repository-local settings instead if that is what you want.

```bash
git config --global user.name "Your Name"
git config --global user.email "YOUR-COMMIT-EMAIL"
```

For grouping research repositories under a separate GitHub namespace, create an organization in the GitHub website and select the Free plan if it meets your needs. A personal account also works. You must have permission to create repositories under the chosen owner. This does not change local folder locations.

On a new Mac without an SSH key:

```bash
ssh-keygen -t ed25519 -C "YOUR-GITHUB-EMAIL"
```

Accept the standard file location and choose a passphrase. If a key already exists, reuse it or choose a different name; do not overwrite it. Add the key to the agent/keychain:

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

Create `~/.ssh/config` if absent, or merge this block into existing configuration without overwriting it:

```sshconfig
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

Use the actual key filename if different. Restrict permissions with `chmod 700 ~/.ssh` and `chmod 600 ~/.ssh/config`. Copy the public key using `pbcopy < ~/.ssh/id_ed25519.pub`, then add it in GitHub Settings → SSH and GPG keys → New SSH key as an authentication key. Never paste the private key into chat or the project.

Check access and sign in to GitHub CLI:

```bash
ssh -T git@github.com
gh auth login --hostname github.com --git-protocol ssh --web
gh auth status
```

On first SSH connection, verify the displayed host fingerprint against GitHub's official fingerprints before accepting it. GitHub's successful SSH test says you are authenticated but shell access is unavailable; its exit code may still be 1. If `gh` offers to upload a key you already added, skip the duplicate upload. SSH authenticates Git pushes; CLI login enables repository creation. Codex uses local tools, rather than a key copied into each project. Agent operations can still need filesystem/network permissions. A sandbox/keychain error alone does not establish a bad login.

Other operating systems should follow [GitHub's platform-specific SSH guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent). See also [SSH fingerprints](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints), [CLI login](https://cli.github.com/manual/gh_auth_login), and [repository creation](https://cli.github.com/manual/gh_repo_create).

### 3. Set Your Personal Destination

From the Factory root:

```bash
cp .factory.example.json .factory.local.json
```

Edit the local copy:

```json
{
  "github_owners": {
    "collaborative-research": "YOUR-GITHUB-OWNER"
  },
  "visibility": "private"
}
```

`github_owners` maps each project type to an organization or account name. Add another entry when another template exists. `visibility` currently supports `private` only. This is an agent-read preference file, not input to the Python generator. Without it, local generation works and GitHub setup asks for the owner. Explicit destinations in your request override defaults.

The local file is excluded from Git. It contains no SSH key, token, or password. Never put credentials in either configuration file. Generated projects do not receive this file or depend on it. Changing it affects future setup requests, not existing project remotes. The Factory's own repository destination is supplied separately; research defaults do not apply to it.

## Create and Use a Project

In Codex, with the Factory open:

> Create a Collaborative Research project named "Urban Trees" about "How urban trees affect summer temperatures" at "../Researches/Urban Trees".

This creates files locally. To include GitHub setup, say:

> Create the project and connect it to a private GitHub repository using my configured owner, with repository name "urban-trees".

For a previously generated project, ask from the Factory:

> Connect the Collaborative Research project at "../Researches/Urban Trees" to GitHub using my configured owner and repository name "urban-trees".

The setup skill creates a separate private repository, links it via SSH, and performs the first commit/push after checking the files. Existing folders/repositories are not overwritten. If setup fails, the local project is retained and the agent reports what remains.

For generation without an agent, run:

```bash
python3 scripts/init.py --type collaborative-research --name "Urban Trees" --topic "How urban trees affect summer temperatures" --destination "../Researches/Urban Trees"
```

The destination must not exist and must be outside the Factory. Relative paths resolve from the current shell directory. The generator performs no Git/network operations and starts no research.

Open the generated folder as a separate Codex project and an Obsidian vault. Follow [the template's own guide](../types/collaborative-research/README.md) for research, memory, and graph workflows.

## Save, Restore, and Share

Inside a connected project, say:

> Save this project to GitHub.

The local `save-project` skill commits relevant existing changes and pushes the current branch to origin. It does not generate memory entries or upload automatically. Rules, local skills, graph settings, and both research memory layers are included. Temporary `work/` output and personal workspace state are excluded. A failed push is reported as a local commit without successful remote backup; it never triggers a force push. Commit history contains earlier saved memory versions, including later-edited or deleted thoughts.

An independent project can connect without Factory: ask "Connect this project to a private GitHub repository at OWNER/REPOSITORY."

To restore:

```bash
git clone git@github.com:OWNER/REPOSITORY.git
```

Open the cloned folder in Codex and Obsidian. Empty `.gitkeep` files preserve blank template directories. GitHub does not restore temporary research output, Codex chats, credentials, or native machine memory.

To back up the Factory itself, provide its separate explicit `OWNER/REPOSITORY`, then use its setup/save skills. To give Factory to another person, share its Git-tracked files or a clean archive. Exclude `.factory.local.json`, `.git/`, the Factory's root `.obsidian/`, and root `work/`. Keep hidden template files and skills. `.gitignore` applies to Git, not arbitrary folder/ZIP copies. The recipient creates their own local configuration and authenticates their own computer.

## Available Templates and Updates

- [Collaborative Research](../types/collaborative-research/README.md): research partnership, controlled long-term memory, and an Obsidian graph.

Each type has its own guide and complete blueprint under `types/<type-id>/`. Template changes affect future projects only. Existing projects are updated only by an explicit request; their saved research is not overwritten by the Factory.
