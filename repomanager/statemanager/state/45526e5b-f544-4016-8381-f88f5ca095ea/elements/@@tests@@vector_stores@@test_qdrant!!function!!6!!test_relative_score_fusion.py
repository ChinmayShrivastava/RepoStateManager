def test_relative_score_fusion() -> None:
    nodes = [
        TextNode(
            text="lorem ipsum",
            id_="1",
        ),
        TextNode(
            text="lorem ipsum",
            id_="2",
        ),
        TextNode(
            text="lorem ipsum",
            id_="3",
        ),
    ]

    sparse_result = VectorStoreQueryResult(
        ids=["1", "2", "3"],
        similarities=[0.2, 0.3, 0.4],
        nodes=nodes,
    )

    dense_result = VectorStoreQueryResult(
        ids=["3", "2", "1"],
        similarities=[0.8, 0.5, 0.6],
        nodes=nodes[::-1],
    )

    fused_result = relative_score_fusion(dense_result, sparse_result, top_k=3)
    assert fused_result.ids == ["3", "2", "1"]

    # make sparse result empty
    sparse_result = VectorStoreQueryResult(
        ids=[],
        similarities=[],
        nodes=[],
    )

    fused_result = relative_score_fusion(dense_result, sparse_result, top_k=3)
    assert fused_result.ids == ["3", "1", "2"]

    # make both results a single node
    sparse_result = VectorStoreQueryResult(
        ids=["1"],
        similarities=[0.2],
        nodes=[nodes[0]],
    )

    dense_result = VectorStoreQueryResult(
        ids=["1"],
        similarities=[0.8],
        nodes=[nodes[0]],
    )

    fused_result = relative_score_fusion(dense_result, sparse_result, top_k=3)
    assert fused_result.ids == ["1"]
