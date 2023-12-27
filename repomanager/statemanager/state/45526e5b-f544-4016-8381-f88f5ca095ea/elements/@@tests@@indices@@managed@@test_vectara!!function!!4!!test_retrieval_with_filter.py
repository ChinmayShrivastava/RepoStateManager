def test_retrieval_with_filter() -> None:
    docs = get_docs()
    try:
        index = VectaraIndex.from_documents(docs)
    except ValueError:
        pytest.skip("Missing Vectara credentials, skipping test")

    assert isinstance(index, VectaraIndex)
    qe = index.as_retriever(similarity_top_k=1, filter="doc.test_num = '1'")
    res = qe.retrieve("how will I look?")
    assert len(res) == 1
    assert res[0].node.get_content() == docs[0].text

    remove_docs(index, index.doc_ids)
