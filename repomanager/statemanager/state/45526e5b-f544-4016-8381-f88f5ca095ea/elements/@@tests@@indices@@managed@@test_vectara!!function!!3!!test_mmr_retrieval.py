def test_mmr_retrieval() -> None:
    docs = get_docs()
    try:
        index = VectaraIndex.from_documents(docs)
    except ValueError:
        pytest.skip("Missing Vectara credentials, skipping test")

    assert isinstance(index, VectaraIndex)

    # test with diversity bias = 0
    qe = index.as_retriever(
        similarity_top_k=2,
        n_sentences_before=0,
        n_sentences_after=0,
        vectara_query_mode="mmr",
        mmr_k=10,
        mmr_diversity_bias=0.0,
    )
    res = qe.retrieve("how will I look?")
    assert len(res) == 2
    assert res[0].node.get_content() == docs[2].text
    assert res[1].node.get_content() == docs[3].text

    # test with diversity bias = 1
    qe = index.as_retriever(
        similarity_top_k=2,
        n_sentences_before=0,
        n_sentences_after=0,
        vectara_query_mode="mmr",
        mmr_k=10,
        mmr_diversity_bias=1.0,
    )
    res = qe.retrieve("how will I look?")
    assert len(res) == 2
    assert res[0].node.get_content() == docs[2].text
    assert res[1].node.get_content() == docs[0].text

    remove_docs(index, index.doc_ids)
