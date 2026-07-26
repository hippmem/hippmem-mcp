"""Tests for hippmem-mcp server."""

from hippmem_mcp.server import mcp


class TestServerMetadata:
    def test_server_name(self):
        assert mcp.name == "hippmem"

    def test_version(self):
        from hippmem_mcp import __version__
        assert isinstance(__version__, str)
        assert len(__version__) > 0


class TestToolsRegistration:
    def test_write_memory_tool(self):
        tools = mcp._tool_manager._tools
        assert "write_memory" in tools

    def test_retrieve_memories_tool(self):
        tools = mcp._tool_manager._tools
        assert "retrieve_memories" in tools


class TestWriteMemoryFunctional:
    def test_basic_write(self):
        result = write_memory_standalone("Test memory")
        assert "memory_id" in result
        assert isinstance(result["links_created"], int)

    def test_write_with_content_type(self):
        result = write_memory_standalone("Decide to use Rust", content_type="Decision")
        assert "memory_id" in result

    def test_write_empty_content(self):
        result = write_memory_standalone("")
        assert "memory_id" in result

    def test_write_long_content(self):
        long_text = "The user prefers Rust for development. " * 50
        result = write_memory_standalone(long_text)
        assert "memory_id" in result


class TestRetrieveMemoriesFunctional:
    def test_retrieve_after_write(self):
        write_memory_standalone("The user prefers Rust for development.")
        results = retrieve_memories_standalone("What does the user prefer?")
        assert len(results) > 0
        r = results[0]
        assert "memory_id" in r
        assert "score" in r
        assert "content" in r
        assert "dimensions" in r

    def test_retrieve_with_top_k(self):
        for i in range(5):
            write_memory_standalone(f"Memory {i}: test content for retrieval tuning.")
        results = retrieve_memories_standalone("test content", top_k=3)
        assert len(results) <= 3

    def test_retrieve_no_match(self):
        results = retrieve_memories_standalone("xyzzy_nonexistent_query_12345")
        # Should return results (possibly low-scoring), not throw
        assert isinstance(results, list)


class TestToolSignature:
    def test_write_memory_parameters(self):
        fn = mcp._tool_manager._tools["write_memory"].fn
        import inspect
        sig = inspect.signature(fn)
        params = list(sig.parameters.keys())
        assert "content" in params

    def test_retrieve_memories_parameters(self):
        fn = mcp._tool_manager._tools["retrieve_memories"].fn
        import inspect
        sig = inspect.signature(fn)
        params = list(sig.parameters.keys())
        assert "query" in params
        assert "top_k" in params


# ---------------------------------------------------------------------------
# Standalone helpers that bypass FastMCP context for functional testing
# ---------------------------------------------------------------------------

def write_memory_standalone(content, content_type=None, importance=None):
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
        import os
        import tempfile

        from hippmem import Engine

        tmpdir = tempfile.mkdtemp()
        _test_engine = Engine.open(os.path.join(tmpdir, "test.redb"))
    return _test_engine
