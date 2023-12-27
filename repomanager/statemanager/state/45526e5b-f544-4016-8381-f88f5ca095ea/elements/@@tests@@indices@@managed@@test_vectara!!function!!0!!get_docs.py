def get_docs() -> List[Document]:
    inputs = [
        {
            "text": "This is test text for Vectara integration with LlamaIndex",
            "metadata": {"test_num": "1"},
        },
        {
            "text": "And now for something completely different",
            "metadata": {"test_num": "2"},
        },
        {
            "text": "when 900 years you will be, look as good you will not",
            "metadata": {"test_num": "3"},
        },
        {
            "text": "when 850 years you will be, look as good you will not",
            "metadata": {"test_num": "4"},
        },
    ]
    docs: List[Document] = []
    for inp in inputs:
        doc = Document(
            text=str(inp["text"]),
            metadata=inp["metadata"],  # type: ignore
        )
        docs.append(doc)
    return docs
