# Slash commands

A plugin can bundle its own slash commands: reusable, invokable prompts
that show up as `/command-name` in an interactive session.

## File layout

```text
commands/
└── my-command.prompt.md
```

Point `plugin.json`'s `commands` field at the directory (or directories) if
it isn't the conventional `commands/`.

## Format

```markdown
---
description: "One-line summary shown in autocomplete."
name: my-command
agent: "agent"
model: "Claude Sonnet 4.6"
tools: ["search/codebase"]
argument-hint: "Optional hint for expected input"
---

Instructions for what this command should do when invoked, written exactly
like a prompt you'd type yourself. Reference `$ARGUMENTS` or similar if the
command should incorporate free-text the user typed after the command name.
```

| Field           | Required | Notes |
| --------------- | -------- | ----- |
| `description`   | No       | Shown in slash-command autocomplete — write it like a short imperative summary of what happens. |
| `name`          | No       | Defaults to the filename (without `.prompt.md`). |
| `agent`         | No       | Which agent handles this command: `ask`, `agent`, `plan`, or a custom agent name from this plugin (or another installed one). |
| `model`         | No       | Pin a specific model for this command if it has consistent requirements. |
| `tools`         | No       | Restrict the toolset available while this command runs. |
| `argument-hint` | No       | Placeholder text shown to hint what input the command expects. |

## When to add a command vs. a skill

A command is for a short, explicitly user-invoked action ("run this exact
workflow now"). A skill is for knowledge/capability Copilot should reach for
on its own when it judges the task calls for it. If the workflow only makes
sense when a person deliberately kicks it off (e.g. "/release-notes"), it's
a command. If it should activate automatically based on the shape of a
request, it's a skill.
