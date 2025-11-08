import tempfile
from pathlib import Path

from hooks.no_emoji import fix_file, main, parse_whitelist, remove_emoji_with_spaces


def test_parse_whitelist_with_characters():
    """Test whitelist parsing with emoji characters."""
    whitelist = parse_whitelist(['✅', '🚀', '❌'])
    assert whitelist == {'✅', '🚀', '❌'}


def test_parse_whitelist_with_shortcodes():
    """Test whitelist parsing with shortcodes."""
    whitelist = parse_whitelist([':check_mark_button:', ':rocket:'])
    assert '✅' in whitelist
    assert '🚀' in whitelist


def test_parse_whitelist_mixed():
    """Test whitelist parsing with mixed formats."""
    whitelist = parse_whitelist(['✅', ':rocket:'])
    assert '✅' in whitelist
    assert '🚀' in whitelist or ':rocket:' in whitelist


def test_remove_emoji_with_trailing_space():
    """Test removing emoji with trailing space (priority 1)."""
    text = "Hello 😊 world"
    result = remove_emoji_with_spaces(text, "😊", 6, 7)
    assert result == "Hello world"


def test_remove_emoji_with_multiple_trailing_spaces():
    """Test removing emoji with multiple trailing spaces."""
    text = "Hello 😊  world"
    result = remove_emoji_with_spaces(text, "😊", 6, 7)
    assert result == "Hello world"


def test_remove_emoji_with_leading_space():
    """Test removing emoji with leading space when no trailing (priority 2)."""
    text = "Hello 😊world"
    result = remove_emoji_with_spaces(text, "😊", 6, 7)
    assert result == "Helloworld"


def test_remove_emoji_only():
    """Test removing emoji without spaces (priority 3)."""
    text = "Hello😊world"
    result = remove_emoji_with_spaces(text, "😊", 5, 6)
    assert result == "Helloworld"


def test_remove_emoji_at_start():
    """Test removing emoji at start of text."""
    text = "😊 Hello"
    result = remove_emoji_with_spaces(text, "😊", 0, 1)
    assert result == "Hello"


def test_remove_emoji_at_end():
    """Test removing emoji at end of text."""
    text = "Hello 😊"
    result = remove_emoji_with_spaces(text, "😊", 6, 7)
    assert result == "Hello"


def test_fix_file_with_trailing_space():
    """Test fixing file removes emoji with trailing space."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("# Comment 😊 here\n")
        f.write('print("test")\n')
        filepath = Path(f.name)

    try:
        result = fix_file(filepath, set())
        assert result is True

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert content == "# Comment here\n" + 'print("test")\n'
    finally:
        filepath.unlink()


def test_fix_file_with_leading_space():
    """Test fixing file removes emoji with leading space when no trailing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("# Comment 😊here\n")
        filepath = Path(f.name)

    try:
        result = fix_file(filepath, set())
        assert result is True

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert content == "# Commenthere\n"
    finally:
        filepath.unlink()


def test_fix_file_emoji_only():
    """Test fixing file removes emoji without spaces."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("test😊value\n")
        filepath = Path(f.name)

    try:
        result = fix_file(filepath, set())
        assert result is True

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert content == "testvalue\n"
    finally:
        filepath.unlink()


def test_fix_file_multiple_emoji():
    """Test fixing file with multiple emoji on same line."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("Success ✅ and party 🎉 time\n")
        filepath = Path(f.name)

    try:
        result = fix_file(filepath, set())
        assert result is True

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert content == "Success and party time\n"
    finally:
        filepath.unlink()


def test_fix_file_no_emoji():
    """Test fixing file without emoji returns False."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("# Clean comment\n")
        f.write('print("test")\n')
        filepath = Path(f.name)

    try:
        result = fix_file(filepath, set())
        assert result is False
    finally:
        filepath.unlink()


def test_fix_file_with_whitelist():
    """Test whitelist preserves specific emoji."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("# TODO ✅ done, party 🎉 removed\n")
        filepath = Path(f.name)

    try:
        whitelist = {'✅'}
        result = fix_file(filepath, whitelist)
        assert result is True

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert '✅' in content
        assert '🎉' not in content
        assert content == "# TODO ✅ done, party removed\n"
    finally:
        filepath.unlink()


def test_fix_file_binary():
    """Test binary files don't crash."""
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".bin", delete=False) as f:
        f.write(b"\x00\x01\x02\x03")
        filepath = Path(f.name)

    try:
        result = fix_file(filepath, set())
        assert result is False
    finally:
        filepath.unlink()


def test_fix_file_complex_emoji_zwj():
    """Test fixing file with ZWJ sequences (family emoji)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("# Family 👨‍👩‍👧‍👦 test\n")
        filepath = Path(f.name)

    try:
        result = fix_file(filepath, set())
        assert result is True

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert '👨‍👩‍👧‍👦' not in content
        assert content == "# Family test\n"
    finally:
        filepath.unlink()


def test_fix_file_complex_emoji_skin_tone():
    """Test fixing file with skin tone modifiers."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("# Wave 👋🏻 bye\n")
        filepath = Path(f.name)

    try:
        result = fix_file(filepath, set())
        assert result is True

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert '👋🏻' not in content
        assert content == "# Wave bye\n"
    finally:
        filepath.unlink()


def test_fix_file_complex_emoji_flag():
    """Test fixing file with flag emoji (Regional Indicators)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("# USA 🇺🇸 flag\n")
        filepath = Path(f.name)

    try:
        result = fix_file(filepath, set())
        assert result is True

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert '🇺🇸' not in content
        assert content == "# USA flag\n"
    finally:
        filepath.unlink()


def test_main_no_files():
    """Test main with no files returns 0."""
    result = main([])
    assert result == 0


def test_main_with_clean_file():
    """Test main with clean file returns 0."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write('print("clean")\n')
        filepath = Path(f.name)

    try:
        result = main([str(filepath)])
        assert result == 0
    finally:
        filepath.unlink()


def test_main_with_emoji_file():
    """Test main with emoji file returns 1 and fixes file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write('print("test 🔥 here")\n')
        filepath = Path(f.name)

    try:
        result = main([str(filepath)])
        assert result == 1

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert '🔥' not in content
        assert content == 'print("test here")\n'
    finally:
        filepath.unlink()


def test_main_with_whitelist():
    """Test main respects whitelist."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write('# TODO ✅ done\n')
        filepath = Path(f.name)

    try:
        result = main(['--allow-emoji', '✅', str(filepath)])
        assert result == 0

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert '✅' in content
    finally:
        filepath.unlink()


def test_main_with_whitelist_shortcode():
    """Test main respects whitelist with shortcodes."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write('# Rocket 🚀 test\n')
        filepath = Path(f.name)

    try:
        result = main(['--allow-emoji', ':rocket:', str(filepath)])
        assert result == 0

        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        assert '🚀' in content
    finally:
        filepath.unlink()


def test_main_multiple_files():
    """Test main with multiple files."""
    files = []
    try:
        for i in range(3):
            f = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8")
            if i == 0:
                f.write('print("clean")\n')
            else:
                f.write(f'print("emoji 😊 {i}")\n')
            f.close()
            files.append(Path(f.name))

        result = main([str(f) for f in files])
        assert result == 1

        with open(files[0], encoding="utf-8") as f:
            assert '😊' not in f.read()

        with open(files[1], encoding="utf-8") as f:
            assert '😊' not in f.read()
    finally:
        for filepath in files:
            filepath.unlink()
