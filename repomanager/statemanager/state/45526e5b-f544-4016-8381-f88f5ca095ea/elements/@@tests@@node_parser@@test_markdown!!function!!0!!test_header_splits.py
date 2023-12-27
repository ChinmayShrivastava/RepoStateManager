def test_header_splits() -> None:
    markdown_parser = MarkdownNodeParser()

    splits = markdown_parser.get_nodes_from_documents(
        [
            Document(
                text="""# Main Header

Header 1 content

# Header 2
Header 2 content
    """
            )
        ]
    )
    assert len(splits) == 2
    assert splits[0].metadata == {"Header 1": "Main Header"}
    assert splits[1].metadata == {"Header 1": "Header 2"}
    assert splits[0].text == "Main Header\n\nHeader 1 content"
    assert splits[1].text == "Header 2\nHeader 2 content"
