---
name: mermaid-diagrams
description: Author and validate Mermaid diagrams embedded in project documentation. Use whenever docs/ includes architecture, sequence, flow, state, deployment, data-flow, or dependency diagrams.
license: MIT
---

# Mermaid diagrams

Use fenced `mermaid` blocks with stable labels, a short caption, and a
sentence explaining the diagram's purpose. Keep diagrams readable and show
trust boundaries, external systems, data direction, and failure paths when
relevant.

Validate every diagram with the open-source Mermaid CLI before delivery:

```sh
npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg
```

`mmdc` is the equivalent executable when it is already installed. Use a
temporary directory for extracted diagram sources and generated artifacts
unless the project explicitly versions rendered diagrams. Report the exact
validation command and result in the document or handoff; do not treat
syntax highlighting as validation.
