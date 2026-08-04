# Authoring custom agents

Custom agents are subagents with their own context window: the main agent
can hand off a task to them instead of doing it inline. Use an agent (over
a skill) when the work is substantial enough to benefit from a fresh,
separate context — long or semi-independent tasks, or a persona whose tool
access should be deliberately restricted (e.g. a reviewer that can't edit
files).

## File layout

Each agent is one Markdown file with a `.agent.md` extension, in the
plugin's `agents/` directory (or wherever `plugin.json`'s `agents` field
points):

```text
agents/
└── my-agent.agent.md
```

The filename (without `.agent.md`) is what's used with
`copilot --agent <name>` and in agent-selection UI, so prefer lowercase
with hyphens even though the `name` frontmatter field can differ.

## Frontmatter

```markdown
---
name: my-agent
description: What this agent is expert in, and when it should be used.
tools: ["bash", "edit", "view"]
model: "Claude Sonnet 4.6"
---

You are ... (the agent's system prompt / instructions body)
```

| Field         | Required | Notes |
| ------------- | -------- | ----- |
| `name`        | Yes      | Identifier shown in agent lists. |
| `description` | Yes      | States the agent's expertise *and* when to use it — this is how the main agent decides whether to delegate to it. Be concrete: name the trigger conditions (task types, keywords, file kinds), not just the general subject area. |
| `tools`       | No       | Restricts the agent's toolset. Omit to grant access to all tools. Restrict deliberately for agents that should never mutate state (e.g. a reviewer with `["view", "grep", "bash"]` and no `edit`). |
| `model`       | No       | Pin a specific model if this agent's task benefits from a particular model's strengths, otherwise let it inherit the session default. |

## Writing the instructions body

The body below the frontmatter is the agent's system prompt. Keep it
focused on:
- The agent's domain expertise and the standards it should hold work to.
- Any specific process it should follow (steps, checks, required actions).
- Constraints (what it must *not* do — e.g. "never push to main").

Avoid duplicating information that belongs in the `description` (that's for
delegation-selection, this is for behavior once selected).

## Agent vs. skill — quick check

- Does the task need its own context window, or offload from the main
  conversation? → agent.
- Is it really just "extra instructions/knowledge/scripts for a particular
  kind of task, injected into the current conversation"? → skill.
- Needing restricted tool access on its own isn't sufficient reason for an
  agent — but combined with a genuinely separate task scope, it usually is.
