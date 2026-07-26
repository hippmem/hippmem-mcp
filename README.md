# hippmem-mcp

**MCP server for [HIPPMEM](https://github.com/hippmem/hippmem) — give AI tools long-term associative memory.**

[![CI](https://github.com/hippmem/hippmem-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/hippmem/hippmem-mcp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/hippmem-mcp.svg)](https://pypi.org/project/hippmem-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/hippmem-mcp.svg)](https://pypi.org/project/hippmem-mcp/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## What is HIPPMEM?

[HIPPMEM](https://github.com/hippmem/hippmem) is a native associative memory engine for AI agents, written in Rust. Instead of storing text chunks and searching them by vector similarity, it discovers associations between memories at write time and retrieves them via spreading activation at read time — so the AI recalls not just *what* was said, but *how things connect* and *why*.

It runs fully offline with a deterministic fallback backend.

## What is hippmem-mcp?

hippmem-mcp wraps HIPPMEM as a [Model Context Protocol](https://modelcontextprotocol.io/) server. Configure it once in Claude Desktop (or any MCP-compatible tool), and your AI assistant gains persistent, associative memory across sessions — no API key required.

```
AI Tool (Claude Desktop / VS Code / ...)
        │  MCP protocol (stdio)
        ▼
  hippmem-mcp
        │  Python bindings
        ▼
  hippmem Engine (Rust)
        │
        ▼
  Local storage (redb + Tantivy + HNSW)
```

## Key Features

- **Zero config** — `pip install` then one JSON block in your MCP client configuration; deterministic fallback backend works offline
- **Write-time association discovery** — entities, topics, goals, causal links extracted and scored automatically
- **Spreading activation retrieval** — multi-channel seed recall (BM25 + entity + semantic + temporal + topic) fused by RRF
- **Graph evolution** — co-activated connections strengthen (Hebbian learning); stale edges decay
- **Explanation traces** — every result shows *why* it was recalled via `dimensions` and `matched_dimensions`
- **Single-file storage** — one redb file + Tantivy full-text index + HNSW vector index; no external database

## Install

```bash
pip install hippmem-mcp
```

Requires Python ≥ 3.11.

## Configure

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hippmem": {
      "command": "python",
      "args": ["-m", "hippmem_mcp.server"]
    }
  }
}
```

Or use the entry point:

```json
{
  "mcpServers": {
    "hippmem": {
      "command": "hippmem-mcp"
    }
  }
}
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `HIPPMEM_EMBEDDING_PROVIDER` | *(empty = deterministic)* | Embedding backend: `openai-compatible` or leave empty for offline fallback |
| `HIPPMEM_EMBEDDING_BASE_URL` | `https://api.openai.com/v1` | API endpoint when using remote embeddings |
| `HIPPMEM_EMBEDDING_MODEL` | `text-embedding-3-small` | Model name for embeddings |
| `OPENAI_API_KEY` | *(none)* | API key for OpenAI-compatible embedding services |

The deterministic fallback backend requires no API key, no GPU, and no network connection.

### Claude Code

Claude Code supports MCP natively. Add to your Claude Code MCP config (`.claude/mcp.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "hippmem": {
      "command": "hippmem-mcp"
    }
  }
}
```

Then in any Claude Code session:

```
Use retrieve_memories to check what we know about this project before starting.
```

### Other MCP Clients

hippmem-mcp speaks standard MCP over stdio. Configure any [MCP-compatible client](https://modelcontextprotocol.io/clients) the same way — point the `command` to `hippmem-mcp` or `python -m hippmem_mcp.server`.

## Tools

| Tool | Description |
|------|-------------|
| `write_memory` | Write a memory. The engine automatically discovers associations with existing memories. Supports `content_type` (Decision, Preference, ProjectKnowledge, TaskState, Correction, Event, Reflection) and `importance` (0.0–1.0). |
| `retrieve_memories` | Cross-session associative recall via multi-channel seed retrieval + spreading activation. Returns scored results with `dimensions` explaining *why* each memory was recalled. Supports `top_k` and `max_hops` tuning. |

## Development

```bash
git clone https://github.com/hippmem/hippmem-mcp.git
cd hippmem-mcp
pip install -e ".[dev]"
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for commit conventions, PR workflow, and DCO requirements.

## Documentation

- [Best Practices](docs/best-practices.md) — when to write, how to query, prompt templates
- [HIPPMEM main project](https://github.com/hippmem/hippmem) — engine architecture, concepts, and API reference
- [MCP specification](https://modelcontextprotocol.io/) — Model Context Protocol
- [Changelog](CHANGELOG.md)
- [Security policy](SECURITY.md)

## License

Apache 2.0. See [LICENSE](LICENSE) and [COPYRIGHT](COPYRIGHT).

The underlying HIPPMEM engine (`hippmem`) is AGPL-3.0-only. A commercial license is available — contact hippmem@gmail.com.
