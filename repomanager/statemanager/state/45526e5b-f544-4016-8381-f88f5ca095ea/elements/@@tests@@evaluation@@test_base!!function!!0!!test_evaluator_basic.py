def test_evaluator_basic() -> None:
    test_evaluator = MockEvaluator()
    eval_result_0 = test_evaluator.evaluate(
        query="test query",
        response="test response",
        contexts=["test context 1", "test context 2"],
    )

    eval_result_1 = test_evaluator.evaluate_response(
        query="test query",
        response=Response(
            response="test response",
            source_nodes=[
                NodeWithScore(node=TextNode(text="test context 1"), score=1.0),
                NodeWithScore(node=TextNode(text="test context 2"), score=1.0),
            ],
        ),
    )

    assert eval_result_0 == eval_result_1
