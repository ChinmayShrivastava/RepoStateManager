def test_neighbor_tags_splits() -> None:
    html_parser = HTMLNodeParser(tags=["p"])

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
    <p>This is the first paragraph.</p>
    <p>This is the second paragraph</p>
</body>
</html>
    """
            )
        ]
    )
    assert len(splits) == 1
