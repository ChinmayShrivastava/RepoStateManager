class TestMongoDBAtlasVectorSearch:
    @classmethod
    def setup_class(cls) -> None:
        # insure the test collection is empty
        assert collection.count_documents({}) == 0  # type: ignore[index]

    @classmethod
    def teardown_class(cls) -> None:
        # delete all the documents in the collection
        collection.delete_many({})  # type: ignore[index]

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        # delete all the documents in the collection
        collection.delete_many({})  # type: ignore[index]

    def test_add_and_delete(self) -> None:
        vector_store = MongoDBAtlasVectorSearch(
            mongodb_client=test_client,  # type: ignore
            db_name=DB_NAME,
            collection_name=COLLECTION_NAME,
            index_name=INDEX_NAME,
        )
        sleep(1)  # waits for mongot to update Lucene's index
        vector_store.add(
            [
                TextNode(
                    text="test node text",
                    id_="test node id",
                    relationships={
                        NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test doc id")
                    },
                    embedding=[0.5, 0.5],
                )
            ]
        )

        assert collection.count_documents({}) == 1

        vector_store.delete("test doc id")

        assert collection.count_documents({}) == 0

    def test_query(self, node_embeddings: list[TextNode]) -> None:
        vector_store = MongoDBAtlasVectorSearch(
            mongodb_client=test_client,  # type: ignore
            db_name=DB_NAME,
            collection_name=COLLECTION_NAME,
            index_name=INDEX_NAME,
        )
        vector_store.add(node_embeddings)  # type: ignore
        sleep(1)  # wait for mongot to update the index

        res = vector_store.query(
            VectorStoreQuery(query_embedding=[1.0, 0.0, 0.0], similarity_top_k=1)
        )

        assert res.nodes
        assert res.nodes[0].get_content() == "lorem ipsum"
