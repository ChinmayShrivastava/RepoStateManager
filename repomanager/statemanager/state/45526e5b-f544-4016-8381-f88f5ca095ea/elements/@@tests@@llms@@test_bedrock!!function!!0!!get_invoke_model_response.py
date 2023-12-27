def get_invoke_model_response(payload: str) -> dict:
    raw_stream_bytes = payload.encode()
    raw_stream = BytesIO(raw_stream_bytes)
    content_length = len(raw_stream_bytes)

    return {
        "ResponseMetadata": {
            "HTTPHeaders": {
                "connection": "keep-alive",
                "content-length": "246",
                "content-type": "application/json",
                "date": "Fri, 20 Oct 2023 08:20:44 GMT",
                "x-amzn-requestid": "667dq648-fbc3-4a7b-8f0e-4575f1f1f11d",
            },
            "HTTPStatusCode": 200,
            "RequestId": "667dq648-fbc3-4a7b-8f0e-4575f1f1f11d",
            "RetryAttempts": 0,
        },
        "body": StreamingBody(
            raw_stream=raw_stream,
            content_length=content_length,
        ),
        "contentType": "application/json",
    }
