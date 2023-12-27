def test_backwards_compatibility() -> None:
    import deeplake
    from deeplake.core.vectorstore import utils

    # create data
    texts, embeddings, ids, metadatas, images = utils.create_data(
        number_of_data=NUMBER_OF_DATA, embedding_dim=EMBEDDING_DIM
    )
    metadatas = [metadata.update({"doc_id": "2"}) for metadata in metadatas]
    node = TextNode(
        text="test node text",
        metadata={"key": "value", "doc_id": "1"},
        id_="1",
        embedding=[1.0 for i in range(EMBEDDING_DIM)],
    )

    nodes = [node for i in range(10)]

    dataset_path = "local_ds1"
    ds = deeplake.empty(dataset_path)
    ds.create_tensor("ids", htype="text")
    ds.create_tensor("embedding", htype="embedding")
    ds.create_tensor("text", htype="text")
    ds.create_tensor("metadata", htype="json")

    ds.extend(
        {
            "ids": ids,
            "text": texts,
            "metadata": metadatas,
            "embedding": embeddings,
        }
    )

    vectorstore = DeepLakeVectorStore(
        dataset_path=dataset_path,
        overwrite=False,
        verbose=False,
    )

    vectorstore.add(nodes)
    assert len(vectorstore.vectorstore) == 20
    deeplake.delete(dataset_path)
