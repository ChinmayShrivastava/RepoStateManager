def create_sample_documents(n: int) -> List[TextNode]:
    nodes: List[TextNode] = []

    for i in range(n):
        nodes.append(
            TextNode(
                text=f"test node text {i}",
                relationships={
                    NodeRelationship.SOURCE: RelatedNodeInfo(node_id=f"test doc id {i}")
                },
                embedding=[0.5, 0.5],
            )
        )

    return nodes
