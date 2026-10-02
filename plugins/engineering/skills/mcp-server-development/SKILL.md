---
name: mcp-server-development
description: MCP server and client development guidance sourced from the anthropics/skills mcp-builder reference docs (vendored in references/). Use whenever designing, building, adding, modifying, reviewing, testing, or evaluating MCP servers, clients, or tools, including tool names, descriptions, annotations, input validation, response formats, pagination, errors, transports (Streamable HTTP or stdio), auth, and MCP evaluations, in Python, TypeScript/Node, or C#/.NET.
---

# MCP server development

The knowledge for this skill comes from the `references/` directory, which contains unmodified copies of the
[anthropics/skills `mcp-builder` reference docs](https://github.com/anthropics/skills/tree/main/skills/mcp-builder/reference)
(Apache 2.0; see `SOURCE.md`). Treat those files as the authoritative guidance. This file only routes you to the right
reference and maps its concepts onto other stacks; it does not replace them.

## Which reference to read

Read the relevant reference before making changes. Do not rely on memory.

| Task | Read |
| ---- | ---- |
| Any tool design or change: naming, descriptions, annotations, response formats, pagination, transport choice, security, errors, testing, docs | `references/mcp_best_practices.md` (always read first) |
| Designing evaluation questions that test whether an LLM can use the server's tools effectively | `references/evaluation.md` |
| Python server (FastMCP, Pydantic) | `references/python_mcp_server.md` |
| TypeScript/Node server (MCP TypeScript SDK, Zod) | `references/node_mcp_server.md` |
| Any other language, such as C#/.NET | Both language guides for patterns and quality checklists, translated using the mapping below |

Follow the repository's existing language and SDK. Do not introduce a second language or SDK just because a reference uses it.

## Before changing a repository

1. Find the MCP SDK and its version in the project's dependency manifest. Verify version-specific APIs against the installed
   package or its documentation before relying on them.
2. Locate where tools are registered, how the transport is configured, and where existing tests live.
3. Identify the existing tool contracts that clients may depend on.

## Mapping the references to C#/.NET

For the official C# SDK (`ModelContextProtocol` / `ModelContextProtocol.AspNetCore`), concepts from the references map as
follows. Confirm member names against the installed version.

| Reference concept | C# |
| ----------------- | -- |
| Tool registration (`@mcp.tool`, `server.registerTool`) | `[McpServerTool]` method on a class registered with `.WithTools<T>()` (or `[McpServerToolType]` plus assembly scanning) |
| Tool / parameter descriptions (docstrings, Zod `.describe`) | `[Description]` on the method and on each parameter |
| `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`, `title` | `McpServerToolAttribute` properties `ReadOnly`, `Destructive`, `Idempotent`, `OpenWorld`, `Title` |
| Structured output / output schema | `UseStructuredContent` and `OutputSchemaType` on `McpServerToolAttribute`; returned records serialized with `System.Text.Json` |
| Input schema validation (Pydantic/Zod) | Explicit validation at the tool boundary, plus precise parameter `[Description]`s that state formats and limits |
| Tool errors reported in results (`isError: true`) | Return tool-level failures as results with actionable messages; reserve protocol-level `McpException` errors for protocol or transport failures |
| Async/await best practices | `async` methods that accept and pass through a `CancellationToken` |
| Streamable HTTP transport | `.WithHttpTransport()` and `app.MapMcp(...)`; clients use `HttpClientTransport` with `HttpTransportMode.StreamableHttp` |
| stdio transport | `.WithStdioServerTransport()`; send logs to stderr, never stdout |

## Applying the references to existing servers

- **Tool naming.** Apply the references' `snake_case`, service-prefixed naming (`{service}_{action}_{resource}`) to new tools.
  Renaming an existing tool is a breaking change for clients, so flag the mismatch and rename only when explicitly asked.
- **Response formats and pagination.** Apply this guidance to new tools that return data or lists. Do not retrofit existing
  tool contracts unless requested.
- **Security.** Follow the references' input-validation, auth, error-exposure, and DNS-rebinding guidance. Never log or print
  tokens, authorization headers, API keys, or connection strings.
- **Testing.** Add focused tests in the repository's existing test framework for valid and invalid inputs and for changed
  behavior. For transport or client changes, also verify against a running server, for example with the MCP Inspector
  (`npx @modelcontextprotocol/inspector`).
- **Evaluations.** Use `references/evaluation.md` to design evaluation questions. Its harness (`scripts/evaluation.py`) is
  not vendored, and it sends tool data to an external model API using an API key. Do not install or run it without explicit
  user approval.
- Keep infrastructure and deployment changes out of scope unless explicitly requested.
