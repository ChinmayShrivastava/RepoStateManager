def node_embeddings() -> List[TextNode]:
    return [
        TextNode(
            text="lorem ipsum",
            id_="AF3BE6C4-5F43-4D74-B075-6B0E07900DE8",
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-0")},
            metadata={"weight": 1.0, "rank": "a"},
            embedding=[1.0, 0.0],
        ),
        TextNode(
            text="lorem ipsum",
            id_="7D9CD555-846C-445C-A9DD-F8924A01411D",
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-1")},
            metadata={"weight": 2.0, "rank": "c"},
            embedding=[0.0, 1.0],
        ),
        TextNode(
            text="lorem ipsum",
            id_="452D24AB-F185-414C-A352-590B4B9EE51B",
            relationships={NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test-2")},
            metadata={"weight": 3.0, "rank": "b"},
            embedding=[1.0, 1.0],
        ),
    ]
