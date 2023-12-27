def test_header_metadata() -> None:
    markdown_parser = MarkdownNodeParser()

    splits = markdown_parser.get_nodes_from_documents(
        [
            Document(
                text="""# Main Header
Content
## Sub-header
Content
### Sub-sub header
Content
# New title
    """
            )
        ]
    )
    assert len(splits) == 4
    assert splits[0].metadata == {"Header 1": "Main Header"}
    assert splits[1].metadata == {"Header 1": "Main Header", "Header 2": "Sub-header"}
    assert splits[2].metadata == {
        "Header 1": "Main Header",
        "Header 2": "Sub-header",
        "Header 3": "Sub-sub header",
    }
    assert splits[3].metadata == {"Header 1": "New title"}
