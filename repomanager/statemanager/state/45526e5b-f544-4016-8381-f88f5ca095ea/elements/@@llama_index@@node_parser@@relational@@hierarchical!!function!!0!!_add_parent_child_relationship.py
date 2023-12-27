def _add_parent_child_relationship(parent_node: BaseNode, child_node: BaseNode) -> None:
    """Add parent/child relationship between nodes."""
    child_list = parent_node.relationships.get(NodeRelationship.CHILD, [])
    child_list.append(child_node.as_related_node_info())
    parent_node.relationships[NodeRelationship.CHILD] = child_list

    child_node.relationships[
        NodeRelationship.PARENT
    ] = parent_node.as_related_node_info()
