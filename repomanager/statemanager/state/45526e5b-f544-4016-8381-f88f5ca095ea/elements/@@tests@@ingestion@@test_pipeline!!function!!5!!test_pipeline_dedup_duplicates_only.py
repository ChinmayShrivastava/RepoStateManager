def test_pipeline_dedup_duplicates_only() -> None:
    documents = [
        Document(text="one", doc_id="1"),
        Document(text="two", doc_id="2"),
        Document(text="three", doc_id="3"),
    ]

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=25, chunk_overlap=0),
        ],
        docstore=SimpleDocumentStore(),
    )

    nodes = pipeline.run(documents=documents)
    assert len(nodes) == 3

    nodes = pipeline.run(documents=documents)
    assert len(nodes) == 0
