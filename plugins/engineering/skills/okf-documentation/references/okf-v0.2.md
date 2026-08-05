# OKF v0.2 coverage reference

This reference summarizes the authoritative
[Open Knowledge Format v0.2 specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
for agents working in a project's `docs/` directory. It is an operational
checklist, not a replacement for the specification.

## 1. Bundle and concept model

- Treat the target `docs/` directory as a self-contained knowledge bundle:
  a hierarchical tree of Markdown files.
- `index.md` and `log.md` are reserved at every directory level. They are
  not concept documents.
- Every other `.md` file is one concept and must begin with a YAML
  frontmatter block delimited by `---`, followed by a Markdown body.
- The concept ID is its bundle-relative path without `.md`.
- A bundle may be a repository, archive, or subdirectory; do not prescribe
  a serving, storage, taxonomy, or query system.
- Keep Markdown structured with headings, lists, tables, code fences, and
  links so humans and agents can retrieve it.

## 2. Frontmatter

`type` is the only required field and must be a non-empty descriptive string.
Unknown types and extension keys are valid and must be preserved.

Use these optional fields when applicable:

| Field | Requirement |
| --- | --- |
| `title` | Human-readable display name; otherwise derive from filename. |
| `description` | One-sentence summary suitable for indexes and search. |
| `resource` | Canonical URI or bundle path for the described asset. |
| `tags` | List of short cross-cutting labels. |
| `sources` | Provenance entries for internal or external source material. |
| `generated` | `{by, at}` describing who/what produced the current content. |
| `verified` | One event or list of `{by, at}` verification events. |
| `status` | `draft`, `stable`, or `deprecated`; absent means `stable`. |
| `stale_after` | Absolute `YYYY-MM-DD` date; stale when today is on/after it. |

Do not invent a credibility score. A `sources` entry requires `resource`
and may include `id`, `title`, `author`, `usage_count`, and
`last_modified`. A sibling `usage_window: {from, to}` frames usage counts;
an entry may override it. Attribute claims with Markdown footnotes whose
labels match stable `sources[].id` values.

`generated.by` and `verified[].by` use these actor forms:

- `<producer>/<version>` for agents and tools.
- `human:<id>` for people; this prefix creates the human-reviewed trust tier.
- `process:<id>` for automated processes.

Consumers derive trust, rather than storing a score:

- no `verified`: unverified;
- only non-human verifiers: machine-confirmed;
- at least one `human:` verifier: human-reviewed.

Treat a bare `verified: {by, at}` mapping as a one-item list. Keep
`generated.at` (content change) distinct from `verified` (confirmation).

## 3. Links and paths

- Use standard Markdown links for directed relationships between concepts.
- Prefer bundle-root absolute paths such as `/architecture/system.md`;
  relative paths are also valid.
- Broken links are tolerated and may represent future knowledge.
- URI/path fields accept absolute URLs, root-relative paths, and relative
  paths.
- Use `references/` conventionally for mirrored source material,
  computation files, executor instructions, and attester code.

When a bundle grows, organize concepts into coherent subdirectories such as
`architecture/`, `risks/`, `operations/`, `security/`, or
`computations/`, using the project's domain rather than creating a flat
directory or one oversized document. Each meaningful directory should have
its own `index.md` for progressive disclosure and `log.md` for local
history. Keep the bundle-root index linked to each subdirectory, and keep
local indexes linked to their concepts.

Use stable bundle-root links for durable cross-directory relationships.
Describe the relationship in surrounding prose because OKF links are
directed but intentionally untyped. When adding or moving a concept, update
the relevant indexes, relationship links, and log entries; do not silently
leave navigation stale. Prefer a new superseding concept and redirects or
deprecation notes over renaming a heavily referenced concept.

## 4. Indexes and logs

`index.md` is a progressive-disclosure directory listing with headings and
Markdown links plus short descriptions. It has no frontmatter, except the
bundle-root `index.md` may contain frontmatter solely for
`okf_version: "0.2"`. Keep links current and include every important
concept or subdirectory.

`log.md` is a flat, newest-first update history. Group entries under
`YYYY-MM-DD` headings and describe creations, updates, and deprecations.

## 5. Attested Computations

An `Attested Computation` is its own concept, linked to by concepts that use
its value. It must define:

- `runtime`: how parameters and execution are interpreted;
- `parameters`: typed named values with `name`, `type`, and `required`;
- `computation`: optional path to sanctioned code, otherwise one body
  `# Computation` fence;
- `executor.resource` and `executor.receipt`: how to run it and the receipt
  fields returned;
- `attester.resource`: deterministic, non-LLM code that checks the receipt.

Agents may supply values only for declared parameters; they must not rewrite
or edit the sanctioned computation. Consumers discover, load, parameterize,
execute, inspect the receipt, run the attester, and refuse or warn on failed
attestation or stale definitions. Runtime receipts and verdicts are not
stored in the bundle unless a project explicitly defines separate records.
Verification of a definition is distinct from per-run attestation.

## 6. Conformance and versioning

Before delivery, check that:

1. Every non-reserved `.md` file has parseable YAML frontmatter.
2. Every concept frontmatter has non-empty `type`.
3. Every present `index.md` and `log.md` follows its reserved-file rules.
4. `okf_version: "0.2"` appears only in the bundle-root `index.md`.
5. Links, sources, diagrams, evidence, and lifecycle status are reviewable.

Optional families may be absent; their absence must not invalidate a bundle.
Consumers must tolerate unknown types, extension keys, broken links, and
missing indexes. OKF v0.2 uses `generated.at` instead of legacy `timestamp`
and `sources` instead of a body `# Citations` list; legacy consumers may
provide those fallbacks when explicitly needed.
