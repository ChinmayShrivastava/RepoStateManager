def documents() -> List[Document]:
    """Get documents."""
    # NOTE: one document for now
    # NOTE: in this unit test, document text == triplets
    doc_text = "(foo, is, bar)\n" "(hello, is not, world)\n" "(Jane, is mother of, Bob)"
    return [Document(text=doc_text)]
