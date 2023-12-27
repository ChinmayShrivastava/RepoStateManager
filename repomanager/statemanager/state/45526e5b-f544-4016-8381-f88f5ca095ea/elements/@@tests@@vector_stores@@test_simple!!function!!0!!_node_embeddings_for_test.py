def _node_embeddings_for_test() -> List[TextNode]:
    return [
        TextNode(
            text="lorem ipsum",
            id_=_NODE_ID_WEIGHT_1_RANK_A,
            embedding=[1.0, 0.0],
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-0")},
            metadata={"weight": 1.0, "rank": "a"},
        ),
        TextNode(
            text="lorem ipsum",
            id_=_NODE_ID_WEIGHT_2_RANK_C,
            embedding=[0.0, 1.0],
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-1")},
            metadata={"weight": 2.0, "rank": "c"},
        ),
        TextNode(
            text="lorem ipsum",
            id_=_NODE_ID_WEIGHT_3_RANK_C,
            embedding=[1.0, 1.0],
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-2")},
            metadata={"weight": 3.0, "rank": "c"},
        ),
    ]
