# Changelog

All notable changes to this project are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.0] — unreleased

### Added
- Initial release: MCP server for HIPPMEM associative memory.
- `write_memory` tool — write a memory; engine auto-discovers associations (entity, causal, semantic, topic, temporal).
- `retrieve_memories` tool — multi-channel associative recall via spreading activation with explanation traces.
- FastMCP high-level API with lifespan management.
- Stdio transport for Claude Desktop and other MCP-compatible tools.
- Deterministic fallback backend — zero-config, no API key, no network required.

[0.1.0]: https://github.com/hippmem/hippmem-mcp/releases/tag/v0.1.0
