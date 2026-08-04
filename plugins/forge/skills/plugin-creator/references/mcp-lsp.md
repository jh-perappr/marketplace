# MCP and LSP server configuration

## MCP servers

Point `plugin.json`'s `mcpServers` field at a config file (conventionally
`.mcp.json` at the plugin root) or inline the definitions directly in
`plugin.json`. Use MCP servers to give Copilot access to external tools and
data sources — issue trackers, databases, CI systems, design tools, etc. —
rather than for behaviors a skill or agent could handle with the CLI's
built-in tools.

Only bundle an MCP server in a plugin if the plugin's whole purpose
benefits from it being pre-wired — e.g. "encapsulate a complex MCP server
setup" is one of the core reasons plugins exist. Don't reach for an MCP
server when a skill/script would do.

Example (`.mcp.json`):

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@example/my-mcp-server"],
      "env": { "API_TOKEN": "${MY_SERVER_TOKEN}" }
    }
  }
}
```

Exact server-definition fields depend on the MCP server's own transport
(stdio command, or remote URL) — consult that server's documentation for
its specific config shape. Never hardcode secrets into the plugin; reference
environment variables instead.

## LSP servers

Point `plugin.json`'s `lspServers` field at a config file (conventionally
`lsp.json` or `lsp-config/servers.json`) or inline the definitions.

```json
{
  "lspServers": {
    "my-lsp": {
      "command": "my-language-server",
      "fileExtensions": { ".myext": "mylang" }
    }
  }
}
```

For cross-platform launch scripts, use `bash`/`powershell` instead of
`command`, exactly as with hooks:

```json
{
  "lspServers": {
    "my-lsp": {
      "bash": "${PLUGIN_ROOT}/scripts/start-lsp.sh",
      "powershell": "${PLUGIN_ROOT}/scripts/start-lsp.ps1",
      "fileExtensions": { ".myext": "mylang" }
    }
  }
}
```

| Field                   | Required | Notes |
| ----------------------- | -------- | ----- |
| `command`/`bash`/`powershell` | At least one | How to launch the server. `${PLUGIN_ROOT}` resolves to the plugin's own directory — use it instead of a relative or absolute path so the plugin works regardless of where it's installed. |
| `cwd`                   | No       | Working directory; supports `${PLUGIN_ROOT}`. |
| `args`                  | No       | Args for `command` (ignored for `bash`/`powershell`). |
| `env`                   | No       | Environment variables for the server process. |
| `fileExtensions`        | Yes      | Maps file extensions to language IDs, e.g. `{ ".ts": "typescript" }`. |
| `rootUri`               | No       | Project root relative to the git root (default `.`). |
| `initializationOptions` | No       | Passed through to the server's LSP `initialize` request. |

Only add an LSP server to a plugin if the plugin is specifically about
supporting a language/tooling ecosystem that isn't already covered.
