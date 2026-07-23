# Shell Completion

The Agentic Workspace CLI supports tab completion for bash and zsh. Completion covers all commands, subcommands, flags, and flag values (e.g. `--ide vscode|cursor`).

## Setup

### Bash

**Option 1: Auto-updating (recommended)** — always in sync after `pipx upgrade`, no manual steps needed.

```bash
echo 'eval "$(workspace completion bash)"' >> ~/.bashrc
source ~/.bashrc
```

**Option 2: Static file** — faster shell startup, but must be regenerated after each CLI upgrade.

> Requires the `bash-completion` package — see [Bash Prerequisites](#bash-prerequisites) below.

```bash
mkdir -p ~/.local/share/bash-completion/completions
workspace completion bash > ~/.local/share/bash-completion/completions/workspace
```

### Zsh

**Option 1: Auto-updating (recommended)** — always in sync after `pipx upgrade`, no manual steps needed.

```bash
echo 'eval "$(workspace completion zsh)"' >> ~/.zshrc
source ~/.zshrc
```

**Option 2: Static file** — faster shell startup, but must be regenerated after each CLI upgrade.

```bash
mkdir -p ~/.zfunc
workspace completion zsh > ~/.zfunc/_workspace
```

Add to `~/.zshrc` (before `compinit`):

```bash
fpath=(~/.zfunc $fpath)
autoload -Uz compinit && compinit
```

Then reload: `source ~/.zshrc`

### Bash Prerequisites

Option 2 (static file) for Bash requires the `bash-completion` package:

```bash
# macOS (Homebrew)
brew install bash-completion@2

# Ubuntu/Debian
sudo apt install bash-completion
```

Ensure it is sourced in your `~/.bashrc`:

```bash
# macOS (Homebrew)
[[ -r "/opt/homebrew/etc/profile.d/bash_completion.sh" ]] && source "/opt/homebrew/etc/profile.d/bash_completion.sh"

# Linux (usually sourced automatically; if not, add to ~/.bashrc)
[[ -r "/usr/share/bash-completion/bash_completion" ]] && source "/usr/share/bash-completion/bash_completion"
```

Option 1 (auto-updating) does not require `bash-completion`. Zsh has built-in completion support and requires no additional packages for either option.

## Dynamic Template Name Completion

Commands that accept an existing template name (`view`, `edit`, `load`, `delete`, `upgrade`) support dynamic tab completion of template names. The completion script reads template JSON files from `~/.workspace-templates/` at tab-press time, so newly created templates are available immediately.

Commands that accept a *new* name (`save`, `create`) do not offer template name suggestions.

## Verifying

After setup, open a new terminal and test:

```bash
# Complete commands
workspace <TAB>
# Shows: catalog  code  completion  setup-devcontainer  template

# Complete template subcommands
workspace template <TAB>
# Shows: create  delete  edit  list  load  save  upgrade  view

# Complete flags
workspace code --<TAB>
# Shows: --help  --ide  --regenerate-shell-env

# Complete flag values
workspace code --ide <TAB>
# Shows: cursor  vscode

# Complete template names (requires templates in ~/.workspace-templates/)
workspace template view <TAB>
# Shows: my-template  work-profile  ...
```

## Updating After CLI Upgrades

If you used **Option 1 (auto-updating)**, completions stay in sync automatically — no action needed after `pipx upgrade agentic-workspace`.

If you used **Option 2 (static file)**, regenerate the completion script after each CLI upgrade:

```bash
# After: pipx upgrade agentic-workspace

# Bash
workspace completion bash > ~/.local/share/bash-completion/completions/workspace

# Zsh
workspace completion zsh > ~/.zfunc/_workspace
```

## Troubleshooting

### Completions not working after setup

- Open a **new terminal window** — completions are loaded at shell startup.
- For zsh, ensure `compinit` is called **after** setting `fpath`.

### Zsh: `command not found: compdef`

Run `compinit` before the completion script is sourced:

```bash
autoload -Uz compinit && compinit
```

### Bash: completions directory not loaded

Only applies to Option 2 (static file). Ensure `bash-completion` is installed and sourced — see [Bash Prerequisites](#bash-prerequisites).

### Completions are stale after CLI upgrade

Only applies to Option 2 (static file). Regenerate the completion script — see [Updating After CLI Upgrades](#updating-after-cli-upgrades). To avoid this in the future, switch to Option 1 (auto-updating).
