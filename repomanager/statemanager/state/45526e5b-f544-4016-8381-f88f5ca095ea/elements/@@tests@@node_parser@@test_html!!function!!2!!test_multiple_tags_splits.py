def test_multiple_tags_splits() -> None:
    html_parser = HTMLNodeParser(tags=["h2", "p"])

    splits = html_parser.get_nodes_from_documents(
        [
            Document(
                text="""
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1 id="title">This is the Title</h1>
    <p>This is a paragraph of text.</p>
    <div>
        <h2 id="section1">Section 1</h2>
    </div>
    <p>This is the first paragraph.</p>
</body>
</html>
    """
            )
        ]
    )
    assert len(splits) == 3
    assert splits[0].text == "This is a paragraph of text."
    assert splits[1].text == "Section 1"
    assert splits[2].text == "This is the first paragraph."
    assert splits[0].metadata["tag"] == "p"
    assert splits[1].metadata["tag"] == "h2"
    assert splits[2].metadata["tag"] == "p"
