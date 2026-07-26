"""HIPPMEM MCP server — give AI tools long-term associative memory.

Usage:
    pip install hippmem-mcp
    hippmem-mcp                    # stdio transport (for Claude Desktop etc.)
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from hippmem import Engine
from mcp.server.fastmcp import FastMCP


@dataclass
class AppContext:
    engine: Engine


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    engine = Engine.open()
    try:
        yield AppContext(engine=engine)
    finally:
        engine.close()


mcp = FastMCP("hippmem", lifespan=lifespan)


@mcp.tool()
def write_memory(
    content: str,
    content_type: str | None = None,
    importance: float | None = None,
) -> dict:
    """Write a memory to HIPPMEM.

    The engine automatically discovers associations (entity, causal,
    semantic, topic, temporal) with existing memories.

    Args:
        content: The memory text to store.
        content_type: One of Decision, Preference, ProjectKnowledge,
                      TaskState, Correction, Event, Reflection.
        importance: 0.0-1.0 importance hint.
    """
    ctx = mcp.get_context()
    engine = ctx.request_context.lifespan_context.engine
    out = engine.write(content, content_type=content_type, importance=importance)
    return {
        "memory_id": out.memory_id,
        "links_created": out.links_count,
    }


@mcp.tool()
def retrieve_memories(
    query: str,
    top_k: int = 5,
    max_hops: int | None = None,
) -> list[dict]:
    """Retrieve memories via multi-channel associative recall.

    Finds not just keyword matches, but memories connected by entity,
    causal, semantic, and temporal associations. Returns WHY, not just WHAT.

    Args:
        query: Natural-language search query.
        top_k: Maximum number of results.
        max_hops: Graph traversal depth (None = auto).
    """
    ctx = mcp.get_context()
    engine = ctx.request_context.lifespan_context.engine
    results = engine.retrieve(query, top_k=top_k, max_hops=max_hops)
    return [
        {
            "memory_id": r.memory_id,
            "score": round(r.score, 3),
            "content": r.content,
            "content_type": r.content_type,
            "dimensions": r.dimensions,
        }
        for r in results.results
    ]


def main():
    """Entry point. Run with stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
