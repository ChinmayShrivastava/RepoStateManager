def test_html_code_splitter() -> None:
    """Test case for code splitting using typescript."""
    if "CI" in os.environ:
        return

    code_splitter = CodeSplitter(
        language="html", chunk_lines=4, chunk_lines_overlap=1, max_chars=50
    )

    text = """\
<!DOCTYPE html>
<html>
<head>
    <title>My Example Page</title>
</head>
<body>
    <h1>Welcome to My Example Page</h1>
    <p>This is a basic HTML page example.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>
    <img src="https://example.com/image.jpg" alt="Example Image">
</body>
</html>"""

    chunks = code_splitter.split_text(text)
    assert chunks[0].startswith("<!DOCTYPE html>")
    assert chunks[1].startswith("<html>")
    assert chunks[2].startswith("<head>")
