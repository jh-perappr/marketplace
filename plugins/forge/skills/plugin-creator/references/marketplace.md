# This repo's marketplace

This repository (`jh-perappr/marketplace`) is itself a Copilot CLI plugin
marketplace. `.github/plugin/marketplace.json` lists every plugin under
`plugins/`.

## `marketplace.json` shape

```json
{
  "name": "marketplace",
  "owner": { "name": "...", "email": "..." },
  "metadata": {
    "description": "Custom Copilot CLI plugin marketplace for the harness project",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "forge",
      "description": "...",
      "version": "0.1.1",
      "source": "./plugins/forge"
    }
  ]
}
```

Each entry in `plugins` needs `name`, `description`, `version`, and
`source` (path to the plugin directory relative to the repo root — the
leading `./` is optional).

## Adding a new plugin to this marketplace

1. Create `plugins/<plugin-name>/` with its `plugin.json` and components
   (see the main `SKILL.md` workflow).
2. Add a matching entry to the `plugins` array in
   `.github/plugin/marketplace.json`. Keep `description` and `version` here
   in sync with the plugin's own `plugin.json` — they're meant to describe
   the same thing, not drift independently.
3. Commit and open a PR as normal.

## Versioning is (mostly) automatic

`.github/workflows/plugin-release.yml` runs on every push to `main` that
touches `plugins/**`:

- It detects which plugin directories changed in that push.
- For each changed plugin: if the commit itself already changed the
  `version` field in that plugin's `plugin.json`, that manual bump is
  respected as-is (no double bump).
- Otherwise, it auto-increments the patch version (`x.y.z` → `x.y.(z+1)`).
- It keeps `.github/plugin/marketplace.json`'s version for that plugin in
  sync with the plugin's own `plugin.json` version.
- Release commits are tagged `[skip release]` so they don't recursively
  retrigger the workflow.

**Implication for authoring:** don't manually bump `version` for routine
changes — let CI do it. Only hand-bump `version` in `plugin.json` when you
specifically want a minor/major release (e.g. `0.1.0` → `0.2.0` for a
notable new capability) rather than an automatic patch bump.
