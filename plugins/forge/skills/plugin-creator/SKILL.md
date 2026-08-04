---
name: plugin-creator
description: Guide for authoring, scaffolding, validating, and registering GitHub Copilot CLI plugins (plugin.json manifest, custom agents, skills, hooks, MCP servers, LSP servers, and slash commands). Use this whenever someone wants to create a new Copilot CLI plugin, add a plugin to this marketplace repository, add a component (agent/skill/hook/MCP server/LSP server/command) to an existing plugin, or asks about plugin.json fields, plugin structure, or how plugins get versioned and released in this repo. Also use it when the request mentions "forge plugin", "new plugin", "plugin.json", or extending the marketplace at .github/plugin/marketplace.json.
license: MIT
---

# Authoring GitHub Copilot CLI plugins

A Copilot CLI plugin is a directory that bundles reusable customizations —
agents, skills, hooks, MCP servers, LSP servers, and slash commands — into a
single installable unit, described by a `plugin.json` manifest. This skill
covers how to design, scaffold, and validate a plugin from scratch, and how
to add it to this repository's marketplace so it can be installed and kept
up to date.

Read the reference file for a component before writing it — each one
documents the exact schema and common mistakes. Don't guess field names.

## Workflow

1. **Clarify scope.** Ask (or infer from the request) what the plugin should
   do, and which components it actually needs. Not every plugin needs every
   component — a plugin that only bundles an MCP server config doesn't need
   an `agents/` directory. Resist the urge to scaffold empty directories for
   components the plugin doesn't use; empty `agents/` or `skills/` folders
   are just noise.

2. **Scaffold the directory.** Under `plugins/<plugin-name>/` (kebab-case,
   letters/numbers/hyphens only, matching the `name` field), create only the
   subdirectories the plugin needs:
   ```text
   plugins/<plugin-name>/
   ├── plugin.json           # always required
   ├── agents/               # if the plugin ships custom agents
   ├── skills/               # if the plugin ships skills
   ├── commands/             # if the plugin ships slash commands
   ├── hooks.json            # if the plugin reacts to session events
   ├── .mcp.json             # if the plugin wires up MCP servers
   └── lsp.json              # if the plugin wires up LSP servers
   ```
   See `references/plugin-json.md` for the full manifest schema, including
   how to point these fields at non-default paths (e.g. multiple skill
   directories).

3. **Write `plugin.json` first.** It's the only required file, and pins down
   the plugin's name, description, and where every other component lives.
   See `references/plugin-json.md`.

4. **Author each component** using the matching reference file:
   - Custom agents → `references/agents.md`
   - Skills → `references/skills.md`
   - Hooks → `references/hooks.md`
   - MCP and LSP servers → `references/mcp-lsp.md`
   - Slash commands → `references/commands.md`

   Templates for each component type live under `templates/` — copy and
   adapt rather than writing frontmatter from memory, since small YAML
   mistakes (wrong key name, missing quotes) silently break loading.

5. **Validate structure and JSON.** Before calling it done:
   - `plugin.json` and any `hooks.json`/`.mcp.json`/`lsp.json` must be valid
     JSON (`jq . plugin.json` or `python -m json.tool plugin.json`).
   - Every `*.agent.md` and `SKILL.md` needs valid YAML frontmatter with the
     required `name` and `description` keys.
   - Every path referenced in `plugin.json` must actually exist.
   - Skill directory names and each skill's `name` field should match.

6. **Test it locally** before considering the plugin done:
   ```shell
   copilot plugin install ./plugins/<plugin-name>
   copilot plugin list
   ```
   Then in an interactive session, confirm the components loaded:
   `/agent` (custom agents), `/skills list` (skills), `/mcp` (MCP servers).
   If you edit the plugin after installing it, reinstall
   (`copilot plugin install ./plugins/<plugin-name>`) to refresh the cache —
   the CLI reads from a cached copy, not live from disk.

