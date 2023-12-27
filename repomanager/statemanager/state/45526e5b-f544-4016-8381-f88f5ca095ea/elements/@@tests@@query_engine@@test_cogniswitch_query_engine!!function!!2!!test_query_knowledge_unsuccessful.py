def test_query_knowledge_unsuccessful(
    mock_post: Any, query_engine: CogniswitchQueryEngine
) -> None:
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"message": "Bad Request"}
    response = query_engine.query_knowledge("what is life?")
    assert isinstance(response, Response)
    assert response.response == "Bad Request"
