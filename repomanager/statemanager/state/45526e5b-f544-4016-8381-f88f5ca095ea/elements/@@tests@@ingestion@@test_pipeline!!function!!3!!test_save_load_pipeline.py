def test_save_load_pipeline() -> None:
    documents = [
        Document(text="one", doc_id="1"),
        Document(text="two", doc_id="2"),
        Document(text="one", doc_id="1"),
    ]

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=25, chunk_overlap=0),
        ],
        docstore=SimpleDocumentStore(),
    )

    nodes = pipeline.run(documents=documents)
    assert len(nodes) == 2
    assert pipeline.docstore is not None
    assert len(pipeline.docstore.docs) == 2

    # dedup will catch the last node
    nodes = pipeline.run(documents=[documents[-1]])
    assert len(nodes) == 0
    assert pipeline.docstore is not None
    assert len(pipeline.docstore.docs) == 2

    # test save/load
    pipeline.persist("./test_pipeline")

    pipeline2 = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=25, chunk_overlap=0),
        ],
    )

    pipeline2.load("./test_pipeline")

    # dedup will catch the last node
    nodes = pipeline.run(documents=[documents[-1]])
    assert len(nodes) == 0
    assert pipeline.docstore is not None
    assert len(pipeline.docstore.docs) == 2
