def node_embeddings() -> List[TextNode]:
    return [
        TextNode(
            text="epsilla test text 0.",
            id_="1",
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-0")},
            metadata={
                "date": "2023-08-02",
            },
            embedding=[1.0, 0.0],
        ),
        TextNode(
            text="epsilla test text 1.",
            id_="2",
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-1")},
            metadata={
                "date": "2023-08-11",
            },
            embedding=[0.0, 1.0],
        ),
    ]