7. **Register it in this repository's marketplace**, if this plugin should
   be discoverable alongside the others here. Add an entry to the `plugins`
   array in `.github/plugin/marketplace.json`:
   ```json
   {
     "name": "<plugin-name>",
     "description": "<same tone/detail as plugin.json description>",
     "version": "<matches plugin.json version, typically 0.1.0 to start>",
     "source": "./plugins/<plugin-name>"
   }
   ```
   Keep the marketplace `description` and `version` in sync with
   `plugin.json` — they should never drift. Don't hand-bump the version on
   every trivial edit: `.github/workflows/plugin-release.yml` auto-increments
   the patch version on merge to `main` for any plugin whose files changed
   (unless you already bumped `version` yourself in the same change, in which
   case your bump is respected as-is), and keeps `marketplace.json` synced
   automatically. Only bump `version` manually for a deliberate minor/major
   release.

## Key things to get right

- **`name` is load-bearing.** It's the plugin directory's identity for
  install/uninstall/enable/disable and must be kebab-case, ≤64 chars. It's
  also what people type when uninstalling
  (`copilot plugin uninstall <name>`), so keep it stable once published —
  renaming breaks existing installs.
- **Component paths default sensibly.** `agents`, `skills` default to
  `agents/` and `skills/` respectively if omitted from `plugin.json` — only
  set them explicitly if you deviate from the convention (e.g. multiple
  skill directories, or a non-standard hooks file location).
- **Skills are the biggest lever for specialized behavior**, but only
  trigger when Copilot decides they're relevant — so a skill's
  `description` needs to say both what it does *and* when to use it,
  concretely (trigger phrases, file types, task shapes). A skill that's
  never invoked is dead weight. See `references/skills.md` for how to write
  a strong description.
- **Agents run in a separate context window.** Use an agent (not a skill)
  when the work benefits from being offloaded — long, semi-independent
  tasks — rather than just needing extra instructions injected into the
  main conversation.
- **Hooks and pre-approved tools are a trust boundary.** Anything in
  `allowed-tools`/`tools` runs without asking the user first. Only
  pre-approve `bash`/`shell` for scripts you've written and reviewed
  yourself.
- **One plugin, one coherent purpose.** If you find yourself bundling
  unrelated agents/skills/MCP servers "because they're handy," consider
  whether that's really two plugins.

## Reference files

- `references/plugin-json.md` — full `plugin.json` field reference,
  component path defaults, Open Plugin Spec notes.
- `references/agents.md` — `*.agent.md` frontmatter, tool restriction,
  model pinning, when to use an agent vs. a skill.
- `references/skills.md` — `SKILL.md` structure, writing triggering
  descriptions, bundling scripts/references/assets, progressive disclosure.
- `references/hooks.md` — `hooks.json` structure, available hook triggers,
  bash/powershell cross-platform scripts.
- `references/mcp-lsp.md` — `.mcp.json` and `lsp.json` formats.
- `references/commands.md` — slash command (`*.prompt.md`) format.
- `references/marketplace.md` — this repo's `marketplace.json` layout and
  the auto-release workflow.

## Templates

Copy from `templates/` as a starting point rather than writing JSON or
frontmatter from memory:
- `templates/plugin.json` — manifest skeleton.
- `templates/hooks.json` — a working `sessionStart` hook example.
- `templates/.mcp.json` — an MCP server config skeleton.
- `templates/agents/plugin-reviewer.agent.md` — a **working agent**, not a
  placeholder: it actually runs the validator below and reviews a plugin's
  descriptions and component usage. Copy it into a new plugin, or use it as
  a concrete reference for how to scope tools and instructions for a real
  reviewer agent.
- `templates/skills/validate-plugin/` — a **complete, working skill**, not
  a placeholder: it bundles `scripts/validate-plugin.py` (run via `uv run`,
  no dependencies needed), which discovers and reports every component a
  plugin declares (agents, skills, commands, hooks, MCP/LSP servers) and
  checks a plugin directory's `plugin.json` (valid JSON, kebab-case
  `name`, every referenced path exists), validates any `hooks.json`/
  `.mcp.json`/`lsp.json`, confirms every agent/skill file has proper
  frontmatter, and checks skill directory names match their declared
  names. Copy this directory into a new plugin whenever it should be able
  to validate its own structure before install — or read it as a concrete
  example of how a skill bundles and invokes a script (see
  `references/skills.md`).

Run the validator against any plugin you're building to catch structural
mistakes before testing with `copilot plugin install`:

```shell
uv run plugins/forge/skills/plugin-creator/templates/skills/validate-plugin/scripts/validate-plugin.py plugins/<plugin-name>
```
