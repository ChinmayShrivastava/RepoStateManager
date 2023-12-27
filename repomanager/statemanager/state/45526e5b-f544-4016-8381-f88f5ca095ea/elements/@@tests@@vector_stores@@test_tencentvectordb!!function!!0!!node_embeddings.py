def node_embeddings() -> List[TextNode]:
    return [
        TextNode(
            text="test text 1",
            id_="31BA2AA7-E066-452D-B0A6-0935FACE94FC",
            relationships={
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-doc-1")
            },
            metadata={"author": "Kiwi", "age": 23},
            embedding=[0.12, 0.32],
        ),
        TextNode(
            text="test text 2",
            id_="38500E76-5436-44A0-9C47-F86AAD56234D",
            relationships={
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-doc-2")
            },
            metadata={"author": "Chris", "age": 33},
            embedding=[0.21, 0.22],
        ),
        TextNode(
            text="test text 3",
            id_="9F90A339-2F51-4229-8280-816669102F7F",
            relationships={
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-doc-3")
            },
            metadata={"author": "jerry", "age": 41},
            embedding=[0.49, 0.88],
        ),
    ]
