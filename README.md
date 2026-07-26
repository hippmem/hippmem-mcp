# hippmem-mcp

**MCP server for [HIPPMEM](https://github.com/hippmem/hippmem) — give AI tools long-term associative memory.**

[![CI](https://github.com/hippmem/hippmem-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/hippmem/hippmem-mcp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/hippmem-mcp.svg)](https://pypi.org/project/hippmem-mcp/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

## What is this?

hippmem-mcp is a [Model Context Protocol](https://modelcontextprotocol.io/) server
that wraps HIPPMEM. Configure it once in Claude Desktop (or any MCP-compatible
tool), and your AI assistant gains persistent, associative memory across sessions.

## Install

```bash
pip install hippmem-mcp
```

## Configure Claude Desktop

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

## Tools

| Tool | Description |
|------|-------------|
| `write_memory` | Write a memory. Engine auto-discovers associations. |
| `retrieve_memories` | Cross-session associative recall. Finds WHY, not just WHAT. |

## License

Apache 2.0 (D8). See [LICENSE](LICENSE).
