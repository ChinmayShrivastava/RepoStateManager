def text_node() -> TextNode:
    return TextNode(
        text="hello world",
        metadata={"foo": "bar"},
        embedding=[0.1, 0.2, 0.3],
    )
