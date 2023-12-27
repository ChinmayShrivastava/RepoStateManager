def test_file_upload() -> None:
    try:
        index = VectaraIndex()
    except ValueError:
        pytest.skip("Missing Vectara credentials, skipping test")

    file_path = "docs/examples/data/paul_graham/paul_graham_essay.txt"
    id = index.insert_file(file_path)

    assert isinstance(index, VectaraIndex)

    # test query with Vectara summarization (default)
    query_engine = index.as_query_engine(similarity_top_k=3)
    res = query_engine.query("What software did Paul Graham write?")
    assert "paul graham" in str(res).lower() and "software" in str(res).lower()

    # test query with VectorStoreQuery (using OpenAI for summarization)
    query_engine = index.as_query_engine(similarity_top_k=3, summary_enabled=False)
    res = query_engine.query("What software did Paul Graham write?")
    assert "paul graham" in str(res).lower() and "software" in str(res).lower()

    remove_docs(index, [id])
