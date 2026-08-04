# Authoring skills

A skill is a directory of instructions (and optionally scripts, references,
and assets) that Copilot loads into context only when it decides the skill
is relevant to the current task. Skills are the right tool for "extra
knowledge or capability for a specific kind of task" — as opposed to agents,
which offload work to a separate context window (see `agents.md`).

## Minimum layout

```text
skills/
└── my-skill/
    └── SKILL.md
```

The subdirectory name should be lowercase-with-hyphens and typically matches
the skill's `name` frontmatter field. A plugin can ship many skills, each in
its own subdirectory.

## `SKILL.md` frontmatter

```markdown
---
name: my-skill
description: What the skill does, and precisely when Copilot should use it.
license: MIT
allowed-tools: bash
---

Instructions, in Markdown, for how to perform the task...
```

| Field           | Required | Notes |
| --------------- | -------- | ----- |
| `name`          | Yes      | Lowercase, hyphens for spaces. |
| `description`   | Yes      | The single biggest lever for whether this skill ever actually triggers. See "Writing a triggering description" below. |
| `license`       | No       | License covering this skill's content. |
| `allowed-tools` | No       | Tools Copilot may use without asking for confirmation each time it uses this skill. **Only pre-approve `bash`/`shell` for scripts you wrote and reviewed yourself** — it removes the human-in-the-loop check before running terminal commands, which is exactly the gap prompt-injected or malicious skills would exploit. |

## Writing a triggering description

Copilot decides whether to consult a skill based only on its `name` +
`description` (it hasn't read the body yet at that point). A skill with
great instructions but a vague description simply won't get used. So the
description should cover:

1. **What it does** — concretely, not just the general subject.
2. **When to use it** — trigger phrases, file types, task shapes, even if
   the user doesn't explicitly name the skill or invoke it by name.

Weak: `"Helps with GitHub Actions."`
Stronger: `"Guide for debugging failing GitHub Actions workflows. Use this whenever asked to investigate, fix, or debug a failing CI/workflow run, or when a pull request shows failed checks."`

It's fine — even encouraged — to be a little insistent in the description
("make sure to use this whenever...") since the failure mode to guard
against is under-triggering, not over-triggering.

## Progressive disclosure — keep `SKILL.md` itself lean

Skills load in three tiers:
1. `name` + `description` — always in context.
2. `SKILL.md` body — loaded once the skill triggers.
3. Everything else in the skill's directory (scripts, reference docs,
   templates/assets) — loaded or executed only as needed.

Keep `SKILL.md` itself under roughly 500 lines. If a skill covers several
sub-domains (e.g. different frameworks, or several distinct component
types), split the detail into a `references/` directory and have `SKILL.md`
point to the right file for the right situation, rather than inlining
everything. This skill (`plugin-creator`) is itself an example of that
pattern.

## Bundling a script

```text
skills/image-convert/
├── SKILL.md
└── convert-svg-to-png.sh
```

Reference the script from the instructions body (e.g. "run
`convert-svg-to-png.sh` from this skill's directory, passing the SVG path as
the first argument"). Copilot discovers every file in the skill's directory
automatically when the skill is invoked — you don't need to register the
script anywhere else.

## Skill vs. custom instructions

Use plain custom/repository instructions for guidance relevant to nearly
every task (coding standards, style). Reserve skills for detailed,
specialized instructions that should only be pulled into context when
actually relevant — that's what keeps the default context window lean.
