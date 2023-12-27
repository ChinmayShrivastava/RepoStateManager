def test_start_end_char_idx() -> None:
    text = """\
def foo():
    print("bar")

def baz():
    print("bbq")"""
    document = Document(text=text)
    code_splitter = CodeSplitter(
        language="python", chunk_lines=4, chunk_lines_overlap=1, max_chars=30
    )
    nodes: List[TextNode] = code_splitter.get_nodes_from_documents([document])
    for node in nodes:
        assert node.start_char_idx is not None
        assert node.end_char_idx is not None
        assert node.end_char_idx - node.start_char_idx == len(
            node.get_content(metadata_mode=MetadataMode.NONE)
        )
