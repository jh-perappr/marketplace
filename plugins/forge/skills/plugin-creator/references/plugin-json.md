# `plugin.json` reference

Every plugin needs exactly one `plugin.json` at the root of its directory.
It is the manifest: it names the plugin and tells the CLI where to find its
components. All fields except `name` are optional.

## Required field

| Field  | Type   | Notes |
| ------ | ------ | ----- |
| `name` | string | Kebab-case (letters, numbers, hyphens only), max 64 chars. This is the identifier used for `copilot plugin install/uninstall/enable/disable`, so treat it as a stable public API once the plugin is shared. |

## Optional metadata fields

| Field         | Type      | Notes |
| ------------- | --------- | ----- |
| `description` | string    | Max 1024 chars. Shown when browsing a marketplace — write it for a human deciding whether to install, not just for search. |
| `version`     | string    | Semantic version (`1.0.0`). In this repo, leave this alone after the first commit unless you're doing a deliberate release — CI auto-bumps the patch version on merge. |
| `author`      | object    | `{ "name": ..., "email": ..., "url": ... }`. Only `name` is required. |
| `homepage`    | string    | Plugin homepage URL. |
| `repository`  | string    | Source repository URL. |
| `license`     | string    | SPDX identifier, e.g. `MIT`. |
| `keywords`    | string[]  | Search keywords for marketplace browsing. |
| `category`    | string    | Plugin category. |
| `tags`        | string[]  | Additional tags. |

## Component path fields

All optional — the CLI falls back to the listed default convention if a
field is omitted. Only set these explicitly when you deviate from the
convention (multiple directories, a renamed file, etc.).

| Field        | Type                            | Default   | Points to |
| ------------ | -------------------------------- | --------- | --------- |
| `agents`     | string \| string[]               | `agents/` | Directories containing `*.agent.md` files. |
| `skills`     | string \| string[]               | `skills/` | Directories containing `SKILL.md`-bearing subdirectories. |
| `commands`   | string \| string[]               | —         | Directories containing slash command files. |
| `hooks`      | string \| object                 | —         | Path to a hooks config file, or an inline hooks object. |
| `mcpServers` | string \| object                 | —         | Path to an MCP config file (e.g. `.mcp.json`), or inline server definitions. |
| `lspServers` | string \| object                 | —         | Path to an LSP config file, or inline server definitions. |
| `extensions` | string \| string[] \| object      | —         | Path(s) to extension directories. `{ paths: [...], exclusive: true }` suppresses built-in extensions. |

Multiple skill/agent directories are a real pattern — e.g.
`"skills": ["skills/", "extra-skills/"]` — useful when a plugin groups
skills by domain but still wants them all installed together.

## Minimal example

```json
{
  "name": "my-dev-tools",
  "description": "React development utilities: component scaffolding, test running, and a Storybook-aware review agent.",
  "version": "0.1.0",
  "author": { "name": "Jane Doe", "email": "jane@example.com" },
  "license": "MIT",
  "keywords": ["react", "frontend"],
  "agents": "agents/",
  "skills": ["skills/"]
}
```

Only include the component fields (`agents`, `skills`, `hooks`,
`mcpServers`, `lspServers`, `commands`) that this plugin actually uses.

## Open Plugin Spec support

Setting a `$schema` field to the canonical Agent Plugins (Open Plugin Spec)
v1.0.0 schema URL opts a plugin into that spec's semantics additively (it
also changes what the `extensions` field means). Only do this if you
specifically need interop with tools built against that external spec —
most plugins in this repo don't need it.
