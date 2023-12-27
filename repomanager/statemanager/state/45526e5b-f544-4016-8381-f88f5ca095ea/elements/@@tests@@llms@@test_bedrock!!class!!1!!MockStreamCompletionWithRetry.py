class MockStreamCompletionWithRetry:
    def __init__(self, expected_prompt: str):
        self.expected_prompt = expected_prompt

    def mock_stream_completion_with_retry(
        self, request_body: str, *args: Any, **kwargs: Any
    ) -> dict:
        assert json.loads(request_body) == {
            "inputText": self.expected_prompt,
            "textGenerationConfig": {"maxTokenCount": 512, "temperature": 0.5},
        }
        return {
            "ResponseMetadata": {
                "HTTPHeaders": {
                    "connection": "keep-alive",
                    "content-type": "application/vnd.amazon.eventstream",
                    "date": "Fri, 20 Oct 2023 11:59:03 GMT",
                    "transfer-encoding": "chunked",
                    "x-amzn-bedrock-content-type": "application/json",
                    "x-amzn-requestid": "ef9af51b-7ba5-4020-3793-f4733226qb84",
                },
                "HTTPStatusCode": 200,
                "RequestId": "ef9af51b-7ba5-4020-3793-f4733226qb84",
                "RetryAttempts": 0,
            },
            "body": MockEventStream(),
            "contentType": "application/json",
        }
