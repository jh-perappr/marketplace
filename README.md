# marketplace

A custom [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli) plugin marketplace for the `harness` project. It bundles reusable agents, skills, hooks, and MCP/LSP wiring for Copilot CLI as installable plugins, so teams can share consistent customizations instead of hand-rolling them per machine.

Plugins currently published here:

- **[forge](plugins/forge)** — the plugin for maintaining and extending this very marketplace. **Recommended starting point.** It ships the **`forger`** agent, an expert in scaffolding, validating, and registering Copilot CLI plugins, and the `plugin-creator` skill with full reference docs and templates.
- **[engineering](plugins/engineering)** — an end-to-end engineering delivery team (program manager, solution architect, GRC, backend/frontend/platform engineers, CRM, and documentation skills).

## Installation

Install a plugin directly from this repo path or add the whole marketplace so all plugins stay discoverable and updatable:

```shell
# Install a single plugin
copilot plugin install ./plugins/forge

# Or register this repo as a marketplace to install/update any plugin from it
copilot plugin marketplace add jh-perappr/marketplace
copilot plugin install forge
```

Verify installation:

```shell
copilot plugin list
```

Then in an interactive session, confirm components loaded with `/agent`, `/skills list`, or `/mcp`.

## Updating

Plugin versions are auto-bumped and published on merge to `main` (see `.github/workflows/plugin-release.yml`). To pick up the latest release:

```shell
copilot plugin marketplace update
copilot plugin install forge   # reinstall to refresh the cached copy
```

## Authoring a new plugin

Use the **forge** plugin's **forger** agent — it knows this repo's conventions end to end and will scaffold, validate, and register plugins for you:

```shell
copilot --agent forge:forger
```

Ask it to create a new plugin, add an agent/skill/hook/MCP server to an existing one, or explain `plugin.json` fields. For the manual workflow, see `plugins/forge/skills/plugin-creator/SKILL.md`.

## Agent-specific aliases (persisting across terminal restarts)

To jump straight into a given agent without typing the full command each time, add a shell alias to your shell's persistent startup file.

**Linux / macOS (bash):**

```shell
echo 'alias forger="copilot --agent forge:forger"' >> ~/.bashrc
source ~/.bashrc
```

**macOS (zsh, the default shell on modern macOS):**

```shell
echo 'alias forger="copilot --agent forge:forger"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell):**

```powershell
# Create a profile file if you don't already have one
if (!(Test-Path -Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }

Add-Content -Path $PROFILE -Value 'function forger { copilot --agent forge:forger @args }'
. $PROFILE
```

Because these are written to your shell's own startup file (`~/.bashrc`, `~/.zshrc`, or your PowerShell `$PROFILE`), they're loaded automatically every time you open a new terminal — no need to redefine them per session.
