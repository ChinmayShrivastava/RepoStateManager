def test_single_splits() -> None:
    html_parser = HTMLNodeParser(tags=["h1"])

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
</body>
</html>
    """
            )
        ]
    )
    assert len(splits) == 1
    assert splits[0].text == "This is the Title"
    assert splits[0].metadata["tag"] == "h1"
