---
name: validate-plugin
description: Validates that a GitHub Copilot CLI plugin directory is structurally correct and reports every component it contains — plugin.json is valid JSON with a proper name, every path it references exists, hooks/MCP/LSP configs are valid JSON, every agent/skill file has the required frontmatter, and skill directory names match their declared names. Use this whenever asked to check, validate, lint, review, or summarize a Copilot CLI plugin directory before installing or shipping it.
license: MIT
allowed-tools: bash
---

# Validate a Copilot CLI plugin's structure

Before installing or shipping a plugin, run the bundled script against its
directory:

```shell
uv run scripts/validate-plugin.py /path/to/plugin-dir
```

(Omit the path to check the current directory. The script requires
[`uv`](https://docs.astral.sh/uv/) — it has no third-party dependencies,
but `uv run` is the standard way to execute a self-contained Python script
without needing a pre-existing virtualenv or global install.)

## What you get

A single, neat report with two parts:

1. **Components** — every agent, skill, command, hook trigger, and MCP/LSP
   server the plugin actually declares, discovered directly from
   `plugin.json` and the files on disk (not just what you'd have to
   remember was in there). This alone is useful any time you're asked to
   "summarize this plugin" or "what does this plugin include."
2. **Validation** — a `PASS`/`FAIL` line per check, covering:
   - `plugin.json` exists and is valid JSON.
   - `plugin.json` has a `name` field, and it's kebab-case.
   - Every path referenced by `plugin.json`'s component fields (`agents`,
     `skills`, `commands`, and any `hooks`/`mcpServers`/`lspServers`
     fields that point at a file rather than an inline object) actually
     exists on disk.
   - `hooks.json`, `.mcp.json`, and `lsp.json` (whether referenced
     explicitly or found at their conventional path) are valid JSON.
   - Every `*.agent.md` file and every `SKILL.md` file has both `name` and
     `description` in its YAML frontmatter.
   - Every skill's declared `name` matches the directory it lives in
     (the convention every skill should follow).

The report ends with a one-line summary (`N passed, M failed`) and the
script exits `0` if everything passes, `1` if anything fails — safe to use
as a pre-flight check before `copilot plugin install`, or to wire into CI.
Fix every `FAIL` line before installing.

This script only checks structure (valid JSON, required fields, files
existing, naming conventions) — it can't judge whether descriptions are
well-written or whether an agent's instructions make sense. Pair it with a
human read of the content, especially the `description` fields that drive
whether skills/agents actually get used.
