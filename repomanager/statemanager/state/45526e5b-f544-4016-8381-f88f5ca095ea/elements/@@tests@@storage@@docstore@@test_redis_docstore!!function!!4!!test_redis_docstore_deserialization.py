def test_redis_docstore_deserialization(
    redis_docstore: RedisDocumentStore, documents: List[Document]
) -> None:
    from llama_index import (
        Document,
        StorageContext,
        SummaryIndex,
    )
    from llama_index.storage.docstore import RedisDocumentStore
    from llama_index.storage.index_store import RedisIndexStore

    ds = RedisDocumentStore.from_host_and_port("127.0.0.1", 6379, namespace="data4")
    idxs = RedisIndexStore.from_host_and_port("127.0.0.1", 6379, namespace="data4")

    storage_context = StorageContext.from_defaults(docstore=ds, index_store=idxs)

    index = SummaryIndex.from_documents(
        [Document(text="hello world2")], storage_context=storage_context
    )
    # fails here
    doc = index.docstore.docs
    print(doc)
