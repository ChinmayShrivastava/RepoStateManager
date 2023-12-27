def test_query_knowledge_successful(
    mock_post: Any, query_engine: CogniswitchQueryEngine
) -> None:
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"data": {"answer": "42"}}
    response = query_engine.query_knowledge("What is the meaning of life?")
    assert isinstance(response, Response)
    assert response.response == "42"
