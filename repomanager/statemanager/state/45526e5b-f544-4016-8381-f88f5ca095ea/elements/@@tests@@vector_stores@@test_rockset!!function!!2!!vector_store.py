def vector_store() -> Generator[RocksetVectorStore, None, None]:
    store = RocksetVectorStore.with_new_collection(collection="test", dimensions=2)
    store = RocksetVectorStore(collection="test")
    store.add(
        [
            TextNode(
                text="Apples are blue",
                metadata={"type": "fruit"},  # type: ignore[call-arg]
                embedding=[0.9, 0.1],
            ),
            TextNode(
                text="Tomatoes are black",
                metadata={"type": "veggie"},  # type: ignore[call-arg]
                embedding=[0.5, 0.5],
            ),
            TextNode(
                text="Brownies are orange",
                metadata={"type": "dessert"},  # type: ignore[call-arg]
                embedding=[0.1, 0.9],
            ),
        ]
    )
    while collection_is_empty(store.client, "test"):  # wait until docs are added
        sleep(0.1)
    yield store
    store.client.Collections.delete(collection="test")
    while collection_exists(store.client, "test"):  # wait until collection is deleted
        sleep(0.1)
