# pre-commit-hooks

A collection of useful pre-commit hooks for code quality.

## Hooks

### `no-emoji`

Automatically removes emoji characters from source code files with smart space handling.

**Why?** Emoji in code can cause issues with:
- Terminal rendering
- Cross-platform compatibility
- Professional code standards
- Version control diffs

**How it works:**

The hook automatically removes emoji from files using smart space removal logic:

1. **Priority 1:** Remove emoji + trailing space(s) after it
2. **Priority 2:** Remove emoji + leading space(s) before it (if no trailing)
3. **Priority 3:** Remove emoji only (if no surrounding spaces)

**Examples:**

```python
# Before
print("Success 😊 here")  # Emoji with trailing space

# After (automatic fix)
print("Success here")  # Emoji + trailing space removed
```

```python
# Before
value = test😊data  # No spaces around emoji

# After (automatic fix)
value = testdata  # Only emoji removed
```

**Basic usage:**

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/nikolay-e/pre-commit-hooks
    rev: v2.0.0
    hooks:
      - id: no-emoji
```

**Whitelist specific emoji:**

You can allow specific emoji (useful for TODO markers, status indicators, etc.):

```yaml
repos:
  - repo: https://github.com/nikolay-e/pre-commit-hooks
    rev: v2.0.0
    hooks:
      - id: no-emoji
        args: ['--allow-emoji=✅', '--allow-emoji=❌']
```

Or use emoji shortcodes:

```yaml
      - id: no-emoji
        args: ['--allow-emoji=:check_mark:', '--allow-emoji=:x:']
```

**Options:**

- `--allow-emoji EMOJI` / `-a EMOJI`: Allow specific emoji (can be used multiple times)
  - Accepts emoji characters: `--allow-emoji=✅`
  - Accepts shortcodes: `--allow-emoji=:rocket:`

**Supported emoji:**

This hook uses the `emoji` library (v2.15.0+) which supports:
- All standard Unicode emoji (Unicode 16.0)
- ZWJ sequences (combined emoji like 👨‍👩‍👧‍👦)
- Skin tone modifiers (e.g., 👋🏻, 👋🏿)
- Flag emoji (Regional Indicators like 🇺🇸, 🇷🇺)
- Variation selectors and emoji presentations

## Installation

### As a pre-commit hook (recommended)

```yaml
repos:
  - repo: https://github.com/nikolay-e/pre-commit-hooks
    rev: v2.0.0
    hooks:
      - id: no-emoji
```

Pre-commit will automatically install the required dependencies (`emoji>=2.15.0`).

### Standalone

```bash
pip install git+https://github.com/nikolay-e/pre-commit-hooks
no-emoji file1.py file2.js
```

**Note:** The hook requires Python 3.8+ and the `emoji` library (installed automatically).

## Development

### Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e .  # Installs hook with emoji dependency
pip install pytest  # For running tests
```

### Run tests

```bash
pytest tests/ -v
```

### Test the hook locally

```bash
# Auto-fix a file
python hooks/no_emoji.py test_file.py

# With whitelist
python hooks/no_emoji.py --allow-emoji=✅ test_file.py
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Author

Nikolay Eremeev
