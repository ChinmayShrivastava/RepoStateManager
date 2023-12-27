def _group_nodes_by_source(nodes: Sequence[BaseNode]) -> List[_NodeGroup]:
    """Returns a list of lists of nodes where each list has all the nodes
    from the same document.
    """
    groups: Dict[str, _NodeGroup] = {}
    for node in nodes:
        source_node: RelatedNodeInfo
        if isinstance(node.source_node, RelatedNodeInfo):
            source_node = node.source_node
        else:
            source_node = RelatedNodeInfo(node_id=_default_doc_id)

        if source_node.node_id not in groups:
            groups[source_node.node_id] = _NodeGroup(source_node=source_node, nodes=[])

        groups[source_node.node_id].nodes.append(node)

    return list(groups.values())
