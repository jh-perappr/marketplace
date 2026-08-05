---
name: okf-documentation
description: Create and review OKF v0.2 knowledge bundles under docs/ as Markdown concepts with YAML frontmatter, provenance, trust, lifecycle, links, indexes, logs, and attested computations. Use for architecture, GRC, program decisions, risks, runbooks, project knowledge, or any docs/ change.
license: MIT
---

# OKF v0.2 documentation

Follow the full contract in `references/okf-v0.2.md`. Treat `docs/` as an
OKF knowledge bundle: every non-reserved `.md` file is a concept with YAML
frontmatter and a non-empty `type`.

- Use descriptive `type`, `title`, `description`, `resource`, and `tags` as
  applicable; preserve unknown extension keys.
- Record provenance in `sources`, authorship/time in `generated`, checks in
  `verified`, and freshness with `status` and `stale_after`.
- Use standard Markdown links for relationships, bundle-relative paths, and
  `references/` for source material, executors, and attesters.
- Keep root and directory `index.md` files as frontmatter-free progressive
  disclosure lists; keep `log.md` files as newest-first ISO-date histories.
- As concepts grow, group them by domain or lifecycle in subdirectories,
  add a local `index.md` and `log.md`, and link concepts through stable
  bundle-root paths; update both ends of important relationships.
- Use `human:<id>`, `<producer>/<version>`, and `process:<id>` actor forms.
- Define `Attested Computation` concepts with runtime, typed parameters,
  executor receipt, and deterministic attester contracts; never improvise or
  edit a sanctioned computation.

For architecture and GRC records, use stable names such as
`docs/adr-<number>-<short-title>.md` and `docs/grc-<short-title>.md` without
overwriting existing files. Add `okf_version: "0.2"` only to the bundle-root
`index.md`. Use `mermaid-diagrams` for diagrams and validate every diagram
with `mmdc` or the open-source Mermaid CLI before delivery.
