"""Tests for hippmem-mcp server."""

import pytest
from hippmem_mcp.server import mcp


def test_server_name():
    assert mcp.name == "hippmem"


def test_write_memory_tool():
    """write_memory is a registered tool."""
    tools = mcp._tool_manager._tools
    assert "write_memory" in tools


def test_retrieve_memories_tool():
    """retrieve_memories is a registered tool."""
    tools = mcp._tool_manager._tools
    assert "retrieve_memories" in tools


def test_write_memory_functional():
    """write_memory returns expected fields."""
    result = write_memory_standalone("Test memory")
    assert "memory_id" in result
    assert "links_created" in result


def test_retrieve_memories_functional():
    """retrieve_memories returns results after writing."""
    write_memory_standalone("The user prefers Rust for development.")
    results = retrieve_memories_standalone("What does the user prefer?")
    assert len(results) > 0
    r = results[0]
    assert "memory_id" in r
    assert "score" in r
    assert "content" in r
    assert "dimensions" in r


# Standalone helpers that bypass FastMCP context for testing
def write_memory_standalone(content, content_type=None, importance=None):
    from hippmem import Engine
    import tempfile, os
    # Use a module-level engine for test isolation
    e = _get_test_engine()
    out = e.write(content, content_type=content_type, importance=importance)
    return {"memory_id": out.memory_id, "links_created": out.links_count}


def retrieve_memories_standalone(query, top_k=5):
    e = _get_test_engine()
    results = e.retrieve(query, top_k=top_k)
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


_test_engine = None


def _get_test_engine():
    global _test_engine
    if _test_engine is None:
        from hippmem import Engine
        import tempfile, os
        tmpdir = tempfile.mkdtemp()
        _test_engine = Engine.open(os.path.join(tmpdir, "test.redb"))
    return _test_engine
