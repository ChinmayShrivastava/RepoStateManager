def test_typescript_code_splitter() -> None:
    """Test case for code splitting using typescript."""
    if "CI" in os.environ:
        return

    code_splitter = CodeSplitter(
        language="typescript", chunk_lines=4, chunk_lines_overlap=1, max_chars=50
    )

    text = """\
function foo() {
    console.log("bar");
}

function baz() {
    console.log("bbq");
}"""

    chunks = code_splitter.split_text(text)
    assert chunks[0].startswith("function foo()")
    assert chunks[1].startswith("function baz()")
