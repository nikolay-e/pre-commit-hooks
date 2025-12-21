# pre-commit-hooks

> Extends [../CLAUDE.md](../CLAUDE.md)

Collection of pre-commit hooks for code quality.

## Hooks

### `no-emoji`

Removes emoji from source code with smart space handling.

```yaml
repos:
  - repo: https://github.com/nikolay-e/pre-commit-hooks
    rev: v2.0.0
    hooks:
      - id: no-emoji
        args: ["--allow-emoji=✅", "--allow-emoji=❌"] # whitelist
```

**Space removal priority:**

1. Emoji + trailing space
2. Emoji + leading space
3. Emoji only

**Supports:** Unicode 16.0, ZWJ sequences, skin tones, flags.

## Development

```bash
pip install -e .
pip install pytest pre-commit
pre-commit install

# Test
pytest tests/ -v
python hooks/no_emoji.py test_file.py
```

## Structure

```
pre-commit-hooks/
├── hooks/no_emoji.py    # Main hook
├── tests/               # Pytest tests
└── .pre-commit-config.yaml
```
