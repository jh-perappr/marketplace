# Hooks

Hooks run shell commands at specific points during an agent session —
useful for logging, notifications, enforcing checks (e.g. auto-run tests
after edits), or gating tool use.

## File location

A plugin's hooks live in a `hooks.json` at the plugin root (or wherever
`plugin.json`'s `hooks` field points), or under a `hooks/` directory.

## Structure

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [ ... ],
    "sessionEnd": [ ... ],
    "userPromptSubmitted": [ ... ],
    "preToolUse": [ ... ],
    "postToolUse": [ ... ],
    "agentStop": [ ... ],
    "errorOccurred": [ ... ]
  }
}
```

Only include the trigger arrays you actually use — omit the rest rather
than leaving empty arrays.

Each entry in a trigger array is a command hook:

```json
{
  "type": "command",
  "bash": "echo \"Session started: $(date)\" >> logs/session.log",
  "powershell": "Add-Content -Path logs/session.log -Value \"Session started: $(Get-Date)\"",
  "cwd": ".",
  "timeoutSec": 10,
  "env": { "LOG_LEVEL": "INFO" }
}
```

| Field        | Notes |
| ------------ | ----- |
| `bash`       | Script/command for Linux and macOS. |
| `powershell` | Script/command for Windows (requires PowerShell 7+). |
| `cwd`        | Working directory for the command. |
| `timeoutSec` | Default is 30s — raise it for anything slower, but keep hooks fast since they run inline during a session. |
| `env`        | Extra environment variables for the command. |

Provide **both** `bash` and `powershell` if the plugin should work
cross-platform — the CLI picks the right one for the user's OS
automatically. If you only need one platform, it's fine to omit the other.

## Common pitfalls

- Missing `"version": 1` at the top level — hooks silently won't load.
- Invalid JSON — validate with `jq .  hooks.json` before shipping.
- Scripts referenced by path need to be executable (`chmod +x`) and have a
  proper shebang.
- Hook output for triggers that expect structured JSON back must be valid,
  single-line JSON.
- Keep hook commands side-effect-light and fast — they run synchronously at
  key points in every session, so a slow or noisy hook degrades the whole
  experience.
