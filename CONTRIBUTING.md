# Contributing to hippmem-mcp

Thanks for your interest in contributing to hippmem-mcp! This document explains how to report issues, submit changes, and follow the project conventions.

## Reporting Bugs

- Open an issue at <https://github.com/hippmem/hippmem-mcp/issues>.
- Include the hippmem-mcp version (`pip show hippmem-mcp`), Python version (`python --version`), OS, and a minimal reproduction.
- For security vulnerabilities, do **not** open a public issue — see [SECURITY.md](SECURITY.md).

## Submitting a Pull Request

1. Fork the repository.
2. Create a branch from `main`:
   ```bash
   git checkout -b my-fix
   ```
3. Make your changes. Keep PRs focused — one logical change per PR.
4. Ensure tests pass (see [Development Setup](#development-setup)).
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat: add new tool for batch memory retrieval
   fix: handle empty query gracefully
   docs: update configuration examples
   refactor: extract lifespan into separate module
   test: add edge case tests for write_memory
   chore: bump dependencies
   ```
6. Open a PR against `main` and describe the change, the motivation, and any trade-offs.

## Development Setup

```bash
git clone https://github.com/hippmem/hippmem-mcp.git
cd hippmem-mcp
pip install -e ".[dev]"
pytest
```

Requires Python ≥ 3.11. No GPU, API key, or network connection is needed — the deterministic fallback backend provides full offline coverage.

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) with the idioms visible in the existing code.
- Use type annotations on all public function signatures.
- Code comments and documentation are in English.
- Match the surrounding code's naming, density, and idioms.
- Avoid `assert` for runtime validation — raise explicit exceptions.

## Commit Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short imperative summary>

<optional body explaining why and what trade-offs>

<optional footer>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`.

## License

hippmem-mcp is licensed under Apache 2.0 (see [COPYRIGHT](COPYRIGHT)). By contributing, you agree that your contributions will be licensed under the same terms.

## DCO (Developer Certificate of Origin)

All commits must include a `Signed-off-by:` line certifying that you have the right to submit the contribution:

```
feat: add new tool for batch memory retrieval

Signed-off-by: Your Name <you@example.com>
```

Add the line manually to your commit message, or use `git commit -s` to append it automatically. By signing off, you attest to the [Developer Certificate of Origin](https://developercertificate.org/) v1.1.
