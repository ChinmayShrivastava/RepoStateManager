def nodes() -> List[TextNode]:
    """Get documents."""
    # NOTE: one document for now
    return [
        TextNode(
            text="Hello world.",
            relationships={
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test doc")
            },
        ),
        TextNode(
            text="This is a test.",
            relationships={
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test doc")
            },
        ),
        TextNode(
            text="This is another test.",
            relationships={
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test doc")
            },
        ),
        TextNode(
            text="This is a test v2.",
            relationships={
                NodeRelationship.SOURCE: RelatedNodeInfo(node_id="test doc")
            },
        ),
    ]
