def documents() -> List[Document]:
    """Get documents."""
    doc_text1 = "Hello world!"
    doc_text2 = "This is the first test. answer is A"
    doc_text3 = "This is the second test. answer is B"
    doc_text4 = "This is the third test. answer is C"

    return [
        Document(text=doc_text1),
        Document(text=doc_text2),
        Document(text=doc_text3),
        Document(text=doc_text4),
    ]
