#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Validates a GitHub Copilot CLI plugin directory and prints a report.

Usage:
    uv run scripts/validate-plugin.py [PLUGIN_DIR]

Defaults to the current directory. Discovers every component the plugin
declares (agents, skills, hooks, MCP servers, LSP servers, commands),
prints them in a neat report, and runs a set of structural checks against
plugin.json, its referenced paths, and every agent/skill file's
frontmatter. Exits 0 if everything passes, 1 if anything fails.

Run via `uv run` so it works standalone with no virtualenv setup — uv
reads the inline metadata block above and provisions the right Python
automatically. No third-party dependencies are needed, but the block is
kept so this stays true even if the script grows some later.
"""
import json
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class Report:
    def __init__(self):
        self.checks = []  # (passed: bool, message: str)

    def check(self, passed, message):
        self.checks.append((passed, message))
        return passed

    @property
    def failed_count(self):
        return sum(1 for passed, _ in self.checks if not passed)

    @property
    def passed_count(self):
        return sum(1 for passed, _ in self.checks if passed)


def load_json(path):
    """Returns (data, error_message). error_message is None on success."""
    try:
        return json.loads(path.read_text()), None
    except FileNotFoundError:
        return None, f"{path} does not exist"
    except json.JSONDecodeError as e:
        return None, f"{path} is not valid JSON ({e})"


def parse_frontmatter(path):
    """Returns a dict of simple top-level `key: value` frontmatter fields."""
    text = path.read_text()
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def as_path_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [v for v in value if isinstance(v, str)]
    return []


def discover_agents(plugin_dir, manifest):
    agents = []
    for rel in as_path_list(manifest.get("agents")) or ["agents"]:
        agent_dir = plugin_dir / rel
        if agent_dir.is_dir():
            agents.extend(sorted(agent_dir.glob("*.agent.md")))
    return agents


def discover_skills(plugin_dir, manifest):
    skills = []
    for rel in as_path_list(manifest.get("skills")) or ["skills"]:
        skills_dir = plugin_dir / rel
        if skills_dir.is_dir():
            skills.extend(sorted(skills_dir.glob("*/SKILL.md")))
    return skills


def discover_commands(plugin_dir, manifest):
    commands = []
    for rel in as_path_list(manifest.get("commands")):
        cmd_dir = plugin_dir / rel
        if cmd_dir.is_dir():
            commands.extend(sorted(cmd_dir.glob("*.prompt.md")))
    return commands


def resolve_config(plugin_dir, manifest, field, default_filename):
    """Returns (kind, value) where kind is 'file', 'inline', or None.

    Looks at the plugin.json field first (a path string or an inline
    object); falls back to the conventional default filename at the
    plugin root if the field is absent but the file exists anyway.
    """
    value = manifest.get(field)
    if isinstance(value, str):
        return "file", plugin_dir / value
    if isinstance(value, dict):
        return "inline", value
    default_path = plugin_dir / default_filename
    if default_path.is_file():
        return "file", default_path
    return None, None


def report_component_list(title, items, describe):
    if not items:
        print(f"  {title}: none")
        return
    print(f"  {title} ({len(items)}):")
    for item in items:
        print(f"    - {describe(item)}")


def main():
    plugin_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    report = Report()

    manifest_path = plugin_dir / "plugin.json"
    manifest, error = load_json(manifest_path)
    if error:
        report.check(False, error)
        print_final_report(plugin_dir, None, report, [], [], [], None, None, [])
        sys.exit(1)
    report.check(True, f"{manifest_path.name} is valid JSON")

    name = manifest.get("name", "")
    if not name:
        report.check(False, "plugin.json is missing the required \"name\" field")
    elif not NAME_RE.match(name):
        report.check(False, f"plugin.json \"name\" (\"{name}\") is not kebab-case")
    else:
        report.check(True, f"plugin.json \"name\" is \"{name}\" (valid kebab-case)")

    # Referenced component paths must exist.
    referenced = []
    for field in ("agents", "skills", "commands"):
        referenced.extend(as_path_list(manifest.get(field)))
    for field in ("hooks", "mcpServers", "lspServers"):
        val = manifest.get(field)
        if isinstance(val, str):
            referenced.append(val)
    for rel in referenced:
        full = plugin_dir / rel
        report.check(full.exists(), f"referenced path \"{rel}\" exists" if full.exists()
                     else f"plugin.json references \"{rel}\" but {full} does not exist")

    # Discover components.
    agents = discover_agents(plugin_dir, manifest)
    skills = discover_skills(plugin_dir, manifest)
    commands = discover_commands(plugin_dir, manifest)
    hooks_kind, hooks_val = resolve_config(plugin_dir, manifest, "hooks", "hooks.json")
    mcp_kind, mcp_val = resolve_config(plugin_dir, manifest, "mcpServers", ".mcp.json")
    lsp_kind, lsp_val = resolve_config(plugin_dir, manifest, "lspServers", "lsp.json")

    # Validate agent/skill frontmatter.
    for agent_file in agents:
        fields = parse_frontmatter(agent_file)
        rel = agent_file.relative_to(plugin_dir)
        if "name" in fields and "description" in fields:
            report.check(True, f"{rel} has name + description in frontmatter")
        else:
            missing = [k for k in ("name", "description") if k not in fields]
            report.check(False, f"{rel} is missing {', '.join(missing)} in frontmatter")

    for skill_file in skills:
        fields = parse_frontmatter(skill_file)
        rel = skill_file.relative_to(plugin_dir)
        if "name" in fields and "description" in fields:
            report.check(True, f"{rel} has name + description in frontmatter")
        else:
            missing = [k for k in ("name", "description") if k not in fields]
            report.check(False, f"{rel} is missing {', '.join(missing)} in frontmatter")
        # The skill's directory name should match its declared name, per convention.
        dir_name = skill_file.parent.name
        declared_name = fields.get("name")
        if declared_name and declared_name != dir_name:
            report.check(False, f"{rel} declares name \"{declared_name}\" but lives in "
                                 f"directory \"{dir_name}\" (convention is for these to match)")

    # Validate any inline/file hooks, mcp, lsp configs are well-formed JSON.
    for kind, val, label in ((hooks_kind, hooks_val, "hooks config"),
                             (mcp_kind, mcp_val, "mcpServers config"),
                             (lsp_kind, lsp_val, "lspServers config")):
        if kind == "file":
            data, err = load_json(val)
            if err:
                report.check(False, err)
            else:
                report.check(True, f"{val.relative_to(plugin_dir)} is valid JSON")

    print_final_report(plugin_dir, manifest, report, agents, skills, commands,
                        (hooks_kind, hooks_val), (mcp_kind, mcp_val), commands)
    sys.exit(1 if report.failed_count else 0)


def print_final_report(plugin_dir, manifest, report, agents, skills, commands,
                        hooks, mcp, _unused):
    name = (manifest or {}).get("name", "(unknown)")
    version = (manifest or {}).get("version", "unversioned")
    description = (manifest or {}).get("description", "")

    print(f"=== Plugin: {name} (v{version}) ===")
    if description:
        print(description)
    print()
    print("Components:")
    report_component_list("Agents", agents,
                           lambda p: f"{p.name.removesuffix('.agent.md')} ({p.relative_to(plugin_dir)})")
    report_component_list("Skills", skills,
                           lambda p: f"{p.parent.name} ({p.relative_to(plugin_dir)})")
    report_component_list("Commands", commands,
                           lambda p: f"{p.name.removesuffix('.prompt.md')} ({p.relative_to(plugin_dir)})")

    hooks_kind, hooks_val = hooks
    if hooks_kind == "file":
        data, err = load_json(hooks_val)
        triggers = sorted((data or {}).get("hooks", {}).keys()) if not err else []
        print(f"  Hooks: {hooks_val.relative_to(plugin_dir)}"
              + (f" ({', '.join(triggers)})" if triggers else ""))
    elif hooks_kind == "inline":
        triggers = sorted(hooks_val.get("hooks", {}).keys())
        print(f"  Hooks: inline ({', '.join(triggers)})" if triggers else "  Hooks: inline")
    else:
        print("  Hooks: none")

    mcp_kind, mcp_val = mcp
    if mcp_kind == "file":
        data, err = load_json(mcp_val)
        servers = sorted((data or {}).get("mcpServers", {}).keys()) if not err else []
        print(f"  MCP servers: {mcp_val.relative_to(plugin_dir)}"
              + (f" ({', '.join(servers)})" if servers else ""))
    elif mcp_kind == "inline":
        servers = sorted(mcp_val.get("mcpServers", mcp_val).keys())
        print(f"  MCP servers: inline ({', '.join(servers)})" if servers else "  MCP servers: inline")
    else:
        print("  MCP servers: none")

    print()
    print("Validation:")
    for passed, message in report.checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {message}")

    print()
    status = "All checks passed" if report.failed_count == 0 else "Some checks failed"
    print(f"Summary: {status} — {report.passed_count} passed, {report.failed_count} failed")


if __name__ == "__main__":
    main()
