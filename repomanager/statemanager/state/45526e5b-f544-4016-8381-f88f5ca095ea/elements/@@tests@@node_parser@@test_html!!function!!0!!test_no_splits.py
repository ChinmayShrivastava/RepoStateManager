def test_no_splits() -> None:
    html_parser = HTMLNodeParser(tags=["h2"])

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
    print(splits)
    assert len(splits) == 0
