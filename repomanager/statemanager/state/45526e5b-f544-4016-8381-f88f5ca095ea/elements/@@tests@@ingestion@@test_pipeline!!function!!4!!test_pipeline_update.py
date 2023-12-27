def test_pipeline_update() -> None:
    document1 = Document.example()
    document1.id_ = "1"

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=25, chunk_overlap=0),
        ],
        docstore=SimpleDocumentStore(),
    )

    nodes = pipeline.run(documents=[document1])
    assert len(nodes) == 19
    assert pipeline.docstore is not None
    assert len(pipeline.docstore.docs) == 1

    # adjust document content
    document1 = Document(text="test", doc_id="1")

    # run pipeline again
    nodes = pipeline.run(documents=[document1])

    assert len(nodes) == 1
    assert pipeline.docstore is not None
    assert len(pipeline.docstore.docs) == 1
    assert next(iter(pipeline.docstore.docs.values())).text == "test"  # type: ignore
