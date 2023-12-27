    def _completion_with_retry(**kwargs: Any) -> Any:
        if stream:
            return client.invoke_model_with_response_stream(
                modelId=model, body=request_body
            )
        return client.invoke_model(modelId=model, body=request_body)
