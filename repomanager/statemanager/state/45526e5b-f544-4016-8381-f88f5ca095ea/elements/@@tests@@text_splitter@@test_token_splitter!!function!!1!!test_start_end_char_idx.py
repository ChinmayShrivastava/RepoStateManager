def test_start_end_char_idx() -> None:
    document = Document(text="foo bar hello world baz bbq")
    text_splitter = TokenTextSplitter(chunk_size=3, chunk_overlap=1)
    nodes: List[TextNode] = text_splitter.get_nodes_from_documents([document])
    for node in nodes:
        assert node.start_char_idx is not None
        assert node.end_char_idx is not None
        assert node.end_char_idx - node.start_char_idx == len(
            node.get_content(metadata_mode=MetadataMode.NONE)
        )
