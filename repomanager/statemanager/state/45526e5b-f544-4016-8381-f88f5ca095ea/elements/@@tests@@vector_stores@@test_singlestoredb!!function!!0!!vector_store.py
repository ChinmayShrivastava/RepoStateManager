def vector_store() -> Generator[SingleStoreVectorStore, None, None]:
    if "SINGLESTOREDB_URL" in os.environ and "/" in os.environ["SINGLESTOREDB_URL"]:
        url = os.environ["SINGLESTOREDB_URL"]
        table_name = "test"
        singlestoredb_found = True
        store = SingleStoreVectorStore(table_name=table_name)
        store.add(
            [
                TextNode(
                    text="Apples are blue",
                    metadata={"type": "fruit"},
                    embedding=[0.9, 0.1],
                ),
                TextNode(
                    text="Tomatoes are black",
                    metadata={"type": "veggie"},
                    embedding=[0.5, 0.5],
                ),
                TextNode(
                    text="Brownies are orange",
                    metadata={"type": "dessert"},
                    embedding=[0.1, 0.9],
                ),
            ]
        )
        yield store
