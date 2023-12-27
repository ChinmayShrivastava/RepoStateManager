def test_forward_back_processor(tmp_path: Path) -> None:
    """Test forward-back processor."""
    nodes = [
        TextNode(text="Hello world.", id_="3"),
        TextNode(text="This is a test.", id_="2"),
        TextNode(text="This is another test.", id_="1"),
        TextNode(text="This is a test v2.", id_="4"),
        TextNode(text="This is a test v3.", id_="5"),
    ]
    nodes_with_scores = [NodeWithScore(node=node) for node in nodes]
    for i, node in enumerate(nodes):
        if i > 0:
            node.relationships.update(
                {
                    NodeRelationship.PREVIOUS: RelatedNodeInfo(
                        node_id=nodes[i - 1].node_id
                    )
                },
            )
        if i < len(nodes) - 1:
            node.relationships.update(
                {NodeRelationship.NEXT: RelatedNodeInfo(node_id=nodes[i + 1].node_id)},
            )

    docstore = SimpleDocumentStore()
    docstore.add_documents(nodes)

    # check for a single node
    node_postprocessor = PrevNextNodePostprocessor(
        docstore=docstore, num_nodes=2, mode="next"
    )
    processed_nodes = node_postprocessor.postprocess_nodes([nodes_with_scores[0]])
    assert len(processed_nodes) == 3
    assert processed_nodes[0].node.node_id == "3"
    assert processed_nodes[1].node.node_id == "2"
    assert processed_nodes[2].node.node_id == "1"

    # check for multiple nodes (nodes should not be duped)
    node_postprocessor = PrevNextNodePostprocessor(
        docstore=docstore, num_nodes=1, mode="next"
    )
    processed_nodes = node_postprocessor.postprocess_nodes(
        [nodes_with_scores[1], nodes_with_scores[2]]
    )
    assert len(processed_nodes) == 3
    assert processed_nodes[0].node.node_id == "2"
    assert processed_nodes[1].node.node_id == "1"
    assert processed_nodes[2].node.node_id == "4"

    # check for previous
    node_postprocessor = PrevNextNodePostprocessor(
        docstore=docstore, num_nodes=1, mode="previous"
    )
    processed_nodes = node_postprocessor.postprocess_nodes(
        [nodes_with_scores[1], nodes_with_scores[2]]
    )
    assert len(processed_nodes) == 3
    assert processed_nodes[0].node.node_id == "3"
    assert processed_nodes[1].node.node_id == "2"
    assert processed_nodes[2].node.node_id == "1"

    # check that both works
    node_postprocessor = PrevNextNodePostprocessor(
        docstore=docstore, num_nodes=1, mode="both"
    )
    processed_nodes = node_postprocessor.postprocess_nodes([nodes_with_scores[2]])
    assert len(processed_nodes) == 3
    # nodes are sorted
    assert processed_nodes[0].node.node_id == "2"
    assert processed_nodes[1].node.node_id == "1"
    assert processed_nodes[2].node.node_id == "4"

    # check that num_nodes too high still works
    node_postprocessor = PrevNextNodePostprocessor(
        docstore=docstore, num_nodes=4, mode="both"
    )
    processed_nodes = node_postprocessor.postprocess_nodes([nodes_with_scores[2]])
    assert len(processed_nodes) == 5
    # nodes are sorted
    assert processed_nodes[0].node.node_id == "3"
    assert processed_nodes[1].node.node_id == "2"
    assert processed_nodes[2].node.node_id == "1"
    assert processed_nodes[3].node.node_id == "4"
    assert processed_nodes[4].node.node_id == "5"

    # check that nodes with gaps works
    node_postprocessor = PrevNextNodePostprocessor(
        docstore=docstore, num_nodes=1, mode="both"
    )
    processed_nodes = node_postprocessor.postprocess_nodes(
        [nodes_with_scores[0], nodes_with_scores[4]]
    )
    assert len(processed_nodes) == 4
    # nodes are sorted
    assert processed_nodes[0].node.node_id == "3"
    assert processed_nodes[1].node.node_id == "2"
    assert processed_nodes[2].node.node_id == "4"
    assert processed_nodes[3].node.node_id == "5"

    # check that nodes with gaps works
    node_postprocessor = PrevNextNodePostprocessor(
        docstore=docstore, num_nodes=0, mode="both"
    )
    processed_nodes = node_postprocessor.postprocess_nodes(
        [nodes_with_scores[0], nodes_with_scores[4]]
    )
    assert len(processed_nodes) == 2
    # nodes are sorted
    assert processed_nodes[0].node.node_id == "3"
    assert processed_nodes[1].node.node_id == "5"

    # check that raises value error for invalid mode
    with pytest.raises(ValueError):
        PrevNextNodePostprocessor(docstore=docstore, num_nodes=4, mode="asdfasdf")
